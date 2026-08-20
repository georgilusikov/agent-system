#!/usr/bin/env python3
"""commutator_check.py — универсальный движок коммутаторов склейки (identity-стичинга).

JTBD (owner 2026-06-26, источник avtoall identity-stitching):
«это очень важно, добавь в gap theory все формальные критерии склейки, в список
коммутаторов, кросс-чеков и чеклистов чтобы когда я прошу выписать тест-кейсы и
проверки, ты это учитывал».

Корень: когда несколько ключей (clientID, rick_rid, phone_hash, email_hash,
counter_user_id_hash, …) слепляются под один anchor (userID / deal_id / person_id),
склейка может быть ОШИБОЧНОЙ — anchor приписан к чужому факту, задвоен, или
inferred донором без доказательства. До этого скрипта проверки писались руками
client-specific (avtoall tests/test_join_commutators.py C1-C19, R1-R7). Этот движок —
универсальный: декларируешь identity-граф в конфиге → получаешь набор коммутаторов
PASS/FAIL/INCONCLUSIVE по 7 формальным семействам. Хардкод клиента запрещён.

Семь формальных семейств коммутаторов склейки (см. gap theory playbook §Теорема склейки):
  B — Bijectivity (обратный путь):  key → ровно один anchor (1:1). Hub = склейка к чужому.
  F — Fan-out (прямой путь):        anchor → ограниченная мощность key (shared-device).
  P — Provenance (direct vs donor): доля событий с anchor НАПРЯМУЮ vs donor-fill.
  C — Conservation (сохранение):    join не теряет/не дублирует строки; base-key non-null.
  T — Temporal (причинность):       donor-событие по времени ≤ целевого (нет back-dating).
  X — Cross-system reconcile:       два независимых пути к факту совпадают (web↔crm revenue).
  R — Round-trip (коммутатор):      key→anchor→key возвращает тот же key (диаграмма замыкается).

Два режима:
  1. --emit-checklist  — БЕЗ данных: по списку ключей печатает канонический чеклист
     тест-кейсов (что обязан проверить), markdown-таблица. Это ответ на «выпиши проверки».
  2. <config.yaml>     — С данными (parquet/csv): прогоняет объявленные коммутаторы,
     печатает результат PASS/FAIL/INCONCLUSIVE + violation %. pandas обязателен.

Использование:
    python3 commutator_check.py --emit-checklist --anchor userID \\
        --keys client_id,rick_rid,phone_hash,email_hash
    python3 commutator_check.py config.yaml          # прогон по данным
    python3 commutator_check.py --self-test          # smoke (без pandas)

Формат config.yaml:
    dataset: "gold/by-day/*.parquet"   # glob ИЛИ один файл (parquet/csv)
    anchor: avtoall_user_id            # склеенный identity-ключ
    keys: [client_id, rick_rid, phone_hash, email_hash, counter_user_id_hash]
    event_col: event_name              # опц. — для фильтра/порядка
    time_col: event_time               # опц. — для T (temporal)
    checks:
      bijectivity:                     # B: key → ≤max_fanout anchors
        - {key: client_id, max_fanout: 1, max_violation_rate: 0.02}
      fanout:                          # F: anchor → ≤max_per_anchor keys
        - {key: phone_hash, max_per_anchor: 5, max_violation_rate: 0.02, min_len: 12}
      conservation:                    # C: доля строк без base-key
        - {key: client_id, max_loss: 0.0, scope_event: "ecommerce purchase"}
      provenance:                      # P: доля direct (anchor на самом событии)
        - {key: avtoall_user_id, group_by: client_id, direct_min: 1.0}
      roundtrip:                       # R: key→anchor→key замыкается
        - {key: client_id, max_violation_rate: 0.02}
      temporal:                        # T: donor.time ≤ target.time
        - {donor_event: "ecommerce detail", target_event: "ecommerce purchase",
           group_by: avtoall_user_id, min_ok_rate: 0.95}
      reconcile:                       # X: путь A revenue ≈ путь B revenue
        - {label: "web↔crm", left_value: item_price, right_dataset: "crm/*.parquet",
           right_value: amount, join_key: avtoall_user_id, max_rel_diff: 0.05}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml  # type: ignore

    def _load(text: str) -> dict:
        return yaml.safe_load(text)
except Exception:  # pragma: no cover
    def _load(text: str) -> dict:
        return json.loads(text)


# ── семь формальных семейств (SSOT для чеклиста и для движка) ──────────────────
FAMILIES = {
    "B": ("Bijectivity (обратный путь)", "key → ровно один anchor (1:1). Hub = склейка к чужому."),
    "F": ("Fan-out (прямой путь)", "anchor → ограниченная мощность key (shared-device detection)."),
    "P": ("Provenance (direct vs donor)", "доля событий с anchor напрямую vs donor-fill."),
    "C": ("Conservation (сохранение)", "join не теряет/не дублирует; base-key non-null."),
    "T": ("Temporal (причинность)", "donor-событие по времени ≤ целевого (нет back-dating)."),
    "X": ("Cross-system reconcile", "два независимых пути к факту совпадают (revenue web↔crm)."),
    "R": ("Round-trip (коммутатор)", "key→anchor→key возвращает тот же key (диаграмма замыкается)."),
}

STATUS_EMOJI = {"PASS": "✅", "FAIL": "❌", "INCONCLUSIVE": "⚪"}

# структурные коммутаторы (FAIL = anchor приписан к чужому факту / потерян / задвоен —
# склейка ОБЪЕКТИВНО сломана) vs интерпретивные (FAIL = свойство, которое аналитик
# трактует по своей модели склейки: donor-fill доля, multi-device, reorder, расхождение
# источников — не обязательно «баг», но обязательно к РЕШЕНИЮ).
STRUCTURAL = {"B", "F", "C"}
INTERPRETIVE = {"P", "R", "T", "X"}


def _norm_series(s):
    return s.fillna("").astype(str).str.strip().replace({"nan": "", "None": "", "NaN": ""})


# ════════════════════════════════════════════════════════════════════════════
# Режим 1 — emit-checklist (без данных): ответ на «выпиши тест-кейсы и проверки»
# ════════════════════════════════════════════════════════════════════════════
def emit_checklist(anchor: str, keys: list[str]) -> str:
    anchor = (anchor or "anchor").strip()
    keys = [k.strip() for k in keys if k.strip()]
    if not keys:
        keys = ["client_id", "rick_rid", "phone_hash", "email_hash"]

    rows: list[tuple[str, str, str, str]] = []  # (code, family, тест-кейс, порог-дефолт)
    n = {f: 0 for f in FAMILIES}  # per-family counter (как в run_checks)

    def add(fam: str, case: str, thr: str):
        n[fam] += 1
        rows.append((f"{fam}{n[fam]}", FAMILIES[fam][0].split(" (")[0], case, thr))

    # B — биективность обратного пути по КАЖДОМУ ключу
    for k in keys:
        add("B", f"каждый `{k}` ведёт ровно к одному `{anchor}` (1:1, не hub к чужому)",
            "≤2% ключей мостят >1 anchor")
    # F — fan-out прямого пути (shared-device) по КАЖДОМУ ключу
    for k in keys:
        add("F", f"`{anchor}` несёт ограниченное число `{k}` (общий девайс / приписка)",
            "phone/email ≤1; clientID ≤3; rid ≤N")
    # P — provenance: anchor напрямую vs donor-fill
    add("P", f"`{anchor}` присутствует НАПРЯМУЮ на событии vs donor-fill инференс (доля direct)",
        "direct ≥ объявленного порога, donor помечен")
    # C — conservation
    add("C", f"каждая строка несёт base-key (`{keys[0]}`) — склейка не теряет базу",
        "0% потерь / 0 дублей при group")
    # R — round-trip коммутатор (ТОЛЬКО для пар где ожидается биекция)
    add("R", f"для пар с ожидаемой БИЕКЦИЕЙ (phone↔person, transaction↔deal): "
            f"key→`{anchor}`→key замыкается. Many-to-one (clientID→userID) НЕ обязан — пропустить",
        "≤2% незамкнутых; не применять к many-to-one")
    # T — temporal causality
    add("T", f"donor-событие (давшее `{anchor}`) по времени ≤ целевого (нет back-dating)",
        "≥95% без инверсии; INCONCLUSIVE если нет time_col")
    # X — cross-system reconcile
    add("X", f"факт по `{anchor}` сходится двумя независимыми путями (web↔crm revenue/count)",
        "rel-diff ≤5%; INCONCLUSIVE если нет 2-го источника")

    out: list[str] = []
    out.append(f"## Коммутаторы склейки — чеклист тест-кейсов (anchor=`{anchor}`, keys={len(keys)})")
    out.append("")
    out.append("Источник: gap theory playbook §Теорема склейки · 7 семейств B/F/P/C/T/R/X.")
    out.append("Каждый кейс ПАДАЕТ если склейка ошибочна (а не «ок» по умолчанию).")
    out.append("")
    out.append("| Code | Семейство | Тест-кейс (проверка) | Порог-дефолт |")
    out.append("|---|---|---|---|")
    for code, fam, case, thr in rows:
        out.append(f"| {code} | {fam} | {case} | {thr} |")
    out.append("")
    out.append("**Семь семейств (формальные критерии):**")
    out.append("")
    out.append("| Сем. | Что | Формальный критерий |")
    out.append("|---|---|---|")
    for f, (name, desc) in FAMILIES.items():
        out.append(f"| {f} | {name} | {desc} |")
    out.append("")
    out.append("Запуск с данными: объяви `keys`/`checks` в config.yaml → "
               "`python3 commutator_check.py config.yaml`.")
    return "\n".join(out)


# ════════════════════════════════════════════════════════════════════════════
# Режим 2 — прогон по данным
# ════════════════════════════════════════════════════════════════════════════
def _load_frame(pattern: str, cols=None):
    import glob as _glob  # bracket-safe stdlib glob
    import pandas as pd  # lazy
    base = Path(pattern)
    if any(ch in Path(pattern).name for ch in "*?["):
        # Глоб ТОЛЬКО в имени; родитель — литерал и может содержать квадратные скобки.
        # Path.parent literal + Path.glob(name) корректно сохраняют такой путь.
        root = Path(pattern).parent
        files = sorted(root.glob(Path(pattern).name))
        # bracket-dir footgun: если name-glob дал 0, родитель мог содержать скобки →
        # stdlib glob.glob с escape на родителе (без silent INCONCLUSIVE на реальной папке).
        if not files:
            files = sorted(Path(p) for p in _glob.glob(_glob.escape(str(root)) + "/" + Path(pattern).name))
    elif base.is_dir():
        files = sorted(base.glob("*.parquet")) or sorted(base.glob("*.csv"))
    else:
        files = [base] if base.exists() else []
    if not files:
        return None
    frames = []
    for f in files:
        if f.suffix == ".csv":
            frames.append(pd.read_csv(f))
        else:
            try:
                frames.append(pd.read_parquet(f, columns=cols))
            except Exception:
                frames.append(pd.read_parquet(f))
    return pd.concat(frames, ignore_index=True) if frames else None


def _result(code: str, fam: str, status: str, detail: str) -> dict:
    return {"code": code, "family": fam, "status": status, "detail": detail}


def run_checks(cfg: dict) -> list[dict]:
    df = _load_frame(str(cfg.get("dataset", "")))
    anchor = cfg.get("anchor", "")
    checks = cfg.get("checks", {}) or {}
    event_col = cfg.get("event_col")
    time_col = cfg.get("time_col")
    results: list[dict] = []
    n = {f: 0 for f in FAMILIES}

    def code(f: str) -> str:
        n[f] += 1
        return f"{f}{n[f]}"

    if df is None:
        results.append(_result("—", "all", "INCONCLUSIVE",
                               f"датасет `{cfg.get('dataset')}` пуст/не найден — нечего прогонять"))
        return results

    def scoped(spec):
        ev = spec.get("scope_event")
        if ev and event_col and event_col in df.columns:
            return df[df[event_col] == ev]
        return df

    # B — bijectivity (key → anchor)
    for spec in checks.get("bijectivity", []):
        k = spec["key"]; c = code("B")
        if k not in df.columns or anchor not in df.columns:
            results.append(_result(c, "B", "INCONCLUSIVE", f"нет колонки {k}/{anchor}")); continue
        sub = scoped(spec)
        kk = _norm_series(sub[k]); aa = _norm_series(sub[anchor])
        m = (kk != "") & (aa != "")
        per_key = sub[m].assign(_k=kk[m], _a=aa[m]).groupby("_k")["_a"].nunique()
        if per_key.empty:
            results.append(_result(c, "B", "INCONCLUSIVE", f"{k}: нет непустых пар")); continue
        rate = float((per_key > spec.get("max_fanout", 1)).mean())
        thr = spec.get("max_violation_rate", 0.02)
        st = "PASS" if rate <= thr else "FAIL"
        results.append(_result(c, "B", st,
                               f"{k}→>{spec.get('max_fanout',1)} {anchor}: {round(100*rate,2)}% (порог {round(100*thr,1)}%)"))

    # F — fan-out (anchor → key)
    for spec in checks.get("fanout", []):
        k = spec["key"]; c = code("F")
        if k not in df.columns or anchor not in df.columns:
            results.append(_result(c, "F", "INCONCLUSIVE", f"нет колонки {k}/{anchor}")); continue
        sub = scoped(spec)
        kk = _norm_series(sub[k]); aa = _norm_series(sub[anchor])
        if spec.get("min_len"):
            kk = kk.where(kk.str.len() >= spec["min_len"], "")
        m = (kk != "") & (aa != "")
        if not m.any():
            results.append(_result(c, "F", "INCONCLUSIVE", f"{k}: нет валидных значений")); continue
        per_anchor = sub[m].assign(_k=kk[m], _a=aa[m]).groupby("_a")["_k"].nunique()
        rate = float((per_anchor > spec.get("max_per_anchor", 1)).mean())
        thr = spec.get("max_violation_rate", 0.02)
        st = "PASS" if rate <= thr else "FAIL"
        results.append(_result(c, "F", st,
                               f"{anchor}→>{spec.get('max_per_anchor',1)} {k}: {round(100*rate,2)}% (порог {round(100*thr,1)}%)"))

    # C — conservation
    for spec in checks.get("conservation", []):
        k = spec["key"]; c = code("C")
        if k not in df.columns:
            results.append(_result(c, "C", "INCONCLUSIVE", f"нет колонки {k}")); continue
        sub = scoped(spec)
        total = len(sub)
        if total == 0:
            results.append(_result(c, "C", "INCONCLUSIVE", "scope пуст")); continue
        loss = float((_norm_series(sub[k]) == "").mean())
        thr = spec.get("max_loss", 0.0)
        st = "PASS" if loss <= thr + 1e-9 else "FAIL"
        results.append(_result(c, "C", st,
                               f"{k} пуст на {round(100*loss,2)}% строк ({total} всего, порог {round(100*thr,1)}%)"))

    # P — provenance (direct vs donor-fill)
    for spec in checks.get("provenance", []):
        k = spec.get("key", anchor); c = code("P")
        gb = spec.get("group_by")
        if k not in df.columns or (gb and gb not in df.columns):
            results.append(_result(c, "P", "INCONCLUSIVE", f"нет колонки {k}/{gb}")); continue
        kk = _norm_series(df[k])
        direct = float((kk != "").mean())
        thr = spec.get("direct_min", 1.0)
        st = "PASS" if direct >= thr - 1e-9 else "FAIL"
        results.append(_result(c, "P", st,
                               f"{k} direct на {round(100*direct,2)}% строк (порог ≥{round(100*thr,1)}%); остальное donor-fill"))

    # R — round-trip key→anchor→key
    for spec in checks.get("roundtrip", []):
        k = spec["key"]; c = code("R")
        if k not in df.columns or anchor not in df.columns:
            results.append(_result(c, "R", "INCONCLUSIVE", f"нет колонки {k}/{anchor}")); continue
        kk = _norm_series(df[k]); aa = _norm_series(df[anchor])
        m = (kk != "") & (aa != "")
        if not m.any():
            results.append(_result(c, "R", "INCONCLUSIVE", "нет пар")); continue
        pairs = df[m].assign(_k=kk[m], _a=aa[m])
        k2a = pairs.groupby("_k")["_a"].agg(lambda s: s.iloc[0])  # каноничный anchor каждого key
        a2k = pairs.groupby("_a")["_k"].nunique()                 # сколько key у anchor
        # round-trip ломается если anchor выбранного key несёт >1 key
        broken = float((pairs["_a"].map(a2k) > 1).mean())
        thr = spec.get("max_violation_rate", 0.02)
        st = "PASS" if broken <= thr else "FAIL"
        results.append(_result(c, "R", st,
                               f"{k}→{anchor}→{k} не замыкается на {round(100*broken,2)}% (порог {round(100*thr,1)}%)"))

    # T — temporal causality
    for spec in checks.get("temporal", []):
        c = code("T")
        gb = spec.get("group_by", anchor)
        if not time_col or time_col not in df.columns or not event_col or event_col not in df.columns:
            results.append(_result(c, "T", "INCONCLUSIVE",
                                   "нет time_col/event_col — temporal требует event_time доноров")); continue
        de, te = spec.get("donor_event"), spec.get("target_event")
        d = df[df[event_col] == de]; t = df[df[event_col] == te]
        if d.empty or t.empty:
            results.append(_result(c, "T", "INCONCLUSIVE", f"нет событий {de}/{te}")); continue
        fd = d.assign(_g=_norm_series(d[gb])).groupby("_g")[time_col].min()
        ft = t.assign(_g=_norm_series(t[gb])).groupby("_g")[time_col].min()
        common = [g for g in ft.index if g in fd.index and g != ""]
        if not common:
            results.append(_result(c, "T", "INCONCLUSIVE", "нет общих групп donor+target")); continue
        inv = sum(1 for g in common if str(fd[g]) > str(ft[g]))
        ok = 1 - inv / len(common)
        thr = spec.get("min_ok_rate", 0.95)
        st = "PASS" if ok >= thr else "FAIL"
        results.append(_result(c, "T", st,
                               f"{de}≤{te}: {round(100*ok,1)}% без инверсии (порог ≥{round(100*thr,1)}%)"))

    # X — cross-system reconcile
    for spec in checks.get("reconcile", []):
        c = code("X")
        right = _load_frame(str(spec.get("right_dataset", "")))
        if right is None:
            results.append(_result(c, "X", "INCONCLUSIVE",
                                   f"2-й источник `{spec.get('right_dataset')}` не выгружен — reconcile невозможен")); continue
        jk = spec.get("join_key", anchor)
        lv, rv = spec.get("left_value"), spec.get("right_value")
        import pandas as pd
        if jk not in df.columns or jk not in right.columns or lv not in df.columns or rv not in right.columns:
            results.append(_result(c, "X", "INCONCLUSIVE", "нет join_key/value колонок в одном из источников")); continue
        L = pd.to_numeric(df[lv], errors="coerce").fillna(0).groupby(_norm_series(df[jk])).sum()
        R = pd.to_numeric(right[rv], errors="coerce").fillna(0).groupby(_norm_series(right[jk])).sum()
        common = L.index.intersection(R.index).difference([""])
        if len(common) == 0:
            results.append(_result(c, "X", "INCONCLUSIVE", "нет общих join_key")); continue
        diff = (L[common] - R[common]).abs().sum()
        base = max(R[common].abs().sum(), 1e-9)
        rel = float(diff / base)
        thr = spec.get("max_rel_diff", 0.05)
        st = "PASS" if rel <= thr else "FAIL"
        results.append(_result(c, "X", st,
                               f"{spec.get('label','reconcile')}: rel-diff {round(100*rel,2)}% (порог ≤{round(100*thr,1)}%)"))

    if not results:
        results.append(_result("—", "all", "INCONCLUSIVE", "в config.checks нет ни одной проверки"))
    return results


def render_results(cfg: dict, results: list[dict]) -> str:
    out: list[str] = []
    out.append(f"## Коммутаторы склейки — прогон (anchor=`{cfg.get('anchor','?')}`, "
               f"dataset=`{cfg.get('dataset','?')}`)")
    out.append("")
    out.append("| Code | Семейство | Статус | Детали |")
    out.append("|---|---|---|---|")
    for r in results:
        em = STATUS_EMOJI.get(r["status"], "")
        out.append(f"| {r['code']} | {r['family']} | {em} {r['status']} | {r['detail']} |")
    out.append("")
    fails = [r for r in results if r["status"] == "FAIL"]
    inconc = [r for r in results if r["status"] == "INCONCLUSIVE"]
    passed = [r for r in results if r["status"] == "PASS"]
    struct_fail = [r for r in fails if r["family"] in STRUCTURAL]
    interp_fail = [r for r in fails if r["family"] in INTERPRETIVE]
    if struct_fail:
        verdict = "склейка ОШИБОЧНА (структурный коммутатор сломан — anchor к чужому факту)"
    elif interp_fail:
        verdict = "склейка структурно цела; интерпретивные коммутаторы требуют решения аналитика по порогу"
    elif passed:
        verdict = "склейка ДОКАЗАНА"
    else:
        verdict = "INCONCLUSIVE — данных недостаточно"
    out.append(f"**Итог:** {len(passed)} PASS / {len(fails)} FAIL "
               f"({len(struct_fail)} структурных / {len(interp_fail)} интерпретивных) / "
               f"{len(inconc)} INCONCLUSIVE → `{verdict}`")
    if struct_fail:
        out.append("")
        out.append("Структурный FAIL (B/F/C) = склейка приписала anchor к чужому факту / потеряла базу / "
                   "задвоила. Не доставлять данные пока не закрыт.")
    if interp_fail and not struct_fail:
        out.append("")
        out.append("Интерпретивный FAIL (P/R/T/X) = donor-fill доля / multi-device / reorder / расхождение "
                   "источников. Не баг сам по себе — но аналитик ОБЯЗАН зафиксировать решение по порогу.")
    return "\n".join(out)


# ════════════════════════════════════════════════════════════════════════════
def _self_test() -> int:
    # checklist режим — без pandas
    md = emit_checklist("userID", ["client_id", "rick_rid", "phone_hash"])
    assert "B1" in md and "B2" in md and "B3" in md, "B per-key missing"
    for code in ("F1", "P1", "C1", "R1", "T1", "X1"):
        assert code in md, f"family code {code} missing"
    assert "Теорема склейки" in md, "theory ref missing"
    assert md.count("| B") >= 3, "bijectivity rows per key missing"
    # все 7 семейств в легенде
    for f in FAMILIES:
        assert f"| {f} |" in md, f"family {f} legend missing"

    # run режим на синтетике (нужен pandas; если нет — пропускаем data-часть)
    try:
        import pandas as pd
    except Exception:
        print("✅ self-test passed (checklist; pandas отсутствует — data-часть пропущена)")
        return 0
    df = pd.DataFrame({
        "event_name": ["ecommerce purchase"] * 4,
        "avtoall_user_id": ["U1", "U1", "U2", "U2"],
        "client_id": ["C1", "C1", "C2", "C3hub"],
        "phone_hash": ["p" * 12, "p" * 12, "q" * 12, "q" * 12],
        "item_price": [100, 50, 200, 0],
    })
    tmp = Path(__file__).resolve().parent / "_selftest_gold.parquet"
    df.to_parquet(tmp)
    try:
        cfg = {
            "dataset": str(tmp), "anchor": "avtoall_user_id", "event_col": "event_name",
            "checks": {
                "bijectivity": [{"key": "client_id", "max_fanout": 1, "max_violation_rate": 0.02}],
                "conservation": [{"key": "client_id", "max_loss": 0.0}],
                "provenance": [{"key": "avtoall_user_id", "direct_min": 1.0}],
                "roundtrip": [{"key": "client_id", "max_violation_rate": 0.02}],
                "reconcile": [{"label": "no-2nd", "right_dataset": "nope/*.parquet"}],
            },
        }
        res = run_checks(cfg)
        codes = {r["code"]: r for r in res}
        # client_id 1:1 anchor (C1→U1, C2→U2, C3hub→U2) → каждый clientID 1 userID → B PASS
        assert codes["B1"]["status"] == "PASS", f"B1 expected PASS: {codes['B1']}"
        # conservation: client_id 100% → PASS
        assert codes["C1"]["status"] == "PASS", f"C1: {codes['C1']}"
        # provenance direct 100% → PASS
        assert codes["P1"]["status"] == "PASS", f"P1: {codes['P1']}"
        # reconcile без 2-го источника → INCONCLUSIVE
        assert codes["X1"]["status"] == "INCONCLUSIVE", f"X1: {codes['X1']}"
        md2 = render_results(cfg, res)
        assert "PASS" in md2 and "INCONCLUSIVE" in md2, "render broken"

        # FAIL-кейс: phone hub (один phone на 2 userID) → fan-out обратной стороной;
        # сделаем clientID hub: один clientID на 2 userID
        df2 = pd.DataFrame({
            "event_name": ["ecommerce purchase"] * 4,
            "avtoall_user_id": ["U1", "U2", "U3", "U4"],
            "client_id": ["Cshared", "Cshared", "Cx", "Cy"],
        })
        df2.to_parquet(tmp)
        res2 = run_checks({"dataset": str(tmp), "anchor": "avtoall_user_id",
                           "checks": {"bijectivity": [{"key": "client_id", "max_fanout": 1, "max_violation_rate": 0.02}]}})
        b = {r["code"]: r for r in res2}["B1"]
        assert b["status"] == "FAIL", f"B1 hub expected FAIL: {b}"  # Cshared→2 userID = 33% >2%
    finally:
        tmp.unlink(missing_ok=True)
    print("✅ self-test passed (checklist + 7 families + run PASS/FAIL/INCONCLUSIVE)")
    return 0


def main(argv: list[str]) -> int:
    if "--self-test" in argv:
        return _self_test()
    if "--emit-checklist" in argv:
        anchor = "anchor"; keys: list[str] = []
        for i, a in enumerate(argv):
            if a == "--anchor" and i + 1 < len(argv):
                anchor = argv[i + 1]
            if a == "--keys" and i + 1 < len(argv):
                keys = argv[i + 1].split(",")
        print(emit_checklist(anchor, keys))
        return 0
    args = [a for a in argv[1:] if not a.startswith("--")]
    if not args:
        print("usage: commutator_check.py --emit-checklist --anchor <a> --keys k1,k2 | "
              "commutator_check.py config.yaml | --self-test", file=sys.stderr)
        return 1
    cfg = _load(Path(args[0]).read_text(encoding="utf-8"))
    print(render_results(cfg, run_checks(cfg)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

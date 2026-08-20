#!/usr/bin/env python3
"""Тесты универсального движка коммутаторов склейки (commutator_check.py).

Запуск: python3 -m pytest .agents/skills/2-hypothesis-gap-falsification/tests/test_commutator_check.py -v
"""
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import commutator_check as cc  # noqa: E402

pd = pytest.importorskip("pandas")


# ── checklist режим (без данных) ──────────────────────────────────────────────
def test_emit_checklist_per_key_bijectivity():
    md = cc.emit_checklist("userID", ["client_id", "rick_rid", "phone_hash"])
    # B per key
    assert "B1" in md and "B2" in md and "B3" in md
    # все 7 семейств представлены кодами
    for code in ("F1", "P1", "C1", "R1", "T1", "X1"):
        assert code in md, f"{code} missing"
    # ссылка на каноническую теорию
    assert "Теорема склейки" in md


def test_emit_checklist_default_keys_when_empty():
    md = cc.emit_checklist("anchor", [])
    assert "client_id" in md  # дефолтный набор подставлен


def test_families_legend_complete():
    md = cc.emit_checklist("a", ["k1"])
    for fam in ("B", "F", "P", "C", "T", "X", "R"):
        assert f"| {fam} |" in md


# ── run режим ─────────────────────────────────────────────────────────────────
def _write(tmp_path, df, name="gold.parquet"):
    p = tmp_path / name
    df.to_parquet(p)
    return str(p)


def test_bijectivity_pass_when_1to1(tmp_path):
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U1", "U2"], "client_id": ["C1", "C1", "C2"]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"bijectivity": [{"key": "client_id", "max_fanout": 1, "max_violation_rate": 0.02}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["B1"]["status"] == "PASS"


def test_bijectivity_fail_on_hub(tmp_path):
    # один clientID мостит 2 userID → hub → склейка к чужому
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U2", "U3", "U4"],
                       "client_id": ["Cshared", "Cshared", "Cx", "Cy"]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"bijectivity": [{"key": "client_id", "max_fanout": 1, "max_violation_rate": 0.02}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["B1"]["status"] == "FAIL"


def test_conservation_fail_on_missing_base_key(tmp_path):
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U2"], "client_id": ["C1", ""]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"conservation": [{"key": "client_id", "max_loss": 0.0}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["C1"]["status"] == "FAIL"


def test_provenance_measures_direct_fill(tmp_path):
    # 2 из 4 строк имеют anchor напрямую → direct=50% < порог 0.9 → FAIL
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U1", "", ""], "client_id": ["C1", "C1", "C1", "C1"]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"provenance": [{"key": "avtoall_user_id", "direct_min": 0.9}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["P1"]["status"] == "FAIL"
    assert "50" in r["P1"]["detail"]


def test_fanout_pass_bounded(tmp_path):
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U1"], "phone_hash": ["p" * 12, "p" * 12]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"fanout": [{"key": "phone_hash", "max_per_anchor": 1, "min_len": 12,
                                  "max_violation_rate": 0.02}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["F1"]["status"] == "PASS"


def test_reconcile_inconclusive_without_second_source(tmp_path):
    df = pd.DataFrame({"avtoall_user_id": ["U1"], "item_price": [100]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"reconcile": [{"label": "web↔crm", "right_dataset": "nope/*.parquet",
                                     "join_key": "avtoall_user_id", "left_value": "item_price",
                                     "right_value": "amount"}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["X1"]["status"] == "INCONCLUSIVE"


def test_temporal_inconclusive_without_time_col(tmp_path):
    df = pd.DataFrame({"avtoall_user_id": ["U1"], "event_name": ["ecommerce purchase"]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id", "event_col": "event_name",
           "checks": {"temporal": [{"donor_event": "ecommerce detail",
                                    "target_event": "ecommerce purchase"}]}}
    r = {x["code"]: x for x in cc.run_checks(cfg)}
    assert r["T1"]["status"] == "INCONCLUSIVE"


def test_verdict_structural_vs_interpretive(tmp_path):
    # B PASS, P FAIL → структурно цела, интерпретивный FAIL
    df = pd.DataFrame({"avtoall_user_id": ["U1", ""], "client_id": ["C1", "C2"]})
    cfg = {"dataset": _write(tmp_path, df), "anchor": "avtoall_user_id",
           "checks": {"bijectivity": [{"key": "client_id", "max_fanout": 1, "max_violation_rate": 0.5}],
                      "provenance": [{"key": "avtoall_user_id", "direct_min": 0.9}]}}
    res = cc.run_checks(cfg)
    md = cc.render_results(cfg, res)
    assert "структурно цела" in md


def test_inconclusive_when_dataset_missing():
    res = cc.run_checks({"dataset": "/nonexistent/*.parquet", "anchor": "x", "checks": {}})
    assert res[0]["status"] == "INCONCLUSIVE"


def test_self_test_entrypoint():
    assert cc._self_test() == 0


def test_bracket_dir_path_not_silently_inconclusive(tmp_path):
    """Пути могут содержать литеральные квадратные скобки. Папка с `[...]` в имени
    + glob `*.parquet` должна находить данные, НЕ возвращать silent INCONCLUSIVE."""
    bracket_dir = tmp_path / "[example]" / "gold" / "by-day"
    bracket_dir.mkdir(parents=True)
    df = pd.DataFrame({"avtoall_user_id": ["U1", "U2"], "phone_hash": ["p" * 12, "q" * 12]})
    df.to_parquet(bracket_dir / "day_2026-01-01.parquet")
    cfg = {"dataset": str(bracket_dir) + "/*.parquet", "anchor": "avtoall_user_id",
           "checks": {"fanout": [{"key": "phone_hash", "max_per_anchor": 1, "min_len": 12,
                                  "max_violation_rate": 0.02}]}}
    res = cc.run_checks(cfg)
    statuses = {x["status"] for x in res}
    assert statuses != {"INCONCLUSIVE"}, f"bracket-dir path silently INCONCLUSIVE: {res}"
    assert {x["code"]: x for x in res}["F1"]["status"] == "PASS"


def test_over_merge_detected_at_threshold_1(tmp_path):
    """Урок avtoall: phone fan-out с max_per_anchor=5 МАСКИРУЕТ over-merge;
    реальный инвариант (1 человек = 1 телефон, threshold=1) ловит его."""
    df = pd.DataFrame({
        "avtoall_user_id": ["U1", "U1", "U1", "U2"],
        "phone_hash": ["a" * 12, "b" * 12, "c" * 12, "d" * 12],
    })
    p = _write(tmp_path, df)
    loose = {"dataset": p, "anchor": "avtoall_user_id",
             "checks": {"fanout": [{"key": "phone_hash", "max_per_anchor": 5, "min_len": 12,
                                    "max_violation_rate": 0.02}]}}
    tight = {"dataset": p, "anchor": "avtoall_user_id",
             "checks": {"fanout": [{"key": "phone_hash", "max_per_anchor": 1, "min_len": 12,
                                    "max_violation_rate": 0.02}]}}
    assert {x["code"]: x for x in cc.run_checks(loose)}["F1"]["status"] == "PASS"   # masks
    assert {x["code"]: x for x in cc.run_checks(tight)}["F1"]["status"] == "FAIL"   # catches

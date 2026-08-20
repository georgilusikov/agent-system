# 📚 Skills Index - Справочник

**Версия:** 1.0.0
**Дата:** 2025-01-27
**Всего навыков:** 980
**Категорий:** 20+

## 🚀 Быстрый старт

### Поиск навыка по категории

```bash
# Найти все навыки для Product Manager
grep -A 20 "product_management:" _agent_shared/skills/INDEX.yaml

# Найти UX навыки
grep -A 20 "design_ux:" _agent_shared/skills/INDEX.yaml

# Найти навыки для архитектуры
grep -A 20 "architecture:" _agent_shared/skills/INDEX.yaml
```

### Использование в агенте

```yaml
# В AGENT.md или .mdc файле агента:
skills:
  - ${SKILLS_STUDY_LIBRARY:-~/reference/skills_study_library}/product-manager-toolkit
  - ${SKILLS_STUDY_LIBRARY:-~/reference/skills_study_library}/stakeholder-communication
  - ${SKILLS_STUDY_LIBRARY:-~/reference/skills_study_library}/business-case-development
```

### Использование скрипта поиска

```bash
# Показать все категории
python _agent_shared/skills/search_skills.py --list-all

# Поиск по категории
python _agent_shared/skills/search_skills.py --category product_business

# Поиск по тегу
python _agent_shared/skills/search_skills.py --tag design

# Поиск по ключевому слову
python _agent_shared/skills/search_skills.py --keyword "api"

# Генерация конфига для агента
python _agent_shared/skills/search_skills.py --agent-config product-manager-toolkit,stakeholder-communication

# Экспорт в Markdown
python _agent_shared/skills/search_skills.py --export-md SKILLS_INDEX_EXPORT.md
```

---

## 📂 20 основных категорий

### 1. Product & Business Management (39 навыков)
**Для кого:** Product Manager, Product Owner, Business Analyst
**Основные навыки:**
- `product-manager-toolkit` - RICE, интервью, PRD
- `product-strategist` - стратегия продуктов
- `agile-product-owner` - backlog, sprint planning
- `business-case-development` - бизнес-кейсы
- `stakeholder-communication` - коммуникация со стейкхолдерами

**Подкатегории:**
- Product Management (6 навыков)
- Business Strategy (7 навыков)
- Stakeholder Management (3 навыка)
- Marketing & Growth (8 навыков)
- Conversion Optimization (7 навыков)
- Startup & Operations (3 навыка)

---

### 2. Design & UX (32 навыка)
**Для кого:** UX Designer, UI Designer, Product Designer
**Основные навыки:**
- `design-system-creation` - создание дизайн-систем
- `design-handoff` - передача дизайна разработчикам
- `accessibility-compliance` - доступность (WCAG)
- `ux-researcher-designer` - UX-исследования
- `wireframe-prototyping` - прототипы

**Подкатегории:**
- Design Systems (6 навыков)
- UX Research (7 навыков)
- Visual Design (6 навыков)
- Design Handoff (2 навыка)
- Responsive Design (4 навыка)
- Mobile Design (4 навыка)
- UX Writing (2 навыка)

---

### 3. Software Architecture (21 навык)
**Для кого:** Software Architect, Senior Developer, CTO
**Основные навыки:**
- `architecture-patterns` - архитектурные паттерны
- `c4-architecture` - C4 модель
- `architecture-diagrams` - диаграммы архитектуры
- `architecture-decision-records` - ADR
- `microservices-patterns` - микросервисы

---

## 🎯 Популярные комбинации

### Для Product Manager
```yaml
skills:
  - product-manager-toolkit
  - stakeholder-communication
  - business-case-development
  - user-research-analysis
  - competitive-analysis
```

### Для UX Architect
```yaml
skills:
  - design-system-creation
  - design-handoff
  - accessibility-compliance
  - ux-researcher-designer
  - wireframe-prototyping
```

### Для Software Architect
```yaml
skills:
  - architecture-patterns
  - c4-architecture
  - architecture-diagrams
  - api-design-principles
  - microservices-patterns
```

---

## 📊 Статистика

| Категория | Навыков | Для кого |
|-----------|---------|----------|
| Product & Business | 39 | PM, PO, BA |
| Design & UX | 32 | UX/UI Designer |
| Architecture | 21 | Architect, CTO |
| Frontend | 62 | Frontend Dev |
| Backend | 38 | Backend Dev |
| DevOps | 43 | DevOps, SRE |
| AI/ML | 98 | ML Engineer |
| Testing | 25 | QA, SDET |
| Security | 77 | Security Engineer |
| Data | 31 | Data Engineer |
| Documentation | 38 | Tech Writer |
| Project Mgmt | 27 | PM, Scrum Master |
| Cloud | 48 | Cloud Architect |
| Mobile | 18 | Mobile Dev |
| Database | 24 | DBA |
| Monitoring | 39 | SRE |
| Integration | 52 | Integration Dev |
| Automation | 56 | Automation Dev |
| Communication | 47 | Все роли |
| Research | 95 | Research Scientist |

**ИТОГО:** 980 навыков

---

## 🔗 Полезные ссылки

- **INDEX.yaml:** Полный каталог всех навыков
- **External reference library:** `${SKILLS_STUDY_LIBRARY:-~/reference/skills_study_library}` with repo-local fallback `_skills_study_library/`
- **search_skills.py:** Скрипт для поиска

---

**Обновлено:** 2025-01-27

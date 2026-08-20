#!/bin/bash
# 🔍 Skills Search Tool (Simple Bash Version)
# Утилита для поиска навыков в INDEX.yaml

INDEX_FILE="/Users/georgijlusikov/Documents/курсор/_agent_shared/skills/INDEX.yaml"
DEFAULT_EXTERNAL="$HOME/reference/skills_study_library"
DEFAULT_LOCAL="/Users/georgijlusikov/Documents/курсор/_skills_study_library"
SKILLS_BASE="${SKILLS_STUDY_LIBRARY:-$DEFAULT_EXTERNAL}"

if [ ! -d "$SKILLS_BASE" ] && [ -d "$DEFAULT_LOCAL" ]; then
    SKILLS_BASE="$DEFAULT_LOCAL"
fi

# Показать справку
show_help() {
    echo "🔍 Skills Search Tool"
    echo ""
    echo "Использование:"
    echo "  ./search_skills_simple.sh --list-categories    Список всех категорий"
    echo "  ./search_skills_simple.sh --category <id>      Навыки в категории"
    echo "  ./search_skills_simple.sh --search <word>      Поиск по слову"
    echo "  ./search_skills_simple.sh --pm                 Навыки для Product Manager"
    echo "  ./search_skills_simple.sh --ux                 Навыки для UX Designer"
    echo "  ./search_skills_simple.sh --arch               Навыки для Architect"
    echo ""
}

# Список категорий
list_categories() {
    echo "📚 Все категории навыков:"
    echo ""
    grep -E "^  \w+:" "$INDEX_FILE" | grep -v "^  #" | sed 's/:$//' | sed 's/^  /  - /' | while read cat; do
        name=$(grep -A 1 "  $cat:" "$INDEX_FILE" | grep "name:" | sed 's/.*name: //' | sed 's/"//g')
        echo "  📦 $cat: $name"
    done
}

# Навыки в категории
show_category() {
    local cat_id=$1
    echo "📂 Категория: $cat_id"
    echo ""

    # Найти начало категории
    awk "/^  $cat_id:/,/^  \w+:/" "$INDEX_FILE" | grep -E "^\s+-\s+" | sed 's/^\s*-\s*/  ✅ /'
}

# Поиск по слову
search_skill() {
    local word=$1
    echo "🔍 Поиск: '$word'"
    echo ""

    grep -i "$word" "$INDEX_FILE" | grep "^\s*-\s" | sed 's/^\s*-\s*/  ✅ /' | sort -u
}

# Навыки для Product Manager
show_pm_skills() {
    echo "👔 Навыки для Product Manager:"
    echo ""
    show_category "product_business"
    echo ""
    echo "📁 Пути к навыкам:"
    echo "  - $SKILLS_BASE/product-manager-toolkit"
    echo "  - $SKILLS_BASE/stakeholder-communication"
    echo "  - $SKILLS_BASE/business-case-development"
    echo "  - $SKILLS_BASE/product-strategist"
    echo "  - $SKILLS_BASE/agile-product-owner"
}

# Навыки для UX Designer
show_ux_skills() {
    echo "🎨 Навыки для UX Designer:"
    echo ""
    show_category "design_ux"
    echo ""
    echo "📁 Пути к навыкам:"
    echo "  - $SKILLS_BASE/design-system-creation"
    echo "  - $SKILLS_BASE/design-handoff"
    echo "  - $SKILLS_BASE/accessibility-compliance"
    echo "  - $SKILLS_BASE/ux-researcher-designer"
    echo "  - $SKILLS_BASE/wireframe-prototyping"
}

# Навыки для Architect
show_arch_skills() {
    echo "🏗️  Навыки для Architect:"
    echo ""
    show_category "architecture"
    echo ""
    echo "📁 Пути к навыкам:"
    echo "  - $SKILLS_BASE/architecture-patterns"
    echo "  - $SKILLS_BASE/c4-architecture"
    echo "  - $SKILLS_BASE/architecture-diagrams"
    echo "  - $SKILLS_BASE/api-design-principles"
    echo "  - $SKILLS_BASE/microservices-patterns"
}

# Главная логика
case "$1" in
    --help|-h)
        show_help
        ;;
    --list-categories)
        list_categories
        ;;
    --category)
        if [ -z "$2" ]; then
            echo "❌ Укажите категорию"
            echo "Пример: ./search_skills_simple.sh --category product_business"
        else
            show_category "$2"
        fi
        ;;
    --search)
        if [ -z "$2" ]; then
            echo "❌ Укажите слово для поиска"
            echo "Пример: ./search_skills_simple.sh --search api"
        else
            search_skill "$2"
        fi
        ;;
    --pm)
        show_pm_skills
        ;;
    --ux)
        show_ux_skills
        ;;
    --arch)
        show_arch_skills
        ;;
    *)
        echo "❌ Неизвестная команда: $1"
        echo "Используйте --help для справки"
        exit 1
        ;;
esac

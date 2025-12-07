"""
Prompt templates for AI-generated summaries.

All prompts are in Polish to match the source documents.
"""

# Version tracking for prompts
PROMPT_VERSION = "v1"

# Simple title - plain language version of the legal title
PROMPT_TITLE_SIMPLE = """Jesteś ekspertem od komunikacji prawnej. Twoim zadaniem jest przetłumaczenie tytułu ustawy na prosty, zrozumiały język dla przeciętnego obywatela.

Tytuł ustawy:
{title}

Zasady:
1. Użyj prostego, codziennego języka
2. Zachowaj sens i istotę przepisu
3. Unikaj żargonu prawnego
4. Maksymalnie 1-2 zdania
5. Odpowiedz TYLKO przetłumaczonym tytułem, bez dodatkowych wyjaśnień

Prosty tytuł:"""

# Project description - what the law is about
PROMPT_DESCRIPTION = """Jesteś ekspertem od komunikacji prawnej. Na podstawie tytułu i dostępnych informacji o projekcie ustawy, napisz krótki opis wyjaśniający o czym jest ta ustawa.

Tytuł: {title}
Wnioskodawca: {initiator}
Data utworzenia: {creation_date}

Zasady:
1. Wyjaśnij główny cel ustawy w 2-3 zdaniach
2. Użyj prostego języka zrozumiałego dla każdego
3. Wspomnij kogo dotyczy ustawa (jeśli wiadomo)
4. Unikaj żargonu prawnego

Opis:"""

# OSR summary - based on PDF content
PROMPT_OSR_SUMMARY = """Jesteś ekspertem od analizy legislacyjnej. Na podstawie Oceny Skutków Regulacji (OSR) przygotuj zwięzłe podsumowanie dla obywatela.

Treść OSR:
{osr_content}

Przygotuj podsumowanie zawierające:
1. **Problem**: Jaki problem rozwiązuje ta regulacja? (1-2 zdania)
2. **Rozwiązanie**: Co proponuje ustawa? (1-2 zdania)
3. **Koszty**: Jakie są przewidywane koszty? (dla budżetu, firm, obywateli)
4. **Korzyści**: Jakie korzyści przyniesie ustawa?
5. **Termin**: Kiedy ma wejść w życie?

Użyj prostego języka. Odpowiedz w formacie markdown.

Podsumowanie OSR:"""

# Impact analysis - who is affected
PROMPT_IMPACT = """Jesteś ekspertem od analizy legislacyjnej. Na podstawie dostępnych informacji o projekcie ustawy, określ kogo dotyczy ta ustawa i jaki będzie jej wpływ.

Tytuł: {title}
Opis: {description}
Wnioskodawca: {initiator}

Określ:
1. **Grupy docelowe**: Kogo bezpośrednio dotyczy ta ustawa?
2. **Wpływ pozytywny**: Kto zyska na tej ustawie?
3. **Wpływ negatywny**: Kto może stracić lub ponieść koszty?
4. **Skala**: Czy dotyczy wszystkich obywateli, czy wybranej grupy?

Użyj prostego języka. Bądź konkretny.

Analiza wpływu:"""

# ŚCIEŻKA - App Blueprint

## 1. Complete App Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              APP ENTRY                                       │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                    ┌───────────────────────────────┐
                    │      Is User Logged In?       │
                    └───────────────────────────────┘
                           │                │
                          NO               YES
                           │                │
                           ▼                ▼
              ┌─────────────────┐   ┌─────────────────┐
              │   AUTH FLOW     │   │ Onboarding Done?│
              └─────────────────┘   └─────────────────┘
                                           │        │
                                          NO       YES
                                           │        │
                                           ▼        ▼
                              ┌─────────────────┐  ┌─────────────────┐
                              │ ONBOARDING FLOW │  │    MAIN APP     │
                              └─────────────────┘  └─────────────────┘
```

---

## 2. Auth Flow Screens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               AUTH FLOW                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│     SPLASH      │────▶│     LOGIN       │────▶│    REGISTER     │
│                 │     │                 │◀────│                 │
│   /             │     │   /login        │     │   /register     │
│                 │     │                 │     │                 │
└─────────────────┘     └────────┬────────┘     └────────┬────────┘
                                 │                       │
                                 │                       ▼
                                 │              ┌─────────────────┐
                                 │              │                 │
                                 │              │  EMAIL VERIFY   │
                                 │              │                 │
                                 │              │   /verify       │
                                 │              │                 │
                                 │              └────────┬────────┘
                                 │                       │
                                 ▼                       ▼
                        ┌─────────────────────────────────────────┐
                        │           CHECK ONBOARDING              │
                        └─────────────────────────────────────────┘


SCREEN DETAILS:
═══════════════

┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│        SPLASH           │  │         LOGIN           │  │       REGISTER          │
├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────────┤
│                         │  │                         │  │                         │
│                         │  │        Ścieżka          │  │      Załóż konto        │
│       [  LOGO  ]        │  │                         │  │                         │
│                         │  │  ┌───────────────────┐  │  │  ┌───────────────────┐  │
│        Ścieżka          │  │  │ Email             │  │  │  │ Email             │  │
│                         │  │  └───────────────────┘  │  │  └───────────────────┘  │
│   Śledź prawo.          │  │  ┌───────────────────┐  │  │  ┌───────────────────┐  │
│   Znaj swoich posłów.   │  │  │ Hasło             │  │  │  │ Hasło             │  │
│                         │  │  └───────────────────┘  │  │  └───────────────────┘  │
│                         │  │                         │  │  ┌───────────────────┐  │
│                         │  │  [ Zaloguj się      ]   │  │  │ Powtórz hasło     │  │
│                         │  │                         │  │  └───────────────────┘  │
│                         │  │  ─────── lub ───────    │  │                         │
│                         │  │                         │  │  [ Zarejestruj się  ]   │
│                         │  │  Nie masz konta?        │  │                         │
│                         │  │  Zarejestruj się →      │  │  Masz konto?            │
│                         │  │                         │  │  Zaloguj się →          │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘

┌─────────────────────────┐
│     EMAIL VERIFY        │
├─────────────────────────┤
│                         │
│          ✉️              │
│                         │
│   Sprawdź swoją         │
│   skrzynkę              │
│                         │
│   Wysłaliśmy link       │
│   weryfikacyjny na      │
│   jan@example.com       │
│                         │
│   [ Wyślij ponownie ]   │
│                         │
│   Wróć do logowania →   │
│                         │
└─────────────────────────┘
```

---

## 3. Onboarding Flow Screens

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            ONBOARDING FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   STEP 1        │────▶│   STEP 2        │────▶│   STEP 3        │────▶ MAIN APP
│   NAME          │     │   TOPICS        │     │   POLITICIANS   │
│                 │     │                 │     │                 │
│   /onboarding/1 │     │   /onboarding/2 │     │   /onboarding/3 │
│                 │     │                 │     │                 │
└─────────────────┘     └─────────────────┘     └─────────────────┘


SCREEN DETAILS:
═══════════════

┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐
│    STEP 1: NAME         │  │    STEP 2: TOPICS       │  │   STEP 3: POLITICIANS   │
├─────────────────────────┤  ├─────────────────────────┤  ├─────────────────────────┤
│                         │  │                         │  │                         │
│  Krok 1 z 3   ●○○       │  │  Krok 2 z 3   ●●○       │  │  Krok 3 z 3   ●●●       │
│                         │  │                         │  │                         │
│  Jak masz na imię?      │  │  Jakie tematy Cię       │  │  Kogo chcesz śledzić?   │
│                         │  │  interesują?            │  │                         │
│  ┌───────────────────┐  │  │  Wybierz min. 3         │  │  ┌───────────────────┐  │
│  │ Imię              │  │  │                         │  │  │ 🔍 Szukaj...      │  │
│  └───────────────────┘  │  │  ┌───────┐ ┌───────┐    │  │  └───────────────────┘  │
│                         │  │  │🏥Zdrow.│ │💼Praca│    │  │                         │
│                         │  │  └───────┘ └───────┘    │  │  Popularne              │
│                         │  │  ┌───────┐ ┌───────┐    │  │                         │
│                         │  │  │🎓Eduk.│ │🌍Klimat│   │  │  ┌───────────────────┐  │
│                         │  │  └───────┘ └───────┘    │  │  │👤 Donald Tusk [+] │  │
│                         │  │  ┌───────┐ ┌───────┐    │  │  │  KO               │  │
│                         │  │  │💰Podat.│ │🏠Mieszk│   │  │  └───────────────────┘  │
│                         │  │  └───────┘ └───────┘    │  │  ┌───────────────────┐  │
│                         │  │  ┌───────┐ ┌───────┐    │  │  │👤 J.Kaczyński [+] │  │
│                         │  │  │⚖️Prawo│ │🚗Trans.│   │  │  │  PiS              │  │
│                         │  │  └───────┘ └───────┘    │  │  └───────────────────┘  │
│                         │  │  ┌───────┐ ┌───────┐    │  │  ┌───────────────────┐  │
│                         │  │  │👨‍👩‍👧Rodz.│ │🔒Bezp.│    │  │  │👤 S.Hołownia [✓] │  │
│                         │  │  └───────┘ └───────┘    │  │  │  PL2050           │  │
│                         │  │                         │  │  └───────────────────┘  │
│                         │  │                         │  │                         │
│  [      Dalej →     ]   │  │  [← Wstecz] [Dalej →]   │  │  [← Wstecz][Rozpocznij] │
│                         │  │                         │  │                         │
└─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘
```

---

## 4. Main App Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MAIN APP                                        │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────────┐
                              │                 │
                              │   APP SHELL     │
                              │   (Layout)      │
                              │                 │
                              └────────┬────────┘
                                       │
           ┌───────────┬───────────┬───┴───┬───────────┬───────────┐
           │           │           │       │           │           │
           ▼           ▼           ▼       ▼           ▼           ▼
    ┌───────────┐┌───────────┐┌───────────┐┌───────────┐┌───────────┐
    │           ││           ││           ││           ││           │
    │   HOME    ││   NEWS    ││  BROWSE   ││ POLITICS  ││  PROFILE  │
    │           ││           ││           ││           ││           │
    │  /home    ││  /news    ││  /browse  ││ /politics ││ /profile  │
    │           ││           ││           ││           ││           │
    │  🏠       ││  📰       ││  🔍       ││  🏛️       ││  👤       │
    │           ││           ││           ││           ││           │
    └─────┬─────┘└─────┬─────┘└─────┬─────┘└─────┬─────┘└─────┬─────┘
          │            │            │            │            │
          ▼            ▼            ▼            ▼            ▼
    ┌───────────┐┌───────────┐┌───────────┐┌───────────┐┌───────────┐
    │Story Modal││Daily Summ.││Project    ││Politician ││Edit Topics│
    │           ││Weekly Sum.││  Detail   ││  Profile  ││Edit Politi│
    │           ││Followed   ││           ││           ││Settings   │
    └───────────┘└───────────┘└───────────┘└───────────┘└───────────┘


NAVIGATION:
═══════════

DESKTOP:                                    MOBILE:
┌────────┬─────────────────────────────┐    ┌─────────────────────────────┐
│        │                             │    │ ┌─────────────────────────┐ │
│ Ścieżka│                             │    │ │ 🔍 Szukaj...            │ │ ← Glass
│        │                             │    │ └─────────────────────────┘ │
│ ────── │                             │    │                             │
│        │                             │    │                             │
│ 🏠 Home│      MAIN CONTENT           │    │       MAIN CONTENT          │
│        │                             │    │                             │
│ 📰 News│                             │    │                             │
│        │                             │    │                             │
│ 🔍 Brow│                             │    │                             │
│        │                             │    ├─────────────────────────────┤
│ 🏛️ Pol │                             │    │ ┌─────────────────────────┐ │
│        │                             │    │ │ 🏠  📰  🔍  🏛️  👤    │ │ ← Glass
│ ────── │                             │    │ └─────────────────────────┘ │
│ 👤 Prof│                             │    └─────────────────────────────┘
└────────┴─────────────────────────────┘
```

---

## 5. All Main Screens Detail

### 5.1 HOME Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               HOME SCREEN                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐
│ 🔍 Szukaj...                │ ← Global search (glass)
├─────────────────────────────┤
│                             │
│ STORIES (horizontal scroll) │
│ ┌───┐┌───┐┌───┐┌───┐┌───┐  │
│ │ + ││🟢││🔴││⚪││🟢│  │ ← Rings indicate update type
│ │Add││   ││   ││   ││   │  │   🟢 = positive (passed, signed)
│ └───┘└───┘└───┘└───┘└───┘  │   🔴 = negative (rejected, vetoed)
│ Dodaj Proj1 Proj2 Proj3 ...│   ⚪ = neutral (status change)
│                             │
├─────────────────────────────┤
│                             │
│ Popularne teraz             │ ← Section header
│                             │
│ ┌─────────────────────────┐ │
│ │ 🏛️ Sejm           12h   │ │ ← Category + time
│ │                         │ │
│ │ Ustawa o zmianie        │ │ ← Title (max 2 lines)
│ │ Kodeksu pracy została   │ │
│ │ uchwalona 428 głosami.  │ │ ← Description
│ │                         │ │
│ │ ●────────────────────●  │ │ ← Progress path
│ │ RCL SEJM SENAT PREZ DzU │ │
│ │                         │ │
│ │ 💬 24  🔄 156  ❤️ 1.2k  │ │ ← Interactions (placeholder)
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🏥 Zdrowie         2d   │ │
│ │                         │ │
│ │ Projekt o produktach    │ │
│ │ biobójczych czeka na    │ │
│ │ podpis Prezydenta.      │ │
│ │                         │ │
│ │ ●───────────────────○   │ │
│ │ RCL SEJM SENAT PREZ     │ │
│ │                         │ │
│ │ 💬 8   🔄 42   ❤️ 234   │ │
│ └─────────────────────────┘ │
│                             │
│ [Load more...]              │
│                             │
├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │ ← Bottom nav (glass)
└─────────────────────────────┘


STORY MODAL (when story tapped):
════════════════════════════════

┌─────────────────────────────┐
│                        [✕]  │
│                             │
│ ┌─────────────────────────┐ │
│ │                         │ │
│ │     🟢 POZYTYWNA        │ │ ← Status indicator
│ │       ZMIANA            │ │
│ │                         │ │
│ │ Ustawa o produktach     │ │ ← Project title
│ │ biobójczych             │ │
│ │                         │ │
│ │ ────────────────────    │ │
│ │                         │ │
│ │ Senat przyjął ustawę    │ │ ← What happened
│ │ bez poprawek            │ │
│ │                         │ │
│ │ 16 października 2025    │ │ ← When
│ │                         │ │
│ │ [Zobacz szczegóły →]    │ │ ← CTA to project detail
│ │                         │ │
│ └─────────────────────────┘ │
│                             │
│ ────────●──────────────     │ ← Progress indicator
│                             │
└─────────────────────────────┘
```

### 5.2 NEWS Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                               NEWS SCREEN                                    │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐
│ 🔍 Szukaj...                │
├─────────────────────────────┤
│                             │
│ Podsumowania                │ ← Section: Summary cards
│                             │
│ ┌───────┐┌───────┐┌───────┐ │
│ │  📅   ││  📆   ││  ★    │ │
│ │ Dziś  ││Tydzień││Śledzone│ │
│ └───────┘└───────┘└───────┘ │
│                             │
├─────────────────────────────┤
│                             │
│ Kategorie                   │ ← Section: Filter chips
│                             │
│ [Wszystko] [Rząd]           │
│ [Prezydent] [Ważne]         │
│ [Sejm] [Senat]              │
│                             │
├─────────────────────────────┤
│                             │
│ Najnowsze                   │ ← Section: Feed
│                             │
│ ┌─────────────────────────┐ │
│ │ 🟢 14:32                │ │ ← Type indicator + time
│ │                         │ │
│ │ Prezydent podpisał      │ │
│ │ ustawę o zmianie        │ │
│ │ Kodeksu pracy           │ │
│ │                         │ │
│ │ Wejdzie w życie         │ │
│ │ 1 stycznia 2026 r.      │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ ⚪ 12:15                │ │
│ │                         │ │
│ │ Komisja Zdrowia         │ │
│ │ zakończyła prace        │ │
│ │                         │ │
│ │ Sprawozdawca:           │ │
│ │ Anna Sobolak            │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🔴 wczoraj              │ │
│ │                         │ │
│ │ Prezydent zawetował     │ │
│ │ ustawę o Parku          │ │
│ │ Narodowym Doliny Odry   │ │
│ └─────────────────────────┘ │
│                             │
├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │
└─────────────────────────────┘


SUMMARY MODAL (Daily/Weekly):
═════════════════════════════

┌─────────────────────────────┐
│ Podsumowanie dnia      [✕]  │
├─────────────────────────────┤
│                             │
│ 6 grudnia 2025              │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🟢 2 ustawy podpisane   │ │
│ │ 🔴 1 ustawa zawetowana  │ │
│ │ ⚪ 5 projektów zmieniło │ │
│ │   status                │ │
│ └─────────────────────────┘ │
│                             │
│ Kluczowe wydarzenia:        │
│                             │
│ • Kodeks pracy - podpisany  │
│ • Park Narodowy - WETO      │
│ • Podatki - II czytanie     │
│                             │
│ [Zobacz wszystkie →]        │
│                             │
└─────────────────────────────┘
```

### 5.3 BROWSE Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              BROWSE SCREEN                                   │
└─────────────────────────────────────────────────────────────────────────────┘

DEFAULT VIEW (Categories):              SEARCH VIEW (Results):
══════════════════════════              ══════════════════════

┌─────────────────────────────┐         ┌─────────────────────────────┐
│ 🔍 Szukaj ustawy...         │         │ 🔍 kodeks pracy        [✕]  │
├─────────────────────────────┤         ├─────────────────────────────┤
│                             │         │                             │
│ Filtruj                     │         │ [Typ▼] [Status▼] [Rok▼]    │
│ [Typ▼] [Status▼] [Rok▼] [⚙️]│         │                             │
│                             │         │ 23 wyniki                   │
├─────────────────────────────┤         │                             │
│                             │         │ ┌─────────────────────────┐ │
│ 🚂 POCIĄGI LEGISLACYJNE     │         │ │              OPUBLIK.   │ │
│                             │         │ │ Zmiana Kodeksu pracy    │ │
│ ┌─────────────────────────┐ │         │ │ DU/2025/1423            │ │
│ │ 🏥 ZDROWIE              │ │         │ │                         │ │
│ │                         │ │         │ │ Podpisana 15.10.2025    │ │
│ │ ████░░░░ 3 w Sejmie     │ │         │ │ ●───────────────────●   │ │
│ │ ██████░░ 5 w RCL        │ │         │ └─────────────────────────┘ │
│ │ ████████ 2 opublikowane │ │         │                             │
│ │                         │ │         │ ┌─────────────────────────┐ │
│ │ [Zobacz 10 projektów →] │ │         │ │                   RCL   │ │
│ └─────────────────────────┘ │         │ │ Zmiana Kodeksu          │ │
│                             │         │ │ postępowania karnego    │ │
│ ┌─────────────────────────┐ │         │ │                         │ │
│ │ 💼 PRACA                │ │         │ │ Etap 7/14               │ │
│ │                         │ │         │ │ ●────────○              │ │
│ │ ██░░░░░░ 1 w Sejmie     │ │         │ └─────────────────────────┘ │
│ │ ████████ 4 w RCL        │ │         │                             │
│ │ ██████████ 3 opublik.   │ │         │ ┌─────────────────────────┐ │
│ │                         │ │         │ │                  SEJM   │ │
│ │ [Zobacz 8 projektów →]  │ │         │ │ Zmiana Kodeksu          │ │
│ └─────────────────────────┘ │         │ │ cywilnego               │ │
│                             │         │ │                         │ │
│ ┌─────────────────────────┐ │         │ │ II czytanie             │ │
│ │ 💰 PODATKI              │ │         │ │ ●──────────○            │ │
│ │                         │ │         │ └─────────────────────────┘ │
│ │ ████████ 4 w Sejmie     │ │         │                             │
│ │ ██████░░ 3 w RCL        │ │         │                             │
│ │ ██████████ 5 opublik.   │ │         │                             │
│ │                         │ │         │                             │
│ │ [Zobacz 12 projektów →] │ │         │                             │
│ └─────────────────────────┘ │         │                             │
│                             │         │                             │
├─────────────────────────────┤         ├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │         │ 🏠    📰    🔍    🏛️    👤  │
└─────────────────────────────┘         └─────────────────────────────┘


PROJECT DETAIL (when project tapped):
═════════════════════════════════════

┌─────────────────────────────┐
│ ← Wróć                 [★]  │ ← Back + Follow
├─────────────────────────────┤
│                             │
│ Ustawa o zmianie            │ ← Title
│ Kodeksu pracy               │
│                             │
│ DU/2025/1423 • Opublikowana │ ← ELI + Status badge
│                             │
│ ┌─────────────────────────┐ │
│ │ ●─────────────────────● │ │ ← Progress path
│ │ RCL SEJM SENAT PREZ DzU │ │
│ │  ✓   ✓    ✓    ✓   ✓   │ │
│ └─────────────────────────┘ │
│                             │
├─────────────────────────────┤
│                             │
│ Głosowanie                  │
│                             │
│ 428 za • 3 przeciw • 0 wstrz│
│                             │
│ [Zobacz partie →]           │ ← Opens voting breakdown
│                             │
├─────────────────────────────┤
│                             │
│ Informacje                  │
│                             │
│ Inicjator: Rada Ministrów   │
│ Utworzono: 2024-03-15       │
│ Podpisano: 2025-10-15       │
│                             │
├─────────────────────────────┤
│                             │
│ Komisje                     │
│ • NKK - Komisja Nadzwyczajna│
│   Przew.: B. Dolniak (KO)   │
│                             │
│ Sprawozdawca                │
│ • Sławomir Ćwik             │
│                             │
├─────────────────────────────┤
│                             │
│ Oś czasu                    │
│                             │
│ 15.10 • Prezydent podpisał  │
│ 26.09 • Sejm przyjął poprawk│
│ 24.09 • Senat wniósł poprawk│
│ 12.09 • III czytanie        │
│ ...                         │
│                             │
├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │
└─────────────────────────────┘


VOTING BREAKDOWN MODAL:
═══════════════════════

┌─────────────────────────────┐
│ Głosowanie             [✕]  │
├─────────────────────────────┤
│                             │
│ III czytanie                │
│ 26 września 2025            │
│                             │
│ ┌─────────────────────────┐ │
│ │       PRZYJĘTO          │ │
│ │                         │ │
│ │   428     3      0      │ │
│ │   ZA   PRZECIW WSTRZ    │ │
│ │                         │ │
│ │ [██████████████████░░]  │ │
│ │  99%              1%    │ │
│ └─────────────────────────┘ │
│                             │
│ Jak głosowały partie        │
│                             │
│ ┌─────────────────────────┐ │
│ │ KO               146 ZA │ │
│ │ [██████████████████████]│ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ PiS              175 ZA │ │
│ │ [██████████████████████]│ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ PSL-TD            30 ZA │ │
│ │ [██████████████████████]│ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ Lewica            18 ZA │ │
│ │ [██████████████████████]│ │
│ └─────────────────────────┘ │
│                             │
│ + 6 więcej partii           │
│                             │
└─────────────────────────────┘
```

### 5.4 POLITICS Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             POLITICS SCREEN                                  │
└─────────────────────────────────────────────────────────────────────────────┘

MAIN VIEW:                              POLITICIAN PROFILE:
══════════                              ════════════════════

┌─────────────────────────────┐         ┌─────────────────────────────┐
│ 🔍 Szukaj polityka...       │         │ ← Wróć                 [★]  │
├─────────────────────────────┤         ├─────────────────────────────┤
│                             │         │                             │
│ Partie                      │         │      ┌─────────┐            │
│                             │         │      │   👤    │            │
│ [Wszystkie▼] [Sejm] [Senat] │         │      │  foto   │            │
│                             │         │      └─────────┘            │
│ ┌────┐┌────┐┌────┐┌────┐    │         │                             │
│ │ KO ││PiS ││TD  ││Lew.│    │         │    Anna Sobolak             │
│ │157 ││188 ││ 32 ││ 26 │    │         │    Koalicja Obywatelska     │
│ └────┘└────┘└────┘└────┘    │         │    Poseł X kadencji         │
│                             │         │                             │
├─────────────────────────────┤         ├─────────────────────────────┤
│                             │         │                             │
│ Posłowie                    │         │ Statystyki                  │
│                             │         │                             │
│ ┌─────────────────────────┐ │         │ ┌─────────┐ ┌─────────┐     │
│ │ 👤 Donald Tusk          │ │         │ │  94%    │ │  98%    │     │
│ │    Koalicja Obywatelska │ │         │ │Obecność │ │Z partią │     │
│ │                         │ │         │ └─────────┘ └─────────┘     │
│ │    94% obecność         │ │         │                             │
│ │    98% z partią         │ │         ├─────────────────────────────┤
│ │                         │ │         │                             │
│ │    [Zobacz profil →]    │ │         │ Ostatnie głosowania         │
│ └─────────────────────────┘ │         │                             │
│                             │         │ ┌─────────────────────────┐ │
│ ┌─────────────────────────┐ │         │ │ 🟢 ZA                   │ │
│ │ 👤 Jarosław Kaczyński   │ │         │ │ Zmiana Kodeksu pracy    │ │
│ │    PiS                  │ │         │ │ 12.09.2025              │ │
│ │                         │ │         │ └─────────────────────────┘ │
│ │    87% obecność         │ │         │                             │
│ │    99% z partią         │ │         │ ┌─────────────────────────┐ │
│ │                         │ │         │ │ 🟢 ZA                   │ │
│ │    [Zobacz profil →]    │ │         │ │ Ustawa o biobójczych    │ │
│ └─────────────────────────┘ │         │ │ 26.09.2025              │ │
│                             │         │ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │         │                             │
│ │ 👤 Szymon Hołownia      │ │         │ ┌─────────────────────────┐ │
│ │    Polska 2050          │ │         │ │ ⚪ NIEOBECNY            │ │
│ │    Marszałek Sejmu      │ │         │ │ Zmiana ustawy o VAT     │ │
│ │                         │ │         │ │ 05.09.2025              │ │
│ │    92% obecność         │ │         │ └─────────────────────────┘ │
│ │                         │ │         │                             │
│ │    [Zobacz profil →]    │ │         │ [Zobacz wszystkie →]        │
│ └─────────────────────────┘ │         │                             │
│                             │         ├─────────────────────────────┤
│                             │         │                             │
│                             │         │ Sprawozdawca ustaw          │
│                             │         │ • Ustawa o biobójczych      │
│                             │         │ • Zmiana ustawy o zdrowiu   │
│                             │         │                             │
├─────────────────────────────┤         ├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │         │ 🏠    📰    🔍    🏛️    👤  │
└─────────────────────────────┘         └─────────────────────────────┘
```

### 5.5 PROFILE Screen

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             PROFILE SCREEN                                   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────┐
│                             │
├─────────────────────────────┤
│                             │
│      ┌─────────┐            │
│      │   👤    │            │ ← Avatar
│      └─────────┘            │
│        Jan                  │ ← Name from onboarding
│   jan@example.com           │ ← Email
│                             │
├─────────────────────────────┤
│                             │
│ ┌─────────────────────────┐ │
│ │ ★ Śledzone projekty  12 │ │ ← Links to list
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 👥 Śledzeni politycy  5 │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🏷️ Moje tematy        8 │ │
│ └─────────────────────────┘ │
│                             │
├─────────────────────────────┤
│                             │
│ Ustawienia                  │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🔔 Powiadomienia      → │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ 🎨 Wygląd             → │ │
│ └─────────────────────────┘ │
│                             │
│ ┌─────────────────────────┐ │
│ │ ℹ️ O aplikacji         → │ │
│ └─────────────────────────┘ │
│                             │
├─────────────────────────────┤
│                             │
│ [     Wyloguj się       ]   │
│                             │
├─────────────────────────────┤
│ 🏠    📰    🔍    🏛️    👤  │
└─────────────────────────────┘
```

---

## 6. Complete Screen Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           COMPLETE SCREEN MAP                                │
└─────────────────────────────────────────────────────────────────────────────┘

TOTAL SCREENS: 19

AUTH (4 screens):
├── /                    → Splash
├── /login               → Login
├── /register            → Register
└── /verify              → Email Verification

ONBOARDING (3 screens):
├── /onboarding/name     → Step 1: Name
├── /onboarding/topics   → Step 2: Topics
└── /onboarding/politicians → Step 3: Politicians

MAIN APP (7 screens):
├── /home                → Home (Stories + Feed)
├── /news                → News (Summaries + Updates)
├── /browse              → Browse (Categories + Search)
├── /politics            → Politics (List)
├── /profile             → Profile (Settings)
├── /project/:id         → Project Detail
└── /politician/:id      → Politician Profile

MODALS (5 modals):
├── StoryModal           → Story expanded view
├── DailySummaryModal    → Daily summary
├── WeeklySummaryModal   → Weekly summary
├── VotingBreakdownModal → Party voting
└── FollowedSummaryModal → Followed projects summary
```

---

## 7. Implementation Chain

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         IMPLEMENTATION ORDER                                 │
└─────────────────────────────────────────────────────────────────────────────┘

PHASE 1: Foundation (Day 1 Morning)
═══════════════════════════════════
┌─────┐
│  1  │ Project Setup
├─────┤
│     │ • Create Vite + React + TypeScript project
│     │ • Install dependencies (supabase, framer-motion, tailwind, react-query)
│     │ • Configure Tailwind with custom design tokens
│     │ • Set up folder structure
│     │ • Configure environment variables
└─────┘
    │
    ▼
┌─────┐
│  2  │ Supabase Setup
├─────┤
│     │ • Enable Auth in Supabase dashboard
│     │ • Configure email templates
│     │ • Create supabase client (lib/supabase.ts)
│     │ • Set up auth context/provider
└─────┘
    │
    ▼
┌─────┐
│  3  │ Database Migrations
├─────┤
│     │ • 20251213_001_user_profiles.sql
│     │ • 20251213_002_development_logs.sql
│     │ • 20251213_003_politicians.sql
│     │ • Run migrations: supabase db push
└─────┘


PHASE 2: Auth Flow (Day 1 Afternoon)
════════════════════════════════════
┌─────┐
│  4  │ Base Components
├─────┤
│     │ • Button.tsx
│     │ • Input.tsx
│     │ • Card.tsx
│     │ • Badge.tsx
│     │ • Modal.tsx
└─────┘
    │
    ▼
┌─────┐
│  5  │ Auth Screens
├─────┤
│     │ • Splash screen (/)
│     │ • Login screen (/login)
│     │ • Register screen (/register)
│     │ • Email verify screen (/verify)
│     │ • Auth redirect logic
└─────┘
    │
    ▼
┌─────┐
│  6  │ Auth Guards
├─────┤
│     │ • ProtectedRoute component
│     │ • OnboardingGuard component
│     │ • Auth state persistence
└─────┘


PHASE 3: Onboarding Flow (Day 1 Evening)
════════════════════════════════════════
┌─────┐
│  7  │ Onboarding Screens
├─────┤
│     │ • Step 1: Name (/onboarding/name)
│     │ • Step 2: Topics (/onboarding/topics)
│     │ • Step 3: Politicians (/onboarding/politicians)
│     │ • Progress indicator component
│     │ • Onboarding completion logic
└─────┘


PHASE 4: App Shell (Day 2 Morning)
══════════════════════════════════
┌─────┐
│  8  │ Layout Components
├─────┤
│     │ • GlassSearchBar.tsx (mobile top)
│     │ • BottomNav.tsx (mobile bottom, glass effect)
│     │ • Sidebar.tsx (desktop)
│     │ • AppLayout.tsx (responsive wrapper)
│     │ • useMediaQuery hook
└─────┘
    │
    ▼
┌─────┐
│  9  │ Routing Setup
├─────┤
│     │ • Configure react-router
│     │ • Set up route guards
│     │ • Configure layouts per route group
└─────┘


PHASE 5: Home Screen (Day 2 Afternoon)
══════════════════════════════════════
┌─────┐
│ 10  │ Stories Components
├─────┤
│     │ • StoryCircle.tsx (single story with ring)
│     │ • StoryCarousel.tsx (horizontal scroll)
│     │ • StoryModal.tsx (expanded view)
│     │ • useUserStories hook (fetch followed projects)
└─────┘
    │
    ▼
┌─────┐
│ 11  │ Feed Components
├─────┤
│     │ • PostCard.tsx (Twitter-style card)
│     │ • PostFeed.tsx (infinite scroll list)
│     │ • ProgressPath.tsx (visual progress bar)
│     │ • usePopularPosts hook
└─────┘
    │
    ▼
┌─────┐
│ 12  │ Home Screen Assembly
├─────┤
│     │ • /home page.tsx
│     │ • Connect stories + feed
│     │ • Add pull-to-refresh
│     │ • Add infinite scroll
└─────┘


PHASE 6: News Screen (Day 2 Evening)
════════════════════════════════════
┌─────┐
│ 13  │ News Components
├─────┤
│     │ • SummaryCard.tsx (daily/weekly/followed)
│     │ • CategoryChips.tsx (filter buttons)
│     │ • NewsItem.tsx (individual update)
│     │ • SummaryModal.tsx (expanded summary)
└─────┘
    │
    ▼
┌─────┐
│ 14  │ News Screen Assembly
├─────┤
│     │ • /news page.tsx
│     │ • useDevelopments hook
│     │ • Filter logic
│     │ • Summary generation
└─────┘


PHASE 7: Browse Screen (Day 3 Morning)
══════════════════════════════════════
┌─────┐
│ 15  │ Browse Components
├─────┤
│     │ • CategoryCard.tsx (train category)
│     │ • FilterDropdown.tsx
│     │ • ProjectListItem.tsx (search result)
│     │ • SearchBar.tsx (with filters)
└─────┘
    │
    ▼
┌─────┐
│ 16  │ Project Detail
├─────┤
│     │ • ProjectDetailPage.tsx
│     │ • VotingSection.tsx
│     │ • TimelineSection.tsx
│     │ • CommitteesSection.tsx
│     │ • VotingBreakdownModal.tsx
└─────┘
    │
    ▼
┌─────┐
│ 17  │ Browse Screen Assembly
├─────┤
│     │ • /browse page.tsx
│     │ • /project/:id page.tsx
│     │ • useProjects hook
│     │ • useProjectDetail hook
│     │ • Search + filter logic
└─────┘


PHASE 8: Politics Screen (Day 3 Afternoon)
══════════════════════════════════════════
┌─────┐
│ 18  │ Politics Components
├─────┤
│     │ • PartyFilter.tsx (party chips)
│     │ • PoliticianCard.tsx (list item)
│     │ • VoteIndicator.tsx (yes/no/abstain)
│     │ • StatsCard.tsx (attendance, party loyalty)
└─────┘
    │
    ▼
┌─────┐
│ 19  │ Politician Profile
├─────┤
│     │ • PoliticianProfilePage.tsx
│     │ • VotingHistoryList.tsx
│     │ • ReportedBillsList.tsx
└─────┘
    │
    ▼
┌─────┐
│ 20  │ Politics Screen Assembly
├─────┤
│     │ • /politics page.tsx
│     │ • /politician/:id page.tsx
│     │ • usePoliticians hook
│     │ • usePoliticianDetail hook
└─────┘


PHASE 9: Profile Screen (Day 3 Evening)
═══════════════════════════════════════
┌─────┐
│ 21  │ Profile Components
├─────┤
│     │ • ProfileHeader.tsx
│     │ • FollowedList.tsx
│     │ • SettingsItem.tsx
│     │ • LogoutButton.tsx
└─────┘
    │
    ▼
┌─────┐
│ 22  │ Profile Screen Assembly
├─────┤
│     │ • /profile page.tsx
│     │ • Edit topics modal
│     │ • Edit politicians modal
│     │ • Settings screens
└─────┘


PHASE 10: Polish & Deploy (Day 4)
═════════════════════════════════
┌─────┐
│ 23  │ Animations
├─────┤
│     │ • Page transitions (Framer Motion)
│     │ • List animations (stagger)
│     │ • Story modal animation
│     │ • Progress path animation
│     │ • Micro-interactions
└─────┘
    │
    ▼
┌─────┐
│ 24  │ Final Polish
├─────┤
│     │ • Loading states
│     │ • Error states
│     │ • Empty states
│     │ • Accessibility audit
│     │ • Performance optimization
└─────┘
    │
    ▼
┌─────┐
│ 25  │ Deploy
├─────┤
│     │ • Build production bundle
│     │ • Configure Netlify
│     │ • Set environment variables
│     │ • Deploy
│     │ • Test on real devices
└─────┘
```

---

## 8. Implementation Checklist

```
PHASE 1: Foundation
[ ] Project setup (Vite + React + TS)
[ ] Dependencies installed
[ ] Tailwind configured
[ ] Folder structure created
[ ] Supabase client configured
[ ] Database migrations created and pushed

PHASE 2: Auth
[ ] Button component
[ ] Input component
[ ] Card component
[ ] Splash screen
[ ] Login screen
[ ] Register screen
[ ] Email verify screen
[ ] Auth guards

PHASE 3: Onboarding
[ ] Step 1: Name
[ ] Step 2: Topics
[ ] Step 3: Politicians
[ ] Progress indicator
[ ] Completion logic

PHASE 4: App Shell
[ ] GlassSearchBar
[ ] BottomNav
[ ] Sidebar
[ ] AppLayout
[ ] Routing

PHASE 5: Home
[ ] StoryCircle
[ ] StoryCarousel
[ ] StoryModal
[ ] PostCard
[ ] PostFeed
[ ] ProgressPath
[ ] Home page assembly

PHASE 6: News
[ ] SummaryCard
[ ] CategoryChips
[ ] NewsItem
[ ] SummaryModal
[ ] News page assembly

PHASE 7: Browse
[ ] CategoryCard
[ ] FilterDropdown
[ ] ProjectListItem
[ ] Project detail page
[ ] VotingBreakdownModal
[ ] Browse page assembly

PHASE 8: Politics
[ ] PartyFilter
[ ] PoliticianCard
[ ] VoteIndicator
[ ] Politician profile page
[ ] Politics page assembly

PHASE 9: Profile
[ ] ProfileHeader
[ ] FollowedList
[ ] SettingsItem
[ ] Profile page assembly

PHASE 10: Polish
[ ] Animations
[ ] Loading states
[ ] Error states
[ ] Empty states
[ ] Deploy to Netlify
```

---

## 9. File Structure (Final)

```
frontend/
├── public/
│   ├── favicon.ico
│   └── logo.svg
│
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx              # Splash
│   │   │   ├── login/page.tsx
│   │   │   ├── register/page.tsx
│   │   │   └── verify/page.tsx
│   │   │
│   │   ├── (onboarding)/
│   │   │   ├── layout.tsx
│   │   │   ├── name/page.tsx
│   │   │   ├── topics/page.tsx
│   │   │   └── politicians/page.tsx
│   │   │
│   │   ├── (app)/
│   │   │   ├── layout.tsx            # App shell
│   │   │   ├── home/page.tsx
│   │   │   ├── news/page.tsx
│   │   │   ├── browse/page.tsx
│   │   │   ├── politics/page.tsx
│   │   │   ├── profile/page.tsx
│   │   │   ├── project/[id]/page.tsx
│   │   │   └── politician/[id]/page.tsx
│   │   │
│   │   └── layout.tsx                # Root layout
│   │
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Modal.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── layout/
│   │   │   ├── GlassSearchBar.tsx
│   │   │   ├── BottomNav.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── AppLayout.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── auth/
│   │   │   ├── AuthGuard.tsx
│   │   │   ├── OnboardingGuard.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── onboarding/
│   │   │   ├── ProgressIndicator.tsx
│   │   │   ├── TopicChip.tsx
│   │   │   ├── PoliticianItem.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── stories/
│   │   │   ├── StoryCircle.tsx
│   │   │   ├── StoryCarousel.tsx
│   │   │   ├── StoryModal.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── feed/
│   │   │   ├── PostCard.tsx
│   │   │   ├── PostFeed.tsx
│   │   │   ├── ProgressPath.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── news/
│   │   │   ├── SummaryCard.tsx
│   │   │   ├── CategoryChips.tsx
│   │   │   ├── NewsItem.tsx
│   │   │   ├── SummaryModal.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── browse/
│   │   │   ├── CategoryCard.tsx
│   │   │   ├── FilterDropdown.tsx
│   │   │   ├── ProjectListItem.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── project/
│   │   │   ├── VotingSection.tsx
│   │   │   ├── TimelineSection.tsx
│   │   │   ├── CommitteesSection.tsx
│   │   │   ├── VotingBreakdownModal.tsx
│   │   │   └── index.ts
│   │   │
│   │   ├── politics/
│   │   │   ├── PartyFilter.tsx
│   │   │   ├── PoliticianCard.tsx
│   │   │   ├── VoteIndicator.tsx
│   │   │   ├── StatsCard.tsx
│   │   │   ├── VotingHistoryList.tsx
│   │   │   └── index.ts
│   │   │
│   │   └── profile/
│   │       ├── ProfileHeader.tsx
│   │       ├── FollowedList.tsx
│   │       ├── SettingsItem.tsx
│   │       └── index.ts
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useMediaQuery.ts
│   │   ├── useProjects.ts
│   │   ├── useProjectDetail.ts
│   │   ├── useDevelopments.ts
│   │   ├── usePoliticians.ts
│   │   ├── usePoliticianDetail.ts
│   │   ├── useUserStories.ts
│   │   └── usePopularPosts.ts
│   │
│   ├── lib/
│   │   ├── supabase.ts
│   │   ├── types.ts
│   │   ├── utils.ts
│   │   └── constants.ts
│   │
│   ├── styles/
│   │   └── globals.css
│   │
│   └── main.tsx
│
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
├── vite.config.ts
└── netlify.toml
```

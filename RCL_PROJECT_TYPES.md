# RCL Project Types Reference

## Overview

RCL (legislacja.rcl.gov.pl) tracks **government-stage** legislative work before it reaches Parliament.

---

## Project Types

| typeId | Name | Count | Description |
|--------|------|-------|-------------|
| **1** | Projekty założeń projektów ustaw | 215 | **Draft law assumptions** - conceptual stage before actual bill drafting (largely obsolete since 2016) |
| **2** | Projekty ustaw | 2,431 | **Draft laws (bills)** - actual bill text going through government process toward Sejm |
| **3** | Rozporządzenia Rady Ministrów | 2,399 | **Council of Ministers regulations** - executive regulations by full cabinet |
| **4** | Rozporządzenia Prezesa RM | 1,134 | **Prime Minister regulations** - executive regulations by PM alone |
| **5** | Rozporządzenia Ministrów | 17,854 | **Ministerial regulations** - regulations by individual ministers |
| **6** | OSR ex post | 46 | **Post-implementation reviews** - impact assessment after law is in force |
| **10** | Rozporządzenia (all) | 21,413 | **All regulations** - combined view of types 3+4+5 |

---

## Our Focus

**Primary:** typeId=2 (Draft laws) - These become actual laws via Sejm

**Secondary:** typeId=3,4,5 (Regulations) - Important but don't go through Parliament

**Reference:** typeId=6 (OSR ex post) - Useful for impact analysis patterns

---

## Key Insight

- **Bills (typeId=2)** go: RCL → Sejm → Senate → President → Dziennik Ustaw
- **Regulations (typeId=3,4,5)** go: RCL → Direct publication (no Parliament)

For the hackathon demo, we focus on **typeId=2** to show the full legislative journey.

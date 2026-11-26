# KRR Project 1 - Resolution & Davis-Putnam SAT Solver
**Knowledge Representation and Reasoning (KRR) — 2026**  
**Faculty of Mathematics and Computer Science, University of Bucharest (FMI UniBuc)**  
**Student:** Coman Ioan Alexandru  
**Instructor:** Conf. dr. Marina Anca Cidotă  

---

## 📁 Project Structure

```
C:/Users/legio/Projects/KRR/Project 1/
├── src/                          # Core Prolog implementations (NO explanatory comments as mandated)
│   ├── parser.pl                 # Strict DCG grammar parser for canonical CNF and FOL terms
│   ├── resolution_prop.pl        # Propositional resolution prover with optimizations (C5 p.6)
│   ├── resolution_fol.pl         # First-Order Logic resolution theorem prover
│   ├── davis_putnam.pl           # Davis-Putnam SAT solver (with • operation & 2 strategies)
│   └── main.pl                   # Automated test suite runner
├── gui/
│   └── app.py                    # Graphical User Interface (Python Tkinter)
├── tests/                        # Pre-configured canonical test sets (.txt)
│   ├── s1_prop_1.txt ... 5.txt   # Subject 1 propositional resolution mandatory tests (i - v)
│   ├── s1_fol_own.txt            # Subject 1 FOL: Own student graduation example
│   ├── s1_fol_c3_p30.txt         # Subject 1 FOL: Course example (C3 p.30 Socrates)
│   ├── s1_fol_c3_p33.txt         # Subject 1 FOL: Course example (C3 p.33 Animal lover)
│   ├── s1_fol_c4_p12.txt         # Subject 1 FOL: Course example (C4 p.12 Barber paradox)
│   └── s2_dp_1.txt ... 6.txt     # Subject 2 Davis-Putnam mandatory tests (i - vi)
├── doc/
│   ├── generate_pdf.py           # Automated PDF compiler using ReportLab
│   ├── generate_tree_image.py    # Resolution tree figure generator
│   ├── resolution_tree.png       # Figure 1 for report Section 1.b
│   ├── oral_defense_guide.md     # Line-by-line Romanian oral defense study guide
│   ├── report_draft.md           # Markdown draft of the academic report
│   └── Coman_Ioan_Alexandru_project1.pdf   # Final submission PDF (report + code appendix)
└── README.md
```

---

## 📐 Canonical CNF Input Format

The parser (`src/parser.pl`) enforces **one strict canonical ASCII format** aligned with `Project 1.pdf` and `tests/*.txt` (no syntax aliases or fallbacks):

* **Empty KB:** empty or whitespace-only file `""` $\rightarrow$ `[]`.
* **Clauses (`>= 1`):** joined strictly with `"and"` (whitespace: `' '`, `\t`, `\n`, `\r` allowed around tokens).
* **Empty clause:** strictly `[]` $\rightarrow$ `[]`.
* **Multi-literal clause (`>= 2` literals):** strictly parenthesized `(L1 or L2 ...)`, literals joined with `"or"`.
* **Unit clause (`1` literal):** strictly unparenthesized literal `L` (e.g. `not b`, `e`, `man(socrates)`).
* **Negation:** strictly `"not "` followed by whitespace (`not a`, `not man(X)`).
* **Identifiers:** lowercase start (`[a-z][a-zA-Z0-9_]*`) for propositions/constants/functors; uppercase start (`[A-Z][a-zA-Z0-9_]*`) for FOL variables (`var(Name)`). Nested FOL terms use `f(arg1, arg2)`.
* **Internal clause representation:** `[Clause1, Clause2, ...]` where each clause is a list of `pos(Term)` / `neg(Term)` literals.

---

## 🚀 How to Run

### 1. Graphical User Interface (GUI)
Run the interactive GUI (Python Tkinter):
```powershell
python "C:\Users\legio\Projects\KRR\Project 1\gui\app.py"
```
Features:
* **Propositional Resolution tab:** Pick from preset examples (1–5) or load `.txt` files, view step-by-step resolution derivations and total operation count.
* **FOL Resolution tab:** Run own student graduation example or course benchmarks, inspect unified resolvents and total operations.
* **Davis-Putnam tab:** Test satisfiability on benchmark sets, pick between Strategy 1 (MOMS) and Strategy 2 (DLIS), compare results side-by-side, and inspect truth assignments `{w/true; s/false; ...}`.

### 2. Command Line Automated Test Suite (SWI-Prolog)
Run all 15 tests across Propositional Resolution, FOL Resolution, and Davis-Putnam:
```powershell
swipl -s "C:\Users\legio\Projects\KRR\Project 1\src\main.pl" -g "run_all, halt."
```

### 3. Re-generating the Final Submission PDF
```powershell
python "C:\Users\legio\Projects\KRR\Project 1\doc\generate_pdf.py"
```
The output file is saved as:
`C:\Users\legio\Projects\KRR\Project 1\doc\Coman_Ioan_Alexandru_project1.pdf`

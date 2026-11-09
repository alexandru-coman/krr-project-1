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
│   ├── parser.pl                 # Definite Clause Grammar (DCG) parser for CNF and FOL terms
│   ├── resolution_prop.pl        # Propositional resolution prover with optimizations (C5 p.6)
│   ├── resolution_fol.pl         # First-Order Logic resolution theorem prover
│   ├── davis_putnam.pl           # Davis-Putnam SAT solver (with • operation & 2 strategies)
│   └── main.pl                   # Automated test suite runner
├── gui/
│   └── app.py                    # Graphical User Interface (Python Tkinter)
├── tests/                        # Pre-configured test sets
│   ├── s1_prop_1.txt ... 5.txt   # Subject 1 propositional resolution mandatory tests (i - v)
│   ├── s1_fol_own.txt            # Subject 1 FOL: Own student graduation example
│   ├── s1_fol_c3_p30.txt         # Subject 1 FOL: Course example (C3 p.30 Socrates)
│   ├── s1_fol_c3_p33.txt         # Subject 1 FOL: Course example (C3 p.33 Animal lover)
│   ├── s1_fol_c4_p12.txt         # Subject 1 FOL: Course example (C4 p.12 Barber paradox)
│   └── s2_dp_1.txt ... 6.txt     # Subject 2 Davis-Putnam mandatory tests (i - vi)
├── doc/
│   ├── report_draft.md           # Markdown version of the academic report
│   ├── generate_pdf.py           # Automated PDF compiler using ReportLab
│   └── Coman_Ioan_Alexandru_project1.pdf   # Final submission PDF (2-8 pages report + code)
└── README.md
```

---

## 🚀 How to Run

### 1. Graphical User Interface (GUI)
Run the modern interactive GUI (Python Tkinter):
```powershell
python "C:\Users\legio\Projects\KRR\Project 1\gui\app.py"
```
Features:
* **Propositional Resolution tab:** Pick from preset examples (1–5) or load custom files, see step-by-step resolution derivations and total operation count.
* **FOL Resolution tab:** Run own student graduation example or course benchmarks, inspect variable bindings and refutation trees.
* **Davis-Putnam tab:** Test satisfiability on benchmark sets, pick between Strategy 1 (MOMS) and Strategy 2 (DLIS), compare results side-by-side, and inspect the satisfying truth assignments `{w/true; s/false; ...}`.

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

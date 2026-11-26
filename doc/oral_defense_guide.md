# Ghid Complet pentru Colocviu — Plan de Memorare & Explicații Linie cu Linie (KRR Project 1)

> **Notă:** Acest fișier este strict ghidul tău de studiu pentru proba orală (nu intră în PDF-ul de predare și nu încalcă regula „fără comentarii în `src/`”). Numerotarea liniilor corespunde exact codului final simplificat (`347` de linii în total).

---

## 0. Cum înveți totul în ~30 de minute (Plan în 3 treceri)

Nu încerca să tocești cele `347` de linii cuvânt cu cuvânt — **la colocviu ai codul deschis pe ecran**. Trebuie doar să știi să citești orice bloc de pe ecran și să explici *de ce* există.

### Trecerea 1 (5 min): Reține cele 7 „cărămizi” Prolog
Aproape toate liniile din proiect sunt combinații din exact aceste 7 piese:
1. **`member(X, Lista)`** — verifică dacă `X` e în listă (sau ia elementele pe rând).
2. **`findall(Ce, Conditii, Rezultat)`** — ca un `for + if`: adună într-o listă tot ce respectă condițiile.
3. **`forall(Conditie, Test)`** — verifică dacă *toate* elementele trec testul.
4. **`sort(Lista, Rezultat)`** / **`sort(0/1, @=< / @>=, ...)`** — sortează și scoate dublurile (sau sortează după lungime / scor).
5. **`copy_term` + `numbervars`** — face copie izolată fără să strice originalul / îngheață variabilele (`$VAR(0)`) pentru printare sau subsumpție.
6. **`unify_with_occurs_check` vs `==`** — `unify_with_occurs_check` **unifică sigur** (previne cicluri infinite gen `X = f(X)`), `==` verifică **identitatea strictă** fără a lega variabile.
7. **`\+ \+ (...)`** — probează dacă ceva merge fără să lase variabile legate în urmă.

### Trecerea 2 (10 min): Reține „povestea în 4 pași” a fiecărui fișier
* **`src/parser.pl` (55 linii):** Un singur standard curat (`and`, `or`, `not ` cu spațiu, `(...)` opțional): textul $\rightarrow$ clauze (`cnf_formula`) $\rightarrow$ literali (`disjunction`) $\rightarrow$ `pos`/`neg` (`literal`) $\rightarrow$ literă mare = `var(Name)`, literă mică = constantă/functor (`ident`).
* **`src/resolution_prop.pl` (70 linii):** Curăț dublurile, tautologiile și clauzele subsumate (`preprocess_clauses`) $\rightarrow$ iau mereu cea mai scurtă pereche neîncercată (`pick_shortest_pair`) $\rightarrow$ tai pivotul și sortez (`resolve_on_pivot`) $\rightarrow$ dacă iese `[]` e succes; dacă nu e tautologie/subsumată, arunc ce subsumează ea și continui (`Trace` iese direct în ordine `1..N`).
* **`src/resolution_fol.pl` (95 linii):** Convertesc `var('X')` în variabile Prolog izolate per clauză (`index_and_convert_clauses`) $\rightarrow$ aleg cea mai scurtă pereche unificabilă (`pick_shortest_unifiable_pair`) $\rightarrow$ fac `copy_term`, unific cu `unify_with_occurs_check`, șterg literalii după index (`remove_nth1`) și scot dublurile (`factor_duplicates`) $\rightarrow$ verific `[]` sau subsumpția (`numbervars` + `subset`).
* **`src/davis_putnam.pl` (127 linii):** Curăț clauzele (`simplify_clauses`) $\rightarrow$ testez pe rând: `[]` (`unsat`), listă goală (`sat`), **Unit** (forțez valoarea), **Pure** (apare doar cu un semn), **Glonț `•`** (elimin pivotul ales cu `moms`/`dlis` combinând `+` cu `-`, iar la întoarcere completez atomii rămași din `Cleaned \ [Pivot]` înainte de `infer_pivot_value`).

### Trecerea 3 (15 min): Parcurge liniile de mai jos + Auto-testul din Secțiunea 7

---

## 1. Script pentru Demo-ul Live (ce arăți în fața profesoarei)
1. **Deschizi proiectul în VS Code:** `C:\Users\legio\Projects\KRR\Project 1`.
2. **Rulezi toate cele 15 teste dintr-un click** (`Terminal -> Run Test Task` sau `swipl -s src/main.pl -g "run_all, halt."`).
3. **Deschizi GUI-ul** (`Ctrl+Shift+B` sau `python gui/app.py`) și arăți cele 3 tab-uri:
   * Tab 1 (*Prop*): încarci Exemplele `1–5` (arătând `5, 3, 2, 2, 0` operații, pașii în ordine `Pasul 1 ... Pasul N`, de ce la Ex. 4 sunt `2` operații cu `0` pași în trace și la Ex. 5 `0` operații).
   * Tab 2 (*FOL*): arăți exemplul propriu (*Alex absolvent*, `10` operații, `8` pași în trace) + cele 3 exemple din curs (`C3 p.30`, `C3 p.33`, `C4 p.12`).
   * Tab 3 (*Davis-Putnam*): arăți **Compare Both Strategies Side-by-Side** pe Exemplul 1 (`YES`) și Exemplul 2 (`NOT`).

---

## 2. Explicația rezultatelor celor 15 teste

### Subiectul 1 — Rezoluție Propozițională (`tests/s1_prop_1..5.txt`)
* **`s1_prop_1.txt`** $\rightarrow$ `refutation_success`, **5 ops**, **5 trace steps**: `(f or a or b or not f)` e tautologie și dispare la preprocesare; unitatea `not b` declanșează lanțul până la `[]`.
* **`s1_prop_2.txt`** $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**: contradicție derivată din `(a or not e)` cu `e` și `not a`.
* **`s1_prop_3.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **2 trace steps** (SAT): `(c or f)` + `not c` $\rightarrow$ `[f]`, `[f]` + `(not f or b)` $\rightarrow$ `[b]`, apoi `[b]` subsumează `(not c or b)`; nu mai există literali complementari.
* **`s1_prop_4.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **0 trace steps** (SAT): `(a or b)` cu `(not a or not b)` produce două tautologii (`[b, not b]` și `[a, not a]`). Cele 2 operații se contorizează (`Ops = 2`), dar tautologiile sunt aruncate și nu intră în `Trace`.
* **`s1_prop_5.txt`** $\rightarrow$ `refutation_failure`, **0 ops**, **0 trace steps** (SAT): `[not c]` subsumează `[b, not c]` din preprocesare; rămân `[a, not b]` și `[not c]`, fără perechi complementare.

### Subiectul 1 — Rezoluție FOL (`tests/s1_fol_*.txt`)
* **`s1_fol_own.txt`** (Alex absolvent) $\rightarrow$ `refutation_success`, **10 ops**, **8 trace steps**: 2 rezolvenți generați au fost deja subsumați de clauze existente (săriți din `Trace`).
* **`s1_fol_c3_p30.txt`** (Socrate) $\rightarrow$ `refutation_success`, **2 ops**, **2 trace steps**.
* **`s1_fol_c3_p33.txt`** (Animal lover & killer) $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**.
* **`s1_fol_c4_p12.txt`** (Paradoxul bărbierului) $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**: `person(barber)` se rezolvă direct cu ambele clauze ale paradoxului producând `shaves(barber, barber)` și `¬shaves(barber, barber)`, apoi `[]`.

### Subiectul 2 — Davis-Putnam (`tests/s2_dp_1..6.txt`, strategii MOMS & DLIS)
* **`s2_dp_1.txt`** $\rightarrow$ `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` (`toddler, female, girl` sunt forțate `true` ca unități $\rightarrow$ `child=true` $\rightarrow$ `male=false`; `boy` și `infant` rămân neconstrânși și primesc `true` din oficiu în `fill_missing_atoms`).
* **`s2_dp_2.txt`** $\rightarrow$ `NOT`: `{}` (`toddler` + `female` forțează `girl=true`, care contrazice `not girl`).
* **`s2_dp_3.txt`**, **`s2_dp_4.txt`** $\rightarrow$ `NOT`: `{}` (aceleași formule nesatisfiabile ca la `prop_1` / `prop_2`).
* **`s2_dp_5.txt`** $\rightarrow$ `YES`: `{a/false; b/false; d/true; e/true; f/true}`.
* **`s2_dp_6.txt`** $\rightarrow$ `NOT`: `{}` (`a` și `b` sunt forțate în toate cele 4 combinații posibile).

---

## 3. Explicație linie cu linie — `src/parser.pl` (Liniile 1–55)

* **1:** Declarăm modulul `parser` și exportăm doar `parse_kb_file/2`.
* **3–4:** `:- encoding(utf8).` și `:- set_prolog_flag(double_quotes, chars).` (ghilimelele duble din DCG sunt liste de caractere).
* **6–9:** `parse_kb_file` — Citește tot fișierul în `Text`, îl sparge în `Chars` și pornește gramatica DCG `cnf_formula`.
* **11–15:** `cnf_formula` — Citește o clauză urmată de `"and"` (cu `!`) și recursiv restul, sau ultima clauză `Last`.
* **17–18:** `clause_expr` — Clauză între `(...)` sau direct `disjunction`.
* **20–24:** `disjunction` — Literali separați prin `"or"`.
* **26–27:** `literal` — `"not"` urmat de minim un spațiu (`space1`) dă `neg(Atom)`; altfel `pos(Atom)`.
* **29–34:** `fol_term` — Dacă un nume cu literă mică e urmat de `(Args)`, îl construiește cu `=..`; altfel dacă `IsVar == true` devine `var(Name)`, altfel atomul/constanta `Name`.
* **36–40:** `args` — Argumente separate prin `,`.
* **42–50:** `ident` & `id_rest` — Literă mare $\rightarrow$ variabilă (`true`), literă mică $\rightarrow$ constantă/functor (`false`), urmate de caractere alfanumerice/`_`.
* **52–55:** `space1` (cel puțin un spațiu) & `spaces` (zero sau mai multe spații).

---

## 4. Explicație linie cu linie — `src/resolution_prop.pl` (Liniile 1–70)

* **1:** Exportăm `prove_propositional/4`.
* **3:** Importăm `parser`.
* **5–9:** `prove_propositional/4` — Citește clauzele (`parse_kb_file`), le preprocesează (`preprocess_clauses`), ia `MaxId = length(Clauses)` și rulează `prop_loop` direct (trace-ul e în ordine cronologică `1..N`).
* **11–14:** `preprocess_clauses` — Cu `findall` sortează fiecare clauză (scoate dublurile) și aruncă tautologiile; `drop_subsumed` elimină clauzele subsumate; `index_clauses` le numerotează `1..N`.
* **16–17:** `is_tautology` — Clauza are și `pos(Atom)` și `neg(Atom)`.
* **19–22:** `drop_subsumed` — Curăță restul (`KeptRest`); dacă în `KeptRest` există o clauză inclusă în `Clause` (`subset(Other, Clause)`), aruncă `Clause`.
* **24–27:** `index_clauses` — Atribuie ID-uri `1, 2, 3...`.
* **29–35:** `prop_loop` — Alege perechea cea mai scurtă neîncercată (`pick_shortest_pair`), rezolvă (`resolve_on_pivot`), incrementează `NextOps`, salvează ambele direcții în `NextHistory` și creează `Step`.
* **36–46:** Dacă `Resolvent == []` $\rightarrow$ `refutation_success`; dacă e tautologie sau subsumat (`subsumed_by_any`) îl aruncă; altfel elimină clauzele vechi subsumate de el, îl adaugă cu `NewId` și continuă recursiv.
* **47:** Dacă nu mai sunt perechi noi $\rightarrow$ `refutation_failure`.
* **49–58:** `pick_shortest_pair` — Adună toate perechile `(I1 < I2)` complementare neîncercate, sortează după `Len1 + Len2` și ia prima pereche.
* **60–64:** `resolve_on_pivot` — Șterge `Pivot` și `NegPivot`, lipește restul și sortează.
* **66–67:** `opposite_lit` — Întoarce semnul (`pos` $\leftrightarrow$ `neg`).
* **69–70:** `subsumed_by_any` — Verifică dacă o clauză existentă e inclusă în `Resolvent`.

---

## 5. Explicație linie cu linie — `src/resolution_fol.pl` (Liniile 1–95)

* **1:** Exportăm `prove_fol/4`.
* **3:** Importăm `parser`.
* **5–9:** `prove_fol/4` — Citește clauzele (`parse_kb_file`), convertește variabilele izolat per clauză (`index_and_convert_clauses`) și rulează `fol_loop` (trace în ordine cronologică `1..N`).
* **11–33:** `index_and_convert_clauses`, `convert_literals`, `convert_term`, `convert_terms` — Transformă fiecare `var(Name)` din aceeași clauză într-o variabilă Prolog comună (`MapIn -> MapOut`) și descompune termenii compuși cu `=..`.
* **35–51:** `fol_loop` — Alege cea mai scurtă pereche unificabilă (`pick_shortest_unifiable_pair`), face `copy_term` (*standardizing apart*), rezolvă cu `resolve_and_factor`, îngheață o copie cu `numbervars` pentru afișare (`Step`), verifică `[]` sau subsumpția (`subsumed_by_existing`) și adaugă `NewId`.
* **52:** Dacă nu mai sunt perechi unificabile $\rightarrow$ `refutation_failure`.
* **54–64:** `pick_shortest_unifiable_pair` — Găsește perechile `(I1 < I2)` ale căror literali opuși unifică sigur (`\+ \+ unify_with_occurs_check(Atom1, Atom2)`) și nu sunt în `History`, sortate după `Len1 + Len2`.
* **66–67:** `opposite_atoms` — Extrage atomii dintr-un literal `pos` și unul `neg`.
* **69–74:** `resolve_and_factor` — Unifică atomii cu `unify_with_occurs_check`, șterge exact pozițiile `Idx1`/`Idx2` (`remove_nth1`) și scoate dublurile identice (`factor_duplicates`).
* **76–78:** `remove_nth1` — Elimină al `N`-lea literal fără a compara după unificare.
* **80–85:** `factor_duplicates` — Păstrează o singură copie pentru literali sintactic identici (`==`).
* **87–95:** `subsumed_by_existing` — Copiază ambele clauze, îngheață variabilele din `FreshResolvent` cu `numbervars` și verifică `subset` fără a lega permanent variabile (`\+ \+`).

---

## 6. Explicație linie cu linie — `src/davis_putnam.pl` (Liniile 1–127)

* **1:** Exportăm `solve_dp/4`.
* **3:** Importăm `parser`.
* **5–14:** `solve_dp/4` — Citește clauzele (`parse_kb_file`), salvează toți atomii inițiali (`AllAtoms`), apelează `dp_solve`; dacă iese `sat`, completează atomii lipsă cu `true` și formatează `{...}` cu `'YES'`, altfel `'NOT'` și `'{}'`.
* **16–19:** `dp_solve` — La fiecare pas curăță clauzele (`simplify_clauses`), verifică `[]` (`unsat`) și listă vidă (`sat`).
* **20–24:** **Unit Clause:** Găsește `[UnitLit]`, propagă (`propagate_unit`), reține `(Atom, Value)` și continuă recursiv.
* **25–29:** **Pure Literal:** Găsește literal fără opus (`find_pure_literal`), păstrează clauzele fără el, reține `(Atom, Value)` și continuă recursiv.
* **30–40:** **Regula `•`:** Alege `Pivot` (`pick_pivot_atom`), îl elimină prin rezoluție (`bullet_eliminate`), rezolvă recursiv restul (`SubModel`), apoi completează atomii din `Cleaned \ [Pivot]` lipsă din `SubModel` și deduce valoarea lui `Pivot` din `NegClauses` (`infer_pivot_value`).
* **42–51:** `simplify_clauses`, `drop_subsumed`, `is_tautology` — Sortează/deduplică literalii, aruncă tautologiile și clauzele subsumate.
* **53–63:** `propagate_unit`, `opposite_lit`, `lit_assignment` — Elimină clauzele cu `UnitLit` și șterge `NegUnitLit`.
* **65–69:** `find_pure_literal` — Alege primul literal al cărui opus lipsește.
* **71–87:** `pick_pivot_atom` (`moms` / `dlis`) & `most_frequent_atom` — `moms` caută în clauzele cele mai scurte (`> 1`), `dlis` în toate clauzele active, sortând descrescător (`@>=`) după frecvență.
* **89–101:** `bullet_eliminate` — Separă în `PosClauses`, `NegClauses`, `NeutralClauses`, formează rezolvenții non-tautologici și simplifică.
* **103–111:** `infer_pivot_value` & `lit_true_in_model` — Testează cu `forall` dacă `Pivot = true` satisface toate `NegClauses` sub `ExtSubModel`; altfel `false`.
* **113–127:** `collect_all_atoms`, `fill_missing_atoms`, `format_solution` — Extrage atomii, completează valorile lipsă cu `true` și formatează `{atom/val; ...}`.

---

## 7. Auto-Test Rapid de Colocviu (10 întrebări & răspunsuri)

1. **De ce ai un singur standard în `parser.pl`?**
   > Toate formulele din proiect folosesc același format CNF (`and`, `or`, `not ` cu spațiu, paranteze `(...)`), deci gramatica rămâne curată și ușor de explicat în `55` de linii.
2. **De ce folosești `unify_with_occurs_check` în rezoluția FOL?**
   > Previne unificările ciclice infinite (ex. `X = f(X)`), păstrând corectitudinea algoritmului fără linii în plus.
3. **De ce faci `copy_term` înainte de rezoluția FOL?**
   > *Standardizing apart*: fără `copy_term`, unificarea ar lega variabilele direct în clauzele originale.
4. **Ce face `numbervars` și unde îl folosești?**
   > Îngheață variabilele ca `A, B` pentru afișare în trace (`fol_loop`) și blochează variabilele lui `FreshResolvent` la testul de subsumpție (`subsumed_by_existing`).
5. **Ce face `=..` (univ)?**
   > Desface un termen compus în `[Functor | Argumente]` și îl reasamblează după convertirea argumentelor.
6. **Ce optimizări are rezoluția propozițională (C5 p.6)?**
   > Eliminarea tautologiilor, eliminarea clauzelor subsumate (inițial și dinamic) și evitarea rezoluțiilor repetate prin `History` în ambele direcții.
7. **De ce `s1_prop_4` are `Ops = 2` și `Trace = 0`?**
   > Cele două rezoluții produc tautologii, deci se numără la `Ops` dar sunt eliminate și nu intră în `Trace`.
8. **De ce la `davis_putnam` completezi `OtherAtoms` înainte de `infer_pivot_value`?**
   > Dacă un rezolvent tautologic a făcut să dispară un atom din `Reduced`, `infer_pivot_value` trebuie să știe valoarea implicită `true` a acelui atom ca modelul reconstruit să satisfacă sigur și clauzele cu `+Pivot`.
9. **Diferența dintre MOMS și DLIS?**
   > MOMS numără aparițiile doar în clauzele minime (`> 1`); DLIS numără în toate clauzele active.
10. **Teorema lui Herbrand (pe scurt)?**
    > O mulțime de clauze FOL $S$ e nesatisfiabilă $\iff$ există o submulțime **finită** de instanțe ground din universul Herbrand $H_S$ care e propozițional nesatisfiabilă.

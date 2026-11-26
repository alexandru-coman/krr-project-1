# Ghid Complet pentru Colocviu — Plan de Memorare & Explicații Linie cu Linie (KRR Project 1)

> **Notă:** Acest fișier este strict ghidul tău de studiu pentru proba orală (nu intră în PDF-ul de predare și nu încalcă regula „fără comentarii în `src/`”). Numerotarea liniilor corespunde exact codului final minimal (`310` de linii în modulele de algoritmi).

---

## 0. Cum înveți totul în ~25 de minute (Plan în 3 treceri)

Nu încerca să tocești cele `310` de linii cuvânt cu cuvânt — **la colocviu ai codul deschis pe ecran**. Trebuie doar să știi să citești orice bloc de pe ecran și să explici *de ce* există.

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
* **`src/parser.pl` (52 linii):** Gramatică minimă pe input valid (`and`, `or`, `not ` cu `space1`, paranteze opționale `(...)`, `_` și whitespace standard) $\rightarrow$ scoate liste de `pos(Term)` / `neg(Term)` cu `var(Name)` pentru litere mari.
* **`src/resolution_prop.pl` (69 linii):** Curăț dublurile, tautologiile și clauzele subsumate (`preprocess_clauses`) $\rightarrow$ iau mereu cea mai scurtă pereche neîncercată (`pick_shortest_pair`) $\rightarrow$ tai pivotul și sortez (`resolve_on_pivot`) $\rightarrow$ `[]` e succes; altfel elimin ce subsumează rezolventul și continui (`Trace` în ordine `1..N`).
* **`src/resolution_fol.pl` (72 linii):** Convertesc `var('X')` în variabile Prolog izolate per clauză (`index_and_convert_clauses` + `convert_terms`) $\rightarrow$ aleg cea mai scurtă pereche unificabilă (`unify_with_occurs_check`) $\rightarrow$ extrag și șterg literalii dintr-o singură trecere cu `nth1/4`, deduplic literalii identici cu `sort/2` $\rightarrow$ verific `[]` sau subsumpția (`numbervars` + `subset`).
* **`src/davis_putnam.pl` (117 linii):** Curăț clauzele (`simplify_clauses`) $\rightarrow$ testez pe rând: `[]` (`unsat`), listă goală (`sat`), **Unit / Pure** (împart același `propagate_unit`, cu prioritate Unit $\rightarrow$ Pure), **Glonț `•`** (elimin pivotul ales cu `moms`/`dlis` combinând `+` cu `-`, iar la întoarcere completez atomii rămași din `Cleaned \ [Pivot]` înainte de `infer_pivot_value`).

### Trecerea 3 (10 min): Parcurge liniile de mai jos + Auto-testul din Secțiunea 7

---

## 1. Script pentru Demo-ul Live (ce arăți în fața profesoarei)
1. **Deschizi proiectul în VS Code:** `C:\Users\legio\Projects\KRR\Project 1`.
2. **Rulezi toate cele 15 teste dintr-un click** (`Terminal -> Run Test Task` sau `swipl -s src/main.pl -g "run_all, halt."`).
3. **Deschizi GUI-ul** (`Ctrl+Shift+B` sau `python gui/app.py`) și arăți cele 3 tab-uri:
   * Tab 1 (*Prop*): încarci Exemplele `1–5` (`5, 3, 2, 2, 0` operații, pașii în ordine `Pasul 1 ... Pasul N`).
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
* **`s1_fol_c4_p12.txt`** (Paradoxul bărbierului) $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**: `person(barber)` se rezolvă direct cu ambele clauze ale paradoxului producând `shaves(barber, barber)` și `not shaves(barber, barber)`, apoi `[]`.

### Subiectul 2 — Davis-Putnam (`tests/s2_dp_1..6.txt`, strategii MOMS & DLIS)
* **`s2_dp_1.txt`** $\rightarrow$ `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` (`toddler, female, girl` sunt forțate `true` ca unități $\rightarrow$ `child=true` $\rightarrow$ `male=false`; `boy` și `infant` rămân neconstrânși și primesc `true` din oficiu în `fill_missing_atoms`).
* **`s2_dp_2.txt`** $\rightarrow$ `NOT`: `{}` (`toddler` + `female` forțează `girl=true`, care contrazice `not girl`).
* **`s2_dp_3.txt`**, **`s2_dp_4.txt`** $\rightarrow$ `NOT`: `{}` (aceleași formule nesatisfiabile ca la `prop_1` / `prop_2`).
* **`s2_dp_5.txt`** $\rightarrow$ `YES`: `{a/false; b/false; d/true; e/true; f/true}`.
* **`s2_dp_6.txt`** $\rightarrow$ `NOT`: `{}` (`a` și `b` sunt forțate în toate cele 4 combinații posibile).

---

## 3. Explicație linie cu linie — `src/parser.pl` (Liniile 1–52)

* **1:** Declarăm modulul `parser` și exportăm doar `parse_kb_file/2`.
* **3–4:** `:- encoding(utf8).` și `:- set_prolog_flag(double_quotes, chars).` (ghilimelele duble din DCG sunt liste de caractere).
* **6–9:** `parse_kb_file` — Citește tot fișierul în `Text`, îl sparge în `Chars` și pornește gramatica DCG `cnf_formula`.
* **11–15:** `cnf_formula` — Citește una sau mai multe clauze legate prin `"and"` (cu `!`).
* **17–18:** `clause_expr` — Clauză între paranteze `( ... )` sau direct `disjunction`.
* **20–24:** `disjunction` — Unul sau mai mulți literali legați prin `"or"`.
* **26–27:** `literal` — `"not"` urmat de minim un spațiu (`space1`) dă `neg(Atom)`; altfel `pos(Atom)`.
* **29–34:** `fol_term` — Nume urmat de `(Args)` construit cu `=..`, altfel verifică prima literă: literă mare $\rightarrow$ `var(Name)`, literă mică $\rightarrow$ atom/constantă `Name`.
* **36–40:** `args` — Argumente separate prin `,`.
* **42–47:** `ident` & `id_rest` — Primul caracter `alpha`, restul `alnum` sau `'_'`, lipite cu `atom_chars`.
* **49:** `space1` — Obligatoriu cel puțin un caracter whitespace (` `, `\t`, `\n`, `\r`), urmat de `spaces`.
* **51–52:** `spaces` — 0 sau mai multe caractere whitespace.

---

## 4. Explicație linie cu linie — `src/resolution_prop.pl` (Liniile 1–69)

* **1:** Exportăm `prove_propositional/4`.
* **3:** Importăm `parser`.
* **5–9:** `prove_propositional/4` — Citește clauzele (`parse_kb_file`), le preprocesează (`preprocess_clauses`), ia `MaxId = length(Clauses)` și rulează `prop_loop` direct (`Trace` în ordine cronologică `1..N`).
* **11–14:** `preprocess_clauses` — Sortează fiecare clauză (scoate dublurile), aruncă tautologiile (`is_tautology`), elimină subsumatele (`drop_subsumed`) și numerotează `1..N` (`index_clauses`).
* **16–17:** `is_tautology` — Clauza are și `pos(Atom)` și `neg(Atom)`.
* **19–22:** `drop_subsumed` — Curăță restul (`KeptRest`); dacă în `KeptRest` există o clauză inclusă în `Clause` (`subset(Other, Clause)`), aruncă `Clause`.
* **24–27:** `index_clauses` — Atribuie ID-uri `1, 2, 3...`.
* **29–34:** `prop_loop` — Alege perechea cea mai scurtă neîncercată (`pick_shortest_pair`), rezolvă (`resolve_on_pivot`), incrementează `NextOps`, salvează `resolved(Id1, Id2, Pivot)` în `NextHistory` și creează `Step`.
* **35–45:** Dacă `Resolvent == []` $\rightarrow$ `refutation_success`; dacă e tautologie sau subsumat (`subsumed_by_any`) îl aruncă; altfel elimină clauzele vechi subsumate de el (`\+ subset(Resolvent, Existing)`), îl adaugă cu `NewId` și continuă recursiv.
* **46:** Dacă nu mai sunt perechi noi $\rightarrow$ `refutation_failure`.
* **48–57:** `pick_shortest_pair` — Adună perechile `(I1 < I2)` complementare neîncercate, sortează după `Len1 + Len2` și ia prima pereche.
* **59–63:** `resolve_on_pivot` — Șterge `Pivot` și `NegPivot`, lipește restul și sortează.
* **65–66:** `opposite_lit` — Întoarce semnul (`pos` $\leftrightarrow$ `neg`).
* **68–69:** `subsumed_by_any` — Verifică dacă o clauză existentă e inclusă în `Resolvent`.

---

## 5. Explicație linie cu linie — `src/resolution_fol.pl` (Liniile 1–72)

* **1:** Exportăm `prove_fol/4`.
* **3:** Importăm `parser`.
* **5–9:** `prove_fol/4` — Citește clauzele (`parse_kb_file`), convertește variabilele per clauză (`index_and_convert_clauses`) și rulează `fol_loop` (trace în ordine cronologică `1..N`).
* **11–15:** `index_and_convert_clauses` — Apelează direct `convert_terms` pe toată clauza cu variabile Prolog izolate și dă ID-uri `1..N`.
* **17–27:** `convert_term` & `convert_terms` — Transformă `var(Name)` într-o variabilă Prolog comună în clauză (`MapIn -> MapOut`), descompune termenii compuși (inclusiv `pos(...)`/`neg(...)` și predicatele) recursiv cu `=..`, iar constantele le lasă neschimbate.
* **29–46:** `fol_loop` — Alege perechea cea mai scurtă unificabilă (`pick_shortest_unifiable_pair`), face `copy_term` (*standardizing apart*), extrage și elimină literalii cu `nth1/4`, rezolvă (`resolve_and_factor`), îngheață o copie cu `numbervars` pentru afișare, verifică `[]` sau subsumpția (`subsumed_by_existing`).
* **48–59:** `pick_shortest_unifiable_pair` — Găsește perechile `(I1 < I2)` care unifică sigur (`\+ \+ unify_with_occurs_check(Atom1, Atom2)`) și nu sunt în `History`, sortate după `Len1 + Len2`.
* **61–62:** `opposite_atoms` — Extrage atomii dintr-un literal `pos` și unul `neg`.
* **64–68:** `resolve_and_factor` — Unifică atomii cu `unify_with_occurs_check`, lipește resturile `Rest1` și `Rest2` primite din `nth1/4` și deduplică literalii identici (`==`) cu `sort(Combined, Resolvent)` (fără a unifica variabile).
* **70–72:** `subsumed_by_existing` — Îngheață variabilele lui `Resolvent` (deja izolat în `fol_loop`) cu `numbervars` și verifică `subset(Existing, Resolvent)`; dubla negație `\+ \+` anulează automat toate legările și `numbervars` la ieșire.

---

## 6. Explicație linie cu linie — `src/davis_putnam.pl` (Liniile 1–117)

* **1:** Exportăm `solve_dp/4`.
* **3:** Importăm `parser`.
* **5–14:** `solve_dp/4` — Citește clauzele (`parse_kb_file`), salvează toți atomii inițiali (`AllAtoms`), apelează `dp_solve`; dacă iese `sat`, completează atomii lipsă cu `true` și formatează `{...}` cu `'YES'`, altfel `'NOT'` și `'{}'`.
* **16–19:** `dp_solve` — La fiecare pas curăță clauzele (`simplify_clauses`), verifică `[]` (`unsat`) și listă vidă (`sat`).
* **20–24:** **Unit Clause / Pure Literal:** Încearcă mai întâi `[Lit]` (unit), apoi `find_pure_literal` (pur); pentru un literal pur, opusul lipsește complet din `Cleaned`, deci `propagate_unit` scoate doar clauzele cu `Lit` și lasă restul intacte (`delete` nu modifică nimic), apoi notează `(Atom, Value)` și continuă recursiv.
* **25–35:** **Regula `•`:** Alege `Pivot` (`pick_pivot_atom`), îl elimină prin rezoluție (`bullet_eliminate`), rezolvă recursiv restul (`SubModel`), apoi completează atomii din `Cleaned \ [Pivot]` lipsă din `SubModel` și deduce valoarea lui `Pivot` din `NegClauses` (`infer_pivot_value`).
* **37–46:** `simplify_clauses`, `drop_subsumed`, `is_tautology` — Sortează/deduplică literalii, aruncă tautologiile și clauzele subsumate.
* **48–58:** `propagate_unit`, `opposite_lit`, `lit_assignment` — Elimină clauzele cu `UnitLit` și șterge `NegUnitLit`.
* **60–64:** `find_pure_literal` — Alege primul literal al cărui opus lipsește.
* **66–82:** `pick_pivot_atom` (`moms` / `dlis`) & `most_frequent_atom` — `moms` caută în clauzele cele mai scurte (cele de lungime $\le 1$ au fost deja eliminate), `dlis` în toate clauzele active, sortând descrescător (`@>=`) după frecvență.
* **84–94:** `bullet_eliminate` — Separă în `PosClauses`, `NegClauses`, `NeutralClauses`, formează rezolvenții și îi lipește la `NeutralClauses` în `Combined` (deduplicarea, tautologiile și subsumpția se rulează imediat la începutul următorului pas `dp_solve` prin `simplify_clauses`).
* **96–101:** `infer_pivot_value` — Testează cu `forall` și `lit_assignment/3` dacă `ExtSubModel` satisface toate `NegClauses` când `Pivot = true`; altfel `false`.
* **103–117:** `collect_all_atoms`, `fill_missing_atoms`, `format_solution` — Extrage atomii, completează valorile lipsă cu `true` și formatează `{atom/val; ...}`.

---

## 7. Auto-Test Rapid de Colocviu (10 întrebări & răspunsuri)

1. **De ce e gramatica din `parser.pl` atât de scurtă?**
   > Acceptă formatul standard al proiectului (`and`, `or`, `not `, `(...)`, `_` și whitespace standard) fără cod de validare/respingere inutil.
2. **De ce folosești `unify_with_occurs_check` în rezoluția FOL?**
   > Previne unificările ciclice infinite (ex. `X = f(X)`), păstrând corectitudinea algoritmului.
3. **De ce faci `copy_term` înainte de rezoluția FOL?**
   > *Standardizing apart*: fără `copy_term`, unificarea ar lega variabilele direct în clauzele originale.
4. **Ce face `=..` în `convert_term` și `fol_term`?**
   > Desface un termen compus (inclusiv `pos(Atom)`/`neg(Atom)`) în `[Functor | Argumente]` și îl reasamblează la loc.
5. **Ce face `numbervars` și unde îl folosești?**
   > Îngheață variabilele ca `A, B` pentru afișare în trace (`fol_loop`) și blochează variabilele lui `Resolvent` la testul de subsumpție (`subsumed_by_existing`, anulat apoi automat de `\+ \+`).
6. **Ce optimizări are rezoluția propozițională (C5 p.6)?**
   > Eliminarea tautologiilor, eliminarea clauzelor subsumate (inițial și dinamic) și evitarea rezoluțiilor repetate prin `History` (ordinea `I1 < I2` garantează perechea unică).
7. **De ce `s1_prop_4` are `Ops = 2` și `Trace = 0`?**
   > Cele două rezoluții produc tautologii, deci se numără la `Ops` dar sunt eliminate și nu intră în `Trace`.
8. **De ce la `davis_putnam` completezi `OtherAtoms` înainte de `infer_pivot_value`?**
   > Dacă un rezolvent tautologic a făcut să dispară un atom din `Reduced`, `infer_pivot_value` trebuie să știe valoarea implicită `true` a acelui atom ca modelul reconstruit să satisfacă sigur și clauzele cu `+Pivot`.
9. **Diferența dintre MOMS și DLIS?**
   > MOMS numără aparițiile doar în clauzele cele mai scurte (cele unitare au fost deja eliminate); DLIS numără în toate clauzele active.
10. **Teorema lui Herbrand (pe scurt)?**
    > O mulțime de clauze FOL $S$ e nesatisfiabilă $\iff$ există o submulțime **finită** de instanțe ground din universul Herbrand $H_S$ care e propozițional nesatisfiabilă.

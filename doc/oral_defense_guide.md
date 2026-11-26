# Ghid Complet pentru Colocviu — Plan de Memorare & Explicații Linie cu Linie (KRR Project 1)

> **Notă:** Acest fișier este strict ghidul tău de studiu pentru proba orală (nu intră în PDF-ul de predare și nu încalcă regula „fără comentarii în `src/`”). Numerotarea liniilor corespunde exact codului final (`423` de linii în total).

---

## 0. Cum înveți totul în ~35 de minute (Plan în 3 treceri)

Nu încerca să tocești cele `423` de linii cuvânt cu cuvânt — **la colocviu ai codul deschis pe ecran**. Trebuie doar să știi să citești orice bloc de pe ecran și să explici *de ce* există.

### Trecerea 1 (5 min): Reține cele 7 „cărămizi” Prolog
Aproape toate liniile din proiect sunt combinații din exact aceste 7 piese:
1. **`member(X, Lista)`** — verifică dacă `X` e în listă (sau ia elementele pe rând).
2. **`findall(Ce, Conditii, Rezultat)`** — ca un `for + if`: adună într-o listă tot ce respectă condițiile.
3. **`forall(Conditie, Test)`** — verifică dacă *toate* elementele trec testul.
4. **`sort(Lista, Rezultat)`** / **`sort(0/1, @=< / @>=, ...)`** — sortează și scoate dublurile (sau sortează după prioritate: lungime / scor).
5. **`copy_term` + `numbervars`** — face copie izolată fără să strice originalul / îngheață variabilele (`$VAR(0)`) pentru printare sau subsumpție.
6. **`unify_with_occurs_check` / `=` vs `==`** — `unify_with_occurs_check` **unifică sigur** (oprește cicluri infinite gen `X = f(X)`), `==` verifică **identitatea strictă** fără a lega variabile.
7. **`\+ \+ (...)`** — probează dacă ceva merge fără să lase variabile legate în urmă.

### Trecerea 2 (10 min): Reține „povestea în 4 pași” a fiecărui fișier
* **`src/parser.pl` (82 linii):** Textul din fișier $\rightarrow$ împărțit în clauze (`cnf_clauses`, `conjunction_op` cu operatori expliciți sau newline, granițe de cuvânt prin `keyword`) $\rightarrow$ în literali (`disjunction_op`) $\rightarrow$ în `pos`/`neg` (`literal_expr`, `"not"` doar cu spațiu după el ca să nu confunde `notes`) $\rightarrow$ literă mare/`_` = `var(Name)`, literă mică = constantă/functor (`identifier`).
* **`src/resolution_prop.pl` (73 linii):** Curăț dublurile, tautologiile și clauzele subsumate (`preprocess_clauses`) $\rightarrow$ iau mereu cea mai scurtă pereche neîncercată (`pick_shortest_pair`) $\rightarrow$ tai pivotul și sortez (`resolve_on_pivot`) $\rightarrow$ dacă iese `[]` e succes; dacă nu e tautologie/subsumată, arunc ce subsumează ea și continui; trace-ul iese direct în ordine cronologică (`1..N`).
* **`src/resolution_fol.pl` (139 linii):** Convertesc `var('X')` în variabile Prolog izolate per clauză (`index_and_convert_clauses`) $\rightarrow$ aleg cel mai prioritar pas (`pick_next_step`: rezoluție binară sau factorizare) $\rightarrow$ fac `copy_term`, unific cu `unify_with_occurs_check`, elimin literalii (`remove_nth1`) și dublurile (`factor_duplicates`) $\rightarrow$ verific `[]`, tautologie (`fol_is_tautology`) sau subsumpție exactă (`subsumed_by_existing` cu `LenE =< LenR` și backtracking).
* **`src/davis_putnam.pl` (129 linii):** Curăț clauzele (`simplify_clauses`) $\rightarrow$ testez pe rând: `[]` (`unsat`), listă goală (`sat`), **Unit** (forțez valoarea), **Pure** (apare doar cu un semn), **Glonț `•`** (elimin pivotul ales cu `moms`/`dlis` combinând `+` cu `-`, iar la întoarcere completez mai întâi eventualii atomi rămași neconstrânși din `Cleaned \ [Pivot]` cu `fill_missing_atoms` și abia apoi deduc valoarea lui `Pivot` din `NegClauses` în `infer_pivot_value`).

### Trecerea 3 (20 min): Parcurge liniile de mai jos + Auto-testul din Secțiunea 7

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

## 3. Explicație linie cu linie — `src/parser.pl` (Liniile 1–82)

* **1:** Declarăm modulul `parser` și exportăm doar `parse_kb_file/2`.
* **3:** `:- encoding(utf8).` — Permite citirea corectă a caracterului Unicode `¬`.
* **4:** `:- set_prolog_flag(double_quotes, chars).` — Face ca `"..."` în gramatică să fie liste de caractere pentru DCG.
* **6–9:** `parse_kb_file` — Citește tot fișierul în UTF-8 (`FormulaString`), îl sparge în listă de caractere (`string_chars`) și pornește gramatica DCG de la `cnf_formula` (`phrase`).
* **11–12:** `cnf_formula` — Dacă inputul e gol sau doar spații până la final (`eos_check`), întoarce `[]`; altfel consumă spațiile de la capete și parsează clauzele cu `cnf_clauses`.
* **14–17:** `cnf_clauses` — Citește una sau mai multe clauze legate prin `conjunction_op` (fără să permită operator rămas agățat la final).
* **19–25:** `conjunction_op` & `explicit_conj` — Scanează spațiile cu `scan_ws(HasNL)`; acceptă fie un operator explicit (`"and"`, `"^"`, `"&"`, `";"`), fie separare prin linie nouă (`HasNL == true` urmat de un caracter non-spațiu `peek_non_space`).
* **27–29:** `clause_expr` — O clauză poate fi închisă între `(...)`, între `[...]`, sau fără paranteze.
* **31–34:** `disjunction_expr` — Dacă după literal urmează `disjunction_op`, taie (`!`) și parsează restul literalilor; altfel un singur literal.
* **36:** `disjunction_op` — Operator de SAU între literali: cuvântul `"or"`, `"v"`, sau `"|"`, `","`, cu spații.
* **38–39:** `literal_expr` — Dacă începe cu `negation_prefix`, taie (`!`) ca să nu se reinterpreteze `"not"` drept atom și returnează `neg(Predicate)`; altfel `pos(Predicate)`.
* **41–42:** `negation_prefix` — Recunoaște `"not"` doar când e urmat de un spațiu (`char_type(Char, space)`, ca `"notes"` să rămână atom pozitiv) sau simbolurile `¬`, `~`, `-`.
* **44–49:** `fol_term` — Dacă un nume cu literă mică e urmat de `(Args)`, îl împachetează cu `=..`; altfel dacă `IsVar == true` devine `var(Name)`, altfel constanta/atomul `Name`.
* **51–54:** `arg_list` — Listă de termeni `fol_term` despărțiți prin `,` (suportă funcții imbricate gen `f(g(X), y)`).
* **56–64:** `identifier` & `id_rest` — Literă mare/`_` $\Rightarrow$ variabilă (`true`), literă mică $\Rightarrow$ constantă/functor (`false`), urmată de caractere `alnum` sau `_`.
* **66–82:** `keyword`, `peek_non_id`, `eos_check`, `peek_non_space`, `scan_ws`, `whitespaces` — Verifică granița cuvintelor cheie (`and`, `or`, `v` nu pot fi lipite de alte litere/cifre), detectează newline-urile dintre clauze fără să le piardă, și consumă spațiile albe.

---

## 4. Explicație linie cu linie — `src/resolution_prop.pl` (Liniile 1–73)

* **1:** Exportăm `prove_propositional/4`.
* **3:** Importăm `parser`.
* **5–12:** `prove_propositional/4` — Citește clauzele din fișier (`parse_kb_file`), le preprocesează (`preprocess_clauses`); dacă există deja `[]` $\rightarrow$ `refutation_success` din 0 operații, altfel ia `MaxId = length(Clauses)` și rulează `prop_loop` direct (trace-ul e construit deja în ordinea `1..N`).
* **14–17:** `preprocess_clauses` — Cu `findall` sortează fiecare clauză (scoate dublurile) și aruncă tautologiile; `drop_subsumed` elimină clauzele subsumate; `index_clauses` le numerotează `1..N`.
* **19–20:** `is_tautology` — Clauza are și `pos(Atom)` și `neg(Atom)`.
* **22–25:** `drop_subsumed` — Curăță mai întâi restul (`KeptRest`); dacă în `KeptRest` există o clauză mai mică inclusă în `Clause` (`subset(Other, Clause)`), aruncă `Clause`.
* **27–30:** `index_clauses` — Atribuie ID-uri `1, 2, 3...`.
* **32–33:** `prop_loop` — Alege perechea cea mai scurtă neîncercată (`pick_shortest_pair`) și pune `!`.
* **34:** `resolve_on_pivot` — Combină `Clause1` și `Clause2` eliminând `Pivot` și opusul lui.
* **35–38:** Incrementează `NextOps`, salvează ambele direcții în `NextHistory` (`Id1, Id2, Pivot` și `Id2, Id1, NegPivot`) împotriva repetării și construiește `Step = step(...)`.
* **39–40:** Dacă `Resolvent == []` $\rightarrow$ **succes** (`refutation_success`).
* **41–42:** Dacă rezolventul e tautologie sau subsumat de o clauză existentă (`subsumed_by_any`), îl aruncă și continuă bucla.
* **43–48:** Altfel elimină cu `findall` clauzele vechi subsumate strict de noul `Resolvent`, adaugă `clause(NewId, Resolvent)`, continuă recursiv și pune `Step` în capul lui `Trace` (`[Step | RestTrace]`).
* **50:** Dacă nu mai sunt perechi noi de combinat $\rightarrow$ `refutation_failure`.
* **52–61:** `pick_shortest_pair` — Cu `findall` adună toate perechile `(I1 < I2)` cu literali complementari care nu sunt în `History`, calculează `Size = Len1 + Len2`, verifică să nu fie gol și sortează crescător (`@=<`) după `Size` luând prima pereche.
* **63–67:** `resolve_on_pivot` — Șterge `Pivot` și `NegPivot`, lipește restul și sortează (eliminând dublurile).
* **69–70:** `opposite_lit` — Întoarce semnul literalului (`pos` $\leftrightarrow$ `neg`).
* **72–73:** `subsumed_by_any` — Există în `Clauses` o clauză `Existing` inclusă în `Resolvent` (`subset(Existing, Resolvent)`).

---

## 5. Explicație linie cu linie — `src/resolution_fol.pl` (Liniile 1–139)

* **1:** Exportăm `prove_fol/4`.
* **3:** Importăm `parser`.
* **5–12:** `prove_fol/4` — Citește clauzele (`parse_kb_file`), convertește variabilele izolat per clauză (`index_and_convert_clauses`), verifică `[]` inițial, altfel pornește `fol_loop` (construind `Trace` direct în ordine cronologică `1..N`).
* **14–36:** `index_and_convert_clauses`, `convert_literals`, `convert_term`, `convert_terms` — Transformă fiecare `var(Name)` din interiorul aceleiași clauze într-o variabilă logică Prolog comună (folosind dicționarul `MapIn -> MapOut`), păstrând clauzele independente între ele și descompunând funcțiile compuse cu `=..`.
* **38–54:** `fol_loop` — Alege cel mai prioritar pas (`pick_next_step`: rezoluție binară sau factorizare), îl aplică (`apply_step`), îngheață o copie cu `numbervars` pentru afișare (`Step`), verifică `[]` (`refutation_success`), aruncă tautologiile (`fol_is_tautology`) și clauzele subsumate (`subsumed_by_existing`), altfel adaugă noua clauză cu ID `NewId` și continuă recursiv. Dacă nu mai sunt pași noi, returnează `refutation_failure`.
* **56–75:** `pick_next_step` — Adună candidații de **rezoluție binară** (`cand(Len1+Len2, 1, resolve(...))`) folosind `can_unify_opposite` și candidații de **factorizare** (`cand(Len*2, 2, factor(...))`) între doi literali de același semn din aceeași clauză (`can_unify_same`), apoi sortează cu `sort(0, @=<, ...)` (preferând rezoluțiile cele mai scurte, iar pe cazurile necesare aplicând factorizarea).
* **77–91:** `apply_step` — Face *standardizing apart* cu `copy_term`, extrage literalii cu `nth1`, îi unifică sigur cu **`unify_with_occurs_check/2`** (previne bucle infinite `X = f(X)`), șterge literalii consumați prin index exact (`remove_nth1`) și elimină dublurile identice (`factor_duplicates`).
* **93–108:** `step_history_entry`, `can_unify_opposite`, `can_unify_same`, `opposite_atoms`, `same_atoms` — Utilitare pentru istoric și verificarea non-distructivă a unificabilității (`\+ \+ (copy_term(...), unify_with_occurs_check(...))`).
* **110–119:** `remove_nth1` și `factor_duplicates` — Elimină exact al `N`-lea literal și păstrează o singură copie pentru literali sintactic identici (`==`).
* **121–122:** `fol_is_tautology` — Elimină o clauză doar dacă are același atom sintactic (`A == B`) cu ambele semne (`pos(A)` și `neg(B)`).
* **124–139:** `subsumed_by_existing` & `subsumes_lits` — Verifică $\theta$-subsumpția exactă cu `LenE =< LenR` (astfel încât o clauză lungă să nu-și înghită factorul mai scurt), `numbervars` pe copia rezolventului și backtracking complet prin `member` + `unify_with_occurs_check`.

---

## 6. Explicație linie cu linie — `src/davis_putnam.pl` (Liniile 1–129)

* **1:** Exportăm `solve_dp/4`.
* **3:** Importăm `parser`.
* **5–14:** `solve_dp/4` — Citește clauzele (`parse_kb_file`), salvează toți atomii inițiali (`AllAtoms`), apelează `dp_solve`; dacă iese `sat`, completează atomii lipsă cu `true` și formatează `{...}` cu `'YES'`, altfel `'NOT'` și `'{}'`.
* **16–17:** `dp_solve` — La fiecare pas curăță clauzele (`simplify_clauses`).
* **18:** Dacă există `[]` $\rightarrow$ `unsat` (`NOT`).
* **19:** Dacă nu mai sunt clauze (`[]`) $\rightarrow$ `sat` (`YES`).
* **20–24:** **Unit Clause:** Găsește `[UnitLit]`, propagă valoarea (`propagate_unit`), reține `(Atom, Value)` și apelează recursiv; dacă iese `sat`, o pune în `Model`.
* **25–29:** **Pure Literal:** Găsește literal fără opus (`find_pure_literal`), păstrează cu `findall` doar clauzele fără el, reține `(Atom, Value)` și apelează recursiv.
* **30–40:** **Regula `•`:** Alege `Pivot` (`pick_pivot_atom`), îl elimină prin rezoluție (`bullet_eliminate`), rezolvă recursiv restul (`SubModel`). Dacă e `sat`, mai întâi fixează la `true` atomii din `Cleaned \ [Pivot]` absenți din `SubModel` (`subtract` + `fill_missing_atoms` $\rightarrow$ `ExtSubModel`), apoi deduce valoarea lui `Pivot` din `NegClauses` (`infer_pivot_value`) astfel încât modelul reconstruit să nu contrazică tautologiile eliminate.
* **42–51:** `simplify_clauses`, `drop_subsumed`, `is_tautology` — Sortează/deduplică literalii, aruncă tautologiile și clauzele subsumate.
* **53–63:** `propagate_unit`, `opposite_lit`, `lit_assignment` — Elimină clauzele satisfăcute de `UnitLit` și șterge opusul `NegUnitLit`.
* **65–69:** `find_pure_literal` — Alege primul literal al cărui opus nu apare în `Cleaned`.
* **71–89:** `pick_pivot_atom` & `most_frequent_atom` — `moms` caută clauzele de lungime minimă (`> 1`); `dlis` caută în toate clauzele; alege atomul cu frecvența maximă (`sort(1, @>=, ...)`).
* **91–103:** `bullet_eliminate` — Separă în `PosClauses`, `NegClauses`, `NeutralClauses`, formează toți rezolvenții non-tautologici și simplifică cu `NeutralClauses`.
* **105–113:** `infer_pivot_value` & `lit_true_in_model` — Testează cu `forall` dacă `Pivot = true` împreună cu `ExtSubModel` satisface toate `NegClauses`; altfel alege `Pivot = false`.
* **115–129:** `collect_all_atoms`, `fill_missing_atoms`, `format_solution` — Extrage atomii unici, completează valorile implicite `true` și formatează `{atom/val; ...}`.

---

## 7. Auto-Test Rapid de Colocviu (12 întrebări & răspunsuri)

1. **De ce faci `copy_term` înainte de rezoluția FOL?**
   > *Standardizing apart*: fără `copy_term`, unificarea ar lega variabilele direct în clauzele originale și n-am mai putea refolosi clauza în alți pași.
2. **De ce folosești `unify_with_occurs_check` în locul lui `=`?**
   > În Prolog standard `=` permite unificări ciclice (ex. `p(X, f(X))` cu `¬p(Y, Y)` ar produce `X = f(X)` și ar da fals `refutation_success`). `unify_with_occurs_check` previne aceste bucle infinite și păstrează corectitudinea (soundness).
3. **De ce ai nevoie de factorizare în FOL (`factor/4`) și de `LenE =< LenR` la subsumpție?**
   > De exemplu formula `(p(X) or p(Y)) and (¬p(U) or ¬p(V))` e nesatisfiabilă, dar rezoluția binară simplă păstrează mereu câte 2 literali; factorizarea reduce `[p(X), p(Y)]` la `[p(X)]`, iar condiția `LenE =< LenR` împiedică clauza inițială să își subsumeze propriul factor mai scurt.
4. **Ce face `numbervars` și de ce îl folosești în două locuri?**
   > În `fol_loop` (pe copie) îngheață variabilele ca `A, B` pentru afișare în trace; în `subsumed_by_existing` îngheață clauza specifică (`FreshResolvent`) ca `subsumes_lits` să nu-i lege variabilele în direcția greșită.
5. **Ce face `=..` (univ)?**
   > Desface un termen compus în `[Functor | ListaArgumente]` și îl reasamblează la loc după convertirea argumentelor.
6. **Ce optimizări are rezoluția propozițională (C5 p.6)?**
   > Eliminarea tautologiilor, eliminarea clauzelor subsumate (inițial și dinamic), și evitarea rezoluțiilor repetate prin `History` cu ambele direcții.
7. **De ce `s1_prop_4` are `Ops = 2` și `Trace = 0`?**
   > Cele două rezoluții produc tautologii (`[b, neg(b)]`, `[a, neg(a)]`), deci s-au executat dar nu au intrat în trace-ul util.
8. **De ce `s1_prop_5` are `0` operații?**
   > `[neg(c)]` subsumează `[b, neg(c)]` încă din preprocesare; clauzele rămase n-au literali opuși.
9. **De ce la `davis_putnam` completezi `OtherAtoms` înainte de `infer_pivot_value`?**
   > Dacă un rezolvent tautologic a făcut ca un atom `q` să dispară din `Reduced` (de ex. `(p ∨ ¬q) ∧ (¬p ∨ q)`), `SubModel` e gol; dacă `infer_pivot_value` ar alege `p = false` înainte să știe că `fill_missing_atoms` va pune `q = true`, modelul `{p/false, q/true}` ar încălca clauza `p ∨ ¬q`. Completând `OtherAtoms` cu `true` înainte, `infer_pivot_value` alege corect `p = true`.
10. **Diferența dintre Davis-Putnam (1960) și DPLL?**
    > DP elimină variabile prin rezoluție (`•`); DPLL ramifică cu backtracking (`p = true` / `p = false`).
11. **Diferența dintre MOMS și DLIS?**
    > MOMS numără aparițiile doar în clauzele cele mai scurte (`> 1`); DLIS numără în toate clauzele active.
12. **Teorema lui Herbrand (pe scurt)?**
    > O mulțime de clauze FOL $S$ e nesatisfiabilă $\iff$ există o submulțime **finită** de instanțe ground din universul Herbrand $H_S$ care e propozițional nesatisfiabilă.

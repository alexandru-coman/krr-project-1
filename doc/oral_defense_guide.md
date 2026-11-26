# Ghid Complet pentru Colocviu — Plan de Memorare & Explicații Linie cu Linie (KRR Project 1)

> **Notă:** Acest fișier este strict ghidul tău de studiu pentru proba orală (nu intră în PDF-ul de predare și nu încalcă regula „fără comentarii în `src/`”). Numerotarea liniilor corespunde exact codului final, curățat de cod mort (`360` de linii în total).

---

## 0. Cum înveți totul în ~35 de minute (Plan în 3 treceri)

Nu încerca să tocești cele `360` de linii cuvânt cu cuvânt — **la colocviu ai codul deschis pe ecran**. Trebuie doar să știi să citești orice bloc de pe ecran și să explici *de ce* există.

### Trecerea 1 (5 min): Reține cele 7 „cărămizi” Prolog
Aproape toate liniile din proiect sunt combinații din exact aceste 7 piese:
1. **`member(X, Lista)`** — verifică dacă `X` e în listă (sau ia elementele pe rând).
2. **`findall(Ce, Conditii, Rezultat)`** — ca un `for + if`: adună într-o listă tot ce respectă condițiile.
3. **`forall(Conditie, Test)`** — verifică dacă *toate* elementele trec testul.
4. **`sort(Lista, Rezultat)`** / **`sort(1, @=< / @>=, ...)`** — sortează și scoate dublurile (sau sortează după câmpul 1: lungime / scor).
5. **`copy_term` + `numbervars`** — face copie izolată fără să strice originalul / îngheață variabilele (`$VAR(0)`) pentru printare sau subsumpție.
6. **`=` vs `==`** — `=` **unifică** (leagă variabile), `==` verifică **identitatea strictă** (nu leagă nimic).
7. **`\+ \+ (...)`** — probează dacă ceva merge fără să lase variabile legate în urmă.

### Trecerea 2 (10 min): Reține „povestea în 4 pași” a fiecărui fișier
* **`src/parser.pl` (60 linii):** Textul din fișier $\rightarrow$ împărțit în clauze (`conjunction_op`) $\rightarrow$ în literali (`disjunction_op`) $\rightarrow$ în `pos`/`neg` (`literal_expr`) $\rightarrow$ literă mare/`_` = `var(Name)`, literă mică = constantă/functor (`identifier`).
* **`src/resolution_prop.pl` (74 linii):** Curăț dublurile, tautologiile și clauzele subsumate (`preprocess_clauses`) $\rightarrow$ iau mereu cea mai scurtă pereche neîncercată (`pick_shortest_pair`) $\rightarrow$ tai pivotul și sortez (`resolve_on_pivot`) $\rightarrow$ dacă iese `[]` e succes; dacă nu e tautologie/subsumată, arunc ce subsumează ea și continui.
* **`src/resolution_fol.pl` (100 linii):** Convertesc `var('X')` în variabile Prolog izolate per clauză (`index_and_convert_clauses`) $\rightarrow$ iau cea mai scurtă pereche unificabilă (`pick_shortest_unifiable_pair`) $\rightarrow$ fac `copy_term` pe ambele $\rightarrow$ unific atomii (`=`), șterg literalii (`==`), fac factorizarea (scot dublurile cu `==`) $\rightarrow$ verific `[]` sau subsumpția (`numbervars` + `subset`).
* **`src/davis_putnam.pl` (126 linii):** Curăț clauzele (`simplify_clauses`) $\rightarrow$ testez pe rând: `[]` (`unsat`), listă goală (`sat`), **Unit** (forțez valoarea), **Pure** (apare doar cu un semn), **Glonț `•`** (elimin pivotul ales cu `moms`/`dlis` combinând `+` cu `-` și la întoarcere deduc valoarea pivotului din `NegClauses`).

### Trecerea 3 (20 min): Parcurge liniile de mai jos + Auto-testul din Secțiunea 7

---

## 1. Script pentru Demo-ul Live (ce arăți în fața profesoarei)
1. **Deschizi proiectul în VS Code:** `C:\Users\legio\Projects\KRR\Project 1`.
2. **Rulezi toate cele 15 teste dintr-un click** (`Terminal -> Run Test Task` sau `swipl -s src/main.pl -g "run_all, halt."`).
3. **Deschizi GUI-ul** (`Ctrl+Shift+B` sau `python gui/app.py`) și arăți cele 3 tab-uri:
   * Tab 1 (*Prop*): încarci Exemplele `1–5` (arătând `5, 3, 2, 2, 0` operații și de ce la Ex. 4 sunt `2` operații cu `0` pași în trace, iar la Ex. 5 `0` operații).
   * Tab 2 (*FOL*): arăți exemplul propriu (*Alex absolvent*, `10` operații, `8` pași în trace) + cele 3 exemple din curs (`C3 p.30`, `C3 p.33`, `C4 p.12`).
   * Tab 3 (*Davis-Putnam*): arăți **Compare Both Strategies Side-by-Side** pe Exemplul 1 (`YES`) și Exemplul 2 (`NOT`).

---

## 2. Explicația rezultatelor celor 15 teste

### Subiectul 1 — Rezoluție Propozițională (`tests/s1_prop_1..5.txt`)
* **`s1_prop_1.txt`** $\rightarrow$ `refutation_success`, **5 ops**, **5 trace steps**: `(f or a or b or not f)` e tautologie și dispare la preprocesare; unitatea `not b` declanșează lanțul până la `[]`.
* **`s1_prop_2.txt`** $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**: contradicție derivată din `(a or not e)` cu `e` și `not a`.
* **`s1_prop_3.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **2 trace steps** (SAT): `not c` subsumează `(not c or b)` la preprocesare; `(c or f)` + `not c` $\rightarrow$ `[f]`, `[f]` + `(not f or b)` $\rightarrow$ `[b]`; nu mai există literali complementari.
* **`s1_prop_4.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **0 trace steps** (SAT): `(a or b)` cu `(not a or not b)` produce două tautologii (`[b, not b]` și `[a, not a]`). Cele 2 operații se contorizează (`Ops = 2`), dar tautologiile sunt aruncate și nu intră în `Trace`.
* **`s1_prop_5.txt`** $\rightarrow$ `refutation_failure`, **0 ops**, **0 trace steps** (SAT): `[not c]` subsumează `[b, not c]` din preprocesare; rămân `[a, not b]` și `[not c]`, fără perechi complementare.

### Subiectul 1 — Rezoluție FOL (`tests/s1_fol_*.txt`)
* **`s1_fol_own.txt`** (Alex absolvent) $\rightarrow$ `refutation_success`, **10 ops**, **8 trace steps**: 2 rezolvenți generați au fost deja subsumați de clauze existente (săriți din `Trace`).
* **`s1_fol_c3_p30.txt`** (Socrate) $\rightarrow$ `refutation_success`, **2 ops**, **2 trace steps**.
* **`s1_fol_c3_p33.txt`** (Animal lover & killer) $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**.
* **`s1_fol_c4_p12.txt`** (Paradoxul bărbierului) $\rightarrow$ `refutation_success`, **5 ops**, **3 trace steps**.

### Subiectul 2 — Davis-Putnam (`tests/s2_dp_1..6.txt`, strategii MOMS & DLIS)
* **`s2_dp_1.txt`** $\rightarrow$ `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` (`toddler, female, girl` sunt forțate `true` ca unități $\rightarrow$ `child=true` $\rightarrow$ `male=false`; `boy` și `infant` rămân neconstrânși și primesc `true` din oficiu în `fill_missing_atoms`).
* **`s2_dp_2.txt`** $\rightarrow$ `NOT`: `{}` (`toddler` + `female` forțează `girl=true`, care contrazice `not girl`).
* **`s2_dp_3.txt`**, **`s2_dp_4.txt`** $\rightarrow$ `NOT`: `{}` (aceleași formule nesatisfiabile ca la `prop_1` / `prop_2`).
* **`s2_dp_5.txt`** $\rightarrow$ `YES`: `{a/false; b/false; d/true; e/true; f/true}`.
* **`s2_dp_6.txt`** $\rightarrow$ `NOT`: `{}` (`a` și `b` sunt forțate în toate cele 4 combinații posibile).

---

## 3. Explicație linie cu linie — `src/parser.pl` (Liniile 1–60)

* **1:** Declarăm modulul `parser` și exportăm doar `parse_kb_file/2`.
* **3:** `:- encoding(utf8).` — Permite citirea corectă a caracterului Unicode `¬`.
* **4:** `:- set_prolog_flag(double_quotes, chars).` — Face ca `"..."` în gramatică să fie liste de caractere pentru DCG.
* **6–9:** `parse_kb_file` — Citește tot fișierul în UTF-8 (`FormulaString`), îl sparge în listă de caractere (`string_chars`) și pornește gramatica DCG de la `cnf_formula` (`phrase`).
* **11–13:** `cnf_formula([FirstClause | RestClauses])` — Dacă vede o clauză urmată de `conjunction_op`, taie (`!`) și parsează recursiv restul clauzelor.
* **14:** `cnf_formula([SingleClause])` — Ultima (sau singura) clauză din formulă.
* **15:** `cnf_formula([])` — Fișier gol sau doar spații $\rightarrow$ listă goală.
* **17–18:** `conjunction_op` — Operator de ȘI între clauze: `"and"`, `"^"`, `"&"`, `";"`, sau `newline`, înconjurat de spații.
* **20–22:** `clause_expr` — O clauză poate fi închisă între `(...)`, între `[...]`, sau fără paranteze.
* **24–26:** `disjunction_expr([FirstLit | RestLits])` — Dacă după literal urmează `disjunction_op`, taie (`!`) și parsează restul literalilor.
* **27:** `disjunction_expr([SingleLit])` — Ultimul (sau singurul) literal din clauză.
* **29:** `disjunction_op` — Operator de SAU între literali: `"or"`, `"v"`, `"|"`, `","`, cu spații.
* **31–32:** `literal_expr` — Dacă are prefix de negație (`negation_prefix`), devine `neg(Predicate)`; altfel `pos(Predicate)`.
* **34–35:** `negation_prefix` — Recunoaște `"not"` urmat de spațiu (ca să nu confunde `not_p`), sau simbolurile `¬`, `~`, `-`.
* **37–39:** `fol_term(Compound)` — Dacă un nume cu literă mică (`false`) e urmat de `(Args)`, taie (`!`) și îl împachetează cu `=..` în termen compus (ex: `man(var('X'))`).
* **40–42:** `fol_term(Term)` — Fără paranteze: dacă `IsVar == true` devine `var(Name)`, altfel constanta simplă `Name`.
* **44–47:** `arg_list` — Listă de termeni `fol_term` despărțiți prin `,` (suportă și funcții imbricate gen `f(g(X), y)`).
* **49–51:** `identifier(Name, true)` — Începe cu literă MARE (`upper`) sau `_` $\Rightarrow$ **variabilă** (`true`).
* **52–54:** `identifier(Name, false)` — Începe cu literă MICĂ (`lower`) $\Rightarrow$ **constantă sau nume de predicat/funcție** (`false`).
* **56–57:** `id_rest` — Restul caracterelor din nume: alfanumerice (`alnum`) sau `_`.
* **59–60:** `whitespaces` — Consumă zero sau mai multe spații/tab-uri/newline-uri.

---

## 4. Explicație linie cu linie — `src/resolution_prop.pl` (Liniile 1–74)

* **1:** Exportăm `prove_propositional/4`.
* **3:** Importăm `parser`.
* **5–13:** `prove_propositional/4` — Citește clauzele din fișier (`parse_kb_file`), le preprocesează (`preprocess_clauses`); dacă există deja `[]` $\rightarrow$ `refutation_success` din 0 operații, altfel ia `MaxId = length(Clauses)`, rulează `prop_loop` și inversează trace-ul (`reverse`).
* **15–18:** `preprocess_clauses` — Cu `findall` sortează fiecare clauză (scoate dublurile) și aruncă tautologiile; `drop_subsumed` elimină clauzele subsumate; `index_clauses` le numerotează `1..N`.
* **20–21:** `is_tautology` — Clauza are și `pos(Atom)` și `neg(Atom)`.
* **23–26:** `drop_subsumed` — Curăță mai întâi restul (`KeptRest`); dacă în `KeptRest` există o clauză mai mică inclusă în `Clause` (`subset(Other, Clause)`), aruncă `Clause`.
* **28–31:** `index_clauses` — Atribuie ID-uri `1, 2, 3...`.
* **33–34:** `prop_loop` — Alege perechea cea mai scurtă neîncercată (`pick_shortest_pair`) și pune `!`.
* **35:** `resolve_on_pivot` — Combină `Clause1` și `Clause2` eliminând `Pivot` și opusul lui.
* **36:** Incrementează contorul de operații (`NextOps`).
* **37–38:** Salvează în `NextHistory` ambele direcții (`Id1, Id2, Pivot` și `Id2, Id1, NegPivot`) împotriva repetării.
* **39:** Construiește `Step = step(...)`.
* **40–41:** Dacă `Resolvent == []` $\rightarrow$ **succes** (`refutation_success`).
* **42–43:** Dacă rezolventul e tautologie sau subsumat de o clauză existentă (`subsumed_by_any`), îl aruncă și continuă bucla.
* **44–49:** Altfel elimină cu `findall` clauzele vechi subsumate strict de noul `Resolvent`, adaugă `clause(NewId, Resolvent)`, continuă recursiv și păstrează `Step` în `Trace`.
* **51:** Dacă nu mai sunt perechi noi de combinat $\rightarrow$ `refutation_failure`.
* **53–62:** `pick_shortest_pair` — Cu `findall` adună toate perechile `(I1 < I2)` cu literali complementari care nu sunt în `History`, calculează `Size = Len1 + Len2`, verifică să nu fie gol și sortează crescător (`@=<`) după `Size` luând prima pereche.
* **64–68:** `resolve_on_pivot` — Șterge `Pivot` și `NegPivot`, lipește restul și sortează (eliminând dublurile).
* **70–71:** `opposite_lit` — Întoarce semnul literalului (`pos` $\leftrightarrow$ `neg`).
* **73–74:** `subsumed_by_any` — Există în `Clauses` o clauză `Existing` inclusă în `Resolvent` (`subset(Existing, Resolvent)`).

---

## 5. Explicație linie cu linie — `src/resolution_fol.pl` (Liniile 1–100)

* **1:** Exportăm `prove_fol/4`.
* **3:** Importăm `parser`.
* **5–13:** `prove_fol/4` — Citește clauzele din fișier (`parse_kb_file`), le convertește variabilele per clauză (`index_and_convert_clauses`), verifică `[]` inițial, altfel pornește `fol_loop` și inversează trace-ul.
* **15–19:** `index_and_convert_clauses` — Dă ID-uri `1..N` și convertește fiecare clauză pornind cu un dicționar gol `[]` (variabilele din clauze diferite sunt independente).
* **21–25:** `convert_literals` — Parcurge literalii `pos(Formula)` / `neg(Formula)` păstrând dicționarul `MapIn -> MapMid -> MapOut` în interiorul clauzei.
* **27–28:** `convert_term(var(Name), ...)` — Dacă `Name` există în `MapIn`, refolosește variabila logică `PrologVar`; altfel o creează și o adaugă în dicționar.
* **29–32:** `convert_term(Compound, ...)` — Desface termenul compus cu `=..` în `[Functor | RawArgs]`, convertește recursiv argumentele și reasamblează cu `=..`.
* **33:** `convert_term(Constant, ...)` — Constantele (literă mică) rămân neschimbate.
* **35–37:** `convert_terms` — Convertește recursiv lista de argumente.
* **39–40:** `fol_loop` — Alege perechea cea mai scurtă unificabilă (`pick_shortest_unifiable_pair`) și taie (`!`).
* **41:** `copy_term` pe ambele clauze — *Standardizing apart* (copii proaspete ca unificarea să nu strice originalele).
* **42:** `nth1` — Ia literalii de la pozițiile `Idx1`, `Idx2` din copiile proaspete.
* **43:** `resolve_and_factor` — Unifică, șterge literalii și elimină dublurile.
* **44–45:** Incrementează `Ops` și adaugă `(Id1, Id2, Idx1, Idx2)` în `History`.
* **46–47:** Copiază `Resolvent` în `PrintableResolvent` și aplică `numbervars` ca variabilele să se afișeze curat (`A, B`) fără să înghețe variabilele reale.
* **48–49:** Dacă `Resolvent == []` $\rightarrow$ `refutation_success`.
* **50–51:** Dacă e subsumat (`subsumed_by_existing`) $\rightarrow$ îl ignoră și continuă bucla.
* **52–54:** Altfel adaugă `clause(NewId, Resolvent)` și continuă recursiv.
* **56:** Dacă nu mai sunt perechi de rezolvat $\rightarrow$ `refutation_failure`.
* **58–68:** `pick_shortest_unifiable_pair` — Cu `findall` adună perechile `(I1 < I2)` ale căror literali la pozițiile `Pos1`, `Pos2` pot unifica (`can_unify_opposite`) și nu sunt în `History`; sortează crescător după `Size` și o ia pe prima.
* **70–72:** `can_unify_opposite` — Extrage atomii cu semn opus (`opposite_atoms`) și testează unificabilitatea cu `\+ \+ (copy_term(...), Fresh1 = Fresh2)` fără a lega variabile.
* **74–75:** `opposite_atoms` — Extrage atomii dintr-un literal `pos` și unul `neg`.
* **77–81:** `resolve_and_factor` — Extrage atomii și îi unifică (`Atom1 = Atom2` = MGU), șterge literalii exacți (`remove_exact`), lipește resturile și face factorizarea (`factor_duplicates`).
* **83–84:** `remove_exact` — Șterge prima apariție identică (`==`) fără a unifica alți literali.
* **86–91:** `factor_duplicates` — Păstrează o singură copie dacă doi literali sunt identici (`==`).
* **93–100:** `subsumed_by_existing` — Testează dacă o clauză existentă subsumează `Resolvent`: copiază ambele clauze, îngheață variabilele din `FreshResolvent` cu `numbervars` și verifică `subset`, totul în `\+ \+` ca să nu lege nimic permanent.

---

## 6. Explicație linie cu linie — `src/davis_putnam.pl` (Liniile 1–126)

* **1:** Exportăm `solve_dp/4`.
* **3:** Importăm `parser`.
* **5–14:** `solve_dp/4` — Citește clauzele din fișier (`parse_kb_file`), salvează toți atomii inițiali (`AllAtoms`), apelează `dp_solve`; dacă iese `sat`, completează atomii lipsă cu `true` și formatează `{...}` cu `'YES'`, altfel `'NOT'` și `'{}'`.
* **16–17:** `dp_solve` — La fiecare pas curăță clauzele (`simplify_clauses`).
* **18:** Dacă există `[]` $\rightarrow$ `unsat` (`NOT`).
* **19:** Dacă nu mai sunt clauze (`[]`) $\rightarrow$ `sat` (`YES`).
* **20–24:** **Unit Clause:** Găsește `[UnitLit]`, propagă valoarea (`propagate_unit`), reține `(Atom, Value)` și apelează recursiv; dacă iese `sat`, o pune în `Model`.
* **25–29:** **Pure Literal:** Găsește literal fără opus (`find_pure_literal`), păstrează cu `findall` doar clauzele fără el, reține `(Atom, Value)` și apelează recursiv.
* **30–37:** **Regula `•`:** Alege `Pivot` (`pick_pivot_atom`), îl elimină prin rezoluție (`bullet_eliminate`), rezolvă recursiv restul și, dacă iese `sat`, deduce valoarea lui `Pivot` din `NegClauses` (`infer_pivot_value`).
* **39–41:** `simplify_clauses` — Cu `findall` sortează/deduplică fiecare clauză și aruncă tautologiile, apoi scoate subsumatele cu `drop_subsumed`.
* **43–46:** `drop_subsumed` — Păstrează o clauză doar dacă nicio clauză deja păstrată nu e inclusă în ea (`subset`).
* **48:** `is_tautology` — Clauza conține și `pos(Atom)` și `neg(Atom)`.
* **50–54:** `propagate_unit` — Cu `findall` păstrează doar clauzele fără `UnitLit` și taie opusul `NegUnitLit` din ele.
* **56–57:** `opposite_lit` — Flip `pos` $\leftrightarrow$ `neg`.
* **59–60:** `lit_assignment` — `pos` $\rightarrow$ `true`, `neg` $\rightarrow$ `false`.
* **62–66:** `find_pure_literal` — Lipește clauzele (`append/2`), sortează literalii unici și îl alege pe primul fără opus (`\+ member`).
* **68–76:** `pick_pivot_atom` — `moms` caută lungimea minimă (`> 1`) și alege atomul cel mai frecvent din acele clauze scurte; `dlis` alege atomul cel mai frecvent din toate clauzele; altfel face fallback la `moms`.
* **78–86:** `most_frequent_atom` — Pentru fiecare atom unic numără cu `findall` în câte clauze apare (`pos` sau `neg`), formează `score(Count, Atom)`, sortează descrescător (`@>=`) și îl ia pe primul.
* **88–100:** `bullet_eliminate` — Separă cu `findall` în `PosClauses` (`+Pivot`), `NegClauses` (`-Pivot` fără `+Pivot`) și `NeutralClauses` (fără `Pivot`); combină fiecare `PosClause × NegClause` tăind pivotul și eliminând tautologiile; lipește cu `NeutralClauses` și simplifică.
* **102–107:** `infer_pivot_value` — Testează cu `forall` dacă punând `Pivot = true` (ceea ce satisface deja toate `PosClauses`) rămân satisfăcute și toate `NegClauses` folosind `SubModel`. Dacă da $\rightarrow$ `true`, altfel `false`.
* **109–110:** `lit_true_in_model` — `pos` e adevărat dacă în model e `true`; `neg` dacă e `false`.
* **112–114:** `collect_all_atoms` — Extrage și sortează toți atomii unici din clauze.
* **116–120:** `fill_missing_atoms` — Orice atom din `AllAtoms` absent din `PartialModel` primește `true`.
* **122–126:** `format_solution` — Sortează modelul, formatează `atom/val`, le unește cu `'; '` și pune acolade `"{...}"`.

---

## 7. Auto-Test Rapid de Colocviu (12 întrebări & răspunsuri)

1. **De ce faci `copy_term` înainte de rezoluția FOL?**
   > *Standardizing apart*: fără `copy_term`, unificarea ar lega variabilele direct în clauzele originale și n-am mai putea refolosi clauza în alți pași.
2. **Ce face `\+ \+ (copy_term(A1, F1), copy_term(A2, F2), F1 = F2)`?**
   > Testează dacă doi termeni se *pot* unifica, iar dubla negație anulează imediat legarea variabilelor ca să nu afecteze candidații.
3. **Diferența dintre `=` și `==`?**
   > `=` unifică (leagă variabile), folosit la MGU; `==` verifică identitatea strictă fără să lege nimic (`remove_exact`, `factor_duplicates`).
4. **Ce face `numbervars` și de ce îl folosești în două locuri?**
   > În `fol_loop` (pe copie) îngheață variabilele ca `A, B` pentru afișare în trace; în `subsumed_by_existing` îngheață clauza specifică ca `subset` să nu-i lege variabilele.
5. **Ce face `=..` (univ)?**
   > Desface un termen compus în `[Functor | ListaArgumente]` și îl reasamblează la loc după convertirea argumentelor.
6. **Ce optimizări are rezoluția propozițională (C5 p.6)?**
   > Eliminarea tautologiilor, eliminarea clauzelor subsumate (inițial și dinamic), și evitarea rezoluțiilor repetate prin `History` cu ambele direcții.
7. **De ce `s1_prop_4` are `Ops = 2` și `Trace = 0`?**
   > Cele două rezoluții produc tautologii (`[b, neg(b)]`, `[a, neg(a)]`), deci s-au executat dar nu au intrat în trace-ul util.
8. **De ce `s1_prop_5` are `0` operații?**
   > `[neg(c)]` subsumează `[b, neg(c)]` încă din preprocesare; clauzele rămase n-au literali opuși.
9. **De ce la `davis_putnam` `infer_pivot_value` verifică doar `NegClauses`?**
   > Dacă `Pivot = true`, toate `PosClauses` sunt automat adevărate; verificăm cu `forall` doar dacă `NegClauses` supraviețuiesc cu `SubModel`. Dacă nu, `Pivot = false` (care satisface automat `NegClauses`, iar `PosClauses` sunt deja garantate de rezoluția `•`).
10. **Diferența dintre Davis-Putnam (1960) și DPLL?**
    > DP elimină variabile prin rezoluție (`•`); DPLL ramifică cu backtracking (`p = true` / `p = false`).
11. **Diferența dintre MOMS și DLIS?**
    > MOMS numără aparițiile doar în clauzele cele mai scurte (`> 1`); DLIS numără în toate clauzele active.
12. **Teorema lui Herbrand (pe scurt)?**
    > O mulțime de clauze FOL $S$ e nesatisfiabilă $\iff$ există o submulțime **finită** de instanțe ground din universul Herbrand $H_S$ care e propozițional nesatisfiabilă.

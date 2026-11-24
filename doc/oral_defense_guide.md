# Ghid Complet pentru Colocviu — Explicații Linie cu Linie (KRR Project 1)

> **Notă:** Acest fișier este strict ghidul tău de pregătire pentru prezentarea orală (nu este inclus în PDF-ul generat și nu încalcă regula „fără comentarii în `src/`”).

---

## 1. Harta rapidă & Cele 7 „cărămizi” Prolog

### Cele 4 fișiere dintr-o privire
| Fișier | Rol pe scurt | Ce reții pentru colocviu |
| :--- | :--- | :--- |
| `src/parser.pl` (84 linii) | Citește formule CNF text și scoate liste cu `pos(...)`, `neg(...)`, `var(...)`. | Gramatică **DCG** (`-->`); literă mare/`_` = variabilă (`var(Name)`), literă mică = constantă. |
| `src/resolution_prop.pl` (95 linii) | Rezoluție propozițională + optimizările din **C5 p.6**. | Eliminare tautologii, subsumpție (inițial + dinamic), istoric `(Id1, Id2, Pivot)`, perechea cea mai scurtă. |
| `src/resolution_fol.pl` (123 linii) | Rezoluție First-Order Logic cu unificare. | `copy_term` (*standardizing apart*), unificare MGU (`=`), factorizare (`==`), subsumpție (`numbervars` + `subset`). |
| `src/davis_putnam.pl` (158 linii) | SAT Solver **Davis-Putnam (1960)** cu regula `•`. | Unit clause, Pure literal, regula `•` (`bullet_eliminate`), **MOMS** vs **DLIS**, reconstrucție pivot. |

### Cele 7 instrucțiuni Prolog care apar peste tot
1. **`member(X, Lista)`** — verifică dacă `X` e în listă (sau ia elementele pe rând).
2. **`findall(Ce, Conditii, Rezultat)`** — ca un `for + if`: strânge într-o listă tot ce trece de condiții.
3. **`forall(Conditie, Test)`** — verifică dacă *toate* elementele respectă testul.
4. **`sort(Lista, Rezultat)`** / **`sort(1, @=< / @>=, ...)`** — sortează și scoate dublurile (sau sortează după primul câmp: lungime / scor).
5. **`copy_term` + `numbervars`** — face copie izolată fără să strice originalul / îngheață variabilele ca `$VAR(0)` pentru printare sau subsumpție.
6. **`=` vs `==`** — `=` **unifică** (leagă variabile), `==` verifică **identitatea strictă** (nu leagă nimic).
7. **`\+ \+ (...)`** — probează dacă ceva merge fără să lase variabile legate în urmă.

---

## 2. Explicația testelor (de ce ies numerele astea?)

### Subiectul 1 — Rezoluție Propozițională (`tests/s1_prop_1..5.txt`)
* **`s1_prop_1.txt`** $\rightarrow$ `refutation_success`, **5 ops**, **5 trace steps**: `(f or a or b or not f)` e tautologie și dispare la preprocesare; unitatea `not b` declanșează lanțul până la `[]`.
* **`s1_prop_2.txt`** $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**: contradicție derivată direct din `(a or not e)` cu `e` și `not a`.
* **`s1_prop_3.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **2 trace steps** (SAT): `not c` subsumează `(not c or b)` la preprocesare; `(c or f)` + `not c` $\rightarrow$ `[f]`, `[f]` + `(not f or b)` $\rightarrow$ `[b]`; apoi nu mai există literali complementari.
* **`s1_prop_4.txt`** $\rightarrow$ `refutation_failure`, **2 ops**, **0 trace steps** (SAT): `(a or b)` cu `(not a or not b)` produce două tautologii (`[b, not b]` și `[a, not a]`). Cele 2 operații se contorizează (`Ops = 2`), dar tautologiile sunt aruncate și nu intră în `Trace` (`0` pași utili).
* **`s1_prop_5.txt`** $\rightarrow$ `refutation_failure`, **0 ops**, **0 trace steps** (SAT): `[not c]` subsumează `[b, not c]` încă din preprocesare; rămân `[a, not b]` și `[not c]`, fără perechi opuse.

### Subiectul 1 — Rezoluție FOL (`tests/s1_fol_*.txt`)
* **`s1_fol_own.txt`** (Alex absolvent) $\rightarrow$ `refutation_success`, **10 ops**, **8 trace steps**: 2 rezolvenți generați au fost deja subsumați de clauze existente (nu au intrat în `Trace`).
* **`s1_fol_c3_p30.txt`** (Socrate) $\rightarrow$ `refutation_success`, **2 ops**, **2 trace steps**.
* **`s1_fol_c3_p33.txt`** (Animal lover & killer) $\rightarrow$ `refutation_success`, **3 ops**, **3 trace steps**.
* **`s1_fol_c4_p12.txt`** (Paradoxul bărbierului) $\rightarrow$ `refutation_success`, **5 ops**, **3 trace steps**.

### Subiectul 2 — Davis-Putnam (`tests/s2_dp_1..6.txt`, ambele strategii MOMS & DLIS)
* **`s2_dp_1.txt`** $\rightarrow$ `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` (`toddler, female, girl` sunt forțate `true` ca unități $\rightarrow$ `child=true` $\rightarrow$ `male=false`; `boy` și `infant` rămân neconstrânși și primesc `true` din oficiu în `fill_missing_atoms`).
* **`s2_dp_2.txt`** $\rightarrow$ `NOT`: `{}` (`toddler` + `female` forțează `girl=true`, care se bate cap în cap cu `not girl`).
* **`s2_dp_3.txt`**, **`s2_dp_4.txt`** $\rightarrow$ `NOT`: `{}` (aceleași formule nesatisfiabile ca la `prop_1` / `prop_2`).
* **`s2_dp_5.txt`** $\rightarrow$ `YES`: `{a/false; b/false; d/true; e/true; f/true}`.
* **`s2_dp_6.txt`** $\rightarrow$ `NOT`: `{}` (`a` și `b` sunt forțate în toate cele 4 combinații posibile).

---

## 3. Explicație linie cu linie — `src/parser.pl` (Liniile 1–84)

### Modul, setări și funcții de intrare (Liniile 1–24)
* **1–6:** Declarăm modulul `parser` și exportăm `parse_kb_file/2`, `parse_kb_string/2`, `parse_cnf/2`, `parse_clause/2`.
* **8:** `:- encoding(utf8).` — Să recunoască fără erori simbolul Unicode `¬`.
* **9:** `:- set_prolog_flag(double_quotes, chars).` — Ghilimelele `"..."` din gramatică devin liste de caractere (`chars`), necesare pentru DCG.
* **11–12:** `parse_cnf(FormulaString, Clauses)` — Alias către `parse_kb_string`.
* **14–16:** `parse_clause(ClauseString, Literals)` — Transformă o singură clauză-string în listă de caractere și aplică regula DCG `clause_expr` (ignorând spațiile din capete).
* **18–20:** `parse_kb_file(FilePath, Clauses)` — Citește tot fișierul ca string UTF-8 și îl pasează la `parse_kb_string`.
* **22–24:** `parse_kb_string(FormulaString, Clauses)` — Sparge stringul în caractere și pornește gramatica DCG de la regula de vârf `cnf_formula`.

### Gramatica formulei CNF și a clauzelor (Liniile 26–58)
* **26–28:** `cnf_formula([FirstClause | RestClauses])` — Dacă vede o clauză urmată de un separator de conjuncție (`conjunction_op`), taie cu `!` și parsează recursiv restul clauzelor.
* **29–30:** `cnf_formula([SingleClause])` — Dacă nu mai există separator de conjuncție după ea, e ultima clauză din formulă.
* **31–32:** `cnf_formula([])` — Caz limită: fișier gol / doar spații $\rightarrow$ listă goală de clauze.
* **34–37:** `conjunction_op` — Operator de ȘI între clauze: `"and"`, `"^"`, `"&"`, `";"` sau linie nouă (`newline`), cu spații în jur.
* **39–41:** `clause_expr(Literals)` — O clauză poate fi închisă între `(...)`, între `[...]`, sau fără paranteze, conținând o disjuncție (`disjunction_expr`).
* **43–45:** `disjunction_expr([FirstLit | RestLits])` — Dacă după un literal urmează `disjunction_op`, taie (`!`) și parsează restul literalilor.
* **46–47:** `disjunction_expr([SingleLit])` — Ultimul (sau singurul) literal din clauză.
* **49–50:** `disjunction_op` — Operator de SAU între literali: `"or"`, `"v"`, `"|"`, `","`, cu spații în jur.
* **52–53:** `literal_expr(neg(Predicate))` — Dacă începe cu prefix de negație (`negation_prefix`), împachetează termenul în `neg(...)`.
* **54–55:** `literal_expr(pos(Predicate))` — Altfel îl împachetează în `pos(...)`.
* **57–58:** `negation_prefix` — Recunoaște `"not"` urmat de spațiu (ca să nu confunde `"not_p"`), sau simbolurile `¬`, `~`, `-`.

### Termeni FOL, variabile și identificatori (Liniile 60–84)
* **60–62:** `fol_term(Compound)` — Dacă un identificator cu literă mică (`IsVar = false`) e urmat de `(Args)`, taie (`!`) și îl împachetează cu `=..` într-un termen compus (ex: `man(var('X'))`).
* **63–65:** `fol_term(Term)` — Dacă n-are paranteze după el: dacă `IsVar == true` devine `var(Name)`, altfel rămâne constanta simplă `Name`.
* **67–71:** `arg_list` — O listă de termeni `fol_term` despărțiți prin virgulă `,` (suportă și funcții imbricate, gen `f(g(X), y)`).
* **73–75:** `identifier(Name, true)` — Începe cu literă MARE (`upper`) sau `_` $\Rightarrow$ **variabilă** (`true`).
* **76–78:** `identifier(Name, false)` — Începe cu literă MICĂ (`lower`) $\Rightarrow$ **constantă sau nume de predicat/funcție** (`false`).
* **80–81:** `id_rest` — Restul caracterelor din nume pot fi alfanumerice (`alnum`) sau `_`.
* **83–84:** `whitespaces` — Consumă recursiv zero sau mai multe spații/tab-uri/newline-uri.

---

## 4. Explicație linie cu linie — `src/resolution_prop.pl` (Liniile 1–95)

### Modul și funcția principală (Liniile 1–19)
* **1–4:** Declarăm modulul `resolution_prop` și exportăm `prove_propositional/4` și `prove_propositional/2`.
* **6:** Importăm `parser`.
* **8–9:** `prove_propositional/2` — Scurtătură când vrei doar rezultatul, ignorând numărul de operații și trace-ul (`_, _`).
* **11–12:** `prove_propositional/4` — Încarcă clauzele din listă sau din fișier.
* **13:** `preprocess_clauses(RawClauses, Clauses)` — Aplică curățarea inițială (dubluri, tautologii, subsumpție) și le numerotează cu ID-uri.
* **14–15:** Dacă clauza vidă `[]` există deja din start $\rightarrow$ `refutation_success`, 0 operații.
* **16–18:** Altfel ia `MaxId` = numărul de clauze (`length`), rulează bucla `prop_loop` și întoarce trace-ul în ordinea corectă (`reverse`).

### Preprocesarea: C5 p.6 (Liniile 21–44)
* **21–26:** `preprocess_clauses`:
  * **22–24:** `findall`: pentru fiecare clauză brută, îi sortează literalii (scoțând duplicatele) și păstrează doar ce **nu** e tautologie.
  * **25:** `drop_subsumed` elimină clauzele subsumate (mai slabe).
  * **26:** `index_clauses` le pune etichete `clause(1, ...)`, `clause(2, ...)`.
* **28–31:** `is_tautology` — Clauza conține atât `pos(Atom)` cât și `neg(Atom)` $\rightarrow$ mereu adevărată, inutilă.
* **33–39:** `drop_subsumed` — Curăță mai întâi restul (`KeptRest`); dacă în `KeptRest` există o clauză mai mică inclusă în `Clause` (`subset(Other, Clause)`), o aruncă pe `Clause`.
* **41–44:** `index_clauses` — Atribuie ID-uri crescătoare `1, 2, 3...`.

### Bucla de rezoluție și selecția perechii (Liniile 46–95)
* **46:** `prop_loop` — Motorul iterativ de rezoluție.
* **47–48:** `pick_shortest_pair` — Alege perechea neîncercată cu suma lungimilor minimă și pune `!` (cut) ca să nu se răzgândească.
* **49:** `resolve_on_pivot` — Combină `Clause1` și `Clause2` eliminând `Pivot` și opusul lui.
* **50:** `NextOps is OpsSoFar + 1` — Contorizează operația efectuată.
* **51–52:** `opposite_lit` + `NextHistory` — Înregistrează în istoric **ambele** direcții `(Id1, Id2, Pivot)` și `(Id2, Id1, NegPivot)` ca să nu repete aceeași rezoluție.
* **53:** Construiește înregistrarea pasului `Step = step(...)`.
* **54–55:** Dacă `Resolvent == []` $\rightarrow$ **contradicție!** Oprește bucla cu `refutation_success`.
* **56–57:** Dacă rezolventul e tautologie sau e subsumat de o clauză existentă (`subsumed_by_any`), îl aruncă și continuă bucla fără să-l adauge (de asta nu apare nici în `Trace`).
* **58–63:** Dacă rezolventul e nou și util:
  * **58–60:** `findall` — Elimină dinamic din `Clauses` orice clauză veche subsumată strict de noul `Resolvent` (`Resolvent \== Existing, subset(Resolvent, Existing)`).
  * **61–63:** Îi dă `NewId`, îl adaugă în listă, apelează recursiv `prop_loop` și adaugă `Step` în `Trace`.
* **65:** Cazul de bază când `pick_shortest_pair` nu mai găsește nicio pereche nouă de combinat $\rightarrow$ `refutation_failure`.
* **67–80:** `pick_shortest_pair` — Cu `findall` adună toate perechile `(I1 < I2)` care au un literal complementar și nu sunt în `History`, le calculează `Size = Len1 + Len2`, verifică să nu fie listă goală (`Candidates \== []`), sortează crescător (`@=<`) după `Size` și ia prima pereche.
* **82–87:** `resolve_on_pivot` — Șterge `Pivot` din `Clause1`, șterge `NegPivot` din `Clause2`, lipește resturile (`append`) și sortează (eliminând duplicatele).
* **89–90:** `opposite_lit` — Întoarce semnul literalului (`pos` $\leftrightarrow$ `neg`).
* **92–95:** `subsumed_by_any` — Verifică dacă există în `Clauses` o clauză mai generală/egală inclusă în `Resolvent` (`subset(Existing, Resolvent)`).

---

## 5. Explicație linie cu linie — `src/resolution_fol.pl` (Liniile 1–123)

### Modul, intrare și conversia variabilelor (Liniile 1–49)
* **1–4:** Exportă `prove_fol/4` și `prove_fol/2`.
* **6:** Importă `parser`.
* **8–9:** Scurtătura `prove_fol/2`.
* **11–19:** `prove_fol/4` — Încarcă clauzele, le indexează și convertește variabilele (`index_and_convert_clauses`), verifică `[]` inițial, altfel pornește `fol_loop` și inversează trace-ul.
* **21–25:** `index_and_convert_clauses` — Dă fiecărei clauze un ID (`1, 2, ...`) și apelează `convert_literals` cu un dicționar inițial gol `[]` (astfel variabilele din clauze diferite sunt izolate).
* **27–33:** `convert_literals` — Trece prin fiecare literal `pos(Formula)` / `neg(Formula)` și îi convertește termenii păstrând același dicționar `MapIn -> MapMid -> MapOut` în interiorul aceleiași clauze.
* **35–37:** `convert_term(var(Name), ...)` — Dacă `Name` există deja în `MapIn`, refolosește aceeași variabilă vie `PrologVar`; altfel o creează și o salvează în dicționar.
* **38–43:** `convert_term(Compound, ...)` — Dacă termenul e compus (`compound`), îl desface cu `=..` în `[Functor | RawArgs]`, convertește recursiv argumentele cu `convert_terms` și îl reasamblează la loc cu `=..`.
* **44:** `convert_term(Constant, ...)` — Orice altceva (constantele cu literă mică) rămâne neschimbat.
* **46–49:** `convert_terms` — Parcurge recursiv lista de argumente ale unei funcții/predicat.

### Bucla de rezoluție FOL, unificare și factorizare (Liniile 51–123)
* **51–53:** `fol_loop` — Caută cea mai scurtă pereche de clauze unificabile (`pick_shortest_unifiable_pair`) și taie (`!`).
* **54–55:** `copy_term` pe ambele clauze — *Standardizing apart*: face copii proaspete ca unificarea să nu strice clauzele originale.
* **56–57:** `nth1` — Extrage literalii exact de la pozițiile `Idx1` și `Idx2` din copiile proaspete.
* **58:** `resolve_and_factor` — Unifică literalii, îi șterge și face factorizarea.
* **59–60:** Incrementează `Ops` și adaugă `(Id1, Id2, Idx1, Idx2)` în `History`.
* **61–63:** Face o copie `PrintableResolvent` și aplică `numbervars` ca variabilele să se afișeze frumos (`A, B`) fără a îngheța variabilele reale din `Resolvent`.
* **64–65:** Dacă `Resolvent == []` $\rightarrow$ **succes** (`refutation_success`).
* **66–67:** Dacă e subsumat de o clauză existentă (`subsumed_by_existing`) $\rightarrow$ îl ignoră și continuă bucla.
* **68–70:** Altfel adaugă `clause(NewId, Resolvent)` și continuă recursiv.
* **72:** Dacă nu mai sunt perechi de rezolvat $\rightarrow$ `refutation_failure`.
* **74–87:** `pick_shortest_unifiable_pair` — Adună cu `findall` perechile `(I1 < I2)` cu literali la pozițiile `Pos1`, `Pos2` care pot unifica (`can_unify_opposite`) și nu sunt în `History`; sortează crescător după suma lungimilor și o ia pe prima.
* **89–92:** `can_unify_opposite` — Verifică semne opuse (`pos` vs `neg`) și folosește trucul `\+ \+ (copy_term(...), Fresh1 = Fresh2)` ca să testeze unificabilitatea fără a lăsa variabile legate.
* **94–99:** `resolve_and_factor` — Unifică atomii (`unify_atoms`), șterge literalii exacți (`remove_exact`), lipește resturile și elimină duplicatele (`factor_duplicates`).
* **101–102:** `unify_atoms` — Leagă efectiv atomii cu `=` (calculează MGU).
* **104–105:** `remove_exact` — Șterge prima apariție identică (`==`) a literalului rezolvat (fără să unifice alți literali!).
* **107–113:** `factor_duplicates` — Păstrează o singură copie dacă doi literali din rezolvent sunt identici (`==`).
* **115–123:** `subsumed_by_existing` — Testează dacă o clauză existentă subsumează `Resolvent` folosind `copy_term`, `numbervars` pe `FreshResolvent` (îi îngheață variabilele ca să nu fie modificate) și `subset`, totul în `\+ \+` ca să nu lege nimic permanent.

---

## 6. Explicație linie cu linie — `src/davis_putnam.pl` (Liniile 1–158)

### Modul și intrare (Liniile 1–23)
* **1–6:** Exportă `solve_dp/4`, `solve_dp/3`, `solve_dp/2` și `format_solution/2`.
* **8:** Importă `parser`.
* **10–20:** `solve_dp/4` — Încarcă clauzele, salvează lista tuturor atomilor (`AllAtoms`), apelează `dp_solve`; dacă iese `sat`, completează atomii lipsă cu `true` și formatează `{...}` cu `YES`, altfel returnează `NOT` și `{}`.
* **22–23:** Scurtături cu 3 și 2 parametri (implicit strategia `moms`).

### Bucla principală `dp_solve` (Liniile 25–49)
* **25–26:** Curăță clauzele la fiecare pas (`simplify_clauses`).
* **27–28:** Dacă există `[]` $\rightarrow$ `unsat` (`NOT`).
* **29–30:** Dacă nu mai sunt clauze (`[]`) $\rightarrow$ `sat` (`YES`).
* **31–35:** **Unit Clause:** Găsește `[UnitLit]`, propagă valoarea lui (`propagate_unit`), notează `(Atom, Value)` și apelează recursiv; dacă iese `sat`, o pune în model.
* **36–40:** **Pure Literal:** Găsește un literal care nu are opus (`find_pure_literal`), păstrează cu `findall` doar clauzele fără el, notează `(Atom, Value)` și apelează recursiv.
* **41–49:** **Regula `•`:** Alege `Pivot` (`pick_pivot_atom`), îl elimină prin rezoluție completă (`bullet_eliminate`), rezolvă recursiv restul, iar dacă iese `sat` reconstruiește valoarea lui `Pivot` din `NegClauses` (`infer_pivot_value`).

### Simplificare, unități și literali puri (Liniile 51–85)
* **51–55:** `simplify_clauses` — Sortează și deduplică fiecare clauză, aruncă tautologiile cu `findall`, apoi elimină subsumatele cu `drop_subsumed`.
* **57–60:** `drop_subsumed` — Păstrează clauza doar dacă nu e inclusă de alta deja păstrată (`subset(Other, Clause)`).
* **62–65:** `is_tautology` — Clauza are și `pos(Atom)` și `neg(Atom)`.
* **67–71:** `propagate_unit` — Cu `findall` păstrează doar clauzele fără `UnitLit` și șterge `NegUnitLit` din ele.
* **73–74:** `opposite_lit` — Flip `pos` $\leftrightarrow$ `neg`.
* **76–77:** `lit_assignment` — `pos` $\rightarrow$ `true`, `neg` $\rightarrow$ `false`.
* **79–85:** `find_pure_literal` — Lipește clauzele (`append/2`), sortează literalii unici și îl alege pe primul al cărui opus nu există (`\+ member`).

### MOMS, DLIS, operația `•`, reconstrucție și formatare (Liniile 87–158)
* **87–97:** `pick_pivot_atom` — `moms` ia clauzele cele mai scurte (`Len > 1`, `min_list`) și alege atomul cel mai frecvent din ele; `dlis` alege atomul cel mai frecvent din toate clauzele; altceva face fallback la `moms`.
* **99–109:** `most_frequent_atom` — Pentru fiecare atom unic numără cu `findall` în câte clauze apare (`pos` sau `neg`), formează `score(Count, Atom)`, sortează descrescător (`@>=`) și îl ia pe primul.
* **111–130:** `bullet_eliminate` — Separă cu `findall` în `PosClauses` (`+Pivot`), `NegClauses` (`-Pivot` fără `+Pivot`) și `NeutralClauses` (fără `Pivot`); combină fiecare pereche `PosClause × NegClause` tăind pivotul și eliminând tautologiile; lipește cu `NeutralClauses` și simplifică.
* **132–140:** `infer_pivot_value` — Testează cu `forall` dacă punând `Pivot = true` (care satisface deja `PosClauses`) toate `NegClauses` au măcar un literal adevărat în `[assign(Pivot, true) | SubModel]`. Dacă da $\rightarrow$ `true`, altfel `false`.
* **142–146:** `collect_all_atoms` — Extrage și sortează toți atomii unici din formulă.
* **148–152:** `fill_missing_atoms` — Orice atom din `AllAtoms` absent din `PartialModel` primește `true`.
* **154–158:** `format_solution` — Sortează modelul, formatează fiecare element `atom/val`, le unește cu `'; '` și pune acolade `"{...}"`.

---

## 7. Întrebări rapide de teorie (C1–C5, 10% din notă)
* **Teorema lui Herbrand:** O mulțime de clauze FOL $S$ este nesatisfiabilă $\iff$ există o submulțime **finită** de instanțe ground din universul Herbrand $H_S$ care este propozițional nesatisfiabilă.
* **De ce rezoluția FOL cu unificare e mai bună decât enumerarea Herbrand?** Instanțiază variabilele dinamic doar cât e nevoie (MGU), fără a genera infinitatea de termeni din $H_S$.
* **Diferența Davis-Putnam (1960) vs DPLL (1962):** DP elimină variabile prin rezoluție (`•`), pe când DPLL face ramificare cu backtracking (`p = true` / `p = false`).

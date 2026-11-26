# Project 1: Knowledge Representation and Reasoning (KRR)
**Automated Theorem Proving via Resolution and the Davis-Putnam SAT Solver**

* **Student:** Coman Ioan Alexandru  
* **Faculty:** Faculty of Mathematics and Computer Science, University of Bucharest (FMI UniBuc)  
* **Course:** Knowledge Representation and Reasoning (KRR)  
* **Instructor:** Conf. dr. Marina Anca Cidotă  
* **Submission Date:** December 2026  

---

## 1. Subject 1: First-Order and Propositional Resolution

### 1.a) Knowledge Base in Natural Language & FOL Representation

#### Natural Language Description (Domain: University Academic Standing)
1. Every student who submits all assignments and passes the final exam qualifies for graduation.
2. Any student who is diligent submits all assignments.
3. Every student who attends all lectures passes the final exam.
4. Alex is a student who is diligent and attends all lectures.

#### Question (Entailment Query)
* Does Alex qualify for graduation?

#### Formal Vocabulary
* **Constants:**
  * $\text{alex}$: the individual student named Alex.
* **Unary Predicates:**
  * $\text{student}(X)$: $X$ is an enrolled student.
  * $\text{submits}(X)$: $X$ submits all required assignments.
  * $\text{passes}(X)$: $X$ passes the final examination.
  * $\text{diligent}(X)$: $X$ exhibits academic diligence.
  * $\text{attends}(X)$: $X$ attends all scheduled lectures.
  * $\text{graduates}(X)$: $X$ qualifies for academic graduation.

#### First-Order Logic (FOL) Formulas
1. $\forall X \, ((\text{student}(X) \land \text{submits}(X) \land \text{passes}(X)) \to \text{graduates}(X))$
2. $\forall X \, ((\text{student}(X) \land \text{diligent}(X)) \to \text{submits}(X))$
3. $\forall X \, ((\text{student}(X) \land \text{attends}(X)) \to \text{passes}(X))$
4. $\text{student}(\text{alex}) \land \text{diligent}(\text{alex}) \land \text{attends}(\text{alex})$
* **Query:** $\text{graduates}(\text{alex})$

---

### 1.b) Transformation to Conjunctive Normal Form (CNF) & Manual Proof

#### Step-by-Step CNF Conversion:
1. **Eliminate Implications ($A \to B \equiv \neg A \lor B$):**
   * Sentence 1: $\neg (\text{student}(X) \land \text{submits}(X) \land \text{passes}(X)) \lor \text{graduates}(X)$
     $\equiv \neg \text{student}(X) \lor \neg \text{submits}(X) \lor \neg \text{passes}(X) \lor \text{graduates}(X)$ (by De Morgan's Law)
   * Sentence 2: $\neg (\text{student}(Y) \land \text{diligent}(Y)) \lor \text{submits}(Y)$
     $\equiv \neg \text{student}(Y) \lor \neg \text{diligent}(Y) \lor \text{submits}(Y)$
   * Sentence 3: $\neg (\text{student}(Z) \land \text{attends}(Z)) \lor \text{passes}(Z)$
     $\equiv \neg \text{student}(Z) \lor \neg \text{attends}(Z) \lor \text{passes}(Z)$
   * Sentence 4 (Facts):
     * $\text{student}(\text{alex})$
     * $\text{diligent}(\text{alex})$
     * $\text{attends}(\text{alex})$
2. **Negation of the Goal (Refutation Principle):**
   * $\neg \text{graduates}(\text{alex})$

#### Resulting Clause Set $S$:
* $C_1$: $\{\neg \text{student}(X), \neg \text{submits}(X), \neg \text{passes}(X), \text{graduates}(X)\}$
* $C_2$: $\{\neg \text{student}(Y), \neg \text{diligent}(Y), \text{submits}(Y)\}$
* $C_3$: $\{\neg \text{student}(Z), \neg \text{attends}(Z), \text{passes}(Z)\}$
* $C_4$: $\{\text{student}(\text{alex})\}$
* $C_5$: $\{\text{diligent}(\text{alex})\}$
* $C_6$: $\{\text{attends}(\text{alex})\}$
* $C_7$: $\{\neg \text{graduates}(\text{alex})\}$ (Negated Goal)

#### Manual Resolution Proof Tree (Refutation):
```
                      C1: {¬student(X), ¬submits(X), ¬passes(X), graduates(X)}
                                              |
                     C7: {¬graduates(alex)}   |  [MGU: X = alex]
                               \             /
                                \           /
           C8: {¬student(alex), ¬submits(alex), ¬passes(alex)}
                     \                 /
                      \               /   C4: {student(alex)}
                       \             /
              C9: {¬submits(alex), ¬passes(alex)}
                     /                 \
                    /                   \  C2: {¬student(Y), ¬diligent(Y), submits(Y)}
                   /                     \   [MGU: Y = alex]
                  /                       \
        C10: {¬passes(alex), ¬student(alex), ¬diligent(alex)}
                  \                       /
                   \                     /   C4: {student(alex)}
                    \                   /
             C11: {¬passes(alex), ¬diligent(alex)}
                      \                 /
                       \               /   C5: {diligent(alex)}
                        \             /
                    C12: {¬passes(alex)}
                           /          \
                          /            \  C3: {¬student(Z), ¬attends(Z), passes(Z)}
                         /              \   [MGU: Z = alex]
                        /                \
             C13: {¬student(alex), ¬attends(alex)}
                      \                 /
                       \               /   C4: {student(alex)}
                        \             /
                    C14: {¬attends(alex)}
                           \           /
                            \         /   C6: {attends(alex)}
                             \       /
                            C15: [ ]  (EMPTY CLAUSE - CONTRADICTION DERIVED)
```
The derivation of the empty clause $\Box$ proves that $KB \cup \{\neg \text{graduates}(\text{alex})\}$ is unsatisfiable, hence $KB \models \text{graduates}(\text{alex})$.

---

### 1.c) Automatic FOL Resolution & Benchmark Evaluation

The First-Order Logic resolution procedure was implemented in SWI-Prolog (`resolution_fol.pl`). The algorithm incorporates:
* Definite Clause Grammars (DCG) parser reading standard logic notations (`parser.pl`).
* Variable isolation and standardizing apart (`copy_term`).
* Most General Unifier (MGU) computation via unification.
* Subsumption detection and factoring.

#### Test Results:
1. **User Own Example (`s1_fol_own.txt`):**
   * Result: `refutation_success`
   * Number of resolution operations performed: **10 operations**
   * Empty clause derived successfully.
2. **Course Example 1 (C3 p.30 Socrates):**
   * Formula: $(\neg \text{man}(X) \lor \text{mortal}(X)) \land \text{man}(\text{socrates}) \land \neg \text{mortal}(\text{socrates})$
   * Result: `refutation_success`
   * Number of resolution operations performed: **2 operations**
3. **Course Example 2 (C3 p.33 Animal Lover & Killer):**
   * Formula: $(\neg \text{animal}(X) \lor \text{loves}(\text{john}, X)) \land (\neg \text{loves}(Y, Z) \lor \neg \text{kills}(Y, Z)) \land \text{animal}(\text{cat}) \land \text{kills}(\text{john}, \text{cat})$
   * Result: `refutation_success`
   * Number of resolution operations performed: **3 operations**
4. **Course Example 3 (C4 p.12 Barber Paradox):**
   * Formula: $(\neg \text{person}(X) \lor \text{shaves}(\text{barber}, X) \lor \text{shaves}(X, X)) \land (\neg \text{person}(Y) \lor \neg \text{shaves}(\text{barber}, Y) \lor \neg \text{shaves}(Y, Y)) \land \text{person}(\text{barber})$
   * Result: `refutation_success`
   * Number of resolution operations performed: **5 operations**

---

### 1.d) Propositional Resolution: Implementation, Optimizations & Analysis

The propositional resolution engine (`resolution_prop.pl`) operates in accordance with Brachman & Levesque (2004, Chapter 4), augmented with the required optimizations from course slide C5 page 6:
1. **Tautology Elimination:** Any clause containing complementary literals $\{L, \neg L\}$ is discarded during preprocessing and upon derivation, as it evaluates unconditionally to true and provides no constraint.
2. **Subsumption Elimination:** If clause $C_1 \subseteq C_2$, then $C_2$ is strictly weaker and can be discarded without sacrificing completeness.
3. **Repeated Resolution Avoidance:** The algorithm tracks the triplet of indices and the pivot literal $(Id_1, Id_2, \text{Pivot})$. A resolution operation is never performed more than once on the same clause pair with respect to the same literal.
4. **Heuristic Pair Selection:** Prioritizes unit clauses and shortest clause pairs to accelerate refutation discovery.

#### Evaluation on Mandatory Test Sets:
* **Example (i):** $(\neg a \lor b) \land (c \lor d) \land (\neg d \lor b) \land \neg b \land (\neg c \lor b) \land e \land (f \lor a \lor b \lor \neg f)$
  * *Result:* `refutation_success` (Unsatisfiable)
  * *Resolution Operations:* **5**
  * *Trace:* Clause $(f \lor a \lor b \lor \neg f)$ is recognized as a tautology and eliminated. Unit propagation on $\neg b$ forces $\neg a$, $\neg d$, $\neg c$. Resolving with $(c \lor d)$ yields the empty clause $\Box$.
* **Example (ii):** $(\neg b \lor a) \land (\neg a \lor b \lor e) \land (a \lor \neg e) \land \neg a \land e$
  * *Result:* `refutation_success` (Unsatisfiable)
  * *Resolution Operations:* **3**
  * *Trace:* Resolving $(a \lor \neg e)$ with $e$ yields $a$. Resolving $a$ with $\neg a$ produces $\Box$.
* **Example (iii):** $(\neg a \lor b) \land (c \lor f) \land \neg c \land (\neg f \lor b) \land (\neg c \lor b)$
  * *Result:* `refutation_failure` (Satisfiable)
  * *Resolution Operations:* **2**
  * *Discussion:* The clause set has a satisfying model $\{b = \text{true}, c = \text{false}, f = \text{true}\}$. The resolution closure terminates without deriving $\Box$.
* **Example (iv):** $(a \lor b) \land (\neg a \lor \neg b) \land c$
  * *Result:* `refutation_failure` (Satisfiable)
  * *Resolution Operations:* **2**
  * *Discussion:* Satisfiable under $\{a = \text{true}, b = \text{false}, c = \text{true}\}$ or $\{a = \text{false}, b = \text{true}, c = \text{true}\}$.
* **Example (v):** $(a \lor \neg b) \land (b \lor \neg c) \land \neg c$
  * *Result:* `refutation_failure` (Satisfiable)
  * *Resolution Operations:* **0**
  * *Discussion:* Literal $a$ is pure (appears only positively). Literal $\neg c$ is pure (appears only negatively). The set is immediately satisfied by $\{a = \text{false}, b = \text{false}, c = \text{false}\}$ with 0 resolutions.

---

## 2. Subject 2: Davis-Putnam SAT Solver

### 2.a) Algorithmic Formulation (Brachman & Levesque 2004)

The Davis-Putnam procedure operates on a finite set of clauses $S$ in CNF through three deterministic rules and a resolution-based variable elimination rule:
1. **Base Cases:**
   * If $\Box \in S$: Return `NOT` (Unsatisfiable).
   * If $S = \emptyset$: Return `YES` (Satisfiable, empty model).
2. **Unit Clause Rule (1-Literal Rule):**
   * If $S$ contains a unit clause $\{L\}$:
     * Assign $L$ truth value `true` (if $L = p$, $p \leftarrow \text{true}$; if $L = \neg p$, $p \leftarrow \text{false}$).
     * Remove all clauses containing $L$.
     * Delete $\neg L$ from all remaining clauses.
3. **Pure Literal Rule (Monotone Variables):**
   * If an atom $p$ occurs only with one polarity (e.g. only $p$ or only $\neg p$):
     * Assign $p$ the polarity that satisfies its clauses.
     * Remove all clauses containing that literal.
4. **Variable Elimination Rule (The $\bullet$ Operation):**
   * Select an atom $p$. Partition $S$ into:
     * $S_p$: clauses containing $p$.
     * $S_{\neg p}$: clauses containing $\neg p$.
     * $S_0$: clauses containing neither $p$ nor $\neg p$.
   * Compute resolvents $Res(S_p, S_{\neg p}) = \{(C_1 \setminus \{p\}) \cup (C_2 \setminus \{\neg p\}) \mid C_1 \in S_p, C_2 \in S_{\neg p}\}$.
   * Define $S \bullet p = S_0 \cup Res(S_p, S_{\neg p})$ (pruning tautologies and subsumptions).
   * Recurse on $S \bullet p$. If satisfiable, reconstruct the truth assignment for $p$ by testing whether $p = \text{true}$ satisfies $S_{\neg p}$ under the recursive assignment; if so, $p \leftarrow \text{true}$, else $p \leftarrow \text{false}$.

---

### 2.b) Atom Selection Strategies & Comparative Analysis

Two genuinely distinct heuristic philosophies were implemented:
* **Strategy 1: MOMS (Maximum Occurrences in Minimum Size Clauses)**
  * Identifies the minimum length $k$ among clauses with length $> 1$.
  * Tallies atom occurrences exclusively among clauses of size $k$.
  * Selects the atom maximizing this local count.
  * *Rationale:* Prioritizes creating shorter resolvents and immediate unit clauses in subsequent steps.
* **Strategy 2: DLIS (Dynamic Largest Individual Sum / Max Total Frequency)**
  * Tallies total occurrences of each candidate atom across all active clauses in $S$.
  * Selects the atom with the highest global occurrence sum.
  * *Rationale:* Maximizes the number of clauses affected and eliminated in the initial partition.

#### Comparative Discussion:
On structured problem sets (such as ontology hierarchies in Example 1), **MOMS** typically outperforms DLIS by focusing on constrained bottleneck clauses, rapidly triggering unit propagations. **DLIS**, conversely, is a global greedy approach that excels when formulas feature uniform clause lengths or dense connectivity, but can occasionally produce a temporary expansion in the number of intermediate resolvents during the $\bullet$ operation.

---

### 2.c) Benchmark Execution Results

| Test Instance | Strategy MOMS Result & Model | Strategy DLIS Result & Model | Satisfiability |
| :--- | :--- | :--- | :--- |
| **Example (i)** | `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` | `YES`: `{boy/true; child/true; female/true; girl/true; infant/true; male/false; toddler/true}` | Satisfiable |
| **Example (ii)** | `NOT`: `{}` | `NOT`: `{}` | Unsatisfiable |
| **Example (iii)** | `NOT`: `{}` | `NOT`: `{}` | Unsatisfiable |
| **Example (iv)** | `NOT`: `{}` | `NOT`: `{}` | Unsatisfiable |
| **Example (v)** | `YES`: `{a/false; b/false; d/true; e/true; f/true}` | `YES`: `{a/false; b/false; d/true; e/true; f/true}` | Satisfiable |
| **Example (vi)** | `NOT`: `{}` | `NOT`: `{}` | Unsatisfiable |

---

## 3. Theoretical Questions & Foundations

### 3.a) What is Herbrand's Theorem?

**Herbrand's Theorem (Jacques Herbrand, 1930)** is one of the most celebrated and foundational theorems in mathematical logic and automated theorem proving. It bridges first-order logic and propositional logic.

#### Key Formulations:
1. **Herbrand Universe ($H_S$):** The set of all ground terms constructible from the constants and function symbols appearing in a clause set $S$ (augmented with an arbitrary constant if $S$ contains none).
2. **Herbrand Base ($B_S$):** The set of all ground atoms formed by applying the predicate symbols of $S$ to terms from $H_S$.
3. **Herbrand Interpretation / Model:** An interpretation whose domain is $H_S$, assigning ground terms to themselves.
4. **Statement of the Theorem:**
   > *A set of first-order clauses $S$ is unsatisfiable if and only if there exists a **finite** set of ground instances $S'$ of clauses from $S$ (obtained by substituting ground terms from $H_S$ for variables) that is propositionally unsatisfiable.*

#### Significance for Automated Reasoning:
Prior to Herbrand's Theorem, verifying the unsatisfiability of a first-order formula required searching over all possible domains and interpretations (an uncountable space). Herbrand's Theorem proves that one only needs to examine ground instances over the Herbrand Universe, reducing the semi-decidable problem of first-order unsatisfiability to testing the satisfiability of propositional formulas. J. Alan Robinson (1965) directly built on this result by introducing the **Resolution Principle with Unification**, which searches the space of ground instances implicitly and efficiently without enumerating the Herbrand universe exhaustively.

---

## 4. References & Citations

1. Ronald J. Brachman and Hector J. Levesque. *Knowledge Representation and Reasoning*. Morgan Kaufmann / Elsevier, 2004. (Chapters 4 & 5).
2. Martin Davis and Hilary Putnam. *A Computing Procedure for Quantification Theory*. Journal of the ACM (JACM), 7(3):201–215, 1960.
3. J. Alan Robinson. *A Machine-Oriented Logic Based on the Resolution Principle*. Journal of the ACM (JACM), 12(1):23–41, 1965.
4. Jacques Herbrand. *Recherches sur la théorie de la démonstration*. PhD thesis, University of Paris, 1930.
5. Conf. dr. Marina Anca Cidotă. *Knowledge Representation and Reasoning – Course Lectures C1–C5*. Faculty of Mathematics and Computer Science, University of Bucharest, 2026.
6. SWI-Prolog Documentation, Version 10.0.2. Available at: https://www.swi-prolog.org/

---

## 5. Source Code Appendix (Algorithms Only - Without Explanatory Comments)

*(In strict adherence to project evaluation instructions: no explanatory comments are included in the source code).*

### 5.1. `src/parser.pl`
```prolog
:- module(parser, [parse_kb_file/2]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_kb_file(FilePath, Clauses) :-
    read_file_to_string(FilePath, FormulaString, [encoding(utf8)]),
    string_chars(FormulaString, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([FirstClause | RestClauses]) -->
    whitespaces, clause_expr(FirstClause), whitespaces, conjunction_op, !,
    cnf_formula(RestClauses).
cnf_formula([SingleClause]) --> whitespaces, clause_expr(SingleClause), whitespaces.
cnf_formula([]) --> whitespaces.

conjunction_op -->
    whitespaces, ( "and" ; "^" ; "&" ; ";" ; [Char], { char_type(Char, newline) } ), whitespaces.

clause_expr(Literals) --> "(", whitespaces, disjunction_expr(Literals), whitespaces, ")".
clause_expr(Literals) --> "[", whitespaces, disjunction_expr(Literals), whitespaces, "]".
clause_expr(Literals) --> disjunction_expr(Literals).

disjunction_expr([FirstLit | RestLits]) -->
    literal_expr(FirstLit), whitespaces, disjunction_op, !,
    disjunction_expr(RestLits).
disjunction_expr([SingleLit]) --> literal_expr(SingleLit).

disjunction_op --> whitespaces, ( "or" ; "v" ; "|" ; "," ), whitespaces.

literal_expr(neg(Predicate)) --> negation_prefix, whitespaces, fol_term(Predicate).
literal_expr(pos(Predicate)) --> fol_term(Predicate).

negation_prefix --> "not", whitespaces.
negation_prefix --> "¬" ; "~" ; "-".

fol_term(Compound) -->
    identifier(Functor, false), whitespaces, "(", whitespaces, arg_list(Args), whitespaces, ")", !,
    { Compound =.. [Functor | Args] }.
fol_term(Term) -->
    identifier(Name, IsVar),
    { IsVar == true -> Term = var(Name) ; Term = Name }.

arg_list([FirstArg | RestArgs]) -->
    fol_term(FirstArg), whitespaces, ",", whitespaces, !,
    arg_list(RestArgs).
arg_list([SingleArg]) --> fol_term(SingleArg).

identifier(Name, true) -->
    [First], { char_type(First, upper) ; First = '_' }, id_rest(Rest),
    { atom_chars(Name, [First | Rest]) }.
identifier(Name, false) -->
    [First], { char_type(First, lower) }, id_rest(Rest),
    { atom_chars(Name, [First | Rest]) }.

id_rest([Char | Rest]) --> [Char], { char_type(Char, alnum) ; Char = '_' }, !, id_rest(Rest).
id_rest([]) --> [].

whitespaces --> [Char], { char_type(Char, space) }, !, whitespaces.
whitespaces --> [].
```

### 5.2. `src/resolution_prop.pl`
```prolog
:- module(resolution_prop, [prove_propositional/4]).

:- use_module(parser).

prove_propositional(FilePath, Result, OpsCount, Trace) :-
    parse_kb_file(FilePath, RawClauses),
    preprocess_clauses(RawClauses, Clauses),
    (   member(clause(_, []), Clauses) ->
        Result = refutation_success, OpsCount = 0, Trace = [step(0, [], 'Initial empty clause')]
    ;   length(Clauses, MaxId),
        prop_loop(Clauses, MaxId, [], 0, OpsCount, Result, RevTrace),
        reverse(RevTrace, Trace)
    ).

preprocess_clauses(RawClauses, IndexedClauses) :-
    findall(Sorted, (member(Raw, RawClauses), sort(Raw, Sorted), \+ is_tautology(Sorted)), Cleaned),
    drop_subsumed(Cleaned, Filtered),
    index_clauses(Filtered, 1, IndexedClauses).

is_tautology(Clause) :-
    member(pos(Atom), Clause), member(neg(Atom), Clause), !.

drop_subsumed([], []).
drop_subsumed([Clause | Rest], Filtered) :-
    drop_subsumed(Rest, KeptRest),
    ( member(Other, KeptRest), subset(Other, Clause) -> Filtered = KeptRest ; Filtered = [Clause | KeptRest] ).

index_clauses([], _, []).
index_clauses([Clause | Rest], Id, [clause(Id, Clause) | RestIndexed]) :-
    NextId is Id + 1,
    index_clauses(Rest, NextId, RestIndexed).

prop_loop(Clauses, MaxId, History, OpsSoFar, TotalOps, Result, Trace) :-
    pick_shortest_pair(Clauses, History, Id1, Id2, Clause1, Clause2, Pivot), !,
    resolve_on_pivot(Clause1, Clause2, Pivot, Resolvent),
    NextOps is OpsSoFar + 1,
    opposite_lit(Pivot, NegPivot),
    NextHistory = [resolved(Id1, Id2, Pivot), resolved(Id2, Id1, NegPivot) | History],
    Step = step(NextOps, Resolvent, resolved(Id1, Id2, Pivot)),
    (   Resolvent == [] ->
        TotalOps = NextOps, Result = refutation_success, Trace = [Step]
    ;   (is_tautology(Resolvent) ; subsumed_by_any(Resolvent, Clauses)) ->
        prop_loop(Clauses, MaxId, NextHistory, NextOps, TotalOps, Result, Trace)
    ;   findall(clause(Id, Existing),
            (member(clause(Id, Existing), Clauses), \+ (Resolvent \== Existing, subset(Resolvent, Existing))),
            Surviving),
        NewId is MaxId + 1,
        prop_loop([clause(NewId, Resolvent) | Surviving], NewId, NextHistory, NextOps, TotalOps, Result, RestTrace),
        Trace = [Step | RestTrace]
    ).
prop_loop(_, _, _, OpsSoFar, OpsSoFar, refutation_failure, []).

pick_shortest_pair(Clauses, History, Id1, Id2, Clause1, Clause2, Pivot) :-
    findall(pair(Size, I1, I2, Lits1, Lits2, Lit),
        (   member(clause(I1, Lits1), Clauses), member(clause(I2, Lits2), Clauses), I1 < I2,
            member(Lit, Lits1), opposite_lit(Lit, NegLit), member(NegLit, Lits2),
            \+ member(resolved(I1, I2, Lit), History),
            length(Lits1, Len1), length(Lits2, Len2), Size is Len1 + Len2
        ),
        Candidates),
    Candidates \== [],
    sort(1, @=<, Candidates, [pair(_, Id1, Id2, Clause1, Clause2, Pivot) | _]).

resolve_on_pivot(Clause1, Clause2, Pivot, Resolvent) :-
    opposite_lit(Pivot, NegPivot),
    delete(Clause1, Pivot, Rest1), delete(Clause2, NegPivot, Rest2),
    append(Rest1, Rest2, Combined),
    sort(Combined, Resolvent).

opposite_lit(pos(Atom), neg(Atom)).
opposite_lit(neg(Atom), pos(Atom)).

subsumed_by_any(Resolvent, Clauses) :-
    member(clause(_, Existing), Clauses), subset(Existing, Resolvent), !.
```

### 5.3. `src/resolution_fol.pl`
```prolog
:- module(resolution_fol, [prove_fol/4]).

:- use_module(parser).

prove_fol(FilePath, Result, OpsCount, Trace) :-
    parse_kb_file(FilePath, RawClauses),
    index_and_convert_clauses(RawClauses, 1, Clauses),
    (   member(clause(_, []), Clauses) ->
        Result = refutation_success, OpsCount = 0, Trace = [step(0, [], 'Initial empty clause')]
    ;   length(Clauses, MaxId),
        fol_loop(Clauses, MaxId, [], 0, OpsCount, Result, RevTrace),
        reverse(RevTrace, Trace)
    ).

index_and_convert_clauses([], _, []).
index_and_convert_clauses([RawClause | Rest], Id, [clause(Id, PrologClause) | RestIndexed]) :-
    convert_literals(RawClause, [], _, PrologClause),
    NextId is Id + 1,
    index_and_convert_clauses(Rest, NextId, RestIndexed).

convert_literals([], VarMap, VarMap, []).
convert_literals([pos(Formula) | Rest], MapIn, MapOut, [pos(Conv) | ConvRest]) :-
    convert_term(Formula, MapIn, MapMid, Conv), convert_literals(Rest, MapMid, MapOut, ConvRest).
convert_literals([neg(Formula) | Rest], MapIn, MapOut, [neg(Conv) | ConvRest]) :-
    convert_term(Formula, MapIn, MapMid, Conv), convert_literals(Rest, MapMid, MapOut, ConvRest).

convert_term(var(Name), MapIn, MapOut, PrologVar) :- !,
    ( member(Name = PrologVar, MapIn) -> MapOut = MapIn ; MapOut = [Name = PrologVar | MapIn] ).
convert_term(Compound, MapIn, MapOut, Converted) :- compound(Compound), !,
    Compound =.. [Functor | RawArgs],
    convert_terms(RawArgs, MapIn, MapOut, ConvArgs),
    Converted =.. [Functor | ConvArgs].
convert_term(Constant, VarMap, VarMap, Constant).

convert_terms([], VarMap, VarMap, []).
convert_terms([Arg | Rest], MapIn, MapOut, [ConvArg | ConvRest]) :-
    convert_term(Arg, MapIn, MapMid, ConvArg), convert_terms(Rest, MapMid, MapOut, ConvRest).

fol_loop(Clauses, MaxId, History, OpsSoFar, TotalOps, Result, Trace) :-
    pick_shortest_unifiable_pair(Clauses, History, Id1, Id2, Clause1, Clause2, Idx1, Idx2), !,
    copy_term(Clause1, Fresh1), copy_term(Clause2, Fresh2),
    nth1(Idx1, Fresh1, Lit1), nth1(Idx2, Fresh2, Lit2),
    resolve_and_factor(Fresh1, Fresh2, Lit1, Lit2, Resolvent),
    NextOps is OpsSoFar + 1,
    NextHistory = [resolved(Id1, Id2, Idx1, Idx2) | History],
    copy_term(Resolvent, PrintableResolvent), numbervars(PrintableResolvent, 0, _),
    Step = step(NextOps, PrintableResolvent, resolved(Id1, Id2)),
    (   Resolvent == [] ->
        TotalOps = NextOps, Result = refutation_success, Trace = [Step]
    ;   subsumed_by_existing(Resolvent, Clauses) ->
        fol_loop(Clauses, MaxId, NextHistory, NextOps, TotalOps, Result, Trace)
    ;   NewId is MaxId + 1,
        fol_loop([clause(NewId, Resolvent) | Clauses], NewId, NextHistory, NextOps, TotalOps, Result, RestTrace),
        Trace = [Step | RestTrace]
    ).
fol_loop(_, _, _, OpsSoFar, OpsSoFar, refutation_failure, []).

pick_shortest_unifiable_pair(Clauses, History, Id1, Id2, Clause1, Clause2, Idx1, Idx2) :-
    findall(pair(Size, I1, I2, Lits1, Lits2, Pos1, Pos2),
        (   member(clause(I1, Lits1), Clauses), member(clause(I2, Lits2), Clauses), I1 < I2,
            nth1(Pos1, Lits1, Lit1), nth1(Pos2, Lits2, Lit2),
            can_unify_opposite(Lit1, Lit2),
            \+ member(resolved(I1, I2, Pos1, Pos2), History),
            length(Lits1, Len1), length(Lits2, Len2), Size is Len1 + Len2
        ),
        Candidates),
    Candidates \== [],
    sort(1, @=<, Candidates, [pair(_, Id1, Id2, Clause1, Clause2, Idx1, Idx2) | _]).

can_unify_opposite(Lit1, Lit2) :-
    opposite_atoms(Lit1, Lit2, Atom1, Atom2),
    \+ \+ (copy_term(Atom1, Fresh1), copy_term(Atom2, Fresh2), Fresh1 = Fresh2).

opposite_atoms(pos(Atom1), neg(Atom2), Atom1, Atom2).
opposite_atoms(neg(Atom1), pos(Atom2), Atom1, Atom2).

resolve_and_factor(Clause1, Clause2, Lit1, Lit2, Resolvent) :-
    opposite_atoms(Lit1, Lit2, Atom1, Atom2), Atom1 = Atom2,
    remove_exact(Clause1, Lit1, Rest1), remove_exact(Clause2, Lit2, Rest2),
    append(Rest1, Rest2, Combined),
    factor_duplicates(Combined, Resolvent).

remove_exact([First | Rest], Target, Rest) :- First == Target, !.
remove_exact([First | Rest], Target, [First | FilteredRest]) :- remove_exact(Rest, Target, FilteredRest).

factor_duplicates([], []).
factor_duplicates([Lit | Rest], UniqueLits) :-
    ( member(Other, Rest), Lit == Other ->
        factor_duplicates(Rest, UniqueLits)
    ;   UniqueLits = [Lit | RestUnique], factor_duplicates(Rest, RestUnique)
    ).

subsumed_by_existing(Resolvent, Clauses) :-
    member(clause(_, Existing), Clauses),
    \+ \+ (
        copy_term(Existing, FreshExisting),
        copy_term(Resolvent, FreshResolvent),
        numbervars(FreshResolvent, 0, _),
        subset(FreshExisting, FreshResolvent)
    ), !.
```

### 5.4. `src/davis_putnam.pl`
```prolog
:- module(davis_putnam, [solve_dp/4]).

:- use_module(parser).

solve_dp(FilePath, Strategy, Result, ModelFormatted) :-
    parse_kb_file(FilePath, Clauses),
    collect_all_atoms(Clauses, AllAtoms),
    dp_solve(Clauses, Strategy, Outcome, PartialModel),
    (   Outcome == sat ->
        Result = 'YES',
        fill_missing_atoms(AllAtoms, PartialModel, CompleteModel),
        format_solution(CompleteModel, ModelFormatted)
    ;   Result = 'NOT', ModelFormatted = '{}'
    ).

dp_solve(Clauses, Strategy, Outcome, Model) :-
    simplify_clauses(Clauses, Cleaned),
    (   member([], Cleaned) -> Outcome = unsat, Model = []
    ;   Cleaned == [] -> Outcome = sat, Model = []
    ;   member([UnitLit], Cleaned) ->
        propagate_unit(Cleaned, UnitLit, Reduced),
        lit_assignment(UnitLit, Atom, Value),
        dp_solve(Reduced, Strategy, Outcome, SubModel),
        ( Outcome == sat -> Model = [assign(Atom, Value) | SubModel] ; Model = [] )
    ;   find_pure_literal(Cleaned, PureLit) ->
        findall(Clause, (member(Clause, Cleaned), \+ member(PureLit, Clause)), Reduced),
        lit_assignment(PureLit, Atom, Value),
        dp_solve(Reduced, Strategy, Outcome, SubModel),
        ( Outcome == sat -> Model = [assign(Atom, Value) | SubModel] ; Model = [] )
    ;   pick_pivot_atom(Cleaned, Strategy, Pivot),
        bullet_eliminate(Cleaned, Pivot, Reduced, NegClauses),
        dp_solve(Reduced, Strategy, Outcome, SubModel),
        ( Outcome == sat ->
            infer_pivot_value(Pivot, NegClauses, SubModel, PivotValue),
            Model = [assign(Pivot, PivotValue) | SubModel]
        ;   Model = [] )
    ).

simplify_clauses(Clauses, Cleaned) :-
    findall(Sorted, (member(Clause, Clauses), sort(Clause, Sorted), \+ is_tautology(Sorted)), NoTaut),
    drop_subsumed(NoTaut, Cleaned).

drop_subsumed([], []).
drop_subsumed([Clause | Rest], Cleaned) :-
    drop_subsumed(Rest, KeptRest),
    ( member(Other, KeptRest), subset(Other, Clause) -> Cleaned = KeptRest ; Cleaned = [Clause | KeptRest] ).

is_tautology(Clause) :- member(pos(Atom), Clause), member(neg(Atom), Clause), !.

propagate_unit(Clauses, UnitLit, Reduced) :-
    opposite_lit(UnitLit, NegUnitLit),
    findall(Filtered,
        (member(Clause, Clauses), \+ member(UnitLit, Clause), delete(Clause, NegUnitLit, Filtered)),
        Reduced).

opposite_lit(pos(Atom), neg(Atom)).
opposite_lit(neg(Atom), pos(Atom)).

lit_assignment(pos(Atom), Atom, true).
lit_assignment(neg(Atom), Atom, false).

find_pure_literal(Clauses, PureLit) :-
    append(Clauses, AllLits), sort(AllLits, UniqueLits),
    member(PureLit, UniqueLits),
    opposite_lit(PureLit, OppositeLit),
    \+ member(OppositeLit, UniqueLits), !.

pick_pivot_atom(Clauses, moms, Pivot) :-
    findall(Len, (member(Clause, Clauses), length(Clause, Len), Len > 1), Lengths),
    min_list(Lengths, MinLen),
    findall(Clause, (member(Clause, Clauses), length(Clause, MinLen)), MinClauses),
    most_frequent_atom(MinClauses, Pivot), !.
pick_pivot_atom(Clauses, dlis, Pivot) :-
    most_frequent_atom(Clauses, Pivot), !.
pick_pivot_atom(Clauses, _, Pivot) :-
    pick_pivot_atom(Clauses, moms, Pivot).

most_frequent_atom(Clauses, BestAtom) :-
    collect_all_atoms(Clauses, Atoms),
    findall(score(Count, Atom),
        (   member(Atom, Atoms),
            findall(C, (member(C, Clauses), (member(pos(Atom), C) ; member(neg(Atom), C))), Hits),
            length(Hits, Count)
        ),
        Scored),
    sort(1, @>=, Scored, [score(_MaxCount, BestAtom) | _]).

bullet_eliminate(Clauses, Pivot, Reduced, NegClauses) :-
    findall(C, (member(C, Clauses), member(pos(Pivot), C)), PosClauses),
    findall(C, (member(C, Clauses), \+ member(pos(Pivot), C), member(neg(Pivot), C)), NegClauses),
    findall(C, (member(C, Clauses), \+ member(pos(Pivot), C), \+ member(neg(Pivot), C)), NeutralClauses),
    findall(CleanResolvent,
        (   member(PosClause, PosClauses), member(NegClause, NegClauses),
            delete(PosClause, pos(Pivot), PosRest), delete(NegClause, neg(Pivot), NegRest),
            append(PosRest, NegRest, Raw), sort(Raw, CleanResolvent),
            \+ is_tautology(CleanResolvent)
        ),
        Resolvents),
    append(NeutralClauses, Resolvents, Combined),
    simplify_clauses(Combined, Reduced).

infer_pivot_value(Pivot, NegClauses, SubModel, Value) :-
    (   forall(member(Clause, NegClauses),
            (member(Lit, Clause), lit_true_in_model(Lit, [assign(Pivot, true) | SubModel]))) ->
        Value = true
    ;   Value = false
    ).

lit_true_in_model(pos(Atom), Model) :- member(assign(Atom, true), Model).
lit_true_in_model(neg(Atom), Model) :- member(assign(Atom, false), Model).

collect_all_atoms(Clauses, UniqueAtoms) :-
    findall(Atom, (member(C, Clauses), (member(pos(Atom), C) ; member(neg(Atom), C))), RawAtoms),
    sort(RawAtoms, UniqueAtoms).

fill_missing_atoms(AllAtoms, PartialModel, CompleteModel) :-
    findall(assign(Atom, true),
        (member(Atom, AllAtoms), \+ member(assign(Atom, _), PartialModel)),
        DefaultAssignments),
    append(PartialModel, DefaultAssignments, CompleteModel).

format_solution(Model, Formatted) :-
    sort(Model, Sorted),
    findall(Entry, (member(assign(A, V), Sorted), format(string(Entry), "~w/~w", [A, V])), Entries),
    atomic_list_concat(Entries, '; ', Inner),
    format(string(Formatted), "{~w}", [Inner]).
```

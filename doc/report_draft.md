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
:- module(parser, [
    parse_kb_file/2,
    parse_kb_string/2,
    parse_cnf/2,
    parse_clause/2
]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_cnf(Str, Clauses) :-
    parse_kb_string(Str, Clauses).

parse_clause(Str, Lits) :-
    string_chars(Str, Chars),
    phrase((whitespaces, clause_expr(Lits), whitespaces), Chars).

parse_kb_file(File, Clauses) :-
    read_file_to_string(File, Str, [encoding(utf8)]),
    parse_kb_string(Str, Clauses).

parse_kb_string(Str, Clauses) :-
    string_chars(Str, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([C|Cs]) -->
    whitespaces,
    clause_expr(C),
    whitespaces,
    conj_op,
    !,
    cnf_formula(Cs).
cnf_formula([C]) -->
    whitespaces,
    clause_expr(C),
    whitespaces.
cnf_formula([]) -->
    whitespaces.

conj_op --> whitespaces, "and", whitespaces.
conj_op --> whitespaces, "^", whitespaces.
conj_op --> whitespaces, "&", whitespaces.
conj_op --> whitespaces, ";", whitespaces.
conj_op --> [C], { char_type(C, newline) }, whitespaces.

clause_expr(Lits) -->
    "(", whitespaces, disj_expr(Lits), whitespaces, ")".
clause_expr(Lits) -->
    "[", whitespaces, disj_expr(Lits), whitespaces, "]".
clause_expr(Lits) -->
    disj_expr(Lits).

disj_expr([L|Ls]) -->
    literal_expr(L),
    whitespaces,
    disj_op,
    !,
    disj_expr(Ls).
disj_expr([L]) -->
    literal_expr(L).

disj_op --> whitespaces, "or", whitespaces.
disj_op --> whitespaces, "v", whitespaces.
disj_op --> whitespaces, "|", whitespaces.
disj_op --> whitespaces, ",", whitespaces.

literal_expr(neg(Atom)) -->
    neg_prefix,
    whitespaces,
    atom_expr(Atom).
literal_expr(pos(Atom)) -->
    atom_expr(Atom).

neg_prefix --> "not", whitespaces.
neg_prefix --> ['\u00AC'].
neg_prefix --> "¬".
neg_prefix --> "~".
neg_prefix --> "-".

atom_expr(Term) -->
    fol_term(Term).

fol_term(Term) -->
    identifier(Name, false),
    whitespaces,
    "(", whitespaces, args_expr(Args), whitespaces, ")",
    !,
    { Term =.. [Name|Args] }.
fol_term(Term) -->
    identifier(Name, IsVar),
    { IsVar == true -> Term = var(Name) ; Term = Name }.

args_expr([A|As]) -->
    arg_expr(A),
    whitespaces,
    ",",
    whitespaces,
    !,
    args_expr(As).
args_expr([A]) -->
    arg_expr(A).

arg_expr(Term) -->
    fol_term(Term).

identifier(Name, true) -->
    upper_or_underscore(C),
    id_chars(Rest),
    { atom_chars(Name, [C|Rest]) }.
identifier(Name, false) -->
    lower_letter(C),
    id_chars(Rest),
    { atom_chars(Name, [C|Rest]) }.

upper_or_underscore(C) --> [C], { char_type(C, upper) ; C = '_' }.
lower_letter(C) --> [C], { char_type(C, lower) }.

id_chars([C|Cs]) -->
    [C],
    { char_type(C, alnum) ; C = '_' },
    !,
    id_chars(Cs).
id_chars([]) --> [].

whitespaces --> [C], { char_type(C, space) }, !, whitespaces.
whitespaces --> [].
```

### 5.2. `src/resolution_prop.pl`
```prolog
:- module(resolution_prop, [
    prove_propositional/4,
    prove_propositional/2
]).

:- use_module(parser).

prove_propositional(File, Result) :-
    prove_propositional(File, Result, _, _).

prove_propositional(Input, Result, OpsCount, Trace) :-
    (   is_list(Input) ->
        Clauses = Input
    ;   parse_kb_file(Input, Clauses)
    ),
    preprocess_clauses(Clauses, IndexedClauses),
    (   member(clause(_, []), IndexedClauses) ->
        Result = refutation_success,
        OpsCount = 0,
        Trace = [step(0, [], 'Initial empty clause')]
    ;   find_max_id(IndexedClauses, MaxId),
        resolution_loop(IndexedClauses, MaxId, [], 0, OpsCount, Result, RevTrace),
        reverse(RevTrace, Trace)
    ).

preprocess_clauses(Clauses, Indexed) :-
    clean_clauses(Clauses, Cleaned),
    eliminate_subsumed(Cleaned, Filtered),
    index_clauses(Filtered, 1, Indexed).

clean_clauses([], []).
clean_clauses([C|Cs], Rest) :-
    sort(C, Sorted),
    (   is_tautology(Sorted) ->
        clean_clauses(Cs, Rest)
    ;   Rest = [Sorted|Rest1],
        clean_clauses(Cs, Rest1)
    ).

is_tautology(Clause) :-
    member(pos(A), Clause),
    member(neg(A), Clause),
    !.

eliminate_subsumed([], []).
eliminate_subsumed([C|Cs], Result) :-
    (   member(Other, Cs), subset(Other, C) ->
        eliminate_subsumed(Cs, Result)
    ;   eliminate_subsumed(Cs, Rest),
        (   member(Other, Rest), subset(Other, C) ->
            Result = Rest
        ;   Result = [C|Rest]
        )
    ).

index_clauses([], _, []).
index_clauses([C|Cs], N, [clause(N, C)|Rest]) :-
    N1 is N + 1,
    index_clauses(Cs, N1, Rest).

find_max_id([], 0).
find_max_id([clause(Id, _)|Cs], Max) :-
    find_max_id(Cs, MaxRest),
    Max is max(Id, MaxRest).

resolution_loop(Clauses, MaxId, History, OpsSoFar, TotalOps, Result, Trace) :-
    select_pair(Clauses, History, Id1, Id2, C1, C2, Pivot),
    !,
    resolve_clauses(C1, C2, Pivot, Resolvent),
    NextOps is OpsSoFar + 1,
    NewHistory = [resolved(Id1, Id2, Pivot), resolved(Id2, Id1, NegPivot)|History],
    negated_literal(Pivot, NegPivot),
    Step = step(NextOps, Resolvent, resolved(Id1, Id2, Pivot)),
    (   Resolvent == [] ->
        TotalOps = NextOps,
        Result = refutation_success,
        Trace = [Step]
    ;   (   is_tautology(Resolvent)
        ;   clause_subsumed(Resolvent, Clauses)
        ) ->
        resolution_loop(Clauses, MaxId, NewHistory, NextOps, TotalOps, Result, Trace)
    ;   filter_subsumed_by(Resolvent, Clauses, SurvivingClauses),
        NewId is MaxId + 1,
        NewClause = clause(NewId, Resolvent),
        resolution_loop([NewClause|SurvivingClauses], NewId, NewHistory, NextOps, TotalOps, Result, RestTrace),
        Trace = [Step|RestTrace]
    ).
resolution_loop(_, _, _, OpsSoFar, OpsSoFar, refutation_failure, []).

select_pair(Clauses, History, Id1, Id2, C1, C2, Pivot) :-
    findall(pair(Size, I1, I2, Cl1, Cl2, P),
        (   member(clause(I1, Cl1), Clauses),
            member(clause(I2, Cl2), Clauses),
            I1 < I2,
            member(P, Cl1),
            negated_literal(P, NegP),
            member(NegP, Cl2),
            \+ member(resolved(I1, I2, P), History),
            length(Cl1, L1),
            length(Cl2, L2),
            Size is L1 + L2
        ),
        Pairs
    ),
    Pairs \== [],
    sort(1, @=<, Pairs, [pair(_, Id1, Id2, C1, C2, Pivot)|_]).

resolve_clauses(C1, C2, Pivot, Resolvent) :-
    negated_literal(Pivot, NegPivot),
    delete(C1, Pivot, Rest1),
    delete(C2, NegPivot, Rest2),
    append(Rest1, Rest2, Combined),
    sort(Combined, Resolvent).

negated_literal(pos(A), neg(A)).
negated_literal(neg(A), pos(A)).

clause_subsumed(R, Clauses) :-
    member(clause(_, C), Clauses),
    subset(C, R),
    !.

filter_subsumed_by(R, Clauses, Filtered) :-
    exclude(is_subsumed_by_r(R), Clauses, Filtered).

is_subsumed_by_r(R, clause(_, C)) :-
    R \== C,
    subset(R, C).
```

### 5.3. `src/resolution_fol.pl`
```prolog
:- module(resolution_fol, [
    prove_fol/4,
    prove_fol/2
]).

:- use_module(parser).

prove_fol(File, Result) :-
    prove_fol(File, Result, _, _).

prove_fol(Input, Result, OpsCount, Trace) :-
    (   is_list(Input) ->
        RawClauses = Input
    ;   parse_kb_file(Input, RawClauses)
    ),
    prepare_fol_clauses(RawClauses, Clauses),
    (   member(clause(_, []), Clauses) ->
        Result = refutation_success,
        OpsCount = 0,
        Trace = [step(0, [], 'Initial empty clause')]
    ;   find_max_fol_id(Clauses, MaxId),
        fol_loop(Clauses, MaxId, [], 0, OpsCount, Result, RevTrace),
        reverse(RevTrace, Trace)
    ).

prepare_fol_clauses(RawClauses, Indexed) :-
    index_fol(RawClauses, 1, Indexed).

index_fol([], _, []).
index_fol([C|Cs], N, [clause(N, Converted)|Rest]) :-
    clause_to_prolog_vars(C, Converted),
    N1 is N + 1,
    index_fol(Cs, N1, Rest).

clause_to_prolog_vars(Clause, Converted) :-
    vars_to_prolog(Clause, [], _, Converted).

vars_to_prolog([], Dict, Dict, []).
vars_to_prolog([L|Ls], Dict0, DictOut, [CL|CLs]) :-
    lit_to_prolog(L, Dict0, Dict1, CL),
    vars_to_prolog(Ls, Dict1, DictOut, CLs).

lit_to_prolog(pos(Atom), Dict0, DictOut, pos(CAtom)) :-
    term_to_prolog(Atom, Dict0, DictOut, CAtom).
lit_to_prolog(neg(Atom), Dict0, DictOut, neg(CAtom)) :-
    term_to_prolog(Atom, Dict0, DictOut, CAtom).

term_to_prolog(var(Name), Dict0, DictOut, Var) :-
    !,
    (   member(Name=Var, Dict0) ->
        DictOut = Dict0
    ;   DictOut = [Name=Var|Dict0]
    ).
term_to_prolog(Term, Dict0, DictOut, Converted) :-
    compound(Term),
    !,
    Term =.. [F|Args],
    args_to_prolog(Args, Dict0, DictOut, CArgs),
    Converted =.. [F|CArgs].
term_to_prolog(Atom, Dict, Dict, Atom).

args_to_prolog([], Dict, Dict, []).
args_to_prolog([A|As], Dict0, DictOut, [CA|CAs]) :-
    term_to_prolog(A, Dict0, Dict1, CA),
    args_to_prolog(As, Dict1, DictOut, CAs).

find_max_fol_id([], 0).
find_max_fol_id([clause(Id, _)|Cs], Max) :-
    find_max_fol_id(Cs, MaxRest),
    Max is max(Id, MaxRest).

fol_loop(Clauses, MaxId, History, OpsSoFar, TotalOps, Result, Trace) :-
    select_fol_pair(Clauses, History, Id1, Id2, C1, C2, Index1, Index2),
    !,
    copy_term(C1, FreshC1),
    copy_term(C2, FreshC2),
    nth1(Index1, FreshC1, L1),
    nth1(Index2, FreshC2, L2),
    resolve_fol(FreshC1, FreshC2, L1, L2, Resolvent),
    NextOps is OpsSoFar + 1,
    NewHistory = [resolved(Id1, Id2, Index1, Index2)|History],
    copy_term(Resolvent, PrintableResolvent),
    numbervars(PrintableResolvent, 0, _),
    Step = step(NextOps, PrintableResolvent, resolved(Id1, Id2)),
    (   Resolvent == [] ->
        TotalOps = NextOps,
        Result = refutation_success,
        Trace = [Step]
    ;   fol_clause_exists(Resolvent, Clauses) ->
        fol_loop(Clauses, MaxId, NewHistory, NextOps, TotalOps, Result, Trace)
    ;   NewId is MaxId + 1,
        NewClause = clause(NewId, Resolvent),
        fol_loop([NewClause|Clauses], NewId, NewHistory, NextOps, TotalOps, Result, RestTrace),
        Trace = [Step|RestTrace]
    ).
fol_loop(_, _, _, OpsSoFar, OpsSoFar, refutation_failure, []).

select_fol_pair(Clauses, History, Id1, Id2, C1, C2, Index1, Index2) :-
    findall(cand(Size, I1, I2, Cl1, Cl2, Idx1, Idx2),
        (   member(clause(I1, Cl1), Clauses),
            member(clause(I2, Cl2), Clauses),
            I1 < I2,
            nth1(Idx1, Cl1, Lit1),
            nth1(Idx2, Cl2, Lit2),
            opposite_signs(Lit1, Lit2),
            unifiable_lits(Lit1, Lit2),
            \+ member(resolved(I1, I2, Idx1, Idx2), History),
            length(Cl1, Len1),
            length(Cl2, Len2),
            Size is Len1 + Len2
        ),
        Candidates
    ),
    Candidates \== [],
    sort(1, @=<, Candidates, [cand(_, Id1, Id2, C1, C2, Index1, Index2)|_]).

opposite_signs(pos(_), neg(_)).
opposite_signs(neg(_), pos(_)).

unifiable_lits(pos(A1), neg(A2)) :-
    unify_terms(A1, A2).
unifiable_lits(neg(A1), pos(A2)) :-
    unify_terms(A1, A2).

unify_terms(T1, T2) :-
    \+ \+ (copy_term(T1, CT1), copy_term(T2, CT2), CT1 = CT2).

resolve_fol(C1, C2, L1, L2, Resolvent) :-
    (   L1 = pos(A1), L2 = neg(A2)
    ;   L1 = neg(A1), L2 = pos(A2)
    ),
    A1 = A2,
    delete_literal(C1, L1, Rest1),
    delete_literal(C2, L2, Rest2),
    append(Rest1, Rest2, Combined),
    factor_clause(Combined, Resolvent).

delete_literal([X|Xs], Y, Xs) :-
    X == Y,
    !.
delete_literal([X|Xs], Y, [X|Rest]) :-
    delete_literal(Xs, Y, Rest).

factor_clause([], []).
factor_clause([L|Ls], Result) :-
    (   member(M, Ls), L == M ->
        factor_clause(Ls, Result)
    ;   Result = [L|Rest],
        factor_clause(Ls, Rest)
    ).

fol_clause_exists(R, Clauses) :-
    member(clause(_, C), Clauses),
    subsumes_clause(C, R),
    !.

subsumes_clause(C1, C2) :-
    \+ \+ (
        copy_term(C1, FreshC1),
        copy_term(C2, FreshC2),
        numbervars(FreshC2, 0, _),
        subset(FreshC1, FreshC2)
    ).
```

### 5.4. `src/davis_putnam.pl`
```prolog
:- module(davis_putnam, [
    solve_dp/4,
    solve_dp/3,
    solve_dp/2,
    format_solution/2
]).

:- use_module(parser).

solve_dp(Input, Strategy, Result, ModelFormatted) :-
    (   is_list(Input) ->
        Clauses = Input
    ;   parse_kb_file(Input, Clauses)
    ),
    extract_all_atoms(Clauses, AllAtoms),
    dp_loop(Clauses, Strategy, Outcome, RawModel),
    (   Outcome == sat ->
        Result = 'YES',
        fill_missing_atoms(AllAtoms, RawModel, CompleteModel),
        format_solution(CompleteModel, ModelFormatted)
    ;   Result = 'NOT',
        ModelFormatted = '{}'
    ).

solve_dp(Input, Strategy, Result) :-
    solve_dp(Input, Strategy, Result, _).

solve_dp(Input, Result) :-
    solve_dp(Input, moms, Result, _).

dp_loop(Clauses, Strategy, Outcome, Model) :-
    clean_dp_clauses(Clauses, Cleaned),
    (   member([], Cleaned) ->
        Outcome = unsat,
        Model = []
    ;   Cleaned == [] ->
        Outcome = sat,
        Model = []
    ;   find_unit_clause(Cleaned, UnitLit) ->
        apply_unit_literal(Cleaned, UnitLit, NextClauses),
        unit_to_assignment(UnitLit, Atom, Val),
        dp_loop(NextClauses, Strategy, Outcome, SubModel),
        (   Outcome == sat ->
            Model = [assign(Atom, Val)|SubModel]
        ;   Model = []
        )
    ;   find_pure_literal(Cleaned, PureLit) ->
        apply_pure_literal(Cleaned, PureLit, NextClauses),
        unit_to_assignment(PureLit, Atom, Val),
        dp_loop(NextClauses, Strategy, Outcome, SubModel),
        (   Outcome == sat ->
            Model = [assign(Atom, Val)|SubModel]
        ;   Model = []
        )
    ;   select_atom(Cleaned, Strategy, PivotAtom),
        bullet_operation(Cleaned, PivotAtom, NextClauses, PosClauses, NegClauses),
        dp_loop(NextClauses, Strategy, Outcome, SubModel),
        (   Outcome == sat ->
            reconstruct_atom_value(PivotAtom, PosClauses, NegClauses, SubModel, PivotVal),
            Model = [assign(PivotAtom, PivotVal)|SubModel]
        ;   Model = []
        )
    ).

clean_dp_clauses([], []).
clean_dp_clauses([C|Cs], Result) :-
    sort(C, Sorted),
    (   is_tautology_dp(Sorted) ->
        clean_dp_clauses(Cs, Result)
    ;   clean_dp_clauses(Cs, Rest),
        (   member(Other, Rest), subset(Other, Sorted) ->
            Result = Rest
        ;   Result = [Sorted|Rest]
        )
    ).

is_tautology_dp(Clause) :-
    member(pos(A), Clause),
    member(neg(A), Clause),
    !.

find_unit_clause(Clauses, Lit) :-
    member([Lit], Clauses),
    !.

apply_unit_literal(Clauses, UnitLit, Result) :-
    opposite_lit(UnitLit, NegUnitLit),
    apply_unit_each(Clauses, UnitLit, NegUnitLit, Result).

apply_unit_each([], _, _, []).
apply_unit_each([C|Cs], UnitLit, NegUnitLit, Rest) :-
    (   member(UnitLit, C) ->
        apply_unit_each(Cs, UnitLit, NegUnitLit, Rest)
    ;   delete(C, NegUnitLit, Filtered),
        Rest = [Filtered|Rest1],
        apply_unit_each(Cs, UnitLit, NegUnitLit, Rest1)
    ).

opposite_lit(pos(A), neg(A)).
opposite_lit(neg(A), pos(A)).

unit_to_assignment(pos(A), A, true).
unit_to_assignment(neg(A), A, false).

find_pure_literal(Clauses, Lit) :-
    extract_all_literals(Clauses, Lits),
    sort(Lits, UniqueLits),
    member(Lit, UniqueLits),
    opposite_lit(Lit, NegLit),
    \+ member(NegLit, UniqueLits),
    !.

extract_all_literals([], []).
extract_all_literals([C|Cs], All) :-
    extract_all_literals(Cs, Rest),
    append(C, Rest, All).

apply_pure_literal(Clauses, PureLit, Result) :-
    exclude(contains_lit(PureLit), Clauses, Result).

contains_lit(Lit, Clause) :-
    member(Lit, Clause).

select_atom(Clauses, moms, SelectedAtom) :-
    findall(Len, (member(C, Clauses), length(C, Len), Len > 1), Lens),
    min_list(Lens, MinLen),
    findall(C, (member(C, Clauses), length(C, MinLen)), MinClauses),
    extract_all_atoms(MinClauses, Atoms),
    sort(Atoms, UniqueAtoms),
    map_atom_scores(UniqueAtoms, MinClauses, Scored),
    sort(1, @>=, Scored, [score(_, SelectedAtom)|_]),
    !.
select_atom(Clauses, dlis, SelectedAtom) :-
    extract_all_atoms(Clauses, Atoms),
    sort(Atoms, UniqueAtoms),
    map_atom_scores(UniqueAtoms, Clauses, Scored),
    sort(1, @>=, Scored, [score(_, SelectedAtom)|_]),
    !.
select_atom(Clauses, _, SelectedAtom) :-
    select_atom(Clauses, moms, SelectedAtom).

map_atom_scores([], _, []).
map_atom_scores([A|As], Clauses, [score(Count, A)|Rest]) :-
    count_atom_occurrences(Clauses, A, Count),
    map_atom_scores(As, Clauses, Rest).

count_atom_occurrences([], _, 0).
count_atom_occurrences([C|Cs], A, Total) :-
    count_atom_occurrences(Cs, A, RestCount),
    (   (member(pos(A), C) ; member(neg(A), C)) ->
        Total is RestCount + 1
    ;   Total = RestCount
    ).

bullet_operation(Clauses, Atom, ResultClauses, PosClauses, NegClauses) :-
    partition(has_pos_atom(Atom), Clauses, PosClauses, NonPos),
    partition(has_neg_atom(Atom), NonPos, NegClauses, S0),
    resolve_bullet(PosClauses, NegClauses, Atom, Resolvents),
    append(S0, Resolvents, Combined),
    clean_dp_clauses(Combined, ResultClauses).

has_pos_atom(A, C) :- member(pos(A), C).
has_neg_atom(A, C) :- member(neg(A), C).

resolve_bullet([], _, _, []).
resolve_bullet([P|Ps], Negs, Atom, Resolvents) :-
    resolve_bullet_one(P, Negs, Atom, Res1),
    resolve_bullet(Ps, Negs, Atom, ResRest),
    append(Res1, ResRest, Resolvents).

resolve_bullet_one(_, [], _, []).
resolve_bullet_one(P, [N|Ns], Atom, Result) :-
    delete(P, pos(Atom), RestP),
    delete(N, neg(Atom), RestN),
    append(RestP, RestN, Resolvent),
    sort(Resolvent, CleanResolvent),
    (   is_tautology_dp(CleanResolvent) ->
        resolve_bullet_one(P, Ns, Atom, Result)
    ;   Result = [CleanResolvent|RestRes],
        resolve_bullet_one(P, Ns, Atom, RestRes)
    ).

reconstruct_atom_value(Atom, _, NegClauses, SubModel, Value) :-
    (   clauses_satisfied(NegClauses, [assign(Atom, true)|SubModel]) ->
        Value = true
    ;   Value = false
    ).

clauses_satisfied([], _).
clauses_satisfied([C|Cs], Model) :-
    clause_satisfied(C, Model),
    clauses_satisfied(Cs, Model).

clause_satisfied(Clause, Model) :-
    member(Lit, Clause),
    literal_true_in_model(Lit, Model),
    !.

literal_true_in_model(pos(A), Model) :-
    member(assign(A, true), Model).
literal_true_in_model(neg(A), Model) :-
    member(assign(A, false), Model).

extract_all_atoms([], []).
extract_all_atoms([C|Cs], Atoms) :-
    extract_all_atoms(Cs, Rest),
    clause_atoms(C, CAtoms),
    append(CAtoms, Rest, Atoms).

clause_atoms([], []).
clause_atoms([pos(A)|Ls], [A|Rest]) :- clause_atoms(Ls, Rest).
clause_atoms([neg(A)|Ls], [A|Rest]) :- clause_atoms(Ls, Rest).

fill_missing_atoms([], Model, Model).
fill_missing_atoms([A|As], Model0, ModelOut) :-
    (   member(assign(A, _), Model0) ->
        fill_missing_atoms(As, Model0, ModelOut)
    ;   fill_missing_atoms(As, [assign(A, true)|Model0], ModelOut)
    ).

format_solution(Model, Formatted) :-
    sort(Model, Sorted),
    findall(Entry,
        (   member(assign(A, Val), Sorted),
            format(string(Entry), "~w/~w", [A, Val])
        ),
        Entries
    ),
    atomic_list_concat(Entries, '; ', Inner),
    format(string(Formatted), "{~w}", [Inner]).
```

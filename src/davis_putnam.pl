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

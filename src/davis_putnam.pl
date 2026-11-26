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
    ;   (member([Lit], Cleaned) ; find_pure_literal(Cleaned, Lit)) ->
        propagate_unit(Cleaned, Lit, Reduced),
        lit_assignment(Lit, Atom, Value),
        Model = [assign(Atom, Value) | SubModel],
        dp_solve(Reduced, Strategy, Outcome, SubModel)
    ;   pick_pivot_atom(Cleaned, Strategy, Pivot),
        bullet_eliminate(Cleaned, Pivot, Reduced, NegClauses),
        dp_solve(Reduced, Strategy, Outcome, SubModel),
        ( Outcome == sat ->
            collect_all_atoms(Cleaned, CleanedAtoms),
            subtract(CleanedAtoms, [Pivot], OtherAtoms),
            fill_missing_atoms(OtherAtoms, SubModel, ExtSubModel),
            infer_pivot_value(NegClauses, ExtSubModel, PivotValue),
            Model = [assign(Pivot, PivotValue) | ExtSubModel]
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
    findall(Len, (member(Clause, Clauses), length(Clause, Len)), Lengths),
    min_list(Lengths, MinLen),
    findall(Clause, (member(Clause, Clauses), length(Clause, MinLen)), MinClauses),
    most_frequent_atom(MinClauses, Pivot), !.
pick_pivot_atom(Clauses, dlis, Pivot) :-
    most_frequent_atom(Clauses, Pivot), !.

most_frequent_atom(Clauses, BestAtom) :-
    collect_all_atoms(Clauses, Atoms),
    findall(score(Count, Atom),
        (   member(Atom, Atoms),
            findall(C, (member(C, Clauses), (member(pos(Atom), C) ; member(neg(Atom), C))), Hits),
            length(Hits, Count)
        ),
        Scored),
    sort(1, @>=, Scored, [score(_MaxCount, BestAtom) | _]).

bullet_eliminate(Clauses, Pivot, Combined, NegClauses) :-
    findall(C, (member(C, Clauses), member(pos(Pivot), C)), PosClauses),
    findall(C, (member(C, Clauses), member(neg(Pivot), C)), NegClauses),
    findall(C, (member(C, Clauses), \+ member(pos(Pivot), C), \+ member(neg(Pivot), C)), NeutralClauses),
    findall(Raw,
        (   member(PosClause, PosClauses), member(NegClause, NegClauses),
            delete(PosClause, pos(Pivot), PosRest), delete(NegClause, neg(Pivot), NegRest),
            append(PosRest, NegRest, Raw)
        ),
        Resolvents),
    append(NeutralClauses, Resolvents, Combined).

infer_pivot_value(NegClauses, SubModel, Value) :-
    (   forall(member(Clause, NegClauses),
            (member(Lit, Clause), lit_assignment(Lit, A, V), member(assign(A, V), SubModel))) ->
        Value = true
    ;   Value = false
    ).

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

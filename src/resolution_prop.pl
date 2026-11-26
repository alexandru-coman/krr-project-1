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

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

:- module(resolution_fol, [prove_fol/4]).

:- use_module(parser).

prove_fol(FilePath, Result, OpsCount, Trace) :-
    parse_kb_file(FilePath, RawClauses),
    index_and_convert_clauses(RawClauses, 1, Clauses),
    (   member(clause(_, []), Clauses) ->
        Result = refutation_success, OpsCount = 0, Trace = [step(0, [], 'Initial empty clause')]
    ;   length(Clauses, MaxId),
        fol_loop(Clauses, MaxId, [], 0, OpsCount, Result, Trace)
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
    pick_next_step(Clauses, History, Action), !,
    apply_step(Action, Resolvent, StepTag),
    NextOps is OpsSoFar + 1,
    step_history_entry(Action, HistEntry),
    NextHistory = [HistEntry | History],
    copy_term(Resolvent, PrintableResolvent), numbervars(PrintableResolvent, 0, _),
    Step = step(NextOps, PrintableResolvent, StepTag),
    (   Resolvent == [] ->
        TotalOps = NextOps, Result = refutation_success, Trace = [Step]
    ;   (fol_is_tautology(Resolvent) ; subsumed_by_existing(Resolvent, Clauses)) ->
        fol_loop(Clauses, MaxId, NextHistory, NextOps, TotalOps, Result, Trace)
    ;   NewId is MaxId + 1,
        fol_loop([clause(NewId, Resolvent) | Clauses], NewId, NextHistory, NextOps, TotalOps, Result, RestTrace),
        Trace = [Step | RestTrace]
    ).
fol_loop(_, _, _, OpsSoFar, OpsSoFar, refutation_failure, []).

pick_next_step(Clauses, History, Action) :-
    findall(cand(Size, 1, resolve(I1, I2, Lits1, Lits2, Pos1, Pos2)),
        (   member(clause(I1, Lits1), Clauses), member(clause(I2, Lits2), Clauses), I1 < I2,
            nth1(Pos1, Lits1, Lit1), nth1(Pos2, Lits2, Lit2),
            can_unify(opposite, Lit1, Lit2),
            \+ member(resolved(I1, I2, Pos1, Pos2), History),
            length(Lits1, Len1), length(Lits2, Len2), Size is Len1 + Len2
        ),
        ResCands),
    findall(cand(Size, 2, factor(Id, Lits, Pos1, Pos2)),
        (   member(clause(Id, Lits), Clauses),
            nth1(Pos1, Lits, Lit1), nth1(Pos2, Lits, Lit2), Pos1 < Pos2,
            can_unify(same, Lit1, Lit2),
            \+ member(factored(Id, Pos1, Pos2), History),
            length(Lits, Len), Size is Len * 2
        ),
        FacCands),
    append(ResCands, FacCands, AllCands),
    AllCands \== [],
    sort(0, @=<, AllCands, [cand(_, _, Action) | _]).

apply_step(resolve(Id1, Id2, Clause1, Clause2, Idx1, Idx2), Resolvent, resolved(Id1, Id2)) :-
    copy_term(Clause1, Fresh1), copy_term(Clause2, Fresh2),
    nth1(Idx1, Fresh1, Lit1), nth1(Idx2, Fresh2, Lit2),
    pair_atoms(opposite, Lit1, Lit2, Atom1, Atom2),
    unify_with_occurs_check(Atom1, Atom2),
    remove_nth1(Idx1, Fresh1, Rest1), remove_nth1(Idx2, Fresh2, Rest2),
    append(Rest1, Rest2, Combined),
    factor_duplicates(Combined, Resolvent).
apply_step(factor(Id, Clause, Idx1, Idx2), Factored, factored(Id)) :-
    copy_term(Clause, Fresh),
    nth1(Idx1, Fresh, Lit1), nth1(Idx2, Fresh, Lit2),
    pair_atoms(same, Lit1, Lit2, Atom1, Atom2),
    unify_with_occurs_check(Atom1, Atom2),
    remove_nth1(Idx2, Fresh, Stripped),
    factor_duplicates(Stripped, Factored).

step_history_entry(resolve(I1, I2, _, _, P1, P2), resolved(I1, I2, P1, P2)).
step_history_entry(factor(Id, _, P1, P2), factored(Id, P1, P2)).

can_unify(Mode, Lit1, Lit2) :-
    pair_atoms(Mode, Lit1, Lit2, Atom1, Atom2),
    \+ \+ unify_with_occurs_check(Atom1, Atom2).

pair_atoms(opposite, pos(Atom1), neg(Atom2), Atom1, Atom2).
pair_atoms(opposite, neg(Atom1), pos(Atom2), Atom1, Atom2).
pair_atoms(same, pos(Atom1), pos(Atom2), Atom1, Atom2).
pair_atoms(same, neg(Atom1), neg(Atom2), Atom1, Atom2).

remove_nth1(1, [_ | Rest], Rest) :- !.
remove_nth1(N, [First | Rest], [First | FilteredRest]) :-
    N > 1, Next is N - 1, remove_nth1(Next, Rest, FilteredRest).

factor_duplicates([], []).
factor_duplicates([Lit | Rest], UniqueLits) :-
    ( member(Other, Rest), Lit == Other ->
        factor_duplicates(Rest, UniqueLits)
    ;   UniqueLits = [Lit | RestUnique], factor_duplicates(Rest, RestUnique)
    ).

fol_is_tautology(Clause) :-
    member(pos(A), Clause), member(neg(B), Clause), A == B, !.

subsumed_by_existing(Resolvent, Clauses) :-
    length(Resolvent, LenR),
    member(clause(_, Existing), Clauses),
    length(Existing, LenE), LenE =< LenR,
    \+ \+ (
        copy_term(Existing, FreshExisting),
        copy_term(Resolvent, FreshResolvent),
        numbervars(FreshResolvent, 0, _),
        subsumes_lits(FreshExisting, FreshResolvent)
    ), !.

subsumes_lits([], _).
subsumes_lits([Lit | Rest], Target) :-
    member(Other, Target),
    unify_with_occurs_check(Lit, Other),
    subsumes_lits(Rest, Target).

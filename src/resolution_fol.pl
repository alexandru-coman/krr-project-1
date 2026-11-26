:- module(resolution_fol, [prove_fol/4]).

:- use_module(parser).

prove_fol(FilePath, Result, OpsCount, Trace) :-
    parse_kb_file(FilePath, RawClauses),
    index_and_convert_clauses(RawClauses, 1, Clauses),
    length(Clauses, MaxId),
    fol_loop(Clauses, MaxId, [], 0, OpsCount, Result, Trace).

index_and_convert_clauses([], _, []).
index_and_convert_clauses([RawClause | Rest], Id, [clause(Id, PrologClause) | RestIndexed]) :-
    convert_terms(RawClause, [], _, PrologClause),
    NextId is Id + 1,
    index_and_convert_clauses(Rest, NextId, RestIndexed).

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
    nth1(Idx1, Fresh1, Lit1, Rest1), nth1(Idx2, Fresh2, Lit2, Rest2),
    resolve_and_factor(Rest1, Rest2, Lit1, Lit2, Resolvent),
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
            opposite_atoms(Lit1, Lit2, Atom1, Atom2),
            \+ \+ unify_with_occurs_check(Atom1, Atom2),
            \+ member(resolved(I1, I2, Pos1, Pos2), History),
            length(Lits1, Len1), length(Lits2, Len2), Size is Len1 + Len2
        ),
        Candidates),
    Candidates \== [],
    sort(0, @=<, Candidates, [pair(_, Id1, Id2, Clause1, Clause2, Idx1, Idx2) | _]).

opposite_atoms(pos(Atom1), neg(Atom2), Atom1, Atom2).
opposite_atoms(neg(Atom1), pos(Atom2), Atom1, Atom2).

resolve_and_factor(Rest1, Rest2, Lit1, Lit2, Resolvent) :-
    opposite_atoms(Lit1, Lit2, Atom1, Atom2),
    unify_with_occurs_check(Atom1, Atom2),
    append(Rest1, Rest2, Combined),
    sort(Combined, Resolvent).

subsumed_by_existing(Resolvent, Clauses) :-
    member(clause(_, Existing), Clauses),
    \+ \+ (numbervars(Resolvent, 0, _), subset(Existing, Resolvent)), !.

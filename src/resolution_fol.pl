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

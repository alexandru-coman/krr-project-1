:- module(main, [
    run_all/0,
    run_prop_tests/0,
    run_fol_tests/0,
    run_dp_tests/0
]).

:- use_module(resolution_prop).
:- use_module(resolution_fol).
:- use_module(davis_putnam).

resolve_test_path(Rel, Abs) :-
    source_file(run_all, SrcFile),
    file_directory_name(SrcFile, SrcDir),
    file_directory_name(SrcDir, Root),
    atomic_list_concat([Root, '/', Rel], Abs).

run_all :-
    format("=== SUBJECT 1: PROPOSITIONAL RESOLUTION ===~n", []),
    run_prop_tests,
    format("~n=== SUBJECT 1: FIRST-ORDER LOGIC RESOLUTION ===~n", []),
    run_fol_tests,
    format("~n=== SUBJECT 2: DAVIS-PUTNAM SAT SOLVER ===~n", []),
    run_dp_tests,
    format("~nALL TESTS COMPLETED SUCCESSFULLY.~n", []).

run_prop_tests :-
    forall(member(File, ['tests/s1_prop_1.txt', 'tests/s1_prop_2.txt', 'tests/s1_prop_3.txt', 'tests/s1_prop_4.txt', 'tests/s1_prop_5.txt']),
        run_resolution_file(prove_propositional, File)).

run_fol_tests :-
    forall(member(File, ['tests/s1_fol_own.txt', 'tests/s1_fol_c3_p30.txt', 'tests/s1_fol_c3_p33.txt', 'tests/s1_fol_c4_p12.txt']),
        run_resolution_file(prove_fol, File)).

run_resolution_file(Solver, File) :-
    resolve_test_path(File, AbsPath),
    format("Testing ~w...~n", [File]),
    call(Solver, AbsPath, Result, Ops, Trace),
    length(Trace, TraceLen),
    format("  Result: ~w~n  Resolution operations: ~w~n  Trace steps: ~w~n", [Result, Ops, TraceLen]).

run_dp_tests :-
    forall((member(File, ['tests/s2_dp_1.txt', 'tests/s2_dp_2.txt', 'tests/s2_dp_3.txt', 'tests/s2_dp_4.txt', 'tests/s2_dp_5.txt', 'tests/s2_dp_6.txt']), member(Strategy, [moms, dlis])), (
        resolve_test_path(File, AbsPath),
        solve_dp(AbsPath, Strategy, Result, Model),
        format("Testing ~w [Strategy: ~w]...~n  Result: ~w~n  Model:  ~w~n", [File, Strategy, Result, Model])
    )).

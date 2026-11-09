:- module(main, [
    run_all/0,
    run_prop_tests/0,
    run_fol_tests/0,
    run_dp_tests/0,
    run_prop_file/1,
    run_fol_file/1,
    run_dp_file/2
]).

:- use_module(resolution_prop).
:- use_module(resolution_fol).
:- use_module(davis_putnam).

project_root(Root) :-
    source_file(run_all, SrcFile),
    file_directory_name(SrcFile, SrcDir),
    file_directory_name(SrcDir, Root).

resolve_test_path(Rel, Abs) :-
    project_root(Root),
    atomic_list_concat([Root, '/', Rel], Abs).

run_all :-
    writeln('========================================'),
    writeln(' SUBJECT 1: PROPOSITIONAL RESOLUTION   '),
    writeln('========================================'),
    run_prop_tests,
    nl,
    writeln('========================================'),
    writeln(' SUBJECT 1: FIRST-ORDER LOGIC RESOLUTION'),
    writeln('========================================'),
    run_fol_tests,
    nl,
    writeln('========================================'),
    writeln(' SUBJECT 2: DAVIS-PUTNAM SAT SOLVER    '),
    writeln('========================================'),
    run_dp_tests,
    nl,
    writeln('ALL TESTS COMPLETED SUCCESSFULLY.').

run_prop_tests :-
    PropTests = [
        'tests/s1_prop_1.txt',
        'tests/s1_prop_2.txt',
        'tests/s1_prop_3.txt',
        'tests/s1_prop_4.txt',
        'tests/s1_prop_5.txt'
    ],
    maplist(run_prop_file, PropTests).

run_prop_file(File) :-
    resolve_test_path(File, AbsPath),
    format("Testing ~w...~n", [File]),
    prove_propositional(AbsPath, Result, Ops, Trace),
    format("  Result: ~w~n", [Result]),
    format("  Resolution operations: ~w~n", [Ops]),
    length(Trace, TraceLen),
    format("  Trace steps: ~w~n", [TraceLen]).

run_fol_tests :-
    FolTests = [
        'tests/s1_fol_own.txt',
        'tests/s1_fol_c3_p30.txt',
        'tests/s1_fol_c3_p33.txt',
        'tests/s1_fol_c4_p12.txt'
    ],
    maplist(run_fol_file, FolTests).

run_fol_file(File) :-
    resolve_test_path(File, AbsPath),
    format("Testing ~w...~n", [File]),
    prove_fol(AbsPath, Result, Ops, Trace),
    format("  Result: ~w~n", [Result]),
    format("  Resolution operations: ~w~n", [Ops]),
    length(Trace, TraceLen),
    format("  Trace steps: ~w~n", [TraceLen]).

run_dp_tests :-
    DpTests = [
        'tests/s2_dp_1.txt',
        'tests/s2_dp_2.txt',
        'tests/s2_dp_3.txt',
        'tests/s2_dp_4.txt',
        'tests/s2_dp_5.txt',
        'tests/s2_dp_6.txt'
    ],
    forall(member(F, DpTests),
        (   run_dp_file(F, moms),
            run_dp_file(F, dlis)
        )
    ).

run_dp_file(File, Strategy) :-
    resolve_test_path(File, AbsPath),
    format("Testing ~w [Strategy: ~w]...~n", [File, Strategy]),
    solve_dp(AbsPath, Strategy, Result, Model),
    format("  Result: ~w~n", [Result]),
    format("  Model:  ~w~n", [Model]).

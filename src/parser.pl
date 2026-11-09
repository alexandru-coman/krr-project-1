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

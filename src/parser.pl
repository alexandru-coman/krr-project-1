:- module(parser, [parse_kb_file/2]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_kb_file(FilePath, Clauses) :-
    read_file_to_string(FilePath, Text, [encoding(utf8)]),
    string_chars(Text, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([]) --> spaces, eos, !.
cnf_formula(Clauses) --> spaces, cnf_clauses(Clauses), spaces.

cnf_clauses([First | Rest]) -->
    clause_expr(First), spaces, "and", spaces, !,
    cnf_clauses(Rest).
cnf_clauses([Last]) -->
    clause_expr(Last).

clause_expr([]) --> "[]", !.
clause_expr([First, Second | Rest]) -->
    "(", !, spaces, literal(First), spaces, "or", spaces,
    disjunction_tail(Second, Rest), spaces, ")".
clause_expr([Single]) -->
    literal(Single).

disjunction_tail(First, [Next | Rest]) -->
    literal(First), spaces, "or", spaces, !,
    disjunction_tail(Next, Rest).
disjunction_tail(Last, []) -->
    literal(Last).

literal(neg(Atom)) --> "not", space1, fol_term(Atom), !.
literal(pos(Atom)) --> fol_term(Atom).

fol_term(Term) -->
    ident(Functor, false), "(", spaces, args(Args), spaces, ")", !,
    { Term =.. [Functor | Args] }.
fol_term(Term) -->
    ident(Name, IsVar),
    { IsVar == true -> Term = var(Name) ; Term = Name }.

args([First | Rest]) -->
    fol_term(First), spaces, ",", spaces, !,
    args(Rest).
args([Last]) -->
    fol_term(Last).

ident(Name, true) -->
    [C], { char_type(C, upper) }, id_rest(Rest),
    { atom_chars(Name, [C | Rest]) }.
ident(Name, false) -->
    [C], { char_type(C, lower) }, id_rest(Rest),
    { atom_chars(Name, [C | Rest]), \+ memberchk(Name, [and, or, not]) }.

id_rest([C | Rest]) --> [C], { char_type(C, alnum) ; C = '_' }, !, id_rest(Rest).
id_rest([]) --> [].

eos([], []).

space1 --> [C], { char_type(C, space) }, spaces.

spaces --> [C], { char_type(C, space) }, !, spaces.
spaces --> [].

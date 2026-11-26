:- module(parser, [parse_kb_file/2]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_kb_file(FilePath, Clauses) :-
    read_file_to_string(FilePath, Text, [encoding(utf8)]),
    string_chars(Text, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([First | Rest]) -->
    spaces, clause_expr(First), spaces, "and", spaces, !,
    cnf_formula(Rest).
cnf_formula([Last]) -->
    spaces, clause_expr(Last), spaces.

clause_expr(Lits) --> "(", spaces, disjunction(Lits), spaces, ")", !.
clause_expr(Lits) --> disjunction(Lits).

disjunction([First | Rest]) -->
    literal(First), spaces, "or", spaces, !,
    disjunction(Rest).
disjunction([Last]) -->
    literal(Last).

literal(neg(Atom)) --> "not", space1, fol_term(Atom), !.
literal(pos(Atom)) --> fol_term(Atom).

fol_term(Term) -->
    ident(Functor), "(", spaces, args(Args), spaces, ")", !,
    { Term =.. [Functor | Args] }.
fol_term(Term) -->
    ident(Name),
    { atom_chars(Name, [C | _]), (char_type(C, upper) -> Term = var(Name) ; Term = Name) }.

args([First | Rest]) -->
    fol_term(First), spaces, ",", spaces, !,
    args(Rest).
args([Last]) -->
    fol_term(Last).

ident(Name) -->
    [C], { char_type(C, alpha) }, id_rest(Rest),
    { atom_chars(Name, [C | Rest]) }.

id_rest([C | Rest]) --> [C], { char_type(C, alnum) ; C = '_' }, !, id_rest(Rest).
id_rest([]) --> [].

space1 --> [C], { char_type(C, space) }, spaces.

spaces --> [C], { char_type(C, space) }, !, spaces.
spaces --> [].

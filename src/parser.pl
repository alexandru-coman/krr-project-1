:- module(parser, [
    parse_kb_file/2,
    parse_kb_string/2,
    parse_cnf/2,
    parse_clause/2
]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_cnf(FormulaString, Clauses) :-
    parse_kb_string(FormulaString, Clauses).

parse_clause(ClauseString, Literals) :-
    string_chars(ClauseString, Chars),
    phrase((whitespaces, clause_expr(Literals), whitespaces), Chars).

parse_kb_file(FilePath, Clauses) :-
    read_file_to_string(FilePath, FormulaString, [encoding(utf8)]),
    parse_kb_string(FormulaString, Clauses).

parse_kb_string(FormulaString, Clauses) :-
    string_chars(FormulaString, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([FirstClause | RestClauses]) -->
    whitespaces, clause_expr(FirstClause), whitespaces, conjunction_op, !,
    cnf_formula(RestClauses).
cnf_formula([SingleClause]) --> whitespaces, clause_expr(SingleClause), whitespaces.
cnf_formula([]) --> whitespaces.

conjunction_op -->
    whitespaces, ( "and" ; "^" ; "&" ; ";" ; [Char], { char_type(Char, newline) } ), whitespaces.

clause_expr(Literals) --> "(", whitespaces, disjunction_expr(Literals), whitespaces, ")".
clause_expr(Literals) --> "[", whitespaces, disjunction_expr(Literals), whitespaces, "]".
clause_expr(Literals) --> disjunction_expr(Literals).

disjunction_expr([FirstLit | RestLits]) -->
    literal_expr(FirstLit), whitespaces, disjunction_op, !,
    disjunction_expr(RestLits).
disjunction_expr([SingleLit]) --> literal_expr(SingleLit).

disjunction_op --> whitespaces, ( "or" ; "v" ; "|" ; "," ), whitespaces.

literal_expr(neg(Predicate)) --> negation_prefix, whitespaces, fol_term(Predicate).
literal_expr(pos(Predicate)) --> fol_term(Predicate).

negation_prefix --> "not", whitespaces.
negation_prefix --> ['\u00AC'] ; "¬" ; "~" ; "-".

fol_term(Compound) -->
    identifier(Functor, false), whitespaces, "(", whitespaces, arg_list(Args), whitespaces, ")", !,
    { Compound =.. [Functor | Args] }.
fol_term(Term) -->
    identifier(Name, IsVar),
    { IsVar == true -> Term = var(Name) ; Term = Name }.

arg_list([FirstArg | RestArgs]) -->
    fol_term(FirstArg), whitespaces, ",", whitespaces, !,
    arg_list(RestArgs).
arg_list([SingleArg]) --> fol_term(SingleArg).

identifier(Name, true) -->
    [First], { char_type(First, upper) ; First = '_' }, id_rest(Rest),
    { atom_chars(Name, [First | Rest]) }.
identifier(Name, false) -->
    [First], { char_type(First, lower) }, id_rest(Rest),
    { atom_chars(Name, [First | Rest]) }.

id_rest([Char | Rest]) --> [Char], { char_type(Char, alnum) ; Char = '_' }, !, id_rest(Rest).
id_rest([]) --> [].

whitespaces --> [Char], { char_type(Char, space) }, !, whitespaces.
whitespaces --> [].

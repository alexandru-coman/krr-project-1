:- module(parser, [parse_kb_file/2]).

:- encoding(utf8).
:- set_prolog_flag(double_quotes, chars).

parse_kb_file(FilePath, Clauses) :-
    read_file_to_string(FilePath, FormulaString, [encoding(utf8)]),
    string_chars(FormulaString, Chars),
    phrase(cnf_formula(Clauses), Chars).

cnf_formula([]) --> whitespaces, eos_check, !.
cnf_formula(Clauses) --> whitespaces, cnf_clauses(Clauses), whitespaces.

cnf_clauses([FirstClause | RestClauses]) -->
    clause_expr(FirstClause), conjunction_op, !,
    cnf_clauses(RestClauses).
cnf_clauses([SingleClause]) --> clause_expr(SingleClause).

conjunction_op -->
    scan_ws(HasNL),
    (   explicit_conj, whitespaces
    ;   { HasNL == true }, peek_non_space
    ).

explicit_conj --> keyword("and") ; "^" ; "&" ; ";".

clause_expr(Literals) --> "(", whitespaces, disjunction_expr(Literals), whitespaces, ")".
clause_expr(Literals) --> "[", whitespaces, disjunction_expr(Literals), whitespaces, "]".
clause_expr(Literals) --> disjunction_expr(Literals).

disjunction_expr([FirstLit | RestLits]) -->
    literal_expr(FirstLit), whitespaces, disjunction_op, !,
    disjunction_expr(RestLits).
disjunction_expr([SingleLit]) --> literal_expr(SingleLit).

disjunction_op --> whitespaces, ( keyword("or") ; keyword("v") ; "|" ; "," ), whitespaces.

literal_expr(neg(Predicate)) --> negation_prefix, !, whitespaces, fol_term(Predicate).
literal_expr(pos(Predicate)) --> fol_term(Predicate).

negation_prefix --> "not", [Char], { char_type(Char, space) }, whitespaces.
negation_prefix --> "¬" ; "~" ; "-".

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

keyword(Word) --> Word, peek_non_id.

peek_non_id, [Char] --> [Char], { \+ char_type(Char, alnum), Char \= '_' }, !.
peek_non_id --> eos_check.

eos_check([], []).

peek_non_space, [Char] --> [Char], { \+ char_type(Char, space) }.

scan_ws(HasNL) -->
    [Char], { char_type(Char, space) }, !,
    scan_ws(RestNL),
    { (char_type(Char, newline) -> HasNL = true ; HasNL = RestNL) }.
scan_ws(false) --> [].

whitespaces --> [Char], { char_type(Char, space) }, !, whitespaces.
whitespaces --> [].

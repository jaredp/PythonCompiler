%{ open Ast %}

%token SEMI LPAREN RPAREN LBRACE RBRACE COMMA COLON
%token PLUS MINUS TIMES DIVIDE ASSIGN
%token EQ NEQ LT LEQ GT GEQ
%token RETURN IF ELSE FOR WHILE INT
%token <int> LITERAL
%token <string> ID
%token <string> INDENT
%token EOF

%token DEF PRINT IN PASS

%nonassoc NOELSE
%nonassoc ELSE
%right ASSIGN
%left EQ NEQ
%left LT GT LEQ GEQ
%left PLUS MINUS
%left TIMES DIVIDE

%start program
%type <Ast.program> program

%%

program: program_ { (List.rev (fst $1), List.rev (snd $1)) }

program_:
   /* nothing */	{ [], [] }
 | program_ SEMI	{ $1 }
 | program_ stmt	{ ($2 :: fst $1), snd $1 }
 | program_ fdecl	{ fst $1, ($2 :: snd $1) }

fdecl:
   DEF ID LPAREN formals_opt RPAREN COLON block
     { { fname = $2; formals = $4; body = $7 } }

formals_opt:
    /* nothing */ { [] }
  | formal_list   { List.rev $1 }

formal_list:
    ID                   { [$1] }
  | formal_list COMMA ID { $3 :: $1 }

stmt_list:
    /* nothing */  { [] }
  | stmt_list stmt { $2 :: $1 }

block:
    LBRACE PASS SEMI RBRACE	{ [] }
  | LBRACE stmt_list RBRACE	{ List.rev $2 }

stmt:
    expr SEMI { Expr($1) }
  | RETURN expr SEMI			{ Return($2) }
  | IF expr COLON block			{ If($2, $4, []) }
  | FOR expr_opt SEMI expr_opt SEMI expr_opt COLON block
								{ For($2, $4, $6, $8) }
  | WHILE expr COLON block		{ While($2, $4) }
  | PRINT expr SEMI				{ Expr(Call("print", [$2])) }

expr_opt:
    /* nothing */ { Noexpr }
  | expr          { $1 }

expr:
    LITERAL          { Literal($1) }
  | ID               { Id($1) }
  | expr PLUS   expr { Binop($1, Add,   $3) }
  | expr MINUS  expr { Binop($1, Sub,   $3) }
  | expr TIMES  expr { Binop($1, Mult,  $3) }
  | expr DIVIDE expr { Binop($1, Div,   $3) }
  | expr EQ     expr { Binop($1, Equal, $3) }
  | expr NEQ    expr { Binop($1, Neq,   $3) }
  | expr LT     expr { Binop($1, Less,  $3) }
  | expr LEQ    expr { Binop($1, Leq,   $3) }
  | expr GT     expr { Binop($1, Greater,  $3) }
  | expr GEQ    expr { Binop($1, Geq,   $3) }
  | ID ASSIGN expr   { Assign($1, $3) }
  | ID LPAREN actuals_opt RPAREN { Call($1, $3) }
  | LPAREN expr RPAREN { $2 }

actuals_opt:
    /* nothing */ { [] }
  | actuals_list  { List.rev $1 }

actuals_list:
    expr                    { [$1] }
  | actuals_list COMMA expr { $3 :: $1 }

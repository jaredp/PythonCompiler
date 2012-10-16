{ open Parser }

rule token = parse
  [' ' '\t' '\r' '\n']*'\n'([' ' '\t' '\r']* as ws)
						{ INDENT(ws) }
| [' ' '\t' '\r']		{ token lexbuf }
| '#'[^'\n']*			{ token lexbuf }
| '('					{ LPAREN }
| ')'					{ RPAREN }
| '{'					{ LBRACE }
| '}'					{ RBRACE }
| ':'					{ COLON }
| ';'					{ SEMI }
| ','					{ COMMA }
| '+'					{ PLUS }
| '-'					{ MINUS }
| '*'					{ TIMES }
| '/'					{ DIVIDE }
| '='					{ ASSIGN }
| "=="					{ EQ }
| "!="					{ NEQ }
| '<'					{ LT }
| "<="					{ LEQ }
| ">"					{ GT }
| ">="					{ GEQ }
| "if"					{ IF }
| "else"				{ ELSE }
| "for"					{ FOR }
| "while"				{ WHILE }
| "return"				{ RETURN }
| "int"					{ INT }
| "def"					{ DEF }
| "print"				{ PRINT }
| "in"					{ IN }
| "pass"				{ PASS }
| ['0'-'9']+ as lxm		{ LITERAL(int_of_string lxm) }
| ['a'-'z' 'A'-'Z']['a'-'z' 'A'-'Z' '0'-'9' '_']* as lxm { ID(lxm) }
| eof { EOF }
| _ as char { raise (Failure("illegal character " ^ Char.escaped char)) }

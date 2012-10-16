open Parser

let string_starts_with str prefix =
	let prelen = String.length prefix in
	if String.length str < prelen then false
	else String.sub str 0 prelen = prefix

let buffer_tokens lexer =
	let tbuf = ref [] in
	let rec get_tokens lexbuf = match !tbuf with
		  [] -> tbuf := lexer lexbuf; get_tokens lexbuf
		| t::rs -> tbuf := rs; t
	in get_tokens
	
let processed_tokens lexer = 
	let indentstack = ref [""] in
	fun lexbuf ->
	match lexer lexbuf with
		INDENT(ws) ->
			let oldindent = List.hd !indentstack in
			if ws = oldindent then
				[SEMI]
			else
			if string_starts_with ws oldindent then (
				indentstack := ws::!indentstack;
				[LBRACE]
			) else ( 
				let tbuf = ref [SEMI] in
				while (
					try
						List.hd !indentstack <> ws
					with x ->
						print_string "bad indentation: ";
						print_endline (String.escaped ws);
						raise x
				) do
					indentstack := List.tl !indentstack;
					tbuf := RBRACE::!tbuf;
				done;
				List.rev !tbuf
			)
		 | t -> [t]


let _ =
  let lexbuf = Lexing.from_channel stdin in
  let tpipeline = buffer_tokens (processed_tokens Scanner.token) in
  let program = Parser.program tpipeline lexbuf in
  print_string (Compile.translate program)
 

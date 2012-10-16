open Ast
open Astpp

let rec translate prog =
	Astpp.string_of_program prog
type op = Add | Sub | Mult | Div | Equal | Neq | Less | Leq | Greater | Geq

type expr =
    Literal of int
  | Id of string
  | Binop of expr * op * expr
  | Assign of string * expr
  | Call of string * expr list
  | Noexpr

type stmt =
    Expr of expr
  | Return of expr
  | If of expr * block * block
  | For of expr * expr * expr * block
  | While of expr * block

and block = stmt list

type func_decl = {
    fname : string;
    formals : string list;
    body : block;
  }

type program = block * func_decl list

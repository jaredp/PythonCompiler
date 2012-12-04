#include <stdio.h>

#define P3IntLiteral(v) v
#define P3StringLiteral(v) 0
#define P3MakeFunction(f...) 0

#define AddBinaryOp(lhs, rhs) 		(lhs + rhs)
#define AugAddBinaryOp(lhs, rhs)	(lhs + rhs)
#define SubBinaryOp(lhs, rhs) 		(lhs - rhs)
#define AugSubBinaryOp(lhs, rhs) 	(lhs + rhs)

#define LtCmpOp(lhs, rhs)			(lhs < rhs)
#define EqCmpOp(lhs, rhs)			(lhs == rhs)

#define NotUnaryOp(arg) 			(!arg)
#define isTruthy(arg)				(arg)

#define Py_None						0
#define MyPrint(obj)				printf("%d", obj)
#define PyPrintNl()					printf("\n")


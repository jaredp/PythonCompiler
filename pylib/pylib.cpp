#include "P3Libs.h"
#include <time.h>

int main(int argc, char **argv) {
    Py_Initialize();
	PySys_SetArgv(argc, argv);

    initFnMechanism();
    initModuleMechanism();

    register_globals();

   	try {
		run_main_module();
	} catch (PythonException &e) {
		PyErr_Print();
	}

    Py_Finalize();
	return 0;
}

void raise(...) {
	RAISE;
}

/*********************************************
 * Function call mechanism
 *********************************************/

PyObject *P3Call(PyObject *fn, PyObject *args) {
	PyObject *ret = THROW_ON_NULL(PyObject_Call(fn, args, NULL));
	Py_DECREF(args);
	return ret;
}

/*********************************************
 * Object Oriented mechanisms
 *********************************************/

PyObject *P3GetAttr(PyObject *target, const char *attr) {
	return THROW_ON_NULL(PyObject_GetAttrString(target, attr));
}

void P3AssignAttr(PyObject *target, const char *attr, PyObject *value) {
	THROW_ON_ERRCODE(PyObject_SetAttrString(target, attr, value));
}

void P3DelAttr(PyObject *target, const char *attr) {
	THROW_ON_ERRCODE(PyObject_DelAttrString(target, attr));
}

PyObject *P3GetType(PyObject *o) {
	return THROW_ON_NULL(PyObject_Type(o));
}

/*********************************************
 * Literals
 *********************************************/

PyObject *P3IntLiteral(long value) {
	return THROW_ON_NULL(PyInt_FromLong(value));
}

PyObject *P3FloatLiteral(double value) {
	return THROW_ON_NULL(PyFloat_FromDouble(value));
}

PyObject *P3StringLiteral(const char *value) {
	return THROW_ON_NULL(PyString_InternFromString(value));
}

bool isTruthy(PyObject *object) {
	char truthiness = PyObject_IsTrue(object);
	if (truthiness != -1) {
		return truthiness;
	} else {
		RAISE;
	}
}

PyObject *MyPrint(PyObject *obj) {
	PyObject_Print(obj, stdout, Py_PRINT_RAW);
	fprintf(stdout, " ");
	Py_RETURN_NONE;
}

PyObject *PyPrintNl() {
	fprintf(stdout, "\n");
	Py_RETURN_NONE;
}

PyObject *MakeTuple(PyObject *size_obj) {
	Py_ssize_t size = PyInt_AsSsize_t(size_obj);
	PyObject *tuple = THROW_ON_NULL(PyTuple_New(size));
	return tuple;
}

PyObject *SetTupleComponent(PyObject *tuple, PyObject *index_obj, PyObject *value) {
	//May need to do memory management...
	Py_ssize_t index = PyInt_AsSsize_t(index_obj);
	THROW_ON_NULL(PyTuple_SET_ITEM(tuple, index, value));
	Py_RETURN_NONE;
}

PyObject *Iter(PyObject *container) {
	return THROW_ON_NULL(PyObject_GetIter(container));
}

PyObject *Next(PyObject *iterator) {
	PyObject *next = PyIter_Next(iterator);
	if (next) return next;
	if (!PyErr_Occurred()) return NULL;	
	//THIS IS FRACKING DANGEROUS!!
	//The idea is that whatever is returned will be checked by
	//IsStopIterationSignal

	RAISE;
}

PyObject *IsStopIterationSignal(PyObject *nextretval) {
	if (nextretval == NULL) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	} 
}


PyObject *NewList() {
	return THROW_ON_NULL(PyList_New(0));
}

PyObject *ListAppend(PyObject *list, PyObject *member) {
	THROW_ON_ERRCODE(PyList_Append(list, member));
}

/*********************************************
 * Slice Operations
 *********************************************/

PyObject *Subscript(PyObject *obj, PyObject *subscript) {
	return THROW_ON_NULL(PyObject_GetItem(obj, subscript));
}

PyObject *Slice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step) {
	return Subscript(obj, THROW_ON_NULL(PySlice_New(start, end, step)));
}

PyObject *AssignSubscript(PyObject *obj, PyObject *subscript, PyObject *value) {
	THROW_ON_ERRCODE(PyObject_SetItem(obj, subscript, value));
	Py_RETURN_NONE;
}

PyObject *AssignSlice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step, PyObject *value) {
	return AssignSubscript(obj, THROW_ON_NULL(PySlice_New(start, end, step)), value);
}

PyObject *DeleteSubscript(PyObject *obj, PyObject *subscript) {
	THROW_ON_ERRCODE(PyObject_DelItem(obj, subscript));
	Py_RETURN_NONE;
}

PyObject *DeleteSlice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step) {
	return DeleteSubscript(obj, THROW_ON_NULL(PySlice_New(start, end, step)));
}


/*********************************************
 * Binary Operations
 *********************************************/

#define WRAP_BINOP(WRAPPEDNAME, CPYTHONNAME)			\
PyObject *WRAPPEDNAME(PyObject *lhs, PyObject *rhs) {	\
	return THROW_ON_NULL(CPYTHONNAME(lhs, rhs));		\
}

WRAP_BINOP(AddBinaryOp, PyNumber_Add)
WRAP_BINOP(SubBinaryOp, PyNumber_Subtract)
WRAP_BINOP(MultBinaryOp, PyNumber_Multiply)
WRAP_BINOP(DivBinaryOp, PyNumber_Divide)
WRAP_BINOP(ModBinaryOp, PyNumber_Remainder)
//WRAP_BINOP(PowBinaryOp, PyNumber_Power)
WRAP_BINOP(LShiftBinaryOp, PyNumber_Lshift)
WRAP_BINOP(RShiftBinaryOp, PyNumber_Rshift)
WRAP_BINOP(BitOrBinaryOp, PyNumber_Or)
WRAP_BINOP(BitXorBinaryOp, PyNumber_Xor)
WRAP_BINOP(BitAndBinaryOp, PyNumber_And)
WRAP_BINOP(FloorDivBinaryOp, PyNumber_FloorDivide)

WRAP_BINOP(AugAddBinaryOp, PyNumber_InPlaceAdd)
WRAP_BINOP(AugSubBinaryOp, PyNumber_InPlaceSubtract)
WRAP_BINOP(AugMultBinaryOp, PyNumber_InPlaceMultiply)
WRAP_BINOP(AugDivBinaryOp, PyNumber_InPlaceDivide)
WRAP_BINOP(AugModBinaryOp, PyNumber_InPlaceRemainder)
//WRAP_BINOP(AugPowBinaryOp, )
WRAP_BINOP(AugLShiftBinaryOp, PyNumber_InPlaceLshift)
WRAP_BINOP(AugRShiftBinaryOp, PyNumber_InPlaceRshift)
WRAP_BINOP(AugBitOrBinaryOp, PyNumber_InPlaceOr)
WRAP_BINOP(AugBitXorBinaryOp, PyNumber_InPlaceXor)
WRAP_BINOP(AugBitAndBinaryOp, PyNumber_InPlaceAnd)
WRAP_BINOP(AugFloorDivBinaryOp, PyNumber_InPlaceFloorDivide)

#define WRAP_CMPOP(WRAPPEDNAME, OPID) 							\
PyObject *WRAPPEDNAME(PyObject *lhs, PyObject *rhs) {			\
	return THROW_ON_NULL(PyObject_RichCompare(lhs, rhs, OPID));	\
}

WRAP_CMPOP(EqCmpOp, Py_EQ)
WRAP_CMPOP(NotEqCmpOp, Py_NE)
WRAP_CMPOP(LtCmpOp, Py_LT)
WRAP_CMPOP(LtECmpOp, Py_LE)
WRAP_CMPOP(GtCmpOp, Py_GT)
WRAP_CMPOP(GtECmpOp, Py_GE)

PyObject *IsCmpOp(PyObject *lhs, PyObject *rhs) {
	if (lhs == rhs) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

PyObject *IsNotCmpOp(PyObject *lhs, PyObject *rhs) {
	if (lhs != rhs) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

/*
PyObject *InCmpOp(PyObject *lhs, PyObject *rhs) {}
PyObject *NotInCmpOp(PyObject *lhs, PyObject *rhs) {}
*/

PyObject *NotUnaryOp(PyObject *operand) {
	switch(PyObject_Not(operand)) {
		case 1:
			Py_RETURN_TRUE;
		case 0:
			Py_RETURN_FALSE;
		case -1:
			RAISE;
	}
}


#define WRAP_UNARYOP(WRAPPEDNAME, CPYTHONNAME)		\
PyObject *WRAPPEDNAME(PyObject *operand) {			\
	return THROW_ON_NULL(CPYTHONNAME(operand));		\
}

WRAP_UNARYOP(InvertUnaryOp, PyNumber_Invert)
WRAP_UNARYOP(UAddUnaryOp, PyNumber_Positive)
WRAP_UNARYOP(USubUnaryOp, PyNumber_Negative)

/*
 stdlib
*/

PyObject *P3__builtin__len_POSCALLER(PyObject *argstuple) {
	return P3__builtin__len(PyTuple_GET_ITEM(argstuple, 0));
}

PyObject *P3time_clock_POSCALLER(PyObject *argstuple) {
	return P3time_clock();
}

 PyObject *P3__builtin__len(PyObject *seq) {
 	return P3IntLiteral(THROW_ON_ERRCODE(PySequence_Length(seq)));
 }

PyObject *P3time_clock() {
    return P3FloatLiteral((float)clock() / CLOCKS_PER_SEC);
}

PyObject *P3__builtin__int(PyObject *value) {
	return THROW_ON_NULL(PyNumber_Int(value));
}

PyObject *P3__builtin__raw_input(PyObject *prompt) {
	PyObject_Print(prompt, stdout, Py_PRINT_RAW);
	char input[50];
	fgets(input, 49, stdin);
	return P3StringLiteral(input);
}





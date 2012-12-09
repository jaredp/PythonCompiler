#include "P3Libs.h"
#include <time.h>

#define RAISE throw PythonException()
#define THROW_ON_NULL(e) 					\
({ typeof(e) a = (e); if (a == NULL) RAISE; a;})
#define THROW_ON_ERRCODE(e)					\
({ typeof(e) a = (e); if (a == -1) RAISE; a;})

void initFnMechanism();

int main(int argc, char **argv) {
    Py_Initialize();
    initFnMechanism();

    int start, end;
   	try {
	    start = clock();
		run_main_module();
	    end = clock();
	} catch (PythonException &e) {
		PyErr_Print();
	}

    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("\n%f seconds\n", seconds);

    Py_Finalize();
	return 0;
}

/*********************************************
 * Function call mechanism
 *********************************************/

typedef struct {
	PyObject_HEAD
	fptr plain_caller;
	const char *defined_name;
} P3Function;

PyObject *P3Function_Call(P3Function *p3fn, PyObject *posargs, PyObject *kwargs) {
	//FIXME: hey so those keywords...
	return p3fn->plain_caller(posargs);
}

static PyTypeObject P3Function_Type = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "function",		           /*tp_name*/
    sizeof(P3Function), 	   /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    (ternaryfunc)P3Function_Call,           /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "compiled function",       /* tp_doc */
};


PyObject *P3MakeFunction(fptr fn, const char *defined_name) {
    P3Function *self = (P3Function *)P3Function_Type.tp_alloc(&P3Function_Type, 0);
    THROW_ON_NULL(self);

    self->plain_caller = fn;
    self->defined_name = defined_name;

    return (PyObject *)self;
}

PyObject *P3Call(PyObject *fn, PyObject *args) {
	PyObject *ret = THROW_ON_NULL(PyObject_Call(fn, args, NULL));
	Py_DECREF(args);
	return ret;
}

void initFnMechanism() {
	if (PyType_Ready(&P3Function_Type) != 0) {
		RAISE;
	}
}


/*********************************************
 * Literals
 *********************************************/

inline PyObject *P3IntLiteral(long value) {
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
	Py_RETURN_NONE;
}

PyObject *PyPrintNl() {
	printf("\n");
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

 PyObject *P3__builtin__len(PyObject *seq) {
 	return P3IntLiteral(THROW_ON_ERRCODE(PySequence_Length(seq)));
 }


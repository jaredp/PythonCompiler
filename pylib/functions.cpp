#include "P3Libs.h"
#include <stddef.h>

typedef struct {
	PyObject_HEAD
	fptr plain_caller;
    PyObject *dict;
	const char *defined_name;
} P3Function;

PyObject *P3Function_Call(P3Function *p3fn, PyObject *posargs, PyObject *kwargs) {
	//FIXME: hey so those keywords...
	return p3fn->plain_caller(posargs);
}

static PyTypeObject P3Function_Type = {PyObject_HEAD_INIT(NULL)};


PyObject *P3MakeFunction(fptr fn, const char *defined_name) {
    P3Function *self = (P3Function *)PyType_GenericAlloc(&P3Function_Type, 0);
    THROW_ON_NULL(self);

    self->plain_caller = fn;
    self->defined_name = defined_name;

    return (PyObject *)self;
}

void initFnMechanism() {
    P3Function_Type.tp_call = (ternaryfunc)P3Function_Call;

    P3Function_Type.tp_name = "function";
    P3Function_Type.tp_doc = "compiled function";

    P3Function_Type.tp_basicsize = sizeof(P3Function);
    P3Function_Type.tp_dictoffset = offsetof(P3Function, dict);

    P3Function_Type.tp_flags = Py_TPFLAGS_DEFAULT;

	if (PyType_Ready(&P3Function_Type) != 0) {
		RAISE;
	}
}


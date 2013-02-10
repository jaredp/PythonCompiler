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

void initFnMechanism() {
    P3Function_Type.tp_dictoffset = offsetof(P3Function, dict);
	if (PyType_Ready(&P3Function_Type) != 0) {
		RAISE;
	}
}


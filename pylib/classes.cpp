#include "P3Libs.h"


PyObject *P3MakeClass(const char *name) {
	return THROW_ON_NULL(PyClass_New(NULL, PyDict_New(), PyString_FromString(name)));
}

#import "P3Libs.h"
#import <time.h>

int main(int argc, char **argv) {
    Py_Initialize();

    int start = clock();
	run_main_module();
    int end = clock();

    float seconds = (float)(end - start) / CLOCKS_PER_SEC;
    printf("\n%f seconds\n", seconds);

    Py_Finalize();
	return 0;
}

#define THROW_ON_NULL(e) ({ typeof(e) a = (e); if (a == NULL) throw PythonException(); a;})


PyObject *P3MakeFunction(fptr fn, const char *) {
	return NULL;
}

PyObject *P3Call(PyObject *fn, size_t argcount, PyObject **args) {
	return NULL;
}

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
	return true;
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
	if (!PyErr_Occurred()) return NULL;	//THIS IS FRACKING DANGEROUS!!
	throw PythonException();
}

PyObject *IsStopIterationSignal(PyObject *nextretval) {
	if (nextretval == NULL) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	} 
}

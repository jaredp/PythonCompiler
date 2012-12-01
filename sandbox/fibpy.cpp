#include <Python.h>

PyObject *i1, *i2;

class PythonException {};

class PyObjRef {
	PyObject *ref;
	~PyObjRef() {
		Py_XDECREF(ref);
		ref = NULL;
	}
};

inline int
myPyObject_RichCompareBool(PyObject *o1, PyObject *o2, int opid) {
	int retval = PyObject_RichCompareBool(o1, o2, opid);
	if (retval != -1) {
		return retval;
	} else {
		throw PythonException();
	}
}

inline PyObject *
myPyNumber_Add(PyObject *a, PyObject *b) {
	PyObject *retval = PyNumber_Add(a, b);
	if (retval) {
		return retval;
	} else {
		throw PythonException();
	}
}

inline PyObject *
myPyNumber_Subtract(PyObject *a, PyObject *b) {
	PyObject *retval = PyNumber_Subtract(a, b);
	if (retval) {
		return retval;
	} else {
		throw PythonException();
	}
}


PyObject *
fibfunc(PyObject *n) {
	PyObject *s1, *s2, *s3, *s4, *s5;
	
	int b1 = myPyObject_RichCompareBool(n, i1, Py_EQ);
	if (b1) {
		return i1;
	} else {
		int b2 = myPyObject_RichCompareBool(n, i2, Py_EQ);
		if (b2) {
			return i1;
		} else {
			s1 = myPyNumber_Subtract(n, i1);
			s2 = fibfunc(s1);
			
			s3 = myPyNumber_Subtract(n, i2);
			s4 = fibfunc(s3);
			
			s5 = myPyNumber_Add(s1, s2);
			return s5;
		}
	}
}

void
loadconsts() {
	i1 = PyInt_FromLong(1);
	i2 = PyInt_FromLong(2);
}

void loadfib() {
	for (int j = 1; j < 35; j++) {
		PyObject *i = PyInt_FromLong(j);
		PyObject_Print(fibfunc(i), stdout, 0);
		printf("\n");
	}
}

int
main(int argc, char *argv[])
{
    Py_Initialize();
	
	loadconsts();
	
	try {
		loadfib();
	} catch (...) {
		PyErr_Print();
	}
	
    Py_Finalize();
    return 0;
}

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


PyObject *P3MakeFunction(fptr fn, const char *) {
	return NULL;
}

PyObject *P3Call(PyObject *fn, size_t argcount, PyObject **args) {
	return NULL;
}


PyObject *P3IntLiteral(long value) {
	return PyInt_FromLong(value);
}

PyObject *P3FloatLiteral(double value) {
	return NULL;
}

PyObject *P3StringLiteral(const char *value) {
	return NULL;
}

bool isTruthy(PyObject *object) {
	return true;
}

PyObject *MyPrint(PyObject *obj) {
	PyObject_Print(obj, stdout, 0);
	return Py_None;
}

PyObject *PyPrintNl() {
	printf("\n");
	return Py_None;
}


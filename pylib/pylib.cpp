#import <P3Libs.h>

PyObject *P3None;

int main(int argc, char **argv) {
	// TODO: timer!!

	//Py_init()?
	run_main_module();
	return 0;
}


PyObject *P3MakeFunction(fptr fn, const char *) {
	return NULL;
}

PyObject *P3Call(PyObject *fn, size_t argcount, PyObject **args) {
	return NULL;
}


PyObject *P3IntLiteral(long value) {
	return NULL;
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

PyObject *PyPrint(PyObject *dest, PyObject *obj) {

}

PyObject *MyPrint(PyObject *obj) {

}

PyObject *PyPrintNl() {
	return NULL;
}

PyObject *MakeTuple(PyObject *size) {
	return NULL;
}

PyObject *SetTupleComponent(PyObject *tuple, PyObject *index, PyObject *value) {
	return NULL;
}

PyObject *Iter(PyObject *container) {
	return NULL;
}

PyObject *Next(PyObject *iterator) {
	return NULL;
}

PyObject *IsStopIterationSignal(PyObject *nextretval) {
	return nextretval;
}

PyObject *Globals() {
	return NULL;
}

PyObject *Locals() {
	return NULL;
}

PyObject *Repr(PyObject *obj) {
	return NULL;
}

PyObject *NewList(PyObject *size) {
	return NULL;
}

PyObject *ListAppend(PyObject *member) {
	return NULL;
}

PyObject *NewSet(PyObject *size) {
	return NULL;
}

PyObject *SetAdd(PyObject *member) {
	return NULL;
}

PyObject *NewDict(PyObject *size) {
	return NULL;
}

PyObject *DictSet(PyObject *dict, PyObject *key, PyObject *value) {
	return NULL;
}



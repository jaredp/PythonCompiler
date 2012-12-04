#import <Python.h>

int main(int argc, char **argv);
PyObject *run_main_module();

typedef PyObject *(fptr)(PyObject *, PyObject *);
PyObject *P3MakeFunction(fptr, const char *);

PyObject *P3Call(PyObject *fn, size_t argcount, PyObject **args);

extern PyObject *P3None; // = something static...

PyObject *P3IntLiteral(long value);
PyObject *P3FloatLiteral(double value);
PyObject *P3StringLiteral(const char *value);

bool isTruthy(PyObject *object);
inline bool isTruthy(bool b) { return b; }
/* save some time maybe hopefully */
/*

fns = []
def BuiltinFn(name, *args):
	fns.append((name, args))

# copy paste stdlib.py in

for (fname, args) in fns:
	a = ['PyObject *' + arg for arg in args]
	print 'PyObject *%s(%s);' % (fname, ', '.join(a))

*/

PyObject *Repr(PyObject *obj);
PyObject *PyPrint(PyObject *dest, PyObject *obj);
PyObject *MyPrint(PyObject *obj);
PyObject *PyPrintNl();

PyObject *MakeTuple(PyObject *size);
PyObject *SetTupleComponent(PyObject *tuple, PyObject *index, PyObject *value);

PyObject *Iter(PyObject *container);
PyObject *Next(PyObject *iterator);
PyObject *IsStopIterationSignal(PyObject *nextretval);

PyObject *Globals();
PyObject *Locals();

PyObject *NewList(PyObject *size);
PyObject *ListAppend(PyObject *member);

PyObject *NewSet(PyObject *size);
PyObject *SetAdd(PyObject *member);

PyObject *NewDict(PyObject *size);
PyObject *DictSet(PyObject *dict, PyObject *key, PyObject *value);

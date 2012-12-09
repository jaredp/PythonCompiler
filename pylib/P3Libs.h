#include <Python.h>

class PythonException {};

int main(int argc, char **argv);
PyObject *run_main_module();

typedef PyObject *(*fptr)(PyObject *);
PyObject *P3MakeFunction(fptr, const char *);
PyObject *P3Call(PyObject *fn, PyObject *args);

PyObject *P3MakeClass(const char *name);

PyObject *P3MakeModule(const char *name);
PyObject *P3ModuleRegisterGlobal(const char *name, PyObject **global);

PyObject *P3IntLiteral(long value);
PyObject *P3FloatLiteral(double value);
PyObject *P3StringLiteral(const char *value);

PyObject *P3GetAttr(PyObject *target, const char *attr);
void P3AssignAttr(PyObject *target, const char *attr, PyObject *value);
void P3DelAttr(PyObject *target, const char *attr);


PyObject *P3GetException();

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

PyObject *NewList();
PyObject *ListAppend(PyObject *list, PyObject *member);

PyObject *NewSet(PyObject *size);
PyObject *SetAdd(PyObject *member);

PyObject *NewDict(PyObject *size);
PyObject *DictSet(PyObject *dict, PyObject *key, PyObject *value);

PyObject *Subscript(PyObject *obj, PyObject *subscript, PyObject *value);
PyObject *Slice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step, PyObject *value);
PyObject *AssignSubscript(PyObject *obj, PyObject *subscript, PyObject *value);
PyObject *AssignSlice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step, PyObject *value);
PyObject *DeleteSubscript(PyObject *obj, PyObject *subscript);
PyObject *DeleteSlice(PyObject *obj, PyObject *start, PyObject *end, PyObject *step);


/* operations, binary and unary */

PyObject *AddBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *SubBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *MultBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *DivBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *ModBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *PowBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *LShiftBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *RShiftBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *BitOrBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *BitXorBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *BitAndBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *FloorDivBinaryOp(PyObject *lhs, PyObject *rhs);

PyObject *AugAddBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugSubBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugMultBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugDivBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugModBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugPowBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugLShiftBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugRShiftBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugBitOrBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugBitXorBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugBitAndBinaryOp(PyObject *lhs, PyObject *rhs);
PyObject *AugFloorDivBinaryOp(PyObject *lhs, PyObject *rhs);

PyObject *EqCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *NotEqCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *LtCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *LtECmpOp(PyObject *lhs, PyObject *rhs);
PyObject *GtCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *GtECmpOp(PyObject *lhs, PyObject *rhs);
PyObject *IsCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *IsNotCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *InCmpOp(PyObject *lhs, PyObject *rhs);
PyObject *NotInCmpOp(PyObject *lhs, PyObject *rhs);

PyObject *InvertUnaryOp(PyObject *operand);
PyObject *NotUnaryOp(PyObject *operand);
PyObject *UAddUnaryOp(PyObject *operand);
PyObject *USubUnaryOp(PyObject *operand);

/*

bultin modules

*/

PyObject *P3__builtin__len_POSCALLER(PyObject *argstuple);
PyObject *P3time_clock_POSCALLER(PyObject *argstuple);

PyObject *P3__builtin__len(PyObject *seq);
PyObject *P3time_clock();


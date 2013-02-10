
void initModuleMechanism();

typedef struct {
	PyObject_HEAD
    PyObject *dict;
	const char *defined_name;
} P3Module;

PyAPI_DATA(PyTypeObject) P3Module_Type;

#define DECLARE_MODULE(mname, defined_name)								\
static P3Module mname = {PyObject_HEAD_INIT(&P3Module_Type) NULL, defined_name}

PyObject *P3InitModule(P3Module *module);
void P3ModuleRegisterGlobal(
	P3Module *module,
	const char *name,
	PyCellObject *global
);

#define DECLARE_GLOBAL(gbl)                                             \
static PyCellObject gbl_Cell = {PyObject_HEAD_INIT(&PyCell_Type) NULL}; \
PyObject *&gbl = gbl_Cell.ob_ref


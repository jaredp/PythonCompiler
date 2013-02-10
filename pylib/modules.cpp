#include "P3Libs.h"
#include <stddef.h>

PyTypeObject P3Module_Type = {PyObject_HEAD_INIT(NULL)};

PyObject *P3InitModule(P3Module *module) {
    module->dict = PyDict_New();
}

void P3ModuleRegisterGlobal(PyObject *_module, const char *name, PyCellObject *global) {
    P3Module *module = (P3Module *)_module;
    PyDict_SetItemString(module->dict, name, (PyObject *)global);
}

#define log(obj) PyObject_Print((PyObject *)obj, stdout, 0)

PyObject *P3Module_GetGlobal(P3Module *module, PyObject *identifier) {
    PyObject *cell = PyDict_GetItem(module->dict, identifier);
    return PyCell_GET(cell);
}

int P3Module_SetGlobal(P3Module *module, PyObject *identifier, PyObject *nval) {
    PyObject *cell = PyDict_GetItem(module->dict, identifier);
    PyCell_SET(cell, nval);
    return 0;
}


void initModuleMechanism() {
    P3Module_Type.tp_getattro = (getattrofunc)P3Module_GetGlobal;
    P3Module_Type.tp_setattro = (setattrofunc)P3Module_SetGlobal;

    P3Module_Type.tp_name = "module";
    P3Module_Type.tp_doc = "compiled module";

    P3Module_Type.tp_basicsize = sizeof(P3Module);
    P3Module_Type.tp_flags = Py_TPFLAGS_DEFAULT;

    if (PyType_Ready(&P3Module_Type) != 0) {
        RAISE;
    }
}
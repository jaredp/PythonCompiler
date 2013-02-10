#include "P3Libs.h"
#include <stddef.h>

PyTypeObject P3Module_Type = {0};

PyObject *P3InitModule(P3Module *module) {
    module->dict = PyDict_New();
}

void P3ModuleRegisterGlobal(P3Module *module, const char *name, PyCellObject *global) {

}

#define log(obj) PyObject_Print((PyObject *)obj, stderr, 0)

PyObject *P3Module_GetGlobal(P3Module *module, PyObject *identifier) {
    printf("getting global in ");
    log(module);
    printf(" named ");
    log(identifier);
    printf("\n");

    Py_RETURN_NONE;
}

PyObject *P3Module_SetGlobal(P3Module *module, PyObject *identifier, PyObject *nval) {
    printf("setting global in ");
    log(module);
    printf(" named ");
    log(identifier);
    printf(" to ");
    log(nval);
    printf("\n");

    Py_RETURN_NONE;
}


void initModuleMechanism() {
    P3Module_Type.tp_getattro = (getattrofunc)P3Module_GetGlobal;
    P3Module_Type.tp_setattro = (setattrofunc)P3Module_SetGlobal;

    if (PyType_Ready(&P3Module_Type) != 0) {
        RAISE;
    }
}
#include <Python.h>

static PyObject *SpamError;

static PyObject *
spam_system(PyObject *self, PyObject *args) {
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return Py_BuildValue("i", sts);
}

static PyMethodDef SpamMethods[] = {
    {"system",  spam_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC
initspam(void)
{
    PyObject *m;

    m = Py_InitModule("spam", SpamMethods);
    if (m == NULL)
        return;

    SpamError = PyErr_NewException("spam.error", NULL, NULL);
    Py_INCREF(SpamError);
    PyModule_AddObject(m, "error", SpamError);
}


int main(int argc, char **argv) {
    /* Pass argv[0] to the Python interpreter */
    Py_SetProgramName(argv[0]);
	
    /* Initialize the Python interpreter.  Required. */
    Py_Initialize();
	
    /* Add a static module */
    initspam();

	return 0;
}


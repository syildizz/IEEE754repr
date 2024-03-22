#include "pfloat.h"

// Documentation for the pfloat function.
const char pfloat_functions_docs[] = 
    "Return the floating point representation of the number empirically.\n"
	"\n"
    "e.g. \"-1234.5678\" -> '11000100100110100101001000101011'\n"
	"\n"
    ":param number: The number that that is going to be represented.\n"
    ":param prec: The precision of the floating point number. Can either be \"FLOAT\" or \"DOUBLE\".\n"
    ":returns: String of binary digits that represent the floating point number\n"
    ":raises ValueError: Raises ValueError in case of incorrect precision argument.\n"
	;

// The functions that are exported from the pfloat module.
static PyMethodDef pfloat_functions[] = {
	{"pfloat", (PyCFunction)pfloat, METH_VARARGS, pfloat_functions_docs},
	{NULL, NULL, 0, NULL}
};

// Documentation for the pfloat module.
const char * const pfloat_module_docs = "Python module for testing the IEEE754repr library empirically by creating a floating point number in memory and returning it's bits";

// The attributes of the module.
static struct PyModuleDef pfloat_module = {
	PyModuleDef_HEAD_INIT,
	"pfloat",
	pfloat_module_docs,
	-1,
	pfloat_functions
};

// Entering point for Python.
PyMODINIT_FUNC PyInit_pfloat(void) {
	return PyModule_Create(&pfloat_module);
}

#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include "pfloat.h"

// Used for doing bitwise operations with float.
union floatint {
	float f;
	uint32_t i;
};

// Used for doing bitwise operations with double.
union doublelong {
    double d;
    uint64_t l;
};

// Retrieve the bits from the float using bitwise operations and write to "result" string.
static void sprint_float_representation(union floatint fi, char *result) {
	for (int i = sizeof (union floatint) * 8 - 1; i >= 0; --i) {
		result[sizeof(union floatint)*8 - 1 - i] = 0x30 + ((fi.i & (1 << i)) >> i);
	}
}

// Retrieve the bits from the double using bitwise operations and write to "result" string.
static void sprint_double_representation(union doublelong dl, char* result) {
	// 1L instead of 1... stupidest bug ever!
	for (int i = sizeof (union doublelong) * 8 - 1; i >= 0; --i) {
        result[sizeof(union doublelong)*8 - 1 - i] = 0x30 + ((int)((dl.l & (1L << i)) >> i));
    }
}

PyObject *pfloat(PyObject *self, PyObject *args) {

	// Fail if float is not 32 bits or double is not 64 bits.
    static_assert(sizeof(float) == sizeof(uint32_t), "Size of float is not 32 bit on your system. Compilation aborted.\n");
    static_assert(sizeof(double) == sizeof(uint64_t), "Size of double is not 64 bit on your system. Compilation aborted.\n");

    static union floatint fi;
    static union doublelong dl;

	// The string that will hold the bits.
	char result[sizeof (union doublelong) * 8] = {0};

	// Parse the args from Python.
	// The args must be of type (String, String).
	char *prec, *number;
	if (!PyArg_ParseTuple(args, "ss", &number, &prec)) {
		return NULL;
	}

	// If the precision is specified as "FLOAT".
	if (!strcasecmp(prec, "FLOAT")) {
		// Parse the "number" and assign it to the union.
		fi.f = (float)atof(number);
		// Calculate the bits and write to "result".
		sprint_float_representation(fi, result);
		// Return Python string.
		return PyUnicode_FromStringAndSize(result, sizeof (union floatint) * 8);
	}
	// If the precision is specified as "DOUBLE".
	else if (!strcasecmp(prec, "DOUBLE")) {
		// Parse the "number" and assign it to the union.
		dl.d = atof(number);
		// Calculate the bits and write to "result".
		sprint_double_representation(dl, result);
		// Return Python string.
		return PyUnicode_FromStringAndSize(result, sizeof (union doublelong) * 8);
	}
	else {
		// Throw ValueError is precision argument is invalid.
		PyErr_SetString(PyExc_ValueError, "The precision argument must either be \"FLOAT\" or \"DOUBLE\"");
		return NULL;
	}

}

#include <Python.h>
#include <windows.h>

PyObject *joyget(PyObject *self, PyObject *args) {
	JOYINFOEX jex;
	jex.dwSize = sizeof(JOYINFOEX);
	jex.dwFlags = JOY_RETURNALL;
	joyGetPosEx( 0, &jex );
	
	int pov;
	pov = jex.dwPOV / 4500;
	int x;
	x = 0;
	int y;
	y = 0;
	
	switch(pov) {
		case 0:
			y = -1;
			break;
		case 1:
			y = -1;
			x = 1;
			break;
		case 2:
			x = 1;
			break;
		case 3:
			x = 1;
			y = 1;
			break;
		case 4:
			y = 1;
			break;
		case 5:
			y = 1;
			x = -1;
			break;
		case 6:
			x = -1;
			break;
		case 7:
			x = -1;
			y = -1;
			break;
	}
	
	PyObject *result;
	result = Py_BuildValue("iii", x, y, jex.dwButtons);
	return result;
}

static PyMethodDef module_methods[] = {
	{ "joyget", joyget, METH_NOARGS, NULL },
	{ NULL, NULL, 0, NULL }
};

static struct PyModuleDef modules = {
	PyModuleDef_HEAD_INIT,
	"joython",
	NULL,
	-1,
	module_methods
};

PyMODINIT_FUNC PyInit_joython(void) {
	return PyModule_Create( &modules );
}

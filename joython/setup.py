from distutils.core import setup, Extension

m = Extension("joython", libraries = ["winmm"], sources = ["joython.c"])
setup(name = "joython", version = "0.1", ext_modules = [m])

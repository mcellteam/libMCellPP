from distutils.core import setup, Extension

example_module = Extension(
    name='_example',
    sources=['example.cpp', 'example.i'],
    language='c++',
    swig_opts=['-c++']
    )

setup(
    name='example',
    ext_modules=[example_module],
    py_modules=["example"]
    )

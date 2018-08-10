
# HOWTO:
#   Clone and build libCZI:
#     https://github.com/zeiss-microscopy/libCZI
#   Modify include_libCZI path to libCZI/Src location of the cloned git.
#   Modify include_libCZI path to the build location of libCZI (containing the dynamic library).
#   ( python setup.py clean --all )
#   python setup.py build
#   python setup.py install
#   Copy the built libCZI dynamic library to the appropriate lib location (anaconda lib or system lib location)

from setuptools import setup, Extension
import os
import numpy
import sysconfig
import platform

# modify these paths to point at lib czi source and build
include_libCZI = '/home/pwatkins/gits/libCZI/Src'
lib_libCZI = '/home/pwatkins/gits/libCZI/build/Src/libCZI'
#include_libCZI = '/Users/pwatkins/gits/libCZI/Src'
#lib_libCZI = '/Users/pwatkins/gits/libCZI/build/Src/libCZI'

# platform specific compiler options
extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
platform_ = platform.system()
if platform_ == 'Linux':
    os.environ["CC"] = "g++-6"; os.environ["CXX"] = "g++-6"
    extra_compile_args += ["-std=c++11", "-Wall", "-O3"]
elif platform_ == 'Darwin':
    extra_compile_args += ["-std=c++11", "-Wall", "-O3", "-stdlib=libc++", "-mmacosx-version-min=10.9"]
elif platform_ == 'Windows':
    # xxx - tests required here for windows
    pass

extra_link_args = sysconfig.get_config_var('LDFLAGS').split()
extra_link_args += extra_compile_args

sources = ['_pylibczi.cpp']

module1 = Extension('_pylibczi',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = ['/usr/local/include', numpy.get_include(), include_libCZI],
                    libraries = ['libCZI'],
                    library_dirs = ['/usr/local/lib', lib_libCZI],
                    sources = [os.path.join('_pylibczi',x) for x in sources],
                    extra_compile_args=extra_compile_args,
                    extra_link_args=extra_link_args,
                    language='c++11',
                    )

setup (name = 'pylibczi',
       version = '0.1',
       description = 'Python wrapper for libCZI',
       author = 'Paul Watkins',
       author_email = 'pwatkins@gmail.com',
       url = '',
       long_description = '''
Expose simple read image and meta data for Zeiss czifiles.
''',
       ext_modules = [module1],
       packages = ['pylibczi'],
       )

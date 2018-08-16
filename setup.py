# The MIT License (MIT)
#
# Copyright (c) 2018 Center of Advanced European Studies and Research (caesar)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from setuptools import setup, Extension
import sys, os
#import glob
import numpy
import sysconfig
import platform
import subprocess

# several platform specifc build options
platform_ = platform.system()

# libczi cloned as submodule, get paths to library and build locations.
script_dir = os.path.dirname(os.path.abspath(__file__))
libczi_dir = os.path.join(script_dir, 'libCZI')
build_temp = os.path.join(libczi_dir,'build')
include_libCZI = os.path.join(libczi_dir, 'Src')
lib_libCZI = os.path.join(build_temp, 'Src', 'libCZI')
lib_JxrDecode = os.path.join(build_temp, 'Src', 'JxrDecode')


def build_libCZI():
    env = os.environ.copy()
    cmake_args = ['-DCMAKE_BUILD_TYPE:STRING=Release']
    build_args = []
    if not os.path.exists(build_temp):
        os.makedirs(build_temp)
    try:
        cmake_exe = os.path.join(os.path.dirname(sys.executable), 'cmake')
        subprocess.check_call([cmake_exe, libczi_dir] + cmake_args, cwd=build_temp, env=env)
        subprocess.check_call([cmake_exe, '--build', '.'] + build_args, cwd=build_temp)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise
build_libCZI()


# xxx - so far this was only needed for manylinux, expose as option to setup.py build somehow?
build_static = False

# platform specific compiler / linker options
extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
extra_link_args = sysconfig.get_config_var('LDFLAGS').split()
extra_compile_args += ["-std=c++11", "-Wall", "-O3"]
if platform_ == 'Linux':
    build_static = True
    extra_compile_args += ["-fPIC"]
    if build_static:
        # need to link with g++ linker for static libstdc++ to work
        os.environ["LDSHARED"] = os.environ["CXX"] if 'CXX' in os.environ else 'g++'
        extra_link_args += ['-static-libstdc++', '-shared']
        #extra_link_args += ["-Wl,--no-undefined"] # will not work with manylinux
elif platform_ == 'Darwin':
    mac_ver = platform.mac_ver()[0]
    extra_compile_args += ["-stdlib=libc++", "-mmacosx-version-min="+mac_ver]
elif platform_ == 'Windows':
    assert(False) # xxx - not tested on windows
extra_link_args += extra_compile_args

include_dirs = [numpy.get_include(), include_libCZI]

static_libraries = []
static_lib_dirs = []
libraries = []
library_dirs = []
extra_objects = []
if build_static:
    static_libraries += ['libCZIStatic', 'JxrDecodeStatic']
    static_lib_dirs += [lib_libCZI, lib_JxrDecode]
else:
    libraries += ['libCZI']
    library_dirs += [lib_libCZI]

# second answer at
# https://stackoverflow.com/questions/4597228/how-to-statically-link-a-library-when-compiling-a-python-module-extension
if platform_ == 'Windows':
    libraries.extend(static_libraries)
    library_dirs.extend(static_lib_dirs)
else: # POSIX
    extra_objects += ['{}/lib{}.a'.format(d, l) for d,l in zip(static_lib_dirs, static_libraries)]
    include_dirs.append('/usr/local/include')
    library_dirs.append('/usr/local/lib')

sources = ['_pylibczi.cpp']

module1 = Extension('_pylibczi',
                    define_macros = [('MAJOR_VERSION', '0'),
                                     ('MINOR_VERSION', '1')],
                    include_dirs = include_dirs,
                    libraries = libraries,
                    library_dirs = library_dirs,
                    sources = [os.path.join('_pylibczi',x) for x in sources],
                    extra_compile_args=extra_compile_args,
                    extra_link_args=extra_link_args,
                    language='c++11',
                    extra_objects=extra_objects,
                    )


# xxx - keeping here for reference, this copy works, but decided to link statically
# install the libCZI library into the module directory
#files = glob.glob(os.path.join(lib_libCZI,'*.so'))

install_requires = ['numpy', 'scipy', 'lxml', 'scikit-image', 'matplotlib', 'tifffile']

setup (name = 'pylibczi',
       version=open("pylibczi/_version.py").readlines()[-1].split()[-1].strip("\"'"),
       description = 'Python module utilizing libCZI for reading Zeiss CZI files.',
       author = 'Paul Watkins',
       author_email = 'pwatkins@gmail.com',
       url = 'https://github.com/elhuhdron/pylibczi',
       long_description = '''
Python module to expose libCZI functionality for reading (subset of) Zeiss CZI files and meta-data.
''',
       ext_modules = [module1],
       packages = ['pylibczi'],
       install_requires = install_requires,
       #data_files = files,
       )

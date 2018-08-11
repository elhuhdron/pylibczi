
from setuptools import setup, Extension
import os
import numpy
import sysconfig
import platform
import subprocess


def build_libCZI():
    env = os.environ.copy()
    cmake_args = ['-DCMAKE_BUILD_TYPE:STRING=Release']
    build_args = []
    build_temp = os.path.join('.','libCZI','build')
    if not os.path.exists(build_temp):
        os.makedirs(build_temp)
    try:
        subprocess.check_call(['cmake', '..'] + cmake_args, cwd=build_temp, env=env)
        subprocess.check_call(['cmake', '--build', '.'] + build_args, cwd=build_temp)
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise
build_libCZI()


# platform specific compiler options
extra_compile_args = sysconfig.get_config_var('CFLAGS').split()
extra_link_args = sysconfig.get_config_var('LDFLAGS').split()
platform_ = platform.system()
if platform_ == 'Linux':
    #os.environ["CC"] = "g++-6"; os.environ["CXX"] = "g++-6"
    extra_compile_args += ["-std=c++11", "-Wall", "-O3"]
    extra_compile_args += ["-static-libstdc++", "-static-libgcc", "-static"]
    extra_link_args += ["-Wl,--no-undefined"]
elif platform_ == 'Darwin':
    mac_ver = platform.mac_ver()[0]
    extra_compile_args += ["-std=c++11", "-Wall", "-O3", "-stdlib=libc++", "-mmacosx-version-min="+mac_ver]
elif platform_ == 'Windows':
    assert(False) # xxx - not tested on windows
extra_link_args += extra_compile_args


# libczi cloned as submodule
include_libCZI = os.path.join('.', 'libCZI', 'Src')
lib_libCZI = os.path.join('.', 'libCZI', 'build', 'Src', 'libCZI')
lib_JxrDecode = os.path.join('.', 'libCZI', 'build', 'Src', 'JxrDecode')

# second answer at
# https://stackoverflow.com/questions/4597228/how-to-statically-link-a-library-when-compiling-a-python-module-extension
static_libraries = ['libCZIStatic', 'JxrDecodeStatic']
static_lib_dirs = [lib_libCZI, lib_JxrDecode]
libraries = []
library_dirs = []
include_dirs = [numpy.get_include(), include_libCZI]

if platform_ == 'Windows':
    libraries.extend(static_libraries)
    library_dirs.extend(static_lib_dirs)
    extra_objects = []
else: # POSIX
    extra_objects = ['{}/lib{}.a'.format(d, l) for d,l in zip(static_lib_dirs, static_libraries)]
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

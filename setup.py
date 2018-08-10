
from setuptools import setup, Extension
import os
import numpy
import sysconfig
import platform
import subprocess

# libczi cloned as submodule
include_libCZI = os.path.join('.', 'libCZI', 'Src')
lib_libCZI = os.path.join('.', 'libCZI', 'build', 'Src', 'libCZI')


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
platform_ = platform.system()
if platform_ == 'Linux':
    #os.environ["CC"] = "g++-6"; os.environ["CXX"] = "g++-6"
    extra_compile_args += ["-std=c++11", "-Wall", "-O3"]
elif platform_ == 'Darwin':
    extra_compile_args += ["-std=c++11", "-Wall", "-O3", "-stdlib=libc++", "-mmacosx-version-min=10.9"]
elif platform_ == 'Windows':
    assert(False) # xxx - not tested on windows

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

#!/bin/bash
set -e -x

# Install a system package required by our library
yum install -y libpng-devel zlib-devel

# Install newer devtools that work on manylinux
GCCAR=gcc-7.3-centos5-x86-64.tar.bz2
curl -o ${GCCAR} -L https://github.com/Noctem/pogeo-toolchain/releases/download/v1.5/${GCCAR}
tar xvjf ${GCCAR}
export CC=/toolchain/bin/gcc
export CXX=/toolchain/bin/g++

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install -r /io/dev-requirements.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install pylibczi --no-index -f /io/wheelhouse
    #(cd "$HOME"; "${PYBIN}/nosetests" pymanylinuxdemo)
done

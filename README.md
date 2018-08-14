# pylibczi
Python module to expose [libCZI](https://github.com/zeiss-microscopy/libCZI) functionality for reading (subset of) Zeiss CZI files and meta-data.

## Requirements

libCZI requires a c++11 compatible compiler.
Development requirements are those required for libCZI: libpng, zlib

## Installation

Clone the repository including submodules with `--recurse-submodules`

python (and pip) install steps maybe require admin privileges (sudo) depending on where python is installed on your system.

Install the python requirements:
```
pip install -r dev-requirements.txt
pip install -r requirements.txt
```

Next build and install using `setup.py`. 
```
python setup.py install
```

libCZI is automatically built by `setup.py`, but the binary needs to be copied to a system path, for example in Linux:
```
sudo cp libCZI/build/Src/libCZI/liblibCZI.so /usr/local/lib
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
```

## Usage

For example usage, see [`sample.py`](sample.py). Replace `test.czi` with your own CZI file containing scenes.

## Documentation

[Documentation](https://pylibczi.readthedocs.io/en/latest/index.html) is available on readthedocs.


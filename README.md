# pylibczi
Python module to expose [libCZI](https://github.com/zeiss-microscopy/libCZI) functionality for reading (subset of) Zeiss CZI files and meta-data.

## Installation

Clone the repository including submodules with `--recurse-submodules`

[libCZI](https://github.com/zeiss-microscopy/libCZI) needs to be built and installed in a system path first, for example in Linux:
```
cd libCZI
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE:STRING=Release
cmake --build .
sudo cp Src/libCZI/liblibCZI.so /usr/local/lib
```

Next build and install using setup.py:
```
python setup.py install
```

## Usage

For example usage, see [`sample.py`](sample.py)

## Documentation

[Documentation](https://pylibczi.readthedocs.io/en/latest/index.html) is available on readthedocs.


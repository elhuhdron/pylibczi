# pylibczi

Python module to expose [libCZI](https://github.com/zeiss-microscopy/libCZI) functionality for reading (subset of) Zeiss CZI files and meta-data.

## Installation

The preferred installation method is with `pip install`. This will intall the pylibczi python module and extension binaries ([hosted on PyPI](https://pypi.org/project/pylibczi/)) and also the dependency requirements:
```
pip install pylibczi
pip install -r requirements.txt
```

## Usage

For example usage, see [`sample.py`](sample.py). Replace `test.czi` with your own CZI file containing scenes.

## Documentation

[Documentation](https://pylibczi.readthedocs.io/en/latest/index.html) is available on readthedocs.

## Build

Use these steps to build and install pylibczi locally:

* Clone the repository including submodules (`--recurse-submodules`).
* Requirements:
  * libCZI requires a c++11 compatible compiler.
  * Development requirements are those required for libCZI: **libpng**, **zlib**
  * Install the python requirements:
    ```
    pip install -r requirements.txt
    ```
* Build and install:
  ```
  python setup.py install
  ```
  * libCZI is automatically built as a submodule and linked statically to pylibczi.


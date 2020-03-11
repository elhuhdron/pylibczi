**NOTE: aicspylibczi**  This project has been forked and made into a much more general tool for reading czi files by developers at the Allen Institute for Cell Science at the Allen Institute. Please try this version with ``pip install aicspylibczi`` or visit the [fork homepage](https://github.com/AllenCellModeling/aicspylibczi).

# pylibczi

Python module to expose [libCZI](https://github.com/zeiss-microscopy/libCZI) functionality for reading (subset of) Zeiss CZI files and meta-data.

## Installation

The preferred installation method is with `pip install`.
This will intall the pylibczi python module and extension binaries ([hosted on PyPI](https://pypi.org/project/pylibczi/)):
```
pip install pylibczi
```

## Usage

For example usage, see [`sample.py`](sample.py).
In the first example, replace `test.czi` with your own CZI file containing scenes.
In the second example, replace `test2.czi` with your own CZI file containing grayscale or BGR48 image data.
The latter is a more generic reader for reading and assembling all subblocks.

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
    pip install -r dev-requirements.txt
    ```
* Build and install:
  ```
  python setup.py install
  ```
  * libCZI is automatically built as a submodule and linked statically to pylibczi.


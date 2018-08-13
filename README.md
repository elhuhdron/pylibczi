# pylibczi
Python module to expose [libCZI](https://github.com/zeiss-microscopy/libCZI) functionality for reading (subset of) Zeiss CZI files and meta-data.

libCZI needs to be built and installed in a system path first, for example in Linux:
```
cd libCZI
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE:STRING=Release
cmake --build .
sudo cp Src/libCZI/liblibCZI.so /usr/local/lib
```

pylibczi [documentation](https://pylibczi.readthedocs.io/en/latest/index.html) is available on readthedocs.

For example usage, see [`sample.py`](sample.py)


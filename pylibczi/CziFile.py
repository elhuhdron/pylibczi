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

# Parent class for python wrapper to libczi file for accessing Zeiss czi image and metadata.

import numpy as np
import time
#import os

from lxml import etree as etree

class CziFile(object):
    """Zeiss CZI file object.

    Parent class for pylibczi.

    .. note::

       Utilizes compiled wrapper to libCZI for accessing the CZI file.

    """

    # how many calibration markers to read in, this should essentially be a constant
    nmarkers = 3
    
    # xxx - likely this is a Zeiss bug, 
    #   units for the scale in the xml file are not correct (says microns, given in meters)
    scale_units = 1e6

    # whether to use czifile or pylibczi for reading the czi file
    use_pylibczi = True
    # how to load the czi file
    if use_pylibczi:
        import _pylibczi
        czilib = _pylibczi
    else:
        # https://www.lfd.uci.edu/~gohlke/code/czifile.py.html
        import czifile
        czilib = czifile
        
    def __init__(self, czi_filename, metafile_out='', verbose=False):
        """Initialize a czifile class.

        Args:
           czi_filename (str): Filename of czifile to access.

        Kwargs:
           metafile_out (str): Filename of xml file to optionally export czi meta data to.
           verbose (bool): Print information and times during czi file access.
           
        """
        self.czi_filename = czi_filename
        self.metafile_out = metafile_out

    def read_meta(self):
        """Extract all metadata from czifile.

        Attributes Modified:
            meta_root (etree): xml class containing root of the extracted meta data.
            
        """
        if self.use_pylibczi:
            self.meta_root = etree.fromstring(self.czilib.cziread_meta(self.czi_filename))
        else:
            # get the root of the metadata xml
            #root = ET.fromstring(metastr) # to convert to python etree
            self.meta_root = self.czi.metadata.getroottree()

        if self.metafile_out:
            metastr = etree.tostring(self.meta_root, pretty_print=True).decode('utf-8')
            with open(self.metafile_out, 'w') as file:
                file.write(metastr)

    def read_all_scenes_image(self, verbose=False):
        if verbose:
            print('Loading czi image for all scenes'); t = time.time()
            
        if CziFile.use_pylibczi:
            imgs, coords = CziFile.czilib.cziread_allsubblocks(self.czi_filename)
            #print('\tGot %d subblocks' % (len(imgs)))
            # xxx - put a simpler montage as a class method (moved back to msem)
            #img, _ = czifile.montage(imgs, coords)
        else:
            # (?, scenes, ?, xdim, ydim, colors?)
            img = np.squeeze(CziFile.czilib.CziFile(self.czi_filename).asarray())
            assert( img.ndim == 2 ) # multiple colors or other dims?

        if verbose:
            print('\tdone in %.4f s' % (time.time() - t, ))
            print('\tAll scenes size is %d x %d' % (img.shape[0], img.shape[1]))
            
        return img

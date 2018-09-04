# This file is part of pylibczi.
# Copyright (c) 2018 Center of Advanced European Studies and Research (caesar)
#
# pylibczi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pylibczi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pylibczi.  If not, see <https://www.gnu.org/licenses/>.

# Parent class for python wrapper to libczi file for accessing Zeiss czi image and metadata.

import numpy as np
import time
#import os

from lxml import etree as etree

class CziFile(object):
    """Zeiss CZI file object.

      Args:
        |  czi_filename (str): Filename of czifile to access.

      Kwargs:
        |  metafile_out (str): Filename of xml file to optionally export czi meta data to.
        |  use_pylibczi (bool): Set to false to use Christoph Gohlke's czifile reader instead of libCZI.
        |  verbose (bool): Print information and times during czi file access.

    .. note::

       Utilizes compiled wrapper to libCZI for accessing the CZI file.

    """

    # how many calibration markers to read in, this should essentially be a constant
    nmarkers = 3
    
    # xxx - likely this is a Zeiss bug, 
    #   units for the scale in the xml file are not correct (says microns, given in meters)
    scale_units = 1e6
        
    def __init__(self, czi_filename, metafile_out='', use_pylibczi=True, verbose=False):
        self.czi_filename = czi_filename
        self.metafile_out = metafile_out
        self.czifile_verbose = verbose

        # whether to use czifile or pylibczi for reading the czi file.
        self.use_pylibczi = use_pylibczi
        if use_pylibczi:
            import _pylibczi
            self.czilib = _pylibczi
        else:
            # https://www.lfd.uci.edu/~gohlke/code/czifile.py.html
            import czifile
            self.czilib = czifile

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

    def read_image(self):
        """Read image data from all subblocks and create single montaged image.

        Returns:
          |  (m,n ndarray):  Montaged image from all subblocks.
          |  (nimages, 2): Integer subscripts where subblocks were placed in montaged image.
            
        """
        
        if self.czifile_verbose:
            print('Loading czi image for all scenes'); t = time.time()
            
        if self.use_pylibczi:
            imgs, coords = self.czilib.cziread_allsubblocks(self.czi_filename)
            img, _ = CziFile._montage(imgs, coords)
            # xxx - this does not work for czifiles for which the subblocks have no dimension label.
            #   additionally it seems not possible to create an accessor without specifying a dimension label / index.
            #img = self.czilib.cziread_scene(self.czi_filename, -np.ones((1,), dtype=np.int64))
        else:
            # (?, scenes, ?, xdim, ydim, colors?)
            img = np.squeeze(self.czilib.CziFile(self.czi_filename).asarray())
            assert( img.ndim == 2 ) # multiple colors or other dims?

        if self.czifile_verbose:
            print('\tdone in %.4f s' % (time.time() - t, ))
            print('\tAll scenes size is %d x %d' % (img.shape[0], img.shape[1]))
            
        return img

    @staticmethod
    def plot_image(image, figno=1, doplots_ds=8, reduce=np.mean, interp_string='nearest', show=True):
        """Generic image plot using matplotlib.

        Kwargs:
          |  figno (int): Figure number to use.
          |  doplots_ds (int): Downsampling reduce factor before plotting.
          |  reduce (func): Function to use for block-reduce downsampling.
          |  interp_string (str): Interpolation string for matplotlib imshow.
          |  show (bool): Whether to show images or return immediately.
           
        """
        from matplotlib import pylab as pl
        import skimage.measure as measure
        
        img_ds = measure.block_reduce(image, block_size=(doplots_ds, doplots_ds), 
                                      func=reduce).astype(image.dtype) if doplots_ds > 1 else image
    
        pl.figure(figno)
        ax = pl.subplot(1,1,1)
        ax.imshow(img_ds,interpolation=interp_string, cmap='gray')
        pl.axis('off')

        if show: pl.show()

    @staticmethod
    def _montage(images, coords, bg=0):
        nimages = len(images)
        
        # images should be the same datatype, get the datatype.
        sel = np.array([x is None for x in images])
        fnz = np.nonzero(np.logical_not(sel))[0][0]
        img_dtype = images[fnz].dtype
        
        # get the sizes of all the images.
        img_shapes = np.vstack(np.array([x.shape if x is not None else (0,0) for x in images]))
        
        # calculate size and allocate output image.
        corners = coords.astype(np.double, copy=True)
        corners -= np.nanmin(corners, axis=0)
        sz_out = np.ceil(np.nanmax(corners + img_shapes[:,::-1], axis=0)).astype(np.int64)[::-1]
        image = np.empty(sz_out, dtype=img_dtype); image.fill(bg)

        # convert the image coorners to subscripts.
        corners = np.round(corners).astype(np.int64)
        c = corners[:,::-1]
        
        for i in range(nimages):
            if images[i] is None: continue
            s = img_shapes[i,:]
            image[c[i,0]:c[i,0]+s[0],c[i,1]:c[i,1]+s[1]] = images[i]

        return image, corners

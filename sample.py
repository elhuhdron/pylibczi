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

from matplotlib import pylab as pl

# Read a scene from a czi file containing scene and ROI data.
from pylibczi import CziScene

scene = CziScene('test.czi', scene=1, verbose=True)
img, polygons_points, rois_points, box_corner_pix, box_size_pix = scene.get_scene_info()
scene.plot_scene(figno=3, doplots_ds=16, show=False)

# Load single image from all subblocks in a czi file.
# NOTE: Currently this might not work with libCZI reader.
#   In this case, install Christoph Gohlke's czifile reader (pip install czifile) and set use_pylibczi to False.
from pylibczi import CziFile

czifile = CziFile('test2.czi', use_pylibczi=True, verbose=True)
CziFile.plot_image(czifile.read_image(), figno=4, doplots_ds=16, show=False)

pl.show()

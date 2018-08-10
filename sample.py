
from pylibczi import CziScene

scene = CziScene('test.czi', scene=1, verbose=True)
img, polygons_points, rois_points, box_corner_pix, box_size_pix = scene.get_scene_info()
scene.plot_scene(figno=3, doplots_ds=16)

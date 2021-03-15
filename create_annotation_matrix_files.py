import glob
import os
import sys

import natsort
import numpy as np
from scipy.io import savemat
from scipy.ndimage import label, zoom
from skimage.io import imread


def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("Path {} already exists, might be overwriting data".format(path))

input_path = os.path.abspath(sys.argv[1])
output_path = os.path.abspath(sys.argv[2])
create_dir_if_not_exists(output_path)
print(input_path, output_path)
downsample_factor = 3
factor = 2 ** (downsample_factor - 1)
image_paths = natsort.natsorted(
    glob.glob(os.path.join(input_path, "*.png")))

for path in image_paths:
    img = imread(path)
    ann_type = zoom(img, factor, order=0)
    binary_image = np.zeros_like(ann_type)
    binary_image[ann_type != 0] = 1
    ann_inst, num_cells = label(binary_image)
    assert np.unique(
        ann_inst).tolist() == list(range(0, np.amax(ann_inst) + 1))
    mdict = {"inst_map": ann_inst, "type_map": ann_type}
    output_mat_path = os.path.join(
        output_path, os.path.basename(path).split(".")[0] + ".mat")
    print(path, output_mat_path)
    savemat(
        output_mat_path,
        mdict)

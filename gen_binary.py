from misc.viz_utils import visualize_instances_dict
import numpy as np
import json
from skimage import io
import cv2
import zarr
import sys, getopt, os
import slideio

'''
Converts all json files in a folder to binary zarr.
The corresponding svs files also need to be present to obtain height and width.
All 3 files will have the same name.
Sample call: python gen_binary.py -i /mnt/ibm_lg/snigdha/svs -o /mnt/ibm_lg/snigdha/svs --rerun_zarr_creation False
'''


def main(argv):
	path = ''
	output_path = ''
	rerun_zarr_creation = False
	try:
		opts, args = getopt.getopt(argv,"i:o:",["svs_path=","zarr_path=","rerun_zarr_creation="])
	except getopt.GetoptError:
		print('gen_binary.py -i <svs_path> -o <zarr_path> <rerun_zarr_creation>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--svs_path"):
			path = arg
		elif opt in ("-o", "--zarr_path"):
			output_path = arg
		elif opt in ("--rerun_zarr_creation"):
			rerun_zarr_creation = True


	for file in os.listdir(path):
		inputfile = os.path.join(path,file)
		# processing each json file
		if file.endswith(".json"):
			if os.path.exists(os.path.join(output_path,file.split('.')[0]+".zarr")):
				if not rerun_zarr_creation:
					print("Binary already exists for ", inputfile)
					sys.exit()
			f = open(inputfile)
			print("Loading json file ", inputfile)
			data = json.load(f)
			type_info = {"0" : ["nolabe", [255,255,255]]}
			print("Extracting contour coordinates")
			tile_info_dict = {}
			for i in data['nuc']:
				contour = data['nuc'][str(i)]['contour']
				x_s = [a_tuple[0] for a_tuple in contour]
				y_s = [a_tuple[1] for a_tuple in contour]
				coords = np.empty((len(x_s),2))
				coords[:,0] = x_s
				coords[:,1] = y_s
				tile_info_dict[i] = {'contour': np.int0(coords), 'type':'0'}

			print("Obtaining image size from svs file")
			svs = slideio.open_slide(inputfile.split('.')[0]+".svs",'SVS')
			dims = svs.get_scene(0).rect
			# shape of the max magnification level in svs.
			# This is the image that will be overlaid so it's just an empty black image
			r_mask = np.zeros((dims[3], dims[2]), np.uint8)
			print("Obtaining binary image")
			binary_image = visualize_instances_dict(r_mask, tile_info_dict,
							type_colour=type_info,line_thickness=cv2.FILLED)
			zarr.save(os.path.join(output_path,file.split('.')[0]+".zarr"),binary_image)



if __name__ == "__main__":
   main(sys.argv[1:])

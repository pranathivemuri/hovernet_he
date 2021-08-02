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
Sample call: python gen_binary.py -i /mnt/ibm_lg/snigdha/svs -o /mnt/ibm_lg/snigdha/svs
'''
def main(argv):
	path = ''
	output_path = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:h:w:",["in_path=","out_path="])
	except getopt.GetoptError:
		print('gen_binary.py -i <in_path> -o <output_path>')
		sys.exit(2)

	for opt, arg in opts:
		if opt in ("-i", "--in_path"):
			path = arg
		elif opt in ("-o", "--out_path"):
			output_path = arg

	for file in os.listdir(path):
		# processing each json file
		if file.endswith(".json"):
			inputfile = os.path.join(path,file)
			# no need to run the process if the binary zarr already exists
			if not os.path.exists(inputfile.split('.')[0]+".zarr"):
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
				print("Obtaining overlaid output")
				binary_image = visualize_instances_dict(r_mask, tile_info_dict,
								type_colour=type_info,line_thickness=cv2.FILLED)
				zarr.save(os.path.join(output_path,inputfile.split('.')[0]+".zarr"),binary_image)
			else:
				print("Binary already exists for ", inputfile)

if __name__ == "__main__":
   main(sys.argv[1:])

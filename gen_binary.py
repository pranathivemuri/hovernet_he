from misc.viz_utils import visualize_instances_dict
import numpy as np
import json
from skimage import io
import cv2
import zarr
import sys, getopt, os

'''
Sample call: gen_binary.py -i "/mnt/ibm_sm/home/snigdha/TSP14 UB B2.json" -o /mnt/ibm_sm/home/snigdha/ -h 67343 -w 143424
'''
def main(argv):
	inputfile = ''
	output_path = ''
	image_height= ''
	image_width = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:h:w:",["in_json=","out_path=","im_height=","im_width="])
	except getopt.GetoptError:
		print('gen_binary.py -i <input_json_file> -o <output_path> -h <image_height> -w <im_width>')
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-i", "--in_json"):
			if arg.split('.')[1]=='json':
				inputfile = arg
			else:
				print('gen_binary.py -i <input_json_file> ...')
				sys.exit(2)
		elif opt in ("-o", "--out_path"):
			output_path = arg
		elif opt in ("-h", "--im_height"):
			image_height = int(arg)
		elif opt in ("-w", "--im_width"):
			image_width = int(arg)


	f = open(inputfile)
	print("Loading json file")
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

	# shape of the max magnification level in svs.
	# This is the image that will be overlaid so it's just an empty black image
	r_mask = np.zeros((image_height, image_width), np.uint8)
	print("Obtaining overlaid output")
	overlaid_output = visualize_instances_dict(r_mask, tile_info_dict, type_colour=type_info,line_thickness=cv2.FILLED)
	zarr.save(os.path.join(output_path,inputfile.split('.')[0]+".zarr"),overlaid_output)

if __name__ == "__main__":
   main(sys.argv[1:])

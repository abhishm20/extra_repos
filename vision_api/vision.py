import json
from utils_google import get_vision_api
from utils_image import (read_image, read_image_base64, save_image, draw_face, draw_box, draw_text)

inputfile  = "IMG_1067.jpg"
outputfile = "output.jpg"

def main():

	vision = get_vision_api()
	
	body = make_request(inputfile)
	response = vision.images().annotate(body=body).execute()
	
	show_results(inputfile, response, outputfile)
	
def make_request(inputfile):
	""" Create a request batch (one file at a time) """
	return {
		"requests":[
			{
				"image":{
	    				"content": read_image_base64(inputfile)
	    			},
				"features": [
					{
						"type":"LABEL_DETECTION",
      						"maxResults": 10
      					},
      					{
      						"type":"TEXT_DETECTION",
      						"maxResults": 10
      					}
      				]
			}
		]
	}

def show_results(inputfile, data, outputfile):

	#read original file
	im = read_image(inputfile)

	#draw face, boxes and text for each response
	for r in data['responses']:

		if 'faceAnnotations' in r:
			draw_face(im, r['faceAnnotations'])

		if 'labelAnnotations' in r:
			strs = map(lambda a: a['description'], r['labelAnnotations'])
			im = draw_text(im, ", ".join(strs))

		for field in ['textAnnotations', 'logoAnnotations']:
			if field in r:
				for a in r[field]:
					draw_box(im, a['boundingPoly']['vertices'])

	#save to output file
	save_image(outputfile, im)

if __name__ == '__main__':
	main()
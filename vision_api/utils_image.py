import cv2
from base64 import b64encode

""" read/write utilities """

def read_image(filename):
	return cv2.imread(filename)

def save_image(filename, im):
	cv2.imwrite(filename, im)

def read_image_base64(filename):
	with open(filename, 'rb') as f:
		return b64encode(f.read())


""" OpenCV drawing utilities """

def draw_face(im, annotations):
	for a in annotations:
		tl ,br  = draw_box(im, a['boundingPoly']['vertices'])
		tl_,br_ = draw_box(im, a['fdBoundingPoly']['vertices'])
		draw_angle(im, a['panAngle'], a['tiltAngle'], pt=tl_, size=br_[0]-tl_[0])
		for landmark in a['landmarks']:
			draw_point(im, landmark['position'])
		
def draw_angle(im, pan, tilt, pt, size):
	x_delta = np.interp(pan,  [-180,180], [-size,size])
	y_delta = np.interp(tilt, [-180,180], [-size,size])
	pt2 = (pt[0] + int(x_delta), pt[1] + int(y_delta))
	cv2.arrowedLine(im, pt, pt2, (0,255,0))


def extract_vertices(vertices):
	""" Extract two opposite vertices from a list of 4 (assumption: rectangle) """

	min_x,max_x,min_y,max_y = float("inf"),float("-inf"),float("inf"),float("-inf")

	for v in vertices:
		if v.get('x',min_y) < min_x:
			min_x = v.get('x')
		if v.get('x',max_y) > max_x:
			max_x = v.get('x')
		if v.get('y',min_y) < min_y:
			min_y = v.get('y')
		if v.get('y',max_y) > max_y:
			max_y = v.get('y')

	v1 = next(v for v in vertices if v.get('x') == min_x and v.get('y') == min_y)
	v2 = next(v for v in vertices if v.get('x') == max_x and v.get('y') == max_y)

	return v1,v2


def draw_box(im, vertices):
	v1,v2 = extract_vertices(vertices)
	pt1 = (v1.get('x',0), v1.get('y',0))
	pt2 = (v2.get('x',0), v2.get('y',0))
	cv2.rectangle(im, pt1, pt2, (0,0,255))
	return pt1, pt2

def draw_point(im, position):
	pt = (int(position.get('x',0)), int(position.get('y',0)))
	cv2.circle(im, pt, 3, (0,0,255))
	return pt

def draw_text(im, text):
	font_face = cv2.FONT_HERSHEY_SIMPLEX
	thickness = 1
	for scale in np.arange(2,0,-0.2):
		(w,h),baseline = cv2.getTextSize(text, font_face, scale, thickness)
		if w <= im.shape[1]:
			new_img = cv2.copyMakeBorder(im, 0, baseline*4, 0, 0, cv2.BORDER_CONSTANT, value=0)
			cv2.putText(new_img, text, (baseline*2,new_img.shape[0]-baseline), font_face, scale, (255,255,255), thickness)
			return new_img
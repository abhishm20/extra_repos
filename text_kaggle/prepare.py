from PIL import Image
import os, sys
import util
from scipy import stats
import csv

import numpy as np
from resizeimage import resizeimage

# outfile = 'resize.jpg'
infile = '1box.png'
# grey = 'greyscale.png'


size = 28, 28


img = Image.open(infile)
cropping = min(img.size)

img = img.crop((0, 0, cropping, cropping))

img.thumbnail(size, Image.ANTIALIAS)

img = util.change_contrast(img,100)

img.convert('LA')

y = np.asarray(img.getdata(),dtype=np.float64)

y = [255-i for i in y]

column = []
for i in range(784):
    column.append('pixel'+str(i))


data = [column, y]
with open('input/test123791823.csv', "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)
import cv2
import numpy as np
import matplotlib
from collections import Counter
import csv
matplotlib.use('TkAgg')
import os, sys
from PIL import Image
from os import listdir
from os.path import isfile, join
import matplotlib.pyplot as plt
import pandas as pd
from PIL import ImageEnhance

infile = 'main.png'
outfile = 'resized.png'

################################################

# Resizing and cropping every digits
size = 1049, 5508

im = Image.open(infile)
im = im.resize(size, Image.ANTIALIAS)
im.save(outfile, "PNG")

img = cv2.imread(outfile, 0)

h, w = 210, 325
x, y = 0,0
for y_c in range(3):
    for x_c in range(3):
        plt.subplot(121), plt.imshow(img, cmap='gray')
        plt.title('Original Image'), plt.xticks([]), plt.yticks([])
        new_img = img[y:y + h, x:x + w]

        cv2.imwrite('digits/' + str(x_c) + str(y_c) + '.png', new_img)

        x += 350

    x = 0
    y += 250

#######################################################

# Chaging contract and saving it to csv

dir_name = 'digits'
size = 28, 28
onlyfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
final_images = []
for img_file in onlyfiles:
    if img_file == '.DS_Store':
        continue
    im = Image.open(os.path.join(dir_name, img_file))
    im = im.resize(size, Image.ANTIALIAS)

    y = np.asarray(im.getdata(),dtype=np.float64)

    mean = np.mean(y)

    y_n = []
    for i in y:
        i = 255-i
        # i = 0 if i >= mean else 255
        y_n.append(i)
    final_images.append(y_n)
    print img_file

    y_n = np.reshape(y_n, (28, 28))
    cv2.imwrite(os.path.join(dir_name, img_file), y_n)

column = []
for i in range(784):
    column.append('pixel' + str(i))

data = [column]
data.extend(final_images)
with open('test.csv', "wb") as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    for line in data:
        writer.writerow(line)


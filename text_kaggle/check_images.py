# read test data from CSV file
from PIL import Image
import os, sys
import util
import cv2
import pandas as pd
from scipy import stats
import csv

import numpy as np
from resizeimage import resizeimage


test_images = pd.read_csv('input/test_full.csv').values
# test_images = test_images.astype(np.float)
# y = np.asarray(im.getdata(), dtype=np.float64)

count = 0
for y_n in test_images:

    y_n = np.reshape(y_n, (28, 28))
    cv2.imwrite(os.path.join('digits', str(count)+'.png'), y_n)
    count += 1
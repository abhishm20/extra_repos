import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt

img = cv2.imread('main.png', 0)

edges = cv2.Canny(img,100,200)

cnts = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[1]

idx = 0
for index,c in enumerate(cnts):
    x,y,w,h = cv2.boundingRect(c)
    if w>50 and h>50:
        idx+=1
        new_img=img[y:y+h,x:x+w]
        cv2.imwrite('outs/'+str(idx) + '.png', new_img)

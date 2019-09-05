import cv2
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# from matplotlib import pyplot as plt

img = cv2.imread('challan.png', 0)

edges = cv2.Canny(img,100,200)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()


# Binarize the image and call it thresh.
thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
thresh = thresh[1]

# Find all the contours in thresh. In your case the 3 and the additional strike
# contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

#
cnts = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[1]
# cnts = sorted(cnts[1], key = cv2.contourArea, reverse = True)[:10]
#
#     print screenCnt
idx = 0
# for index,c in enumerate(cnts):
x,y,w,h = cv2.boundingRect(cnts[474])
if w>50 and h>50:
    idx+=1
    new_img=img[y:y+h,x:x+w]
    cv2.imwrite('outs/'+str(idx) + '.png', new_img)

# cv2.drawContours(imgray, [screenCnt], -1, (230, 55, 10), 3)
#
# x,y,w,h = cv2.boundingRect(screenCnt)
# new_img=imgray[y:y+h,x:x+w]
#
# plt.subplot(121)
# plt.imshow(new_img,'gray')
# plt.show()

#

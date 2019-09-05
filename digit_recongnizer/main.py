import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import tensorflow as tf

# setting
LEARNING_RATE = 1e-4

# set to 20000 to get 99.9 accuracy
TRAINING_ITERATION = 20000

DROPOUT = 0.5
BATCH_SIZE = 50

# set to 0 to train on all available data
VALIDATION_SIZE = 2000

# image number to output
IMAGE_TO_DISPLAY = 10

# read training data from CSV file
data = pd.read_csv('./train.csv')

# print data.shape
# print('data({0[0]},{0[1]})'.format(data.shape))
# print (data.head())


images = data.iloc[:,1:].values
images = images.astype(np.float)

# convert from [0:255] => [0.0:1.0]
images = np.multiply(images, 1.0 / 255.0)

# print('images({0[0]},{0[1]})'.format(images.shape))
# print images


image_size = images.shape[1]
# print ('image_size => {0}'.format(image_size))


# in this case all images are square
image_width = image_height = np.ceil(np.sqrt(image_size)).astype(np.uint8)

# print ('image_width => {0}\nimage_height => {1}'.format(image_width,image_height))


# display image
def display(img):
    # (784) => (28,28)
    one_image = img.reshape(image_width, image_height)
    plt.axis('off')
    plt.imshow(one_image, cmap=cm.binary)
    plt.show()


# output image
# display(images[IMAGE_TO_DISPLAY])

labels_flat = data[[0]].values.ravel()
# print('labels_flat({0})'.format(len(labels_flat)))
# print ('labels_flat[{0}] => {1}'.format(IMAGE_TO_DISPLAY,labels_flat[IMAGE_TO_DISPLAY]))

labels_count = np.unique(labels_flat).shape[0]
# print('labels_count => {0}'.format(labels_count))


def dense_to_one_hot(labels_dense, num_classes):
    num_labels = labels_dense.shape[0]
    index_offset = np.arange(num_labels) * num_classes
    labels_one_hot = np.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot

labels = dense_to_one_hot(labels_flat, labels_count)
labels = labels.astype(np.uint8)

# print labels
# print('labels({0[0]},{0[1]})'.format(labels.shape))
# print ('labels[{0}] => {1}'.format(IMAGE_TO_DISPLAY,labels[IMAGE_TO_DISPLAY]))

# split data into training & validation
validation_images = images[:VALIDATION_SIZE]
validation_labels = labels[:VALIDATION_SIZE]

train_images = images[VALIDATION_SIZE:]
train_labels = labels[VALIDATION_SIZE:]


print('train_images({0[0]},{0[1]})'.format(train_images.shape))
print('validation_images({0[0]},{0[1]})'.format(validation_images.shape))
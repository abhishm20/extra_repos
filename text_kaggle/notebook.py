
# coding: utf-8

# # TensorFlow deep NN
# #### A high-level tutorial into Deep Learning using MNIST data and TensorFlow library.
# by [@kakauandme](https://twitter.com/KaKaUandME) and [@thekoshkina](https://twitter.com/thekoshkina)
# 
# Accuracy: 0.99
# 
# **Prerequisites:** fundamental coding skills, a bit of linear algebra, especially matrix operations and perhaps understanding how images are stored in computer memory. To start with machine learning, we suggest [coursera course](https://www.coursera.org/learn/machine-learning) by Andrew Ng.
# 
# 
# Note: 
# 
# *Feel free to fork and adjust* CONSTANTS *to tweak network behaviour and explore how it changes algorithm performance and accuracy. Besides **TensorFlow graph** section can also be modified for learning purposes.*
# 
# *It is highly recommended printing every variable that isn’t 100% clear for you. Also, [tensorboard](https://www.tensorflow.org/versions/master/how_tos/summaries_and_tensorboard/index.html) can be used on a local environment for visualisation and debugging.*
# ## Libraries and settings

# In[1]:

import numpy as np
import pandas as pd

# get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import tensorflow as tf

# settings
LEARNING_RATE = 1e-4
# set to 20000 on local environment to get 0.99 accuracy
TRAINING_ITERATIONS = 200
    
DROPOUT = 0.5
BATCH_SIZE = 50

# set to 0 to train on all available data
VALIDATION_SIZE = 0

# image number to output
# IMAGE_TO_DISPLAY = 10


# ## Data preparation
# To start, we read provided data. The *train.csv* file contains 42000 rows and 785 columns. Each row represents an image of a handwritten digit and a label with the value of this digit.

# In[3]:

# read training data from CSV file 
data = pd.read_csv('input/train.csv')

print('data({0[0]},{0[1]})'.format(data.shape))

# Every image is a "stretched" array of pixel values.

# In[5]:

images = data.iloc[:,1:].values
images = images.astype(np.float)

# convert from [0:255] => [0.0:1.0]
images = np.multiply(images, 1.0 / 255.0)

# In this case it's 784 pixels => 28 * 28px

# In[6]:

image_size = images.shape[1]

# in this case all images are square
image_width = image_height = np.ceil(np.sqrt(image_size)).astype(np.uint8)


# To output one of the images, we reshape this long string of pixels into a 2-dimensional array, which is basically a grayscale image.

# In[7]:


# The corresponding labels are numbers between 0 and 9, describing which digit a given image is of.

# In[8]:

labels_flat = data[[0]].values.ravel()


# In this case, there are ten different digits/labels/classes.

# In[9]:

labels_count = np.unique(labels_flat).shape[0]

print('labels_count => {0}'.format(labels_count))


# For most classification problems "one-hot vectors" are used. A one-hot vector is a vector that contains a single element equal to 1 and the rest of the elements equal to 0. In this case, the *nth* digit is represented as a zero vector with 1 in the *nth* position.

# In[10]:

# convert class labels from scalars to one-hot vectors
# 0 => [1 0 0 0 0 0 0 0 0 0]
# 1 => [0 1 0 0 0 0 0 0 0 0]
# ...
# 9 => [0 0 0 0 0 0 0 0 0 1]
def dense_to_one_hot(labels_dense, num_classes):
    num_labels = labels_dense.shape[0]
    index_offset = np.arange(num_labels) * num_classes
    labels_one_hot = np.zeros((num_labels, num_classes))
    labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
    return labels_one_hot

labels = dense_to_one_hot(labels_flat, labels_count)
labels = labels.astype(np.uint8)

# Lastly we set aside data for validation. It's essential in machine learning to have a separate dataset which doesn't take part in the training and is used to make sure that what we've learned can actually be generalised.

# In[11]:

# split data into training & validation
validation_images = images[:VALIDATION_SIZE]
validation_labels = labels[:VALIDATION_SIZE]

train_images = images[VALIDATION_SIZE:]
train_labels = labels[VALIDATION_SIZE:]


print('train_images({0[0]},{0[1]})'.format(train_images.shape))
print('validation_images({0[0]},{0[1]})'.format(validation_images.shape))


####################################################################

# weight initialization
def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


# convolution
def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# images
x = tf.placeholder('float', shape=[None, image_size])
# labels
y_ = tf.placeholder('float', shape=[None, labels_count])


# first convolutional layer
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])


# (40000,784) => (40000,28,28,1)
image = tf.reshape(x, [-1,image_width , image_height,1])

h_conv1 = tf.nn.relu(conv2d(image, W_conv1) + b_conv1)

h_pool1 = max_pool_2x2(h_conv1)

# Prepare for visualization
# display 32 fetures in 4 by 8 grid
layer1 = tf.reshape(h_conv1, (-1, image_height, image_width, 4 ,8))

# reorder so the channels are in the first dimension, x and y follow.
layer1 = tf.transpose(layer1, (0, 3, 1, 4,2))

layer1 = tf.reshape(layer1, (-1, image_height*4, image_width*8))

# second convolutional layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

h_pool2 = max_pool_2x2(h_conv2)


# Prepare for visualization
# display 64 fetures in 4 by 16 grid
layer2 = tf.reshape(h_conv2, (-1, 14, 14, 4 ,16))

# reorder so the channels are in the first dimension, x and y follow.
layer2 = tf.transpose(layer2, (0, 3, 1, 4,2))

layer2 = tf.reshape(layer2, (-1, 14*4, 14*16))

# densely connected layer
W_fc1 = weight_variable([7 * 7 * 64, 1024])
b_fc1 = bias_variable([1024])

# (40000, 7, 7, 64) => (40000, 3136)
h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])

h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# dropout
keep_prob = tf.placeholder('float')
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# readout layer for deep net
W_fc2 = weight_variable([1024, labels_count])
b_fc2 = bias_variable([labels_count])

y = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

# cost function
cross_entropy = -tf.reduce_sum(y_*tf.log(y))


# optimisation function
train_step = tf.train.AdamOptimizer(LEARNING_RATE).minimize(cross_entropy)

# evaluation
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'))


predict = tf.argmax(y,1)

epochs_completed = 0
index_in_epoch = 0
num_examples = train_images.shape[0]


# serve data by batches
def next_batch(batch_size):

    global train_images
    global train_labels
    global index_in_epoch
    global epochs_completed

    start = index_in_epoch
    index_in_epoch += batch_size

    # when all trainig data have been already used, it is reorder randomly
    if index_in_epoch > num_examples:
        # finished epoch
        epochs_completed += 1
        # shuffle the data
        perm = np.arange(num_examples)
        np.random.shuffle(perm)
        train_images = train_images[perm]
        train_labels = train_labels[perm]
        # start next epoch
        start = 0
        index_in_epoch = batch_size
        assert batch_size <= num_examples
    end = index_in_epoch
    return train_images[start:end], train_labels[start:end]


# start TensorFlow session
init = tf.initialize_all_variables()
sess = tf.InteractiveSession()

sess.run(init)


# visualisation variables
train_accuracies = []
validation_accuracies = []
x_range = []

display_step=1

for i in range(TRAINING_ITERATIONS):
    # get new batch
    batch_xs, batch_ys = next_batch(BATCH_SIZE)

    if i%display_step == 0 or (i+1) == TRAINING_ITERATIONS:

        train_accuracy = accuracy.eval(feed_dict={x:batch_xs,
                                                  y_: batch_ys,
                                                  keep_prob: 1.0})
        if(VALIDATION_SIZE):
            validation_accuracy = accuracy.eval(feed_dict={ x: validation_images[0:BATCH_SIZE],
                                                            y_: validation_labels[0:BATCH_SIZE],
                                                            keep_prob: 1.0})
            print('training_accuracy / validation_accuracy => %.2f / %.2f for step %d'%(train_accuracy, validation_accuracy, i))

            validation_accuracies.append(validation_accuracy)

        else:
             print('training_accuracy => %.4f for step %d'%(train_accuracy, i))
        train_accuracies.append(train_accuracy)
        x_range.append(i)

        # increase display_step
        if i%(display_step*10) == 0 and i:
            display_step *= 10
    # train on batch
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys, keep_prob: DROPOUT})
#######################################################################

# read test data from CSV file
test_images = pd.read_csv('input/test.csv').values
test_images = test_images.astype(np.float)

# convert from [0:255] => [0.0:1.0]
test_images = np.multiply(test_images, 1.0 / 255.0)

print('test_images({0[0]},{0[1]})'.format(test_images.shape))


# predict test set
predicted_lables = predict.eval(feed_dict={x: test_images, keep_prob: 1.0})

# save results
np.savetxt('submission_softmax.csv',
           np.c_[range(1,len(test_images)+1),predicted_lables],
           delimiter=',',
           header = 'ImageId,Label',
           comments = '',
           fmt='%d')

sess.close()


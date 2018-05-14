#Completely copy-pasted from link

# MNIST For ML Beginners!

# This tutorial is intended for readers who are new to both machine learning and TensorFlow.
# Just like programming has Hello World, machine learning has MNIST.
# MNIST is a simple computer vision dataset. It consists of images of handwritten digits.
# Source: https://goo.gl/rLXVsR

# Please help us to improve this section by sending us your
# feedbacks and comments on: https://docs.google.com/forms/d/16fH20Qf8gJ2o31Vnlss2uLJ7wL9vq76TeUGqghTY0uI/viewform

# Removing annoying warnings
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# Importing input data
import random
import input_data
mnist = input_data.read_data_sets(raw_input(), raw_input(), raw_input())


import tensorflow as tf
################################
# Enter your code between here #
################################

x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)#y_ = tf.placeholder(tf.float32, [None, 1)
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))#train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropytrain_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)
sess = tf.InteractiveSession()
tf.global_variables_initializer().run()
for _ in range(1000):
  batch_xs, batch_ys = mnist.train.next_batch(100)
  sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})
#print ' '.join(map(str, [random.randint(0,9) for _ in range(len(mnist.validation.images))]))
correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
########################
#        And here      #
########################
#print(sess.run(accuracy, feed_dict={x: mnist.test.images, y_: mnist.test.labels}))

# Uncomment to get a prediction number for each image

result = sess.run(tf.argmax(y,1), feed_dict={x: mnist.validation.images})
print ' '.join(map(str, result))
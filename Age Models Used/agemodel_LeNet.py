# -*- coding: utf-8 -*-
"""agemodel.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1f6HSZfjmfEWfEH1atwlHPzceff4XHsll
"""

# Commented out IPython magic to ensure Python compatibility.
import cv2
import numpy as np
import pandas as pd 
import time
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.model_selection import train_test_split
from sklearn.utils import compute_class_weight
# %matplotlib inline

from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report,confusion_matrix
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Input, Dense, Activation, Conv2D, MaxPool2D, AveragePooling2D, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import SGD, RMSprop, Adam



data =  pd.read_csv('data/dataset_age_0_5.csv')

data.head()

len(data)

start = time.time()

try:  
    with tf.device('/device:GPU:1'):
        image_list = []
        for path in data["img_path"]:
            img = cv2.imread(path,cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img,(200,200))
            image_list.append(img)
except RuntimeError as e:
  print(e)
end = time.time()
print("time taken for execution :- {}".format(end-start))

data["image"] = image_list
data.head()

data.info()

plt.imshow(data["image"][1])

try:  
    with tf.device('/device:GPU:2'):
        x_data = np.array(image_list)/255
        y_data = data["age"].to_numpy()
except RuntimeError as e:
  print(e)


print(x_data[1])
print(y_data[1])

x_data.shape
y_data.shape

input_shape = (200, 200, 1)

# image_x will contain the original grayscale images 
x_data = x_data.reshape((x_data.shape[0],200,200,1))

print("x_data shape: {}".format(x_data.shape))
print("y_data shape: {}".format(y_data.shape))


train_x, test_x, train_y, test_y = train_test_split(x_data, y_data, test_size=0.3, random_state=42)

print("train_x shape: {}".format(train_x.shape))
print("train_y shape: {}\n".format(train_y.shape))

print("test_x shape: {}".format(test_x.shape))
print("test_y shape: {}".format(test_y.shape))


num_subjects = np.unique(y_data).shape[0]
print("Number of subjects: {}".format(np.unique(y_data).shape[0]))


try:  
    with tf.device('/device:GPU:1'):

     
        # LeNet model:

        model = Sequential()
        
        # define the first set of con-act-pool layer
        model.add(Conv2D(28, kernel_size=(3,3), padding="same",input_shape=input_shape))
        model.add(Activation("relu"))
        model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
          
        # define the second set of con-act-pool layer
        model.add(Conv2D(28, kernel_size=(3,3), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPool2D(pool_size=(2, 2), strides=(2, 2)))
          
        # define the first FC-ACT layers
        model.add(Flatten())
        model.add(Dense(128))
        model.add(Activation("relu"))
        
        # define the second FC layer
        model.add(Dense(num_subjects))
        
        model.add(Activation("softmax"))
        
        model.summary()
        
        
        model.compile(optimizer='adam', 
                      loss='sparse_categorical_crossentropy', 
                      metrics=['accuracy'])
        history = model.fit(train_x, train_y, epochs=30, validation_data=(test_x, test_y), batch_size=150, verbose=1)

       
except RuntimeError as e:
    print(e)



# evaluate model, get train/test accuracy
train_pred = np.argmax(model.predict(train_x), axis=1)
test_pred = np.argmax(model.predict(test_x), axis=1)
print("\nTraining accuracy of model: {}".format(accuracy_score(train_y, train_pred)))
print("Testing accuracy of model: {}".format(accuracy_score(test_y, test_pred)))

print(classification_report(test_y,test_pred))
print(confusion_matrix(test_y,test_pred))

model.evaluate(test_x,test_y)

model.save('models/agemodel_LeNet.h5')

history.history.keys()

# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('Model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.subplots_adjust(top=1.00, bottom=0.0, left=0.0, right=0.95, hspace=0.25,
                        wspace=0.35)
plt.show()


# summarize history for loss
plt.plot(History.history['loss'])
plt.plot(History.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.subplots_adjust(top=1.00, bottom=0.0, left=0.0, right=0.95, hspace=0.25,
                        wspace=0.35)
plt.show()


history.history['loss']


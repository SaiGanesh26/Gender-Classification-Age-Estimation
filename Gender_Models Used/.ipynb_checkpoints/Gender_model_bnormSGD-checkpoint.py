{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {
    "id": "OFjxF7aqryEG"
   },
   "outputs": [],
   "source": [
    "import cv2\n",
    "import numpy as np\n",
    "import pandas as pd \n",
    "import time\n",
    "import matplotlib.pyplot as plt\n",
    "import matplotlib.image as mpimg\n",
    "from sklearn.model_selection import train_test_split\n",
    "from sklearn.utils import compute_class_weight\n",
    "%matplotlib inline\n",
    "\n",
    "from sklearn.metrics import accuracy_score\n",
    "from sklearn.metrics import classification_report,confusion_matrix\n",
    "import tensorflow as tf\n",
    "from tensorflow.keras.models import Model\n",
    "from tensorflow.keras.layers import Input, Dense, Activation, Conv2D, MaxPool2D, AveragePooling2D, Flatten, Dropout, BatchNormalization\n",
    "from tensorflow.keras.optimizers import SGD, RMSprop, Adam"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Num GPUs Available:  [PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:1', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:2', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:3', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:4', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:5', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:6', device_type='GPU'), PhysicalDevice(name='/physical_device:GPU:7', device_type='GPU')]\n"
     ]
    }
   ],
   "source": [
    "print(\"Num GPUs Available: \", tf.config.experimental.list_physical_devices('GPU'))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "#pip install numba "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "# from numba import cuda\n",
    "\n",
    "# cuda.select_device(0)\n",
    "# cuda.close()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "wiki_process =  pd.read_csv(\"data/dataset.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {
    "colab": {
     "base_uri": "https://localhost:8080/"
    },
    "id": "4r48NY_QJYgf",
    "outputId": "f1b49401-8aa4-4e08-a6fa-2474977001a3"
   },
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>gender</th>\n",
       "      <th>img_path</th>\n",
       "      <th>age</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1.0</td>\n",
       "      <td>wiki_crop/17/10000217_1981-05-05_2009.jpg</td>\n",
       "      <td>27</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1.0</td>\n",
       "      <td>wiki_crop/12/100012_1948-07-03_2008.jpg</td>\n",
       "      <td>59</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>0.0</td>\n",
       "      <td>wiki_crop/16/10002116_1971-05-31_2012.jpg</td>\n",
       "      <td>40</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>0.0</td>\n",
       "      <td>wiki_crop/02/10002702_1960-11-09_2012.jpg</td>\n",
       "      <td>51</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>1.0</td>\n",
       "      <td>wiki_crop/41/10003541_1937-09-27_1971.jpg</td>\n",
       "      <td>33</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   gender                                   img_path  age\n",
       "0     1.0  wiki_crop/17/10000217_1981-05-05_2009.jpg   27\n",
       "1     1.0    wiki_crop/12/100012_1948-07-03_2008.jpg   59\n",
       "2     0.0  wiki_crop/16/10002116_1971-05-31_2012.jpg   40\n",
       "3     0.0  wiki_crop/02/10002702_1960-11-09_2012.jpg   51\n",
       "4     1.0  wiki_crop/41/10003541_1937-09-27_1971.jpg   33"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "wiki_process.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "id": "vipIhXCiww3x"
   },
   "outputs": [],
   "source": [
    "start = time.time()\n",
    "try:  \n",
    "    with tf.device('/device:GPU:2'):\n",
    "        image_list = []\n",
    "        for path in wiki_process[\"img_path\"]:\n",
    "            img = cv2.imread(\"data/\" + path,cv2.IMREAD_GRAYSCALE)\n",
    "            img = cv2.resize(img,(300,300))\n",
    "            image_list.append(img)\n",
    "except RuntimeError as e:\n",
    "  print(e)\n",
    "end = time.time()\n",
    "print(\"time taken for execution :- {}\".format(end-start))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# wiki_process = wiki_process.head(500)\n",
    "wiki_process[\"image\"] = image_list\n",
    "wiki_process.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'wiki_process' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[0;32m<ipython-input-1-8d690c5f8ca2>\u001b[0m in \u001b[0;36m<module>\u001b[0;34m\u001b[0m\n\u001b[0;32m----> 1\u001b[0;31m \u001b[0mwiki_process\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0minfo\u001b[0m\u001b[0;34m(\u001b[0m\u001b[0;34m)\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m",
      "\u001b[0;31mNameError\u001b[0m: name 'wiki_process' is not defined"
     ]
    }
   ],
   "source": [
    "wiki_process.info()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "plt.imshow(wiki_process[\"image\"][39454])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "#normalizing the pixel values\n",
    "try:  \n",
    "    with tf.device('/device:GPU:2'):\n",
    "        x_data = np.array(image_list)/255\n",
    "        y_data = wiki_process[\"gender\"].to_numpy()\n",
    "except RuntimeError as e:\n",
    "  print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "x_data.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "y_data.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# image_x will contain the original grayscale images \n",
    "x_data = x_data.reshape((x_data.shape[0],300,300,1))\n",
    "\n",
    "print(\"x_data shape: {}\".format(x_data.shape))\n",
    "print(\"y_data shape: {}\".format(y_data.shape))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "train_x, test_x, train_y, test_y = train_test_split(x_data, y_data, test_size=0.3, random_state=42)\n",
    "\n",
    "print(\"train_x shape: {}\".format(train_x.shape))\n",
    "print(\"train_y shape: {}\\n\".format(train_y.shape))\n",
    "\n",
    "print(\"test_x shape: {}\".format(test_x.shape))\n",
    "print(\"test_y shape: {}\".format(test_y.shape))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# num_subjects = np.unique(y_data).shape[0]\n",
    "# print(\"Number of subjects: {}\".format(np.unique(y_data).shape[0]))"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "if tf.config.experimental.list_physical_devices('GPU'):\n",
    "    strategy = tf.distribute.MirroredStrategy()\n",
    "else:  # use default strategy\n",
    "    strategy = tf.distribute.get_strategy() \n",
    "print(strategy)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# try:  \n",
    "#     with strategy.scope():\n",
    "#         # specify the input size of the images\n",
    "#         images = Input((train_x.shape[1], train_x.shape[2], 1,))\n",
    "#         # a convolution layer of 32 filters of size 9x9 to extract features (valid padding)\n",
    "#         x = Conv2D(64,kernel_size=(3,3),padding=\"valid\")(images)\n",
    "#         x = Conv2D(64,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "        \n",
    "#         # a maxpooling layer to down-sample features with pool size (2, 2)\n",
    "#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)\n",
    "\n",
    "#         x = Conv2D(128,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(128,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "\n",
    "#         # a maxpooling layer to down-sample features with pool size (2, 2)\n",
    "#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)\n",
    "\n",
    "#         x = Conv2D(256,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(256,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(256,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(256,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "\n",
    "#         # a maxpooling layer to down-sample features with pool size (2, 2)\n",
    "#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)\n",
    "        \n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "\n",
    "#         # a maxpooling layer to down-sample features with pool size (2, 2)\n",
    "#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)\n",
    "        \n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "#         x = Conv2D(512,kernel_size=(3,3),padding=\"valid\")(x)\n",
    "        \n",
    "#         # a maxpooling layer to down-sample features with pool size (2, 2)\n",
    "#         x = MaxPool2D(pool_size=(2,2),strides=2)(x)\n",
    "        \n",
    "#         # flatten extracted features to form feature vector\n",
    "#         x = Flatten()(x)\n",
    "\n",
    "# #         # a drop out layer for regularization (25% probability)\n",
    "# #         x = Dropout(rate=0.2,seed=0.25)(x)\n",
    "        \n",
    "#         first fully-connected layer to map the features to vectors of size 256\n",
    "#         x = Dense(4096,activation=\"relu\")(x)\n",
    "#         x = Dense(4096,activation=\"relu\")(x)\n",
    "#         x = Dense(128,activation=\"relu\")(x)\n",
    "        \n",
    "        \n",
    "# #         # anoter drop out layer for regularization (25% probability)\n",
    "# #         x = Dropout(rate=0.2,seed=0.25)(x)\n",
    "        \n",
    "#         # a second fully-connected layer to map the features to a logit vector with one logit per subject\n",
    "#         x = Dense(1)(x)\n",
    "#         # use softmax activation to convert the logits to class probabilities for each subject\n",
    "#         predictions = Activation(\"sigmoid\")(x)\n",
    "\n",
    "#         # create the model using the layers we defined previously\n",
    "#         sample_cnn = Model(inputs=images, outputs=predictions)\n",
    "\n",
    "#         # compile the model so that it uses Adam for optimization during training with cross-entropy loss\n",
    "#         sample_cnn.compile(optimizer=SGD(), loss=\"binary_crossentropy\", metrics=[\"acc\"])\n",
    "\n",
    "#         # print out a summary of the model achitecture\n",
    "#         print(sample_cnn.summary())\n",
    "\n",
    "# except RuntimeError as e:\n",
    "#   print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# start = time.time()\n",
    "# # class_weights = compute_class_weight(\"balanced\", np.unique(train_y), train_y)\n",
    "# # class_weights = dict(enumerate(class_weights))\n",
    "# try:  \n",
    "#     with tf.device('/device:GPU:4'):\n",
    "#         # train model\n",
    "#         history = sample_cnn.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=1,batch_size=150, verbose=1)\n",
    "# except RuntimeError as e:\n",
    "#   print(e)\n",
    "# end = time.time()\n",
    "# print(\"Time spent for training - {}\".format(end-start))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# try:  \n",
    "#     with tf.device('/device:GPU:5'):\n",
    "#         test_pred = sample_cnn.predict(test_x)\n",
    "#         for i in test_pred:\n",
    "#             if i[0] >= 0.5:\n",
    "#                 i[0] = 1\n",
    "#             else:\n",
    "#                 i[0] = 0\n",
    "#         print(test_pred)\n",
    "# except RuntimeError as e:\n",
    "#   print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# test_pred[test_pred<0.5]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# print(classification_report(test_y,test_pred))\n",
    "# print(confusion_matrix(test_y,test_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# test_y[0]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# for i in test_pred:\n",
    "#     if i[0] >= 0.5:\n",
    "#         i[0] = 1\n",
    "#     else:\n",
    "#         i[0] = 0\n",
    "# test_pred"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# history.history.keys()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# # summarize history for accuracy\n",
    "# plt.plot(history.history['acc'])\n",
    "# plt.plot(history.history['val_acc'])\n",
    "# plt.title('model accuracy')\n",
    "# plt.ylabel('accuracy')\n",
    "# plt.xlabel('epoch')\n",
    "# plt.legend(['train', 'test'], loc='upper left')\n",
    "# plt.show()\n",
    "# # summarize history for loss\n",
    "# plt.plot(history.history['loss'])\n",
    "# plt.plot(history.history['val_loss'])\n",
    "# plt.title('model loss')\n",
    "# plt.ylabel('loss')\n",
    "# plt.xlabel('epoch')\n",
    "# plt.legend(['train', 'test'], loc='upper left')\n",
    "# plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# sample_cnn.save(\"models/vgg19_model\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# batch norm SGD Model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:  \n",
    "    with strategy.scope():\n",
    "        # specify the input size of the images\n",
    "        images = Input((train_x.shape[1], train_x.shape[2], 1,))\n",
    "        x = Conv2D(32,kernel_size=(3,3),padding=\"same\")(images)\n",
    "\n",
    "        x = Activation(\"relu\")(x)\n",
    "\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "        x= MaxPool2D(pool_size=(3,3))(x)\n",
    "        x= Dropout(0.25)(x)\n",
    "\n",
    "        x= Conv2D(64, (3,3), padding=\"same\")(x)\n",
    "        x= Activation(\"relu\")(x)\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "        x= Conv2D(64, (3,3), padding=\"same\")(x)\n",
    "        x= Activation(\"relu\")(x)\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "        x= MaxPool2D(pool_size=(2,2))(x)\n",
    "        x= Dropout(0.25)(x)\n",
    "\n",
    "        x= Conv2D(128, (3,3), padding=\"same\")(x)\n",
    "        x= Activation(\"relu\")(x)\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "\n",
    "        x= Conv2D(128, (3,3), padding=\"same\")(x)\n",
    "        x= Activation(\"relu\")(x)\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "        x= MaxPool2D(pool_size=(2,2))(x)\n",
    "        x= Dropout(0.25)(x)\n",
    "\n",
    "        x= Flatten()(x)\n",
    "        x= Dense(1024)(x)\n",
    "        x= Activation(\"relu\")(x)\n",
    "        x= BatchNormalization(axis=chanDim)(x)\n",
    "        x= Dropout(0.5)(x)\n",
    "\n",
    "        x= Dense(1)(x)\n",
    "        \n",
    "        predictions = Activation(\"sigmoid\")(x)\n",
    "\n",
    "        # create the model using the layers we defined previously\n",
    "        model_online = Model(inputs=images, outputs=predictions)\n",
    "\n",
    "        # compile the model so that it uses Adam for optimization during training with cross-entropy loss\n",
    "        model_online.compile(optimizer=SGD(), loss=\"binary_crossentropy\", metrics=[\"acc\"])\n",
    "\n",
    "        # print out a summary of the model achitecture\n",
    "        print(model_online.summary())\n",
    "\n",
    "except RuntimeError as e:\n",
    "  print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "start = time.time()\n",
    "# class_weights = compute_class_weight(\"balanced\", np.unique(train_y), train_y)\n",
    "# class_weights = dict(enumerate(class_weights))\n",
    "try:  \n",
    "    with tf.device('/device:GPU:2'):\n",
    "        # train model\n",
    "        history = sample_cnn.fit(train_x, train_y, validation_data=(test_x, test_y), epochs=50,batch_size=150, verbose=1)\n",
    "except RuntimeError as e:\n",
    "  print(e)\n",
    "end = time.time()\n",
    "print(\"Time spent for training - {}\".format(end-start))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "try:  \n",
    "    with tf.device('/device:GPU:2'):\n",
    "        test_pred = sample_cnn.predict(test_x)\n",
    "        for i in test_pred:\n",
    "            if i[0] >= 0.5:\n",
    "                i[0] = 1\n",
    "            else:\n",
    "                i[0] = 0\n",
    "        print(test_pred)\n",
    "except RuntimeError as e:\n",
    "  print(e)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "print(classification_report(test_y,test_pred))\n",
    "print(confusion_matrix(test_y,test_pred))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "# summarize history for accuracy\n",
    "plt.plot(history.history['acc'])\n",
    "plt.plot(history.history['val_acc'])\n",
    "plt.title('model accuracy')\n",
    "plt.ylabel('accuracy')\n",
    "plt.xlabel('epoch')\n",
    "plt.legend(['train', 'test'], loc='upper left')\n",
    "plt.show()\n",
    "# summarize history for loss\n",
    "plt.plot(history.history['loss'])\n",
    "plt.plot(history.history['val_loss'])\n",
    "plt.title('model loss')\n",
    "plt.ylabel('loss')\n",
    "plt.xlabel('epoch')\n",
    "plt.legend(['train', 'test'], loc='upper left')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "sample_cnn.save(\"models/batch_norm_sgd\")"
   ]
  }
 ],
 "metadata": {
  "colab": {
   "collapsed_sections": [],
   "name": "Gender_Model.ipynb",
   "provenance": []
  },
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 1
}

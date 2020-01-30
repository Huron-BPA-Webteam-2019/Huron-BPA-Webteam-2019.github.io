import pickle 

#X_path = '/content/drive/My Drive/Datasets and Pickles/Pickles/Ames_X.pickle'
#Y_path = '/content/drive/My Drive/Datasets and Pickles/Pickles/Ames_Y.pickle'
'''
with open(X_path,'rb') as f:
  X_data = pickle.load(f)
  print("This is the X data: " , X_data)

with open(Y_path,'rb') as f:
  Y_data = pickle.load(f)
  print("This is the Y data: " , Y_data) #training data
'''

import tensorflow.keras
from tensorflow.keras import models,layers,regularizers
from tensorflow.keras.layers import Dense, Dropout,Conv2D, Flatten
import pandas as pd
import numpy as np
import os

AmesModel = models.Sequential() #json is saved 
# hmm do we just need to rewrite this code in JS
AmesModel.add(Dense(16, activation = 'relu', input_shape = (3,) ))
'''
  AmesModel.add(Dense(8,activation = 'relu',kernel_regularizer = regularizers.l1(0.001)))
'''
AmesModel.add(Dense(8,activation = 'relu',kernel_regularizer = regularizers.l1(0.001)))
AmesModel.add(Dense(1,activation = 'linear'))

AmesModel.compile(optimizer = 'rmsprop', loss = 'mse', metrics = ['mae','mse'])
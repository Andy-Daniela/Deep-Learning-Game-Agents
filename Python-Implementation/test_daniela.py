from __future__ import print_function
from numpy import *
import random
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, LSTM, GlobalAveragePooling1D
from keras.layers import Conv2D, MaxPooling2D, TimeDistributed
from keras import backend as K
from keras.utils import plot_model
from keras import metrics
from dataset import *

#Model parameters
kernel_size = (5,5)

#ds_path = '/Users/andymartinez/Datasets/ASL/Frames'
ds_path = '/Users/danielaflorit/Github/ASL_Dataset/Frames'
d = Dataset(ds_path)
#print str(d)

d.shuffle_dataset()
(X_train, y_train), (X_test, y_test) = d.get_data_split(0.8)
'''print X_train.shape
print '-----------------------------'
print y_train.shape
print '**********************************'
print X_test.shape
print '-----------------------------'
print y_test.shape'''
X_train = X_train.astype('float32')
(numb_examples, numb_frames, rows, cols) = X_train.shape

if K.image_data_format() == 'channels_first':
	X_train = X_train.reshape(numb_examples, numb_frames, 1, rows, cols)
	X_test = X_test.reshape(X_test.shape[0], numb_frames, 1, rows, cols)
	input_shape_conv = (1, rows, cols)
	input_shape_time_dist = (numb_frames, 1, rows, cols)
else:
	X_train = X_train.reshape(numb_examples, numb_frames, rows, cols, 1)
	X_test = X_test.reshape(X_test.shape[0], numb_frames, rows, cols, 1)
	input_shape_conv = (rows, cols, 1)
	input_shape_time_dist = (numb_frames, rows, cols, 1)



#input_shape_time_dist = (numb_frames, rows, cols, 1)

X_test = X_test.astype('float32')
#print(X_train.shape)
#print(X_train.shape)
#print(X_test.shape)
#print(y_train.shape)
#print(y_test.shape)
X_train /= 255.0
X_test /= 255.0

y_train = keras.utils.to_categorical(y_train, d.get_numb_classes())
y_test = keras.utils.to_categorical(y_test, d.get_numb_classes())
#print(X_train.shape)
model = Sequential()
model.add(TimeDistributed(Conv2D(32, kernel_size=kernel_size, padding='same', activation='relu', input_shape=(rows,cols, 1)), input_shape=input_shape_time_dist))
model.add(TimeDistributed(MaxPooling2D(pool_size=(2, 2))))
model.add(TimeDistributed(Flatten()))
model.add(TimeDistributed(Dense(128)))
model.add(TimeDistributed(Dropout(0.5)))
model.add(LSTM(128, return_sequences=False))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(d.get_numb_classes(), activation='softmax'))
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(),metrics=['accuracy'])
model.summary()

#Train model
model.fit(X_train, y_train, batch_size=10, epochs=50,verbose=1, validation_split=0.1)
#Test model
score = model.evaluate(X_test, y_test, verbose=0)
#model_name = 'model_lstm.png'
#plot_model(model, to_file=model_name, show_shapes=True, show_layer_names=True)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
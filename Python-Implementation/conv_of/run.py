from __future__ import print_function
import keras
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from dataset import *
from numpy import *

dataset_path = '/Users/andymartinez/Datasets/ASL/Optical_flow'
train_frac = 0.75
val_frac = 0.05
test_frac = 0.2

dataset = Dataset(dataset_path)
((X_train, y_train),(X_val, y_val),(X_test, y_test)) = dataset.get_data_split(train_frac, val_frac, test_frac)

batch_size = 10
num_classes = dataset.get_numb_classes()
epochs = 30
data_augmentation = True

print("Here!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(X_train.shape, 'train samples')
print(X_val.shape, 'val samples')
print(X_test.shape, 'test samples')
numb_images, img_rows, img_cols, img_channels  = X_train.shape
input_shape = (img_rows, img_cols, img_channels)
#img_channels = 3

X_train = X_train.astype('float32')
X_val = X_val.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255
X_val /= 255

y_train = keras.utils.to_categorical(y_train, num_classes)
y_val = keras.utils.to_categorical(y_val, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

model = Sequential()

model.add(Conv2D(32, (3, 3), padding='same',input_shape=input_shape))
model.add(Activation('relu'))
model.add(Conv2D(32, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(64, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(64, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(512))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes))
model.add(Activation('softmax'))
#model.summary()
model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_val, y_val), shuffle=True)

score = model.evaluate(X_test, y_test, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])
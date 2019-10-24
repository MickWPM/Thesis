import glob
import cv2

import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, BatchNormalization
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
import time
import tensorflow as tf
from tensorflow.python.keras.callbacks import TensorBoard
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

IMAGE_SHAPE= (60, 60, 3)

def get_training_data(split=True):
    images = []
    categories = []
    images_test = []
    categories_test = []
    for file in glob.glob("Training/wally/*.bmp"):
        img = cv2.imread(file)
        Data = img.astype('float32')
        Data /=255
        images.append(img)
        categories.append(1)
        
    for file in glob.glob("Training/notwally/*.bmp"):
        img = cv2.imread(file)
        Data = img.astype('float32')
        Data /=255
        images.append(img)
        categories.append(0)
        
    for file in glob.glob("Training/wallytest/*.bmp"):
        img = cv2.imread(file)
        Data = img.astype('float32')
        Data /=255
        if split:
            images_test.append(img)
            categories_test.append(1)
        else:
            images.append(img)
            categories.append(1)
        
    for file in glob.glob("Training/notwallytest/*.bmp"):
        img = cv2.imread(file)
        Data = img.astype('float32')
        Data /=255
        if split:
            images_test.append(img)
            categories_test.append(0)
        else:
            images.append(img)
            categories.append(0)
    
    #TODO: SHUFFLE IMAGES
    return np.array(images), np.array(images_test), np.array(categories), np.array(categories_test)

def get_new_model(input_shape=IMAGE_SHAPE):
    model = Sequential()
    #model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same', kernel_initializer='glorot_uniform', input_shape=input_shape))#, kernel_regularizer=keras.regularizers.l1(0.01)))
    model.add(Conv2D(128, kernel_size=(3, 3), activation='relu', padding='same', kernel_initializer='glorot_uniform', input_shape=input_shape))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', kernel_initializer='glorot_uniform'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(64, kernel_size=(3, 3), activation='relu', kernel_initializer='glorot_uniform'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', kernel_initializer='glorot_uniform'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(BatchNormalization())
    model.add(Flatten())
    # #model.add(Dense(128, activation='relu', kernel_regularizer=keras.regularizers.l1(0.01)))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dense(64, activation='relu'))
    # model.add(Dense(1, activation='sigmoid'))

    
    #First Hidden Layer
    model.add(Dense(256, activation='relu', kernel_initializer='random_normal'))
    model.add(Dropout(0.25))
    #Second  Hidden Layer
    model.add(Dense(256, activation='relu', kernel_initializer='random_normal'))
    model.add(Dropout(0.25))
    #Output Layer
    model.add(Dense(1, activation='sigmoid', kernel_initializer='random_normal'))
    return model



def RunWallyTrain():
    print("Training model")
    X_train, X_val, y_train, y_val = get_training_data()
    # Get data and split 80% 20% test-validation from shuffled original data
    #X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, shuffle= True)
    
    data, _, labels, _ = get_training_data(split=False)
    X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, shuffle=True)

    print("XTRAIN SHAPE = " + str(X_train.shape))

    batch_size = 50
    epochs = 500

    img_rows, img_cols, channels = IMAGE_SHAPE[0], IMAGE_SHAPE[1], IMAGE_SHAPE[2] # input image dimensions
    if K.image_data_format() == 'channels_first':
        X_train = X_train.reshape(X_train.shape[0], channels, img_rows, img_cols)
        X_val = X_val.reshape(X_val.shape[0], channels, img_rows, img_cols)
        input_shape = (channels, img_rows, img_cols)
    else:
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, channels)
        X_val = X_val.reshape(X_val.shape[0], img_rows, img_cols, channels)
        input_shape = (img_rows, img_cols, channels)

    print('X_train shape:', X_train.shape)
    print(X_train.shape[0], 'train samples')
    print('X_val shape:', X_val.shape)
    print(X_val.shape[0], 'train samples')

    model = get_new_model()

    tensorboard = TensorBoard(log_dir="logs\\Wally2-{}".format(time.time()))
        
    save_best_model = keras.callbacks.ModelCheckpoint("progress_model.h5", monitor='val_loss', verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)

    model.run_eagerly = True
    model.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.SGD(lr=0.05, momentum=0.0, decay=0.0, nesterov=False), metrics=['accuracy'])
    #model.compile(loss=keras.losses.binary_crossentropy, optimizer=keras.optimizers.adam(), metrics=['accuracy'])


    #history = model.fit(np.array(X_train), np.array(y_train), epochs=epochs, verbose=1, validation_data=(X_val, y_val), callbacks=[tensorboard])
    history = model.fit(np.array(X_train), np.array(y_train), batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(X_val, y_val), callbacks=[tensorboard, save_best_model])

    score = model.evaluate(X_val, y_val, verbose=0)

    print("Saving model...")
    model.save("wally_model.h5")
    print("Model saved.")
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])
    eval_model_train=model.evaluate(X_train, y_train)
    eval_model_Val=model.evaluate(X_val, y_val)
    print("eval_model_train="+str(eval_model_train))
    print("eval_model_Val="+str(eval_model_Val))

    print("CONFUSION MATRIX:")
    y_pred=model.predict(X_train)
    print("Y PRED: " + str(y_pred))
    y_pred =(y_pred>0.5)
    cm = confusion_matrix(y_train, y_pred)
    print(cm)

    return model


use_cpu = False


def Train_Wally():
    if use_cpu:
        with tf.device('/cpu:0'):
            return RunWallyTrain()
    else:
        return RunWallyTrain()
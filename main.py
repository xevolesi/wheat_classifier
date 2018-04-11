# Importing the Keras libraries and packages
import tensorflow as tf
import keras
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.layers import Conv2D, Dropout
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
with tf.device("/gpu:0"):
    # Initialising the CNN
    classifier = Sequential()
    # Step 1 - Convolution
    classifier.add(Conv2D(32, (3, 3), input_shape = (182, 182, 3), activation = 'relu'))
    classifier.add(Conv2D(32, (3, 3), activation='relu'))
    # Step 2 - Pooling
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Dropout(0.25))
    # Adding a second convolutional layer
    classifier.add(Conv2D(64, (3, 3), activation = 'relu'))
    classifier.add(Conv2D(64, (3, 3), activation='relu'))
    classifier.add(MaxPooling2D(pool_size = (2, 2)))
    classifier.add(Dropout(0.25))
    # Step 3 - Flattening
    classifier.add(Flatten())
    # Step 4 - Full connection
    classifier.add(Dense(units = 256, activation = 'relu'))
    classifier.add(Dropout(0.5))
    classifier.add(Dense(units = 1, activation = 'sigmoid'))
    # Compiling the CNN
    classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
    # checkpoint
    # Part 2 - Fitting the CNN to the images
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    rotation_range=90,
    horizontal_flip = True)
    test_datagen = ImageDataGenerator(rescale = 1./255)
    training_set = train_datagen.flow_from_directory('dataset/training_set',
    target_size = (182, 182),
    batch_size = 30,
    class_mode = 'binary')
    print("datagenlen " + len(training_set[0][0]).__str__())
    print(training_set.class_indices)
    test_set = test_datagen.flow_from_directory('dataset/test_set',
    target_size = (182, 182),
    batch_size = 10,
    class_mode = 'binary')
    filepath="dabest--{val_acc:.2f}.hdf5"
    checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=False, mode='max')
    callbacks_list = [checkpoint]
    classifier.fit_generator(training_set,
    steps_per_epoch = 25,
    epochs = 25,
    validation_data = test_set,
    validation_steps = 30, callbacks=callbacks_list)
    # Part 3 - Making new predictions
    import numpy as np
    from keras.preprocessing import image
    test_image = image.load_img('dataset/single_prediction/test.jpg', target_size = (182, 182))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    result = classifier.predict(test_image)
    # training_set.class_indices
    if result[0][0] == training_set.class_indices['good']:
        prediction = 'good'
    else:
        prediction = 'bad'
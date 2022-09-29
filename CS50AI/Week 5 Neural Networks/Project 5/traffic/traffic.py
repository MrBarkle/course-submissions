import cv2
import numpy as np
import os
import sys
import tensorflow as tf
from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.
    """

    # Keep track of images and labels
    images = []
    labels = []

    # Get the path to data_dir
    # Assuming data_dir is located in the 'traffic' folder of the
    # current working directory we can create the following path
    path = os.path.join(os.getcwd(), data_dir)

    # Loop through all directories in 'data_dir'. These are categories
    # Simultaneously sort all categories in ascending order
    for category in sorted(os.listdir(path), key=lambda x: (len(x), x)):

        # Gather sub directories in the 'data_dir' directory
        # This is the category's path
        cat_path = os.path.join(path, category)

        # Loop through each image within a category
        for image_name in os.listdir(cat_path):

            # Get images converted to numpy ndarrays
            img = cv2.imread(os.path.join(cat_path, image_name))

            # Get image shape
            height, width, channels = img.shape

            # Check if img is of the desired shape
            if height != IMG_HEIGHT or width != IMG_WIDTH:

                # Resize img using IMG_HEIGHT and IMG_WIDTH
                # The cv2.INTER_LINEAR interpolation method is used to provide
                # the highest quality results for upsizing or downsizing at a
                # modest computational cost
                res = cv2.resize(img, (IMG_WIDTH, IMG_HEIGHT),
                                 interpolation=cv2.INTER_LINEAR)

                # Add newly resized image to 'images' list
                images.append(res)

            else:

                # Add image to 'images' list
                images.append(img)

            # Add current image's corresponding label to 'labels' list
            # This is a str type
            labels.append(int(category))

    # Return a tuple containing both images and labels lists
    return (images, labels)


def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """

    # Store the input shape
    input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)

    # Create a convolutional neural network
    model = tf.keras.models.Sequential([

        # Start by adding 2 sequential 32 filter, 3x3 convolutional layers
        # separated by a batch normalization.
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu',
                               input_shape=input_shape),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),

        # Add a 2x2 Max Pooling
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

        # Add 2 additional 32 filter, 3x3 convolutional layers separated by batch
        # normalization
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(32, kernel_size=(3, 3), activation='relu'),
        tf.keras.layers.BatchNormalization(),

        # Add another 2x2 Max Pooling
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2), strides=2),

        # Flatten layers
        tf.keras.layers.Flatten(),

        # Add Dense hidden layer with 64 units
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.BatchNormalization(),

        # Add Dense output layer with NUM_CATEGORIES output units and softmax
        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    # Get summary of model
    # model.summary()

    # Compile model
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    # Return model
    return model


if __name__ == "__main__":
    main()

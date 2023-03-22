import numpy as np
from numpy.core.numeric import binary_repr
import tensorflow as tf

# Neural Net architectural constants
BINARY_WORD_LENGTH = 11
INPUT_DIMENSION = (BINARY_WORD_LENGTH,)
LAYER_WIDTH = 128
DROPOUT_RATE = 0.2
FINAL_LAYER_DIM = 2

# Training constants
VISUAL_TEST_QUANTITY = 10
TRAINING_PARTITION = VISUAL_TEST_QUANTITY
NUM_TRAINING_SAMPLES = 890
TRAINING_QUANTITY = TRAINING_PARTITION + NUM_TRAINING_SAMPLES
TEST_PARTITION = TRAINING_QUANTITY
NUM_TEST_SAMPLES = 100
TEST_QUANTITY = TEST_PARTITION + NUM_TEST_SAMPLES
TRAINING_RANGE = range(TRAINING_PARTITION, TRAINING_QUANTITY)
TESTING_RANGE = range(TEST_PARTITION, TEST_QUANTITY)
TRAINING_EPOCHS = 10

# Outcome representation
ONE_HOT_EVEN = [0, 1]
ONE_HOT_ODD = [1, 0]


def onehot(i):
    if i % 2 == 0:
        return np.array(ONE_HOT_EVEN)
    else:
        return np.array(ONE_HOT_ODD)

    
def make_binary_array(i):
    return np.array(list(binary_repr(i, BINARY_WORD_LENGTH)))
    
    
x_train = np.array([make_binary_array(i) for i in TRAINING_RANGE])
y_train = np.array([onehot(i) for i in TRAINING_RANGE])

x_test = np.array([make_binary_array(i) for i in TESTING_RANGE])
y_test = np.array([onehot(i) for i in TESTING_RANGE])

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Flatten(input_shape=INPUT_DIMENSION),
        tf.keras.layers.Dense(LAYER_WIDTH, activation="relu"),
        tf.keras.layers.Dense(LAYER_WIDTH, activation="relu"),
        tf.keras.layers.Dense(LAYER_WIDTH, activation="relu"),
        tf.keras.layers.Dense(LAYER_WIDTH, activation="relu"),
        tf.keras.layers.Dropout(DROPOUT_RATE),
        tf.keras.layers.Dense(FINAL_LAYER_DIM, activation="relu"),
    ]
)

loss_fn = tf.losses.CategoricalCrossentropy(from_logits=True)
model.compile(optimizer="adam", loss=loss_fn, metrics=["accuracy"])
model.fit(x_train, y_train, epochs=TRAINING_EPOCHS)


def isEvenDeep(i) -> bool:
    val = np.array(list(binary_repr(i, BINARY_WORD_LENGTH))).reshape(1, -1)
    if model.predict(val)[0][1] > 0:
        return True
    else:
        return False

# We should confirm, right?
for i in range(VISUAL_TEST_QUANTITY):
  print(f"{i} is even? {isEvenDeep(i)}")
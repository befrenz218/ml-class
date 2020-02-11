from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding, LSTM
from keras.layers import Conv1D, Flatten, MaxPooling1D
from keras.datasets import imdb
import wandb
from wandb.keras import WandbCallback
import numpy as np
from keras.preprocessing import text

wandb.init()
config = wandb.config

# set parameters:
config.vocab_size = 1000
config.maxlen = 1000
config.batch_size = 32
config.embedding_dims = 10
config.filters = 16
config.kernel_size = 3
config.hidden_dims = 250
config.epochs = 10

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=config.vocab_size, maxlen=config.maxlen)

X_train = sequence.pad_sequences(X_train, maxlen=config.maxlen)
X_test = sequence.pad_sequences(X_test, maxlen=config.maxlen)

model = Sequential()
model.add(Embedding(config.vocab_size,
                    config.embedding_dims,
                    input_length=config.maxlen))
model.add(Dropout(0.5))
model.add(Conv1D(config.filters,
                 config.kernel_size,
                 padding='valid',
                 activation='relu'))
model.add(MaxPooling1D())
model.add(Conv1D(config.filters,
                 config.kernel_size,
                 padding='valid',
                 activation='relu'))
model.add(MaxPooling1D())
model.add(Flatten())
model.add(Dense(config.hidden_dims, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

model.fit(X_train, y_train,
          batch_size=config.batch_size,
          epochs=config.epochs,
          validation_data=(X_test, y_test), callbacks=[WandbCallback()])

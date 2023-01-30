# -*- coding: utf-8 -*-
"""nlp tensorflow.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F0SXIeljoTn6AByCDCUYLXQs6Ftg8__b
"""

# Commented out IPython magic to ensure Python compatibility.
#importing library
import tensorflow as tf
import numpy as np
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

#preprocessing lib
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

#model select lib
from sklearn.model_selection import train_test_split

df = pd.read_csv('complaints_processed.csv')

df

df.info()

df.isna().any()

#dropping atribut tidak perlu dan buang data kosong
df = df.drop('Unnamed: 0',axis=1)
df = df.dropna()

df.info()

#use 3000 data for faster computation time
df = df.head(3000)

#one hot encoding
product = pd.get_dummies(df['product'])
df_1 = pd.concat([df, product], axis=1)
df_1 = df_1.drop('product',axis=1)
df_1.info()

df_1

X = df_1['narrative']
y = df_1[df_1.columns.drop('narrative')]

#fungsi tokenizer
tokenizer = Tokenizer(num_words=50000, 
                      filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', 
                      lower=True)
tokenizer.fit_on_texts(X.values)
word_index = tokenizer.word_index

print('token = ', len(word_index))

X = tokenizer.texts_to_sequences(df_1['narrative'].values)
X = pad_sequences(X, maxlen=250)
print('data shape = ', X.shape)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20)
print(X_train.shape,y_train.shape)
print(X_test.shape,y_test.shape)

from tensorflow.python import metrics
#model sequential, menggunakan embedding dan LSTM

model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=50000, output_dim=100),
    tf.keras.layers.LSTM(256),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(5, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

callback = tf.keras.callbacks.EarlyStopping(patience=2,monitor='loss')
history = model.fit(X_train, y_train, epochs=10,
                      validation_data=(X_train,y_train),
                    callbacks=[callback])

print("train accuracy", history.history['accuracy'][-1])

eval = model.evaluate(X_test,y_test)
print("testing accuracy", eval[1])

plt.plot(history.history['loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='upper right')
plt.show()

plt.plot(history.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train'], loc='lower right')
plt.show()


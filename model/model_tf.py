import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

df = pd.read_csv('./data/dataset_training.csv')
weight = pd.read_csv('./data/Symptom-severity.csv')

# Mendapatkan nama kolom dari data frame
cols = df.columns
data = df[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df.shape)

df = pd.DataFrame(s, columns = df.columns)
# Mengisi data yang kosong dengan nilai 0
df = df.fillna(value=0)

vals = df.values
symptoms = weight['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = weight[weight['Symptom'] == symptoms[i]]['weight'].values[0]
    
d = pd.DataFrame(vals, columns=cols)

d = d.replace('dischromic _patches', 6)
d = d.replace('spotting_ urination', 6)
df = d.replace('foul_smell_of urine', 5)

(df[cols] == 0).all()

df['Disease'].value_counts()

df['Disease'].unique()

data = df.iloc[:,1:].values
labels = df['Disease'].values

x_train, x_test, y_train, y_test = train_test_split(data, labels, shuffle=True, train_size = 0.85)

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

encoder =  LabelEncoder()
y_train_e = encoder.fit_transform(y_train)
y_train_c = to_categorical(y_train_e, num_classes = 41)

y_test_e = encoder.fit_transform(y_test)
y_test_c = to_categorical(y_test_e, num_classes = 41)

joblib.dump(encoder, "./data/encoder.pkl")
np.save('./data/classes.npy', encoder.classes_)

#Building the RNN
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import datasets, layers, models

model = tf.keras.Sequential([
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(41, activation='softmax')
  ])

model.compile(optimizer='adam', loss='mean_squared_error', metrics = ['accuracy'])

# Fitting the CNN to the Training set
epoch = 2000 
batch_size = 32
model.fit(x_train, y_train_c, epochs=epoch,batch_size=batch_size)

model.save('./data/healthcare_tf.h5')
import pandas as pd
import numpy as np
import joblib

df_testing = pd.read_csv('data/dataset_testing.csv')
weight = pd.read_csv('data/Symptom-severity.csv')

# Mendapatkan nama kolom dari data frame
cols = df_testing.columns
data = df_testing[cols].values.flatten()

s = pd.Series(data)
s = s.str.strip()
s = s.values.reshape(df_testing.shape)

df_testing = pd.DataFrame(s, columns = df_testing.columns)

# Mengisi data yang kosong dengan nilai 0
df_testing = df_testing.fillna(value=0)

vals = df_testing.values
symptoms = weight['Symptom'].unique()

for i in range(len(symptoms)):
    vals[vals == symptoms[i]] = weight[weight['Symptom'] == symptoms[i]]['weight'].values[0]
    
d = pd.DataFrame(vals, columns=cols)

d = d.replace('dischromic _patches', 6)
d = d.replace('spotting_ urination', 6)
df_testing = d.replace('foul_smell_of urine', 5)

(df_testing[cols] == 0).all()

df_testing['Disease'].value_counts()
df_testing['Disease'].unique()

data = df_testing.iloc[:,1:].values
labels = df_testing['Disease'].values

from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical

from tensorflow import keras

model = keras.models.load_model('./data/healthcare_tf.h5')

encoder = joblib.load("./data/encoder.pkl")

labels_e = encoder.transform(labels)
labels_c = to_categorical(labels_e, num_classes = 41)

score = model.evaluate(data, labels_c, batch_size=32)

pred_tf = model.predict(data)

actual = np.argmax(labels_c, axis=1)
predicted = np.argmax(pred_tf, axis=1)

print('Label Actual : ', actual)
print(encoder.inverse_transform(actual))

print('Label Predicted : ', predicted)
print(encoder.inverse_transform(predicted))

print('CNN Score : ', score)
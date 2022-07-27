import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

df = pd.read_csv('data/dataset_training.csv')
weight = pd.read_csv('data/Symptom-severity.csv')

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

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

# Initialising the RNN
model = Sequential()

# Adding the first LSTM layer and some Dropout regularisation
# Adding a second LSTM layer and some Dropout regularisation
# Adding a third LSTM layer and some Dropout regularisation
# Adding a fourth LSTM layer and some Dropout regularisation
# Adding the output layer
model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1],1)))
model.add(Dropout(0.2))

model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))

model.add(LSTM(units=50))
model.add(Dropout(0.2))

model.add(Dense(units=1))

# Compiling the RNN
# Code here
model.compile(optimizer='adam', loss='mean_squared_error', metrics = ['accuracy'])

# Fitting the RNN to the Training set
epoch = 100 
batch_size = 128
model.fit(x_train, y_train_c, epochs=epoch,batch_size=batch_size)

model.save('healthcare1.h5')

score = model.evaluate(x_test, y_test_c, batch_size=batch_size)

y_pred = model.predict(x_test)

actual = np.argmax(y_test_c, axis=1)
predicted = np.argmax(y_pred, axis=1)

print(f"Actual: {actual}")
print(f"Predicted: {predicted}")


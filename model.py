import pandas as pd
import numpy as np
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix

import matplotlib.pyplot as plt
import seaborn as sns

import joblib

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
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

svc = SVC()
svc.fit(x_train, y_train)
joblib.dump(svc, "data/svc.pkl")

pred_svc = svc.predict(x_test)
# print(pred_svc)

# F1-score% = 93.6318161416234 | Accuracy% = 94.03794037940379
conf_mat = confusion_matrix(y_test, pred_svc)
print('SVC F1-score% =', f1_score(y_test, pred_svc, average='macro')*100, '|', 'SVC Accuracy% =', accuracy_score(y_test, pred_svc)*100)

nb = GaussianNB() 
nb.fit(x_train, y_train)
joblib.dump(nb, "data/nb.pkl")

pred_nb = nb.predict(x_test)
# print(pred_nb)

# F1-score% = 88.75354476838021 | Accuracy% = 90.5149051490515
conf_mat = confusion_matrix(y_test, pred_nb)
print('Naive Bayes F1-score% =', f1_score(y_test, pred_nb, average='macro')*100, '|', 'Naive Bayes Accuracy% =', accuracy_score(y_test, pred_nb)*100)

knn = KNeighborsClassifier(n_neighbors = 2, p=2)
knn.fit(x_train, y_train)
joblib.dump(knn, "data/knn.pkl")

pred_knn = knn.predict(x_test)
# print(pred_knn)


# F1-score% = 98.93734129768748 | Accuracy% = 98.91598915989161
conf_mat = confusion_matrix(y_test, pred_knn)
print('KNN F1-score% =', f1_score(y_test, pred_knn, average='macro')*100, '|', 'KNN Accuracy% =', accuracy_score(y_test, pred_knn)*100)
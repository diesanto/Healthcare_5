import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score, confusion_matrix
import joblib

df_testing = pd.read_csv('./data/dataset_testing.csv')
weight = pd.read_csv('./data/Symptom-severity.csv')

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

# Unpickle classifier KNN
knn = joblib.load("./data/knn_mink.pkl")
pred_knn = knn.predict(data)

print('Label Actual : ', labels)
print('Hasil Prediksi KNN :', pred_knn)
print('KNN F1-score% =', f1_score(labels, pred_knn, average='macro')*100, '|', 'KNN Accuracy% =', accuracy_score(labels, pred_knn)*100)

# Unpickle classifier SVC
svc = joblib.load("./data/svc.pkl")
pred_svc = svc.predict(data)

print('Label Actual : ', labels)
print('Hasil Prediksi SVC :', pred_svc)
print('SVC F1-score% =', f1_score(labels, pred_svc, average='macro')*100, '|', 'SVC Accuracy% =', accuracy_score(labels, pred_svc)*100)

# Unpickle classifier Naive Bayes
nb = joblib.load("./data/nb.pkl")
pred_nb = nb.predict(data)

print('Label Actual : ', labels)
print('Hasil Prediksi Naive Bayes :', pred_nb)
print('Naive Bayes F1-score% =', f1_score(labels, pred_nb, average='macro')*100, '|', 'Naive Bayes Accuracy% =', accuracy_score(labels, pred_nb)*100)
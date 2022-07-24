from flask import Flask
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_paginate import Pagination, get_page_parameter, get_page_args
from flask_sqlalchemy import SQLAlchemy

from tensorflow import keras
import pandas as pd
import numpy as np
from sklearn.metrics import f1_score, accuracy_score
import joblib

app = Flask(__name__)

app.config['SECRET_KEY'] = 'xxxxxxxx'

username = 'root'
password = ''
server = 'localhost'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://{username}:{password}@{server}/healthcare_db'.format(username, password, server)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/healthcare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Memanggil SQLAlchemy
db = SQLAlchemy(app)

class Disease(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(20), index=True, unique=True)
    description = db.Column(db.Text())
    
    def to_json(self):
        return {
            'id': self.id,
            'disease': self.disease,
            'description': self.description
        }

class SymptomSeverity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(20), index=True, unique=True)
    weight = db.Column(db.Integer)
    
    def to_json(self):
        return {
            'id': self.id,
            'symptom': self.symptom,
            'weight': self.weight
        }

class SymptomPrecaution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    disease = db.Column(db.String(20), db.ForeignKey('disease.disease'), index=True, unique=True)
    precaution_1 = db.Column(db.String(150))
    precaution_2 = db.Column(db.String(150))
    precaution_3 = db.Column(db.String(150))
    precaution_4 = db.Column(db.String(150))
    
    def to_json(self):
        return {
            'id': self.id,
            'disease': self.disease,
            'precaution_1': self.precaution_1,
            'precaution_2': self.precaution_2,
            'precaution_3': self.precaution_3,
            'precaution_4': self.precaution_4,
        }

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/diseases_list', methods=['GET'], defaults={"page": 1})
@app.route('/diseases_list/<int:page>', methods=['GET'])
def diseases_list(page):
    per_page = 10
    diseases = Disease.query.paginate(page, per_page, error_out = False)

    return render_template('disease/diseases_list.html', diseases = diseases)

@app.route('/symptom_severities_list', methods=['GET'], defaults={"page": 1})
@app.route('/symptom_severities_list/<int:page>', methods=['GET'])
def symptom_severities_list(page):
    per_page = 10
    severities = SymptomSeverity.query.paginate(page, per_page, error_out = False)

    return render_template('symptom/severities_list.html', severities = severities)

@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    
    symptoms = []
    predicts = {}
    if request.method == 'POST': 
        symptoms = request.form.getlist('symptoms') 
        x = [[int(symptoms[i]) if i < len(symptoms) else 0 for i in range(17)]]

        # Unpickle classifier KNN
        knn = joblib.load("data/knn.pkl")
        predicts['pred_knn'] = knn.predict(x)[0]
        predicts['disease_knn'] = Disease.query \
                                .join(SymptomPrecaution, Disease.disease == SymptomPrecaution.disease) \
                                .filter_by(disease = predicts['pred_knn']) \
                                .add_columns(Disease.description, SymptomPrecaution.precaution_1, SymptomPrecaution.precaution_2, SymptomPrecaution.precaution_3, SymptomPrecaution.precaution_4) \
                                .first()

        # Unpickle classifier SVC
        svc = joblib.load("data/svc.pkl")
        predicts['pred_svc'] = svc.predict(x)[0]
        predicts['disease_svc'] = Disease.query \
                                .join(SymptomPrecaution, Disease.disease == SymptomPrecaution.disease) \
                                .filter_by(disease = predicts['pred_svc']) \
                                .add_columns(Disease.description, SymptomPrecaution.precaution_1, SymptomPrecaution.precaution_2, SymptomPrecaution.precaution_3, SymptomPrecaution.precaution_4) \
                                .first()

        
        # Unpickle classifier Naive Bayes
        nb = joblib.load("data/nb.pkl")
        predicts['pred_nb'] = nb.predict(x)[0]
        predicts['disease_nb'] = Disease.query \
                                .join(SymptomPrecaution, Disease.disease == SymptomPrecaution.disease) \
                                .filter_by(disease = predicts['pred_nb']) \
                                .add_columns(Disease.description, SymptomPrecaution.precaution_1, SymptomPrecaution.precaution_2, SymptomPrecaution.precaution_3, SymptomPrecaution.precaution_4) \
                                .first()
        
        # Load classifier Tensorflow - CNN
        model = keras.models.load_model('data/healthcare_tf.h5')
        tf = model.predict(x)

        encoder = joblib.load("data/encoder.pkl")
        pred_tf = encoder.inverse_transform(np.argmax(tf, axis=1))
        predicts['pred_tf'] = pred_tf[0]
        predicts['disease_tf'] = Disease.query \
                                .join(SymptomPrecaution, Disease.disease == SymptomPrecaution.disease) \
                                .filter_by(disease = predicts['pred_tf']) \
                                .add_columns(Disease.description, SymptomPrecaution.precaution_1, SymptomPrecaution.precaution_2, SymptomPrecaution.precaution_3, SymptomPrecaution.precaution_4) \
                                .first()

    severities = SymptomSeverity.query.all()
    return render_template('symptom/diagnosis.html', 
                        severities = severities, 
                        symptoms = symptoms, 
                        predicts = predicts)

if __name__ == '__main__':
    app.run(debug = True)
import pyrebase
from flask import *
import secrets
import time
import json
import pandas as pd
from werkzeug.utils import secure_filename
import io
import random

import pickle

import base64

import seaborn as sns

from statsmodels.graphics.mosaicplot import mosaic

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.datasets import load_iris
from sklearn.datasets import load_boston
from sklearn.datasets import load_diabetes
from sklearn.datasets import load_digits
from sklearn.datasets import load_breast_cancer


from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression, SGDClassifier

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

import datetime
import time
from time import strftime, gmtime

app = Flask(__name__)
app.secret_key = secrets.token_bytes(32)

# Firebase configuration
config = {
    "apiKey": "AIzaSyCqtOhxgh9x2uTTRnCyQ2MFMnsfH5fjFV0",
    "authDomain": "machine-learning-plateform.firebaseapp.com",
    "databaseURL": "https://machine-learning-plateform.firebaseio.com",
    "projectId": "machine-learning-plateform",
    "storageBucket": "machine-learning-plateform.appspot.com",
    "messagingSenderId": "858997576334",
    "appId": "1:858997576334:web:973fcb03973218aba62fdf",
    "measurementId": "G-GJPBZD2GD4"  
}

# Firebase init
firebase = pyrebase.initialize_app(config)
# Firebase authentication
auth = firebase.auth()
# Firebase Database
db = firebase.database()



data = load_iris()
Xtrain, Xtest, Ytrain, Ytest = train_test_split(data.data, data.target, test_size=0.3, random_state=4)


# Create a model
model = LogisticRegression(C=0.1, 
                           max_iter=20, 
                           fit_intercept=True, 
                           n_jobs=3, 
                           solver='liblinear')
model.fit(Xtrain, Ytrain)


pkl_filename = "pickle_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

# Load from file
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)

storage = firebase.storage()
storage.child('models/pickle.pkl').put(pickle_model)



            
            

'''lista = ['a', 'b', 'c']
listb = ['a', 'b']


def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  
# Driver Code 
li1 = [10, 15, 20, 25, 30, 35, 40] 
li2 = [25, 40, 35] 
print(list(set(lista) - set(listb))) 
'''

'''dic = {'1':4500, '2':9000, '3':13500 ,'4':18000}

a = 4600
keys = []

for k, v in dic.items() :
    if a > v :
        keys.append(k)
        
print(keys[-1])'''

'''            ###########################################
            ###########################################
            ##### FOR TEST ONLY #######################
            ###########################################
            data = df.copy()
            data.drop(['cabin', 'body', 'boat', 'home.dest'], axis = 1, inplace = True)
            data.dropna()
            data['age'] = data['age'].fillna(data.groupby(['pclass', 'sex'])['age'].transform('mean'))
            data.head()
            data.dropna(axis = 0, inplace = True)

            dummies = pd.get_dummies(data['pclass'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['pclass', 3.0], inplace = True, axis = 1)

            dummies = pd.get_dummies(data['sex'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['sex', 'male'], inplace = True, axis = 1)

            dummies = pd.get_dummies(data['embarked'])
            data = pd.concat([data, dummies], axis = 1)
            data.drop(['embarked', 'C'], inplace = True, axis = 1)





            ###########################################
            ###########################################
            ##### FOR TEST ONLY #######################
            ###########################################'''


#print([value for key, value in models.items() if element in key])


 


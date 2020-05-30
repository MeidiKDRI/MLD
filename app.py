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



def do_stripplot(data, col1, col2):
    
    # Plot
    sns.stripplot(x=col1, y=col2, data=data);

    # Save as an Image
    stripplot_buff = io.BytesIO()
    plt.savefig(stripplot_buff, format='png')
    stripplot_buff.seek(0)
    stripplot_buffer = b''.join(stripplot_buff)
    stripplot_encoded = base64.b64encode(stripplot_buffer)
    data_stripplot = stripplot_encoded.decode('utf-8')

    return data_stripplot


def do_corr_matrix(data):
    
    # Plot
    palette = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(data.corr(), cmap = palette);
    
    # Save as an Image
    corr_buff = io.BytesIO()
    plt.savefig(corr_buff, format='png')
    corr_buff.seek(0)
    corr_buffer = b''.join(corr_buff)
    corr_encoded = base64.b64encode(corr_buffer)
    data_corr = corr_encoded.decode('utf-8')

    return data_corr

def do_mosaic(data, col):
    
    # Plot
    mosaic(data, [col]);

    # Save as an Image
    mosaic_buff = io.BytesIO()
    plt.savefig(mosaic_buff, format='png')
    mosaic_buff.seek(0)
    mosaic_buffer = b''.join(mosaic_buff)
    mosaic_encoded = base64.b64encode(mosaic_buffer)
    data_mosaic = mosaic_encoded.decode('utf-8')

    return data_mosaic

# Data histogram function
def do_hist(data, col):

    # Plot
    if col == 'all' :
        data.hist(figsize = (10,8), bins = 25)
    else : 
        data.hist(col, figsize = (10,8), bins = 25)

    # Save as an Image
    hist_buff = io.BytesIO()
    plt.savefig(hist_buff, format='png')
    hist_buff.seek(0)
    hist_buffer = b''.join(hist_buff)
    hist_encoded = base64.b64encode(hist_buffer)
    hist = hist_encoded.decode('utf-8')

    return hist

# Data histogram function
def do_heatmap(data):

    # Plot
    plt.rcParams['figure.figsize'] = (10.0, 8.0)
    sns.heatmap(data.isna());

    # Save as an Image
    buff2 = io.BytesIO()
    plt.savefig(buff2, format='png')
    buff2.seek(0)
    buffer = b''.join(buff2)
    encoded = base64.b64encode(buffer)
    heatMap = encoded.decode('utf-8')

    return heatMap

##############################################
############# CONFIG #########################
##############################################
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

##############################################
############# ROUTES #########################
##############################################

#####################
# Index for Home Page
#####################

@app.route('/')
def home() :
    return render_template('index.html')

@app.route('/pricing')
def pricing() :
    return render_template('pricing.html')

############
# Login page
############


@app.route('/login', methods=['GET', 'POST'])
def login() :

    if request.method == 'POST' :

        email    = request.form['email']
        password = request.form['pass']
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user # We store user for next calls.

            # We fetch the user infos
            userInfo = auth.get_account_info(user['idToken'])
            userId   = userInfo['users'][0]['localId']
            username = db.child("users").child(userId).child('username').get().val()
            username = username.capitalize()

            flash(f'Welcome back {username}', 'success')
            return redirect(url_for('dataset'))

        except:

            flash('Please check your account informations.', 'danger')
            return render_template('login.html')

    return render_template('login.html')


#########
# Log Out
#########

@app.route('/logout')
def logout():

    # We refresh session
    session.pop('user', None)
    session.pop('filename', None)
    df = None

    flash('You have been disconnected. We hope to see you back soon.', 'warning')
    return redirect(url_for('home'))


######################
# Change Password Page
######################

@app.route('/change_pass', methods = ['GET', 'POST'])
def change_password() :

    if request.method == 'POST' :

        email = request.form['email']
        auth.send_password_reset_email(email)

        flash('You will receive an email. Please check your box and spam box.', 'warning')
    return render_template('change_pass.html')


##############
# Sign Up Page
##############

@app.route('/register', methods=['GET', 'POST'])
def register() :

    if request.method == 'POST' :

        username     = request.form['username']
        email        = request.form['email']
        function     = request.form['function']
        password     = request.form['pass']
        confirm_pass = request.form['pass_confirmation']

        creation_date = time.time()

        if password == confirm_pass :

            new_user = auth.create_user_with_email_and_password(email, password)
            # We send a confirmation email to the new memeber
            auth.send_email_verification(new_user['idToken'])

            # We need to associate the authentication id with userId in the user database
            userInfo = auth.get_account_info(new_user['idToken'])
            userId = userInfo['users'][0]['localId']

            # User db creation
            userDB = {'username': username, 'email' : email, 'function' : function, 'registration_date' : creation_date}
            db.child('users').child(userId).set(userDB)

            flash('Your account has been created', 'success')
            return redirect(url_for('login'))

        else :

            flash('Please enter the same password for confirmation.', 'warning')
            return render_template('register.html')

    return render_template('register.html')


##########################
# Update informations page
##########################

@app.route('/update_infos', methods=['GET', 'POST'])
def update_infos() :

    user     = session['user']
    user     = auth.refresh(user['refreshToken'])
    userInfo = auth.get_account_info(user['idToken'])
    userId   = userInfo['users'][0]['localId']

    if request.method == 'POST' :

        username     = request.form['username']
        email        = request.form['email']
        function     = request.form['function']

        # User db modification
        userDB = {'username': username, 'email' : email, 'function' : function}
        db.child('users').child(userId).set(userDB)

        flash('Your informations have been changed.', 'success')
        return render_template('settings.html')

    return render_template('update_info.html')


####################
# Delete Account Page
####################

@app.route('/delete_account')
def delete_account() :

    user     = session['user']
    user     = auth.refresh(user['refreshToken'])
    userInfo = auth.get_account_info(user['idToken'])
    userId   = userInfo['users'][0]['localId']

    db.child('users').child(userId).remove()

    flash('Your account has been deleted', 'danger')
    return redirect(url_for('home'))

#####################
# Dataset upload page
#####################
@app.route('/dataset', methods = ['GET', 'POST'])
def dataset() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        global df

        try:
            
            # We fetch the user infos
            userInfo = auth.get_account_info(user['idToken'])
            userId   = userInfo['users'][0]['localId']
            username = db.child("users").child(userId).child('username').get().val()
            username = username.capitalize()
            
            filename = session['filename']
            # Summary
            desc     = df.describe()

            # Dataframe shape
            nb_rows  = df.shape[0]
            nb_col   = df.shape[1]

            # Dataframe informations
            # To display df.infos() in html template, we need to make some manipulations first.
            buffer = pd.compat.StringIO()
            df.info(buf=buffer)
            infos = buffer.getvalue()
            df_infos = pd.DataFrame(infos.split('\n'), columns= ['info'])

            # Missing Values Count
            df_na = df.isna().sum()
            df_na = pd.DataFrame(df_na, columns= ['Missing Value Count'])
            
            return render_template('dataset.html',
                                   username = username,
                                    df_name = filename,
                                    nb_col = nb_col, nb_rows = nb_rows,
                                    dataset = [df.to_html(classes = 'data')],
                                    describe = [desc.to_html(classes = 'data')],
                                    df_infos = [df_infos.to_html(classes = 'data')],
                                    df_na = [df_na.to_html(classes= 'data')])

        except:

            if request.method == 'POST':

                if request.form['upload'] == 'upload_dataset' :
                    df = None
                    f        = request.files['file']
                    filename = secure_filename(f.filename)
                    session['filename'] = filename
                    
                    df = pd.read_csv(f)

                    # Summary
                    desc     = df.describe()

                    # Dataframe shape
                    nb_rows  = df.shape[0]
                    nb_col   = df.shape[1]

                    # Dataframe informations
                    # To display df.infos() in html template, we need to make some manipulations first.
                    buffer = pd.compat.StringIO()
                    df.info(buf=buffer)
                    infos = buffer.getvalue()
                    df_infos = pd.DataFrame(infos.split('\n'), columns= ['info'])

                    # Missing Values Count
                    df_na = df.isna().sum()
                    df_na = pd.DataFrame(df_na, columns= ['Missing Value Count'])

                    return render_template('dataset.html',
                                            df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                            dataset = [df.to_html(classes = 'data')],
                                            describe = [desc.to_html(classes = 'data')],
                                            df_infos = [df_infos.to_html(classes = 'data')],
                                            df_na = [df_na.to_html(classes= 'data')])

                elif request.form['upload'] == 'load_dataset' :

                    df = None
                    dataset_to_load = request.form.get('dataset_to_load')
                    dataset = eval('load_' + dataset_to_load + '()') # eval() allow to convert string to object

                    features = dataset.data
                    y = dataset.target
                                        
                    df = pd.DataFrame(data= np.c_[features, y],
                                        columns= dataset['feature_names'] + ['target'])
                    

                    filename = dataset_to_load + '_sklearn_dataset'
                    session['filename'] = filename
                    
                    # Summary
                    desc     = df.describe()

                    # Dataframe shape
                    nb_rows  = dataset.data.shape[0]
                    nb_col   = dataset.data.shape[1]

                    # Dataframe informations
                    # To display df.infos() in html template, we need to make some manipulations first.
                    buffer = pd.compat.StringIO()
                    df.info(buf=buffer)
                    infos = buffer.getvalue()
                    df_infos = pd.DataFrame(infos.split('\n'), columns= ['info'])
                    
                    # Missing Values Count
                    df_na = df.isna().sum()
                    df_na = pd.DataFrame(df_na, columns= ['Missing Value Count'])

                    return render_template('dataset.html',
                                            df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                            dataset = [df.to_html(classes = 'data')],
                                            describe = [desc.to_html(classes = 'data')],
                                            df_infos = [df_infos.to_html(classes = 'data')],
                                            df_na = [df_na.to_html(classes= 'data')])

                # Ne fonctionne pas correctement
                elif request.form['upload'] == 'reset_dataset' :

                    session.pop('filename', None)

                    df = None

                    return redirect(url_for('dataset'))
                
        return render_template('dataset.html')

    return redirect(url_for('login'))


##################
# Data Exploration
##################

@app.route('/exploration', methods = ['GET', 'POST'])
def exploration() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        global df

        try :

            # We first make a copy of the dataframe
            df = df.copy()
            # Missing Values for form-select
            na_actions = [{'name': 'Drop NA'}, {'name': 'Fill NA'}]

            # Dictionnary of columns for form-select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]

            # Dataframe shape
            nb_rows  = df.shape[0]
            nb_col   = df.shape[1]
            filename = session['filename']

            if request.method == 'POST' :
                
                if request.form['submit'] == 'cleanNan' :

                    # Drop NA
                    dropna_checkbox = request.form.get('dropna_checkbox')
                    dropna_col_selected = request.form.getlist('dropna_col_selector')

                    # Fill NA
                    fillna_checkbox = request.form.get('fillna_checkbox')

                    # Drop NA Management
                    if dropna_checkbox == 'true' :

                        # We handle dropna() depending on selections.
                        if dropna_col_selected[0].lower() == 'all' :

                            df = df.dropna()
                            # New Dataframe shape
                            nb_rows  = df.shape[0]
                            nb_col   = df.shape[1]

                        else :

                            # We drop na on specific columns selected by user
                            df = df.dropna(subset = (dropna_col_selected))
                            # New Dataframe shape
                            nb_rows  = df.shape[0]
                            nb_col   = df.shape[1]

                        return render_template('dataxplo.html',
                                            df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                            dataset = [df.to_html(classes = 'data')],
                                            col_selec = df_col_dic)

                    # Fill NA Management
                    elif fillna_checkbox == 'true' :

                        # Get the value from fillna checkboxes
                        fillnabymean_checkbox = request.form.get('fillnabymean_checkbox')
                        fillnabymedian_checkbox = request.form.get('fillnabymedian_checkbox')
                        fillnabyvalue_checkbox = request.form.get('fillnabyvalue_checkbox')

                        fillna_col_selector = request.form.getlist('fillna_col_selector')

                        # Fill NaN by Mean Value
                        if  fillnabymean_checkbox == 'true' :

                            # On the full dataframe
                            if fillna_col_selector[0].lower() == 'all' :

                                df = df.fillna(df.mean())

                            # On selected columns
                            else :

                                for col in fillna_col_selector:
                                    df[col].fillna(df[col].mean(), inplace=True)

                            return render_template('dataxplo.html',
                                df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                dataset = [df.to_html(classes = 'data')],
                                col_selec = df_col_dic)

                        # Fill NaN by Median Value
                        elif  fillnabymean_checkbox == 'true' :

                            # On the full dataframe
                            if fillna_col_selector[0].lower() == 'all' :

                                df = df.fillna(df.median())

                            # On selected columns
                            else :

                                for col in fillna_col_selector:
                                    df[col].fillna(df[col].median(), inplace=True)

                            return render_template('dataxplo.html',
                                df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                dataset = [df.to_html(classes = 'data')],
                                col_selec = df_col_dic)

                        # Fill NaN by a specific Value
                        elif fillnabyvalue_checkbox == 'true' :

                            # We fetch the value input by user
                            na_value = request.form.get('fill_value')

                            # On the full dataframe
                            if fillna_col_selector[0].lower() == 'all' :

                                df = df.fillna(na_value)

                            # On selected columns
                            else :

                                for col in fillna_col_selector:
                                    df[col].fillna(na_value, inplace=True)

                            return render_template('dataxplo.html',
                                df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                dataset = [df.to_html(classes = 'data')],
                                col_selec = df_col_dic)

                ## Drop duplicates
                elif request.form['submit'] == 'dropDup' :

                    dup_col_selector = request.form.getlist('dup_col_selector')
                    df.drop_duplicates(subset= dup_col_selector, keep = False, inplace = True)
                    
                    return render_template('dataxplo.html',
                                           df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                           dataset = [df.to_html(classes = 'data')],
                                           col_selec = df_col_dic)
                ## Drop column(s)
                elif request.form['submit'] == 'dropCol' :

                    drop_col_selector = request.form.getlist('drop_col_selector')
                    df.drop(columns= drop_col_selector, axis = 1, inplace = True)

                    return render_template('dataxplo.html',
                                           df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                           dataset = [df.to_html(classes = 'data')],
                                           col_selec = df_col_dic)

                return render_template('dataxplo.html', col_selec = df_col_dic)

            return render_template('dataxplo.html',
                                   df_name = filename, nb_col = nb_col, nb_rows = nb_rows,
                                   dataset = [df.to_html(classes = 'data')],
                                   col_selec = df_col_dic)

        except:

            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('dataxplo.html')

        return render_template('dataxplo.html')

    return redirect(url_for('login'))

@app.route('/process', methods= ['GET','POST'])
def process():
    firstName = request.form.get('firstName')
    print(format(firstName))
    return jsonify({'output':'Full Name: ' + format(firstName)})


####################
# Data Visualisation
####################


@app.route('/visualization', methods= ['GET','POST'])
def visualization() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        try:

            filename = session['filename']
            # Dictionnary of columns for form select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]

            if request.method == 'POST':
                
                if request.form['graph'] == 'heat':
                    heatmap = do_heatmap(df)
                    return render_template('dataviz.html',
                                        df_name= filename,
                                        heatmap = heatmap, col_selec= df_col_dic)

                elif request.form['graph'] == 'hist':
                    
                    col_selected = request.form.get('hist_col_selector')
                    hist = do_hist(df, col_selected)

                    return render_template('dataviz.html',
                                        df_name= filename,
                                        hist = hist, col_selec= df_col_dic)


                elif request.form['graph'] == 'mosaic':

                    col_selected = request.form.get('mosaic_col_selector')
                    data_mosaic = do_mosaic(df, col_selected)
                    return render_template('dataviz.html',
                                        df_name= filename,
                                        mosaic = data_mosaic, col_selec= df_col_dic)
                    
                elif request.form['graph'] == 'corr':
                    corr_matrix = do_corr_matrix(df)
                    return render_template('dataviz.html',
                                        df_name= filename,
                                        corr_matrix = corr_matrix, col_selec= df_col_dic)
                    
                    
                elif request.form['graph'] == 'stripplot':
                    col_selected_1 = request.form.get('plot_col_selector_1')
                    col_selected_2 = request.form.get('plot_col_selector_2')

                    stripplot = do_stripplot(df, col_selected_1, col_selected_2)
                    return render_template('dataviz.html',
                                        df_name= filename,
                                        stripplot = stripplot, col_selec= df_col_dic)

            return render_template('dataviz.html',
                                   df_name= filename, col_selec= df_col_dic)
        except:

            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('dataviz.html')

        return render_template('dataviz.html')

    return redirect(url_for('login'))


################
# Model training
################

@app.route('/model', methods = ['GET', 'POST'])
def model() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user
        global df
        global best_model

        try:

            # Dictionnary of columns to display into select tags
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]

            # Models for dictionnaries
            regression_models = ['Linear Regression', 'Logistic Regression']
            classification_models = ['KNN',
                    'KMeans',
                    'Random Forest Classifier',
                    'Decision Tree Classifier',
                    'SGDClassifier']

            # Dictionnary of models to display into select tags
            regression_dic = [{'name': model} for model in regression_models]
            classification_dic = [{'name': model} for model in classification_models]

            # Empty list & dict for the training loop management
            models_list = []
            mods = {}

            if request.method == 'POST':

                # User's input parameters
                label_selected = request.form.get('target')
                features_selected = request.form.getlist('features')
                input_test_size = request.form.get('splitValueInput')
                test_size = float(input_test_size)
                reg_mods_selected = request.form.getlist('reg_model')
                classif_mods_selected = request.form.getlist('class_model')

                # We concat the 2 models lists
                models_list = reg_mods_selected + classif_mods_selected

                minimum_context = {'reg_models' : regression_dic,
                'classif_model'  : classification_dic,
                'col_selec' : df_col_dic}

                # Drop cols for X
                # We compare the user selected cols for X with cols in the df
                col_to_drop = list(set(cols) - set(features_selected))

                X = df.drop(col_to_drop, axis = 1)
                y = df[label_selected]

                # X_train X_test split
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = test_size, random_state = 123456)

                # Training Loop
                models = {'Linear Regression': LinearRegression(),
                        'Logistic Regression' : LogisticRegression(solver= 'lbfgs', max_iter= 10000),
                        'KNN' : KNeighborsClassifier(n_neighbors = 10),
                        'Random Forest Classifier' : RandomForestClassifier(),
                        'Decision Tree Classifier' : DecisionTreeClassifier(),
                        'SGDClassifier' : SGDClassifier()
                        }

                # Check element in the moelds list is in the models dict
                for element in models_list :
                    for k, v in models.items() :
                        if k == element :
                            # Add the key and value model in a new dict
                            mods[k] = v

                # Empties lists for the result dataTable
                model_name = []
                model_list = []
                model_list = []
                runtime_list = []
                scor_list = []
                csv_list = []

                for k, v in mods.items() :

                    start_time = time.time()
                    model = v
                    model = model.fit(X_train, y_train)
                    runtime = time.time() - start_time

                    model_name.append(v)
                    model_list.append(k)
                    runtime_list.append(strftime("%H:%M:%S", gmtime(runtime)))

                    # Scores
                    scor = model.score(X_test, y_test)
                    scor_list.append(round(scor, 3))

                    y_predict = model.predict(X_test)

                # We pass all statistics into a dataframe to compare models
                result = pd.DataFrame({'Model ' : model_list,
                                    'Run time' : runtime_list,
                                    'Accuracy Score' : scor_list})
                # We sort the df by score
                result = result.sort_values(by=['Accuracy Score'], ascending=False)

                # We make a dictionnary to store the best model.
                model_key = model_name
                model_score_value = scor_list
                model_dict = dict(zip(model_key, model_score_value))
                best_model = max(model_dict, key= model_dict.get) # Find the max value in a dict

                return render_template('model.html', df_result = [result.to_html(classes = 'data')],
                        **minimum_context,
                        label_selected = label_selected, features_selected = features_selected, test_size = test_size,
                        reg_mods_selected = reg_mods_selected, classif_mods_selected = classif_mods_selected,
                        best_model = best_model)
                
            return render_template('model.html',
                                   reg_models = regression_dic,
                                   classif_model = classification_dic,
                                   col_selec = df_col_dic)

        except:

            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('model.html')

        return render_template('model.html')

    return redirect(url_for('login'))


############
# Prediction
############

@app.route('/prediction')
def prediction() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        try:

            filename = session['filename']
            # Dictionnary of columns for form select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]

            
            return render_template('prediction.html',
                                   df_name= filename,
                                   best_model = best_model)
        except:

            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('prediction.html')

        return render_template('prediction.html')

    return redirect(url_for('login'))


##########
# Settings
##########

@app.route('/settings')
def settings() :

    # Manage the user connection
    if 'user' in session :

        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        # We fetch user info in the firebase database
        user     = auth.refresh(user['refreshToken'])
        userInfo = auth.get_account_info(user['idToken'])
        userId   = userInfo['users'][0]['localId']
        username = db.child("users").child(userId).child('username').get().val()
        email    = db.child("users").child(userId).child('email').get().val()
        function = db.child("users").child(userId).child('function').get().val()

        return render_template('settings.html', 
                            username = username, 
                            email = email, 
                            function = function)

        return render_template('settings.html')

    return redirect(url_for('login'))


if __name__ == '__main__' :
    app.run(debug=True)
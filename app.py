import pyrebase
from flask import *
import secrets
import time
import json
import pandas as pd
from werkzeug.utils import secure_filename
import io
from flask_wtf import FlaskForm
from wtforms import SelectField


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


class SelectForm(FlaskForm):
    na_act = SelectField('Missing Values', choices=[
        ('dropna()','Drop NA'),('fillna()','Fill NA'),('replace()','Replace NA')])

##############################################
############# ROUTES #########################
##############################################

#####################
# Index for Home Page
#####################

@app.route('/')
def home() :
    return render_template('index.html')

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

    # We refresh session['user']
    session.pop('user', None)

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
            filename = session['filename']
            print(filename)
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
                                df_name = filename,
                                nb_col = nb_col, nb_rows = nb_rows,
                                dataset = [df.to_html(classes = 'data')],
                                describe = [desc.to_html(classes = 'data')],
                                df_infos = [df_infos.to_html(classes = 'data')],
                                df_na = [df_na.to_html(classes= 'data')])
            
        except:
            
            if request.method == 'POST':

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
        
        try :

            # We first make a copy of the dataframe
            df_to_clean = df.copy()
            # Missing Values for form-select
            na_actions = [{'name': 'Drop NA'}, {'name': 'Fill NA'}]

            # Dictionnary of columns for form-select
            cols = df_to_clean.columns
            df_col_dic = [{'name':col} for col in cols]

            if request.method == 'POST' :
                
                na_action_selected = request.form['nan_action']
                col_selected = request.form.getlist('col_selector')

                if na_action_selected.lower() == 'drop na' :
                    
                    # We handle dropna() depending on selections.
                    if col_selected[0].lower() == 'all' :
                        df_wo_na = df_to_clean.dropna()
                    else :
                        df_wo_na = df_to_clean.dropna(subset = (col_selected))

                    return render_template('dataxplo.html',
                                           dataset = [df_wo_na.to_html(classes = 'data')],
                                           na_actions = na_actions, col_selec = df_col_dic,
                                           col_selected = col_selected, na_action_selected = na_action_selected)

                return render_template('dataxplo.html',
                                na_actions = na_actions, col_selec = df_col_dic,
                                col_selected = na_action_selected, na_action_selected =na_action_selected)
                

            return render_template('dataxplo.html',
                                dataset = [df.to_html(classes = 'data')],
                                na_actions = na_actions, col_selec = df_col_dic)

        except:

            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('dataxplo.html')

        return render_template('dataxplo.html')

    return redirect(url_for('login'))




####################
# Data Visualisation
####################

@app.route('/visualization')
def visualization() :

    # Manage the user connection
    if 'user' in session :
        
        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        try:
            # Dictionnary of columns for form select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]
            
            return render_template('dataviz.html', dataset = [df.to_html(classes = 'data')])
        except:
            
            flash('There is no dataframe uploaded. PLease visit DATASET page first', 'warning')
            return render_template('dataviz.html')

        return render_template('dataviz.html')
    
    return redirect(url_for('login'))


################
# Model training
################

@app.route('/model')
def model() :

    # Manage the user connection
    if 'user' in session :
        
        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        try:
            # Dictionnary of columns for form select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]
            
            return render_template('model.html', dataset = [df.to_html(classes = 'data')])
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
            # Dictionnary of columns for form select
            cols = df.columns
            df_col_dic = [{'name':col} for col in cols]
            
            return render_template('prediction.html', dataset = [df.to_html(classes = 'data')])
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
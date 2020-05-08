import pyrebase
from flask import *
import secrets
import time
import json
import pandas as pd
from werkzeug.utils import secure_filename

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

# Index for Home Page
@app.route('/')
def home() :
    return render_template('index.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login() :
    
    not_logged = 'Please check your account informations.'
    logged = 'Welcome Back !'
    
    if request.method == 'POST' :
        email    = request.form['email']
        password = request.form['pass']
        
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = user
            return redirect(url_for('plateform'))
        
        except:
            return render_template('login.html', invalid = not_logged)
        
    return render_template('login.html')

# Log Out
@app.route('/logout')
def logout():
    
    session.pop('user', None)
    return redirect(url_for('home'))

# Change Password Page
@app.route('/change_pass', methods = ['GET', 'POST'])
def change_password() :
    
    if request.method == 'POST' :
        email = request.form['email']
        auth.send_password_reset_email(email)
        
    return render_template('change_pass.html')
 
# Sign Up Page
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
            
            return redirect(url_for('login'))
        
        else :
            return render_template('register.html', warning = 'Please enter the same password for confirmation.')
    
    return render_template('register.html')

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

        # User db creation
        userDB = {'username': username, 'email' : email, 'function' : function}
        db.child('users').child(userId).set(userDB)
        
        return render_template('settings.html', info_updated = 'Your informations have been changed.')

    return render_template('update_info.html')

    
@app.route('/delete_account')
def delete_account() :
    
    user     = session['user']
    user     = auth.refresh(user['refreshToken'])
    userInfo = auth.get_account_info(user['idToken'])
    userId   = userInfo['users'][0]['localId']
    
    db.child('users').child(userId).remove()
    
    return redirect(url_for('home'))

# Plateform
@app.route('/plateform')
def plateform() :
    
    # Manage the user connection
    if 'user' in session :
        
        user = session['user']
        # idToken expires after 1 hour, so we refresh the token to avoid stale token.
        user = auth.refresh(user['refreshToken'])
        session['user'] = user

        return render_template('plateform.html')
    
    return redirect(url_for('login'))

# Upload File
@app.route('/plateform', methods = ['GET', 'POST'])
def upload_file():
    
   if request.method == 'POST':
      f        = request.files['file']
      filename = secure_filename(f.filename)
      df       = pd.read_csv(f)
      desc     = df.describe()
      
      return render_template('plateform.html', df_name = filename,
                             dataset = [df.to_html(classes = 'data')],
                             describe = [desc.to_html(classes = 'data')])

# Plateform Anchors Management
# ----------------------------

# Data Exploration
@app.route('/exploration')
def exploration() :
    
    return redirect(url_for('plateform') + '#exploration')


# Data Visualisation
@app.route('/visualization')
def visualization() :
    return redirect(url_for('plateform') + '#visualization')

# Model training
@app.route('/model')
def model() :
    return redirect(url_for('plateform') + '#model')

# Prediction
@app.route('/prediction')
def prediction() :
    return redirect(url_for('plateform') + '#prediction')

# ----------------------------
# Plateform Anchors Management

# Settings
@app.route('/settings')
def settings() :
    
    try:
        user     = session['user']
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
    
    except:
        return render_template('settings.html')
    
    return render_template('settings.html')

if __name__ == '__main__' :
    app.run(debug=True)
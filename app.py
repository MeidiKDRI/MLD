import pyrebase
from flask import *
import secrets

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
        
        username = request.form['username']
        email = request.form['email']
        function = request.form['function']
        password = request.form['pass']
        confirm_pass = request.form['pass_confirmation']
        
        if password == confirm_pass :
            new_user = auth.create_user_with_email_and_password(email, password)
            auth.send_email_verification(new_user['idToken'])
            return redirect(url_for('login'))
        
        else :
            return render_template('register.html', warning = 'Please enter the same password for confirmation.')
    
    return render_template('register.html')

# Plateform
@app.route('/plateform')
def plateform() :
    
    # Manage the user connection
    if 'user' in session :
        return render_template('plateform.html')
    
    return redirect(url_for('login'))

if __name__ == '__main__' :
    app.run(debug=True)
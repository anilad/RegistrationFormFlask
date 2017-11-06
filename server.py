from flask import Flask, render_template, request, redirect, session, flash
import re

app = Flask(__name__)
app.secret_key = 'keepitsecretkeepitsafe'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')
def index():
    if not 'loggedIn' in session:
        session['loggedIn']=False
    if not 'name' in session:
        session['name'] = None
    if not 'email' in session:
        session['email'] = None
    if not 'password' in session:
        session['password'] = None
    if not 'birthdate' in session:
        session['birthdate']=None
    if not 'count' in session:
        session['count']=0
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    isValid=False
    #check for valid input in fName (cannot be blank)
    if len(request.form['fName'])<1:
        flash('First Name cannot be blank!')
        isValid = True
    else:
        session['fName'] = request.form['fName']
    #check for valid input in lName (cannot be blank)
    if len(request.form['fName'])<1:
        flash('Last Name cannot be blank!')
        isValid = True
    else:
        session['lName'] = (request.form['lName'])
    #check for valid input in email (must be valid email)
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!")
        isValid = True
    elif not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!")
        isValid = True
    else:
        session['email']=request.form['email']
    #check for valid input in password(must be 6-10 characters and  contain upper and lowercase letters and numbers)
    if len(request.form['password'])<6 or len(request.form['password'])>10:
        flash('Password must be 6-10 characters long!')
        isValid=True
    else:
        isNum = False
        isUpper=False
        for el in request.form['password']:
            if not el.isupper():
                isUpper=True
            if not el.isdigit():
                isNum=True
        if isUpper and isNum:  
            flash('Password must contain at least 1 uppercase character and 1 number!')
            isvalid=True
        else:
            session['password']=request.form['password'] 
    
    if isValid:
        return redirect('/')        
    else: 
        name =request.form['fName'] + " " + request.form['lName']
        print name
        session['name']= name
        return redirect('/user')

@app.route('/login', methods=['POST'])
def login():
    return redirect('/user')

@app.route('/user')
def user():
    if session['count']>0:
        greeting = "Welcome back"# {}".format(session['name'])
        session['count'] +=1
    else:
        greeting = "Welcome"# {}".format(session['name'])
        session['count']+=1
    return render_template('userInfo.html', greeting=greeting)

@app.route('/logout')
def logout():
    session['loggedIn']=False;
    return redirect('/')

app.run(debug=True)
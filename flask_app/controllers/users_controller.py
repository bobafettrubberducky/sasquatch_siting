from flask import request, render_template, redirect, session, flash

from flask_app.models.user import User
from flask_app.models.sighting import Sighting

from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#********************* REGISTER *********************************

@app.route("/")
def root():
    return render_template('index.html')

#& Step 0 - CREATE - Validation then Save() new user
@app.route('/register', methods=['POST'])
def register():

    #$ STEP 0 - Validated Register from has correct info populated 
    if not User.validate_register(request.form):
        return redirect('/')
    
    #$ STEP 0A - hash password by re-writing request.form
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        #! Hash the password created by the user
    }

    #$ STEP 0B - Pass `data` into save() method will create new user & receive user_id
    id = User.save(data)
    # id = 1

    #$ STEP 0C - Pack the id=1 store in session dictionary
    session["user_id"] = id
    # session={"user_id":1}


    #$ STEP 0D - SEND to '/dashboard'
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():

    #$ STEP 0E - check if "user_id" in session, if session = {"user_id":1} or {}
    if "user_id" not in session:
        return redirect('/logout')
    
    #$ STEP 0F - unpack session dictionary store value into variable id & store key,value into data dictionary
    data = {
        'id': session['user_id']
    }
    #data = {'id':1}

    #$ STEP 0G - pass the data dict storing id=1 into method get_by_id()
    user = User.get_by_id(data)
    #user = objects instance can be called using attributes (user.first_name)

    #& STEP 0H - get_all grab all recipes from  db -> save list/dict in variable recipes -> send to dashboard.html 
    sightings = Sighting.get_all()
    # recipes = {[]}

    


    return render_template("dashboard.html", user=user, sightings=sightings)


@app.route('/logout')
def logout():
    #$ STEP 0E - clear out session and redirect '/' index.html page
    session.clear()
    return redirect('/')


#********************* LOGIN *********************************

#& LOGIN - Validation 
@app.route('/login', methods=['POST'])
def login():
    
    #$ STEP 1A - pass in request.form (browser Login email & password) into get_by_email()
    user = User.get_by_email(request.form)
    # user = object instance can be called using attributes (user.first_name)

    #$ STEP 1B - checks if user has a value or not 
    if not user:
        flash("Invalid Email", "login")
        return redirect('/')
    # user = False
    # if not False -> flash error and redirect '/'
    #user = objects instance 
    # if not True -> if Falase - > skip code 

    #$ STEP 1C - checks user.password(in database) & request.form ["password"] (in browser) match
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Password Invalid", "login")
        return redirect("/")
    
    #? Print user attributes for debugging
    print("******\n",user.__dict__)
    
    #$ STEP 1D - pack session with key user_id and value user.id of the user logging in email/password in browser to be later used for other url
    session["user_id"] = user.id
    # session = {"user_id":user_id}

    return redirect('/dashboard')
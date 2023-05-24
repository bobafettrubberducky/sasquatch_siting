from flask import redirect, render_template, request, session, flash
from flask_app import app

from flask_app.models.sighting import Sighting
from flask_app.models.user import User

#************* STEP 0 New Sighting ***********************
#& STEP 0 - Crete a new sighting for user logged in (user id = 1, sighting id=1, and so foreign id user_id = 1)
#^ `CREATE`
#^ GET/users/create - show the create user form (
#^ POST/users - create a new user (used in form html)

# RENDER '/new/sighting
@app.route('/new/sighting')
def new_sighting():
    
    #& STEP 0A - check if user_id in session 
    if 'user_id' not in session:
        return redirect ('/logout')
    # if True -> redirect '/logout'
    # IF False -> skip this code 
    
    #& STEP 0B - unpack session to get user_id from users_controller.py
    data = {
        "id" : session['user_id']
    }
    #data = {"id":1}

    #& STEP 0C - pass data={"id":1} into get_by_id() to grab info for id=1
    user = User.get_by_id(data)
    #user = objects instance can be called using attributes (user.first_name)

    #& STEP 0D - render "new_sighting.html" and pass in variable user into html
    return render_template('new_sighting.html',user=user)

#& POST the new sighting in database 
@app.route('/create/sighting', methods=['POST'])
def create_sighting():
    
    #& STEP 0D - check if user_id in session 
    if 'user_id' not in session:
        return redirect ('/logout')
    # if 'user_id not in session{} -> if True -> redirect '/logout'
    # if 'user_id' not in session = {'user_id': 1} -> if false -> skip code
    
    #& STEP 0E - Sighting browser validate populated by user in browser
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    
    #& STEP 0F - recreate request.form since `unpack session['user_id'] into user_id` & `under30 needs to be integer``
    data = {
        "location": request.form['location'],
        "description":request.form['description'],
        "date":request.form['date'],
        "user_id": session['user_id'],
        # user_id:1
        "number": int(request.form["number"])
        # user30: 0 if No button selected or user30: 1 YES button selected 
        #! force under30 to be integer since what come back selected 0 and 1 in new_sighting.html comes as string & we want integer
    } 

    #& STEP 0G CREATE - pass in created data into save() method to save `new sighting` to database under `sightings` table
    Sighting.save(data)

    #& STEP 0H - send back to '/dashboard'
    return redirect('/dashboard')

#****************** STEP 1 - EDIT SIGHTING 


#& STEP 1 - EDIT recipe id=1 for user=1 
#^ `UPDATE`
#^ GET/users/123/edit - show the edit form user with ID 123
#^ POST/users/123/edit - update user with ID 123

#& When Edit button pressed on '/dashboard' grab recipes id  dashboard.html  <a href="/edit/recipe/{recipe.id}">Edit</a>
#& '/edit/recipe/1
@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    
    #& STEP 1A - check if user_id in session 
    if 'user_id' not in session:
        return redirect ('/logout')
    # if 'user_id not in session{} -> if True -> redirect '/logout'
    # if 'user_id' not in session = {'user_id': 1} -> if false -> skip code

    #& Step 1B - save the recipes id to dictionary data 
    data = {
        "id":id
    }
    #data = {"id":1}, recipes id = 1

    #& Step 1B - unpack session and save user foreign key to dictionary user_data 
    user_data = {
        "id":session["user_id"]
    }
    # user_data = {"id": 1}, foreign id of recipes (which is user id = 1)

    #& Step 1C - set objects for attributes of Recipe
    # data = {"id":1}, recipes id 
    edit = Sighting.get_one(data)

    #& Step 1C - set object for attributes of User
    #user_data = {"id":"1"}, foreign id for recipes (which is user id=1)
    user_data = User.get_by_id(user_data)

    #& Step 1D - render the page edit_recipe.html
    return render_template("edit_sighting.html", edit=edit, user_data = user_data)
    #! edit = Instance of objects accessed with attributes for `Recipes`` (edit.id, edit.name, edit.description edit.under30)
    #! user_data = Instance of objects access with attributes for `User`` (user_data.id, user_data.first_name, user_data.last_name)
    #! edit python passed into => edit html
    #! user_data passed into => user_data html 
    #! edit and user_data passed into the html edit_recipe.html 

#& Step 1E - #^ POST/users/123/edit - update user with ID 123
#& "edit_recipe.html" when `submit` button clicked pull up <form action="/update/recipe" method="post"> and send to "/update/recipe"
@app.route('/update/sighting/<int:id>', methods=['POST'])
def update_sighting(id):

    #& Step 1F - Check user_id in session
    if 'user_id' not in session:
        return redirect('/logout')
    # if 'user_id not in session{} -> if True -> redirect '/logout'
    # if 'user_id' not in session = {'user_id': 1} -> if false -> skip code
    
    #& STEP 1G - Edit Recipe browser validate populated by user
    #& If validate_recipe() are false then send you back to "/new/recipe" to input a new recipe
    #& errors will be shown in "new_recipe.html"
    #& Note: there's no reason to input incorrect info since it was prepopulated with previous info so kicked you back to new recipe!
    if not Sighting.validate_sighting(request.form):
        return redirect('/new/sighting')
    
    #& STEP 1H - Create a new request.form since recipe id needs passed in from previous route (where variable edit.id (object) stores  the recipe id=1) &  under30 needs to integer we've re-wrote request.form
    #& Note: we can't use "id" = edit.id since object in previous url (GET '/update/recipe/<int:id>') and we're in (POST /update/recipe' methods=['POST']) so we have to pass it in form, create new url (POST '/update/recipe/<int:id>' methods=['POST']) and set "id" = id
    data = {
        "id":id,
        #! this is recipe id=1, don't need the user_id since we're updating recipe table at id=1 in database
        #! 0. using edit.id, this is where recipe id=1 stored
        #! 1. update the URL of the form action in the edit_recipe.html template to include the recipe ID:
        #!    <form action="/update/recipe/{{ edit.id }}" method="post"> in edit_recipe.html
        #! 2. In the def update_recipe() function, modify the function signature to include the id parameter:
        #!    @app.route('/update/recipe/<int:id>', methods=['POST'])
        #!    def update_recipe(id):
        #! 3. Update the data dictionary to include the id parameter:
        #!    data = { "id": id, ...etc } 
        "location":request.form["location"],
        "description":request.form["description"],
        "date": request.form["date"],
        "number":int(request.form["number"]),
        #! For user30 the value "request.form["under30"]" need to convert the value from a string in html into a integer in python to send to the database. 
    }

    #& STEP 1I - pass in data (new request.form) in update() so that we update recipe table for recipe id=1 in the database 
    Sighting.update(data)
    
    #& Step 1J - redirect '/dashboard' once upload complete
    return redirect('/dashboard')


#*********************** VIEW IN DASHBOARD ***********************

#& STEP 2 - in dashboard.html clicked hypertext "View Instructions" to render show_recipe.html to show the recipe card
#& <a href="/recipe/{{recipe.id}}">View Instructions</a>
@app.route('/sighting/<int:id>')
def show_sighting(id):
#! from the url in browser grabbed recipe id, passed it into `def show_recipe(id), and stored variable id=1 (recipe id). To show info card for recipe id=1. 


    #& Step 2A - Check user_id in session
    if 'user_id' not in session:
        return redirect('/logout')
    # if 'user_id not in session{} -> if True -> redirect '/logout'
    # if 'user_id' not in session = {'user_id': 1} -> if false -> skip code

    #& Step 2B - save the recipes id to dictionary data 
    data = {
        "id":id
    }
    #data = {"id":1}, recipes id = 1

    #& Step 2B - unpack session and save user foreign key to dictionary user_data 
    user_data = {
        "id":session["user_id"]
    }
    # user_data = {"id": 1}, foreign id of recipes (which is user id = 1)

    #& Step 2C - set objects for attributes of Sighting
    # data = {"id":1}, recipes id 
    sighting = Sighting.get_one(data)

    #& Step 2C - set object for attributes of User
    #user_data = {"id":"1"}, foreign id for recipes (which is user id=1)
    user = User.get_by_id(user_data)
    
    #& Step 2C - set object for attributes of sighting.user (we can access the sighting.user.first_name) which is the article user first name which will be accessed in show_sighting.html
    #& using the foreign key user_id for Sighting was able to find user connected to user_id. O yeah
    user_id = sighting.user_id

    user_info = {"id": user_id}

    sighting.user = User.get_by_id(user_info)

    # print("*******\n",sighting.user.first_name)


    #& Step 2D - render show_recipe.html and pass in recipe variable objects (user & recipe) in html so we access info using  attributes 
    return render_template("show_sighting.html", sighting=sighting, user=user)


#**************************** DELETE IN DASHBOARD *******************************

#^ `DELETE` Recipe

#&STEP 3 - in dashboard.html clicked hypertext "DELETE" to remove the sighting from the logged in user dashboard 
@app.route('/destroy/sighting/<int:id>')
def destroy_recipe(id):
#! from the url in browser grabbed recipe id, passed it into `def show_recipe(id), and stored variable id=1 (recipe id). To show info card for recipe id=1.

    #& Step 3A - Check user_id in session
    if 'user_id' not in session:
        return redirect('/logout')
    # if 'user_id not in session{} -> if True -> redirect '/logout'
    # if 'user_id' not in session = {'user_id': 1} -> if false -> skip code

    #& Step 3B - save the sighting id to data dictionary
    data = {
        "id":id
    }

    #& Step 3C - pass the recipe id in the data dictionary into destroy() method to remove recipe from recipes table in db
    Sighting.destroy(data)

    #& Step 4C - once destroyed return back url '/dashboard'
    return redirect("/dashboard")
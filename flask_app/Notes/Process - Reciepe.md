# Process

Wire-frame
1 - Circle Diagram user actions
2 - ERD/DB Set Up

Clickable Prototype
1 - Folder Set Up
2 - Hard-code Template (+ clickable tabs)
3 - Set Up empty routes (& TEST)

Features
1 Seed Database (can do w/ a create method or manually in workbench)
2 Implement Common Model Methods
3 POST ROUTES + VALIDATIONS
4 GET ROUTES + dynamic
5 GET ROUTE - Add prepopulated fields

## ************** WIRE-FRAME ************************

1. Circle Diagram user actions

`/` - (Register & Login page) (index.py)

- Submit -> button -> `/recipes`
- Submit - button -> `/recipes`
- ** Registration Validation
- ** Login Authentication

`/recipes` - (DISPLAY Page) (dashboard.py)

- +Create - anchor tag -> `/recipes/new`
- Logout - anchor tag -> clear session & redirect `/`
- view recipe - anchor tag -> `/recipes/2`
- edit - anchor tag -> `/recipes/edit/4`
- delete - anchor tag -> removed from database

`/recipes/new` - (CREATE Recipe page) (new_recipe.html)

- back to recipes - anchor tag -> `/recipes`
- logout - anchor tag -> clear session & redirect `/`
- Submit - button -> `/recipes`

`recipes/2` -  (DISPLAY Recipe Page) (show_recipe.html)

- back to recipes - anchor tag -> `/recipes`
- logout - anchor tag -> clear session & redirect `/`

`/recipes/edit/4` - (EDIT Recipe) (edit_recipe.html)

- back to recipes - `/recipes`
- logout 
- SUBMIT - button - `/recipes`

2. ERD/DB set up

`One-to-Many Relationship`

Query = `SELECT * FROM recipes.users`

| users      |   | recipes      |
|------------|---|--------------|
| id         |   | id           |
| first_name |   | name         |
| last_name  |   | description  |
| email      |   | under30      |
| password   |   | instructions |
| created_at |   | date_made    |
| updated_at |   | created_at   |
|            |   | updated_at   |
|            |   | user_id      |

## 2. ****************Clickable Prototype ****************

1. Folder Set Up

- flask_app
  - configs
    - mysqlconnection.py
  - controllers
  - models
  - static
  - templates
  - __init__.py
- server.py

## 1. ****************WireFrame ****************

1. Diagram user actions - circle actionable items (anchor tags, submit form button, url)

localhose:5000/cookies

- New Order (anchor tag) -> localhost:500/cookie/new
- Edit -> localhost:500/cookie/edit/4

localhost:500/cookie/new
Validation - all fields required, Name & Cookie Type must be 2 char, Number boxes can't be -#

- Log -> saves a purchase  & redirect to dashboard

localhost:500/cookie/edit/4
Validation - any errors redirec back "cookies/edit", use same id of the order again to show error

- Log -> saves purchase & redirect to dashboard

![Alt text](1.%20Action%20Items.png)

2. ERD/DB Set UP - look columns see title in table (include id, created_at, updated_at) generate MySQL ERD/Forward engineer to create schema, check it it works by running sql query.

Query  = `SELECT * FROM cookie_orders.cookie_orders`

| ERD         |
|-------------|
| id          |
| name        |
| cookie_type |
| num_boxes   |
| updated_at  |
| created_at  |

## 2. ****************Clickable Prototype ****************

1. Folder Set Up

- flask_app -> configs,controllers,models,static,templates,database
- ____ini___.py
- server.py

2. Hard-Code HTML Template (+clickable links)

They're `3 pages` in wire-frame so `3 html` need to be created

3. Set up Empty Routes (Test them)

`GET`
@app.route("/") - redirect "/cookie"
@app.route("/cookie") - Root & DISPLAY
@app.route("/cookie/new") - CREATE
@app.route("/cookie/edit/<order_id>") - EDIT

`POST` ACTION ROUTE
@app.route("/cookies/create", methods=["POST"])
@app.route("/cookies/update", methods=["POST"])

## 3 ****************Features ****************

1. Seed Database (can do w/ a create method or manually in workbench)

`/cookies` ->  `cookie.html`

- New Order (anchor tag) -> `/cookie/new`
- Edit (anchor) -> `/cookie/edit/1`
- Edit (anchor) -> `/cookie/edit/1`

`/cookie/new` -> `new_order.html`

- Back to purchase (Anchor) -> `/cookies` -> `cookie.html`
- Form (`/cookies/create POST`)
- Submit (anchor+button) -> database -> `/cookies`

`/cookie/edit`-> `edit_order.html`

- Back to purchase (Anchor) -> `/cookies` -> `cookie.html`
- Form (`/cookie/update POST`)
- Submit (anchor+button) -> database -> `/cookies`

2. Implement Common Model Methods - Test/Hardcode CREATE method from CRUD

- Make sure query work in MySQL workbench by testing it

`SELECT * FROM  cookie_orders.cookie_orders;`

`INSERT into cookie_orders (name, cookie_type, num_boxes) VALUES ('test', 'test', 4);`

- When testing in models hard code by input values in query and see if values are in workbench MySQL

```python - cookie_order.py
@classmethod
def save(cls):
  query = "INSERT into cookie_orders (name, cookie_type, num_boxes) VALUES ('test', 'test', '13');"
  result = connectToMySQL(cls.DB).query)db(query)
  return result
```

```python - cookie_orders.py
@app.route("/cookies/create", methods=["POST"])
def create_order():
    print("In CREATE POST route")
    print("****************\n",request.form,"\n***************")
    #! ImmutableMultiDict([('name', 'John'), ('cookie_type', 'Cinnamon'), ('num_boxes', '4')]) 
    Cookie_order.save()

    return redirect('/cookies')
```

`Note: query user double quote "" and single quote '' so I could pass in information without errors`

- check Workbench MySQL -> `SELECT * FROM  cookie_orders.cookie_orders;` -> yup values are in the table

3. POST ROUTE

`POST ROUTE - CREATE method`

- POST- included placeholder `%()s` in query then import `request.form` dictionary to populate placeholder

```python - cookie_order.py
@classmethod
    def save(cls, data):
        query = "INSERT into cookie_orders (name, cookie_type, num_boxes) VALUES (%(name)s, %(cookie_type)s, %(num_boxes)s);"
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result
```

```python - cookie_orders.py
@app.route("/cookies/create", methods=["POST"])
def create_order():
    print("In CREATE POST route")

    Cookie_order.save(request.form)

    return redirect('/cookies')
```

- check Workbench MySQL -> `SELECT * FROM  cookie_orders.cookie_orders;` -> yup values are in the table

`POST ROUTE - EDIT method`

```python - cookie_orders.py
@app.route("/cookies/update", methods=["POST"])
def update_order():
    print("In UPDATE POST route")
    print("****************\n",request.form, "\n***************")
    #! ImmutableMultiDict([('name', 'James'), ('cookie_type', 'chicken'), ('num_boxes', '3')])

    Cookie_order.edit(request.form)

    return redirect('/cookies')
```

```python - cookie_order.py
#& EDIT METHOD
    @classmethod 
    def edit(cls,data):
        query = "UPDATE cookie_orders SET name=%(name)s, cookie_type=%(cookie_type)s, num_boxes=%(num_boxes)s WHERE id=%(id)s;"
        # UPDATE table_name SET column1 = value1, column2 = value2, ...WHERE condition;
        result = connectToMySQL(cls.DB).query_db(query, data)
        return result

```

```HTML - edit_order.html
 <input type="hidden" name="id" value="1">
      <!--$ Hard Code id=1 to pass pass through  `/cookies/edit/<order_id>` to pass in id=1 into  `edit(cls,data):` as variable  -->
```

3. POST ROUTE + VALIDATION

`*************** POST ROUTE + VALIDATION - CREATE **********`

``` HTML - new_order.html
    <!--! *** Validation *** -->
      {% with messages = get_flashed_messages() %}
      <!--$ messages = stores list of flashed messages if fields blank and not inter value -->
      <!--$ messages = ["Name required!"."Cookie type required!","Number of boxes required!"]  -->
        {% if messages%}
      <!-- $ if messages -> message= some data in list making it True -> if True -> run code --> 
          {% for message in messages%}
            <p class="error">{{message}}</p>
          {% endfor %}
        {% endif %}
      {% endwith%}
      <!--! **** Validation *** -->
```

```python - models - cookie_order.py
#& VALIDATE METHOD 
    @staticmethod
    def validate_cookie_order(data):
        is_valid = True
        #$ set flag (boolean) to True for variable is_valid

        #& Validate - check if each field is blank
        if len(data["name"]) == 0:
            flash("Name required!")
            is_valid = False
        if len(data["cookie_type"]) == 0:
            flash("Cookie type required!")
            is_valid = False
        if len(data["num_boxes"]) == 0:
            flash("Number of boxes required!")
            is_valid = False
        #& Validate - check if the "number of cookies" are positive
        elif int(data["num_boxes"]) <= 0:
            #$ request.form info comes back as string so we have to cast it as an int before we compare to 0
            flash("Number of boxes must be positive number")
            is_valid = False

        return is_valid
```

```python controllers - cookie_orders.py
@app.route("/cookies/create", methods=["POST"])
def create_order():
    print("In CREATE POST route")

    #& Validation Called
    if Cookie_order.validate_cookie_order(request.form):
        #! If TRUE run the code b/c it's fine
        Cookie_order.save(request.form)
        return redirect("/cookies")
    
    #! IF FALSE - redirect back to the new page so re-enter info
    return redirect('/cookies/new')
```

`********** POST ROUTE + VALIDATION - CREATE **********`

```html templates/edit_order.py
    <!--! *** Validation *** -->
      {% with messages = get_flashed_messages() %}
      <!--$ messages = stores list of flashed messages if fields blank and not inter value -->
      <!--$ messages = ["Name required!"."Cookie type required!","Number of boxes required!"]  -->
        {% if messages%}
      <!-- $ if messages -> message= some data in list making it True -> if True -> run code --> 
          {% for message in messages%}
            <p class="bg-danger text-white">{{message}}</p>
          {% endfor %}
        {% endif %}
      {% endwith%}
      <!--! **** Validation *** -->

<!--! *** Hidden Input - Hardcoded id=1 *** -->
<input type="hidden" name="id" value="1">
      <!--$ Hard Code id=1 to pass pass through  `/cookies/edit/<order_id>` to pass in id=1 into  `edit(cls,data):` as variable  -->
      <!--$ We'll make it dynamic later -->

```

```python - models/cookie_order.py (code already writen & reused for controller)
#& Validate - check if each field is blank
        if len(data["name"]) == 0:
            flash("Name required!")
            is_valid = False
        if len(data["cookie_type"]) == 0:
            flash("Cookie type required!")
            is_valid = False
        if len(data["num_boxes"]) == 0:
            flash("Number of boxes required!")
            is_valid = False
        #& Validate - check if the "number of cookies" are positive
        elif int(data["num_boxes"]) <= 0:
            #$ request.form info comes back as string so we have to cast it as an int before we compare to 0
            flash("Number of boxes must be positive number")
            is_valid = False

```

``` python - controllers/cookie_orders.py
#& UPDATE - POST ROUTE
@app.route("/cookies/update", methods=["POST"])
#$ "/cookies/updat/<id>" isn't needed since we can put `id` in request.form 
def update_order():
    print("In UPDATE POST route")

    #& Validation Called
    if Cookie_order.validate_cookie_order(request.form):
        Cookie_order.edit(request.form)
        return redirect("/cookies")

    return redirect(f"/cookies/edit/{request.form['id']}")
    #$ we just added the id at the end of the f-string. Used the hardcoded  id from `hidden input` passed the value into request.form. id key value pair into request.form
```

1. GET ROUTES

`GET ROUTE - READ`

`******** PSUEDO CODE ********`
Need to create a method called "get_all()" that will get all the information from the database
and give us list of objects

```python - controllers/cookie_orders.py
#& READ - GET ROUTE
@app.route("/cookies")
def index():
    print("In INDEX page route")
   Cookie_order.get_all()
    return render_template("cookie.html")
```

`******** PSUEDO CODE ********`

```python - models/cookie.html
#& READ
    #& We're not passing in any data because getting all information from database 
    @classmethod
    def get_all(cls):

        query = 'SELECT * FROM cookie_orders;'
        users = connectToMySQL(cls.DB).query_db(query)
        #$ users = list/dictionary

        result = []
 
        for user_dict in users:
            #$ loop over the list/dict
            user_object = Cookie_order(user_dict)
            #$ dictionary row unpack data into attributes on the class Cookie_orders
            result.append(user_object)
            #$ append the user objects to list variable result
 
        return result
        #$ return the result = list 
```

```python - controller/cookie_orders.py
#& READ - GET ROUTE
@app.route("/cookies")
def index():
    print("In INDEX page route")
    all_orders = Cookie_order.get_all()
    return render_template("cookie.html", orders = all_orders)
    #! all_orders = variable  list of objects in python
    #! orders = variable list of objects 
    #! all_orders py passes list to = orders in html to cookie.html
```

```html - templates/cookie.html - test jinja {{orders}} on the top html to see if it works
<div class="flex-container with-margins">
            {{orders}}

```

``` html - templates/cookie.html - jinja functional
<tbody>
                    <!--! READ - List Objects -->
                    <!--! Sending in order object list or order object want to change that for each order (order.name, order,cookie_typ, ..etc) -->
                    {% for order in orders%}
                    <tr> 
                        <td>{{order.name}}</td>
                        <td>{{order.cookie_type}}</td>
                        <td>{{order.num_boxes}}</td>
                        <td><a href="/cookies/edit/{{order.id}}">edit</a></td>
                        <!--$ we have to not hardcode `/cookies/edit/<order_id>` in the route-->
                        <!--$ make sure it comes order id dynamically -->
                    </tr>
                    {% endfor %}
                    
                    <!--!  -->
                </tbody>
```

5. GET ROUTE - Add pre-populated fields

`GET ROUTE - EDIT`

- When we go to edit page want to have the values pre-populated so the user doesn't have to type the information again
- add `value` to the input tag to have that info pre-populated for the user

`Psuedo COde`
When the edit page is rendered, edit page give id in the url, use to call Cookie_order.get_one(order_id) that passses
the id from the url into method. When comes back write to variable

```python controllers/cookie_orders.py
#& UPDATE - GET ROUTE
@app.route("/cookies/edit/<order_id>")
def edit_page(order_id):
    #! need to pass in fake argument "order_id" to render page
    print("In EDIT route with id", order_id)

    cookie_order = Cookie_order.get_one(order_id)

    return render_template("edit_order.html")
```

```python models/cookie_order.py
 @classmethod
    def get_one(cls, order_id):
        query = "SELECT * FROM cookie_orders WHERE id = %(id)s;"
        order_dict = connectToMySQL(cls.DB).query_db(query,{"id":order_id})
        #! order_dict = list/ one dictionary
        order = Cookie_order(order_dict[0])
        #! order = order_dict[0] grabs the dictionary then pass into attributes of class Cookie_orders giving objects
        return order
        #! order = objects 
```

```python controllers/cookie_orders.py
#& UPDATE - GET ROUTE
@app.route("/cookies/edit/<order_id>")
def edit_page(order_id):
    #! need to pass in fake argument "order_id" to render page
    print("In EDIT route with id", order_id)

    cookie_order = Cookie_order.get_one(order_id)
    #! id from url passed into method get_one 

    return render_template("edit_order.html",cookie_order = cookie_order)
    #! cookie_order html = cookie_order python variable = objects

```

```html templates/edit_order.html - JINJA TEST
<body>
  <div class="container">

    {{cookie_order}}
    
```

```html templates/edit_order.html - JINJA Functional
<div class="form-group">
        <label for="name">Name</label>
        <input type="text" name="name" class="form-control" value="{{cookie_order.name}}">
      </div>

      <div class="form-group">
        <label for="cookie_type">Cookie Type</label>
        <input type="text" name="cookie_type" class="form-control" value="{{cookie_order.cookie_type}}" >
      </div>

      <div class="form-group">
        <label for="num_boxes">Number of boxes</label>
        <input type="text" name="num_boxes" class="form-control" value="{{cookie_order.num_boxes}}">
      </div>

      <input type="hidden" name="id" value="{{cookie_order.id}}">
      <!--$ when you click on edit it will be different id and different information  -->
      <!--$ provides a way to pass values between the client-side (HTML) and the server-side (backend) without being visible or editable by the user-->
      <!--$ <input type="hidden"> element is used to store the value of {{cookie_order.id}}. This value is hidden from the user's view but can be accessed and processed by the server-side code when the form is submitted. It allows you to send the id of the cookie_order along with the other form data, so the server can identify and handle the specific order when processing the form submission.  -->
    
```

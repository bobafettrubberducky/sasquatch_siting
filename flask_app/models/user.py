from flask_app.configs.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    
    db = "sasquatch"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        #$ setup attributes same way as your database columns
        self.recipes = []
        
    #& Validate Register - POST
    @staticmethod
    def validate_register(user):

        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(User.db).query_db(query,user)

        is_valid = True

        if len(results) >= 1:
            flash("Email already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email!', "register")
            is_valid = False
        if len(user["first_name"]) < 2:
            flash("First name must be at least 2 characters", "register")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least 2 characters", "register")
            is_valid = False
        if len(user["password"]) < 8:
            flash("PASSWORD must be at least 8 characters", "register")
            is_valid = False
        if user["password"] != user["confirm"]:
            flash("Passwords don't match ", "register")
        return is_valid
    
    #& CREATE - create new user using save()
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query,data)
        #! Note: passing INSERT query into database you'll get back `id` for the new user
        # return 1

    #& READ - retrieves a user from DB based on user_id
    @classmethod
    def get_by_id (cls,data):
        #data = {'id':'1'}
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #results = passing id=1 into database return one list/dictionary 
        #results = {["id":1, "first_name": "John", "last_name":"Legend"..etc]}
        return cls(results[0])
        # return instance of the objects (can be called user.first_name)


    #$ READ - retrieves a user from DB based on email 
    @classmethod
    def get_by_email(cls,data):
        #data = request.form = {"email": "john_legend@gmail.com", "password":"123456789"}
        query = "SELECT * FROM users WHERE email=%(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #! note: passing SELECT query into database you'll get back list/dict
        #results = passing email=john_legend into database return one list/dictionary
        #results = {["id":1, "first_name": "John", "last_name":"Legend"..etc]}
        
        if len(results) < 1:
            return False
        #! check no rows (no user found) in results list meaning email doesn't exist in db
        #! prevent key error make sure email exist
        # if True - return False
        # if False -> skip code
    
        return cls(results[0])
        #return instance of the objects (can be called user.first_name, user.email ..etc)

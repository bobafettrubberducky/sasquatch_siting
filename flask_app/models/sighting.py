from flask_app.configs.mysqlconnection import connectToMySQL

from flask import flash

from flask_app.models.user import User

class Sighting:

    db = "sasquatch"

    def __init__(self,data):
        self.id = data['id']
        self.location = data['location']
        self.description = data['description']
        self.date = data['date']
        self.number = data['number']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        #$ setup attributes same way as your database columns

        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM sightings;"
        results = connectToMySQL(cls.db).query_db(query)
        #results = list/dict of all the recipes = [{---}. {---}. {---}]


        all_sightings = []

        for row in results:
            sighting = cls(row) 
            #!dictionary containing data of single sighting
            all_sightings.append(sighting) 
            #! newly created user instance appended to all_sighting list

            sighting.user = User.get_by_id({'id': row['user_id']})
            #! User.get_by_id({'id': row['user_id']})
            # {'id': row['user_id']} - dictionary, id key and assigns the value of row['user_id']. It is used to fetch the user object from the database based on the provided user_id (foreign id from sighting)
            # User.get_by_id({'id': row['user_id']}) - fetch user object from database using get_by_id method of the User class
            #! sighting.user - called to show "sighting" "user" attributes for each recipe user info can be  (ex-sighting.user.firstname, sighting.user.lastname, etc) so we can tag each article
            #* One-to-Many: One: user & Many: sighting, so for every "sighting" we can specify "user" associated to it

        return all_sightings
    

            

        
    
    @staticmethod
    def validate_sighting(sighting):

        is_valid = True

        if len(sighting['location']) == 0:
            flash("Please enter location", 'sighting')
            is_valid = False
        if len(sighting['number']) < 1:
            flash('Please enter number', 'sighting')
            is_valid = False
        if len(sighting['description']) == 0:
            flash('Please enter description', 'sighting')
            is_valid = False
        if sighting['date'] == "":
            flash('Please enter date','sighting')

        return is_valid
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO sightings (location,description, date, number, user_id) VALUES (%(location)s,%(description)s,%(date)s,%(number)s,%(user_id)s);"
        results = connectToMySQL(cls.db).query_db(query,data)
        print('@@@@@@@@@@@@@@@@@@@@\n',results)

        return results
        
        # return recipe_id since INSERT used in query but don't care we just want to save the new recipe in the database

    @classmethod
    def get_one(cls,data):
        #data = {"id":1}, recipes key 
        query = "SELECT * FROM sightings WHERE id=%(id)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        #results = list/dict with one dict
        return cls(results[0])
        # cls(result[0]), creates objects that we can call for the recipes table (recipes.id, recipes.name, etc)

    @classmethod
    def update(cls,data):
        #data = {created request.form}
        query = "UPDATE sightings SET location=%(location)s, description=%(description)s,number=%(number)s, date=%(date)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

        #! for recipe id=1 updating fields with name, description, instructions, under30, and date_made
        #! Note: don't care what comes back just that the field are updated in our database

    @classmethod
    def destroy(cls,data):
        # data = {"id":id} = {"id":1}, sighting id=1
        query = "DELETE FROM sightings WHERE id=%(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)
        #! this will destroy the sighting id = 1  in the mysql database
import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    DATABASE = 'game_platform'

    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#Get functions -----------------------------------------------------------------
    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(user_id)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        if result:
            return cls(result[0])

        return False

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connectToMySQL(cls.DATABASE).query_db(query, data)
        if result:
            return cls(result[0])

        return False

#Modify functions --------------------------------------------------------------
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (username, email, password, created_at, ' \
            'updated_at) VALUES (%(username)s, %(email)s, %(password)s, ' \
            'NOW(), NOW());'
        return connectToMySQL(cls.DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = 'UPDATE users SET username = %(username)s, updated_at = NOW() '\
            'WHERE id = %(user_id)s;'
        connectToMySQL(cls.DATABASE).query_db(query, data)

#Helper functions --------------------------------------------------------------
    @staticmethod
    def validate_new_user(form):
        is_valid = True

        if form['username'] == '':
            flash('A username is required.')
            is_valid = False
        if len(form['username']) < 3:
            flash('Usernames must be at least 3 characters.')
            is_valid = False
        if form['email'] == '':
            flash('An email is required.')
            is_valid = False
        if not EMAIL_REGEX.match(form['email']):
            flash('Invalid email.')
            is_valid = False
        if User.get_by_email(form):
            flash('A user with that email already exists.')
            is_valid = False
        if form['password'] == '':
            flash('A password is required.')
            is_valid = False
        if len(form['password']) < 8:
            flash('Passwords must be at least 8 characters.')
            is_valid = False
        if form['confirm_password'] == '':
            flash('Please confirm your password.')
            is_valid = False
        if form['password'] != form['confirm_password']:
            flash('Passwords don\'t match.')
            is_valid = False

        return is_valid
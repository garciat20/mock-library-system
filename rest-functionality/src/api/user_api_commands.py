from re import L
from flask_restful import Resource, reqparse
from http.client import BAD_REQUEST, UNAUTHORIZED
from flask import abort
from db import rest_commands
import hashlib

class Users(Resource):
    def get(self, id=None):
        if (id == None): 
            # if no users found, return error message
            if (len(rest_commands.list_all_users()[0])) == 0:
                return abort(404, 'No users found')
            return rest_commands.list_all_users() 
        elif (id != None):
             # if no checkout books found, return error message
            if (len(rest_commands.get_checkout_for_user(id)[0])) == 0:
                return abort(404, 'No books found for this user')
            return rest_commands.get_checkout_for_user(id)
      

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()
        hasher = hashlib.sha512()
        hasher.update(args['password'].encode('utf-8'))
        hash_pass = hasher.hexdigest()
        username = args['username']
        return rest_commands.add_user(username, hash_pass)

    def put(self, id=None):
        # To update a users info, we can just have a session_key, maybe ID is too extra
        parser = reqparse.RequestParser()
        parser.add_argument('password', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('session_key', type=str)
        parser.add_argument('library_location', type=str)
        parser.add_argument('book_id', type=int)
        parser.add_argument('checked_out_date', type=str)
        parser.add_argument('user_id', type=int)
        args = parser.parse_args()
        # update username
        session_key = args['session_key']
        username = args['username']
        password = args['password']
        library_location = args['library_location']
        book_id = args['book_id']
        user_id = args['user_id']
        checked_out_date = args['checked_out_date']
        #if (session_key == None): return abort(401, 'Unauthorized. You must login to perform this action.')
        if (session_key == None and username != None and password != None):
            output = rest_commands.login_user(username,password)
            if output == UNAUTHORIZED: return UNAUTHORIZED #abort(401, 'Unauthorized. You must login to perform this action.')
            else: return output
        elif (session_key != None):
            if (username != None):
                return rest_commands.update_user_name(username, session_key, id)
            elif (password != None):
                return rest_commands.update_user_password(password,session_key,id)
        # if (args['password'] == None and id != None and username != None): 
        #     return rest_commands.update_user_name(username, session_key, id)
        # #print("DEBUG EDIT PASSWORD : "  + session_key)
        # if (id != None and checked_out_date == None) :
        #     return rest_commands.update_user_password(password,session_key,id)
        if (checked_out_date != None):
            #if (session_key == None): abort(401, 'You must log in to checkout a book') 
            return rest_commands.user_checkout(user_id,book_id,checked_out_date,library_location)
        
        

    def delete(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('session_key', type=str)
        args = parser.parse_args()
        session_key = args['session_key']
        #print("DEBUG REMOVE USER : " + str(session_key))
        return rest_commands.delete_user(session_key, id)


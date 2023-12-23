from urllib import request
from flask_restful import Resource, reqparse
from db import rest_commands
import hashlib

class Books(Resource):
    def get(self, search_criteria=None):
        # if not none, search_critera will go to list_all_books, so set it default to None
        if (search_criteria == None): 
            return rest_commands.list_all_books()
        return rest_commands.list_all_books_by_criteria(search_criteria)

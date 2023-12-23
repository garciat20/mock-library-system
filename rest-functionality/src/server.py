from flask import Flask
from flask_restful import Resource, Api
from db.rest_commands import *
from api.book_api_commands import Books
from api.user_api_commands import Users
from api.hello_world import HelloWorld

app = Flask(__name__)
api = Api(app)

api.add_resource(Users,'/users',
                '/users/<int:id>',
                '/users/login',
                '/users/checkout-book')
api.add_resource(Books, '/books',
                '/books/<string:search_criteria>')

if __name__ == '__main__':
    rebuild_tables()
    app.run(debug=True, port=4999)
from http.client import BAD_REQUEST, UNAUTHORIZED
from db.db_utils import *
from datetime import datetime 
import secrets

def rebuild_tables():
    exec_sql_file('src/db/schema.sql')
    #exec_sql_file('src/db/insert_data_schema.sql')

def list_all_users():
    sql = """
    SELECT JSON_BUILD_OBJECT ('id',id, 'name', name) FROM library.users
    """
    return exec_get_all(sql)

def list_all_books():
    sql = """
    SELECT JSON_BUILD_OBJECT (
        'title', title, 'author', author, 'genre', book_type, 'publish date', publish_date,
        'copies', book_copies, 'location', library_location) 
    FROM library.inventory"""
    return exec_get_all(sql)

def list_all_books_by_criteria(search_criteria):
    sql = f"""
    SELECT JSON_BUILD_OBJECT (
        'title', title, 'author', author, 'genre', book_type, 'publish date', publish_date,
        'copies', book_copies, 'location', library_location) 
    FROM library.inventory
    WHERE title = '{search_criteria}' 
    OR author = '{search_criteria}'
    OR book_type = '{search_criteria}'
    """

    return exec_get_all(sql)

def user_id_existence(id):
    return exec_get_one(f"SELECT name FROM library.users WHERE id = {id}")

def user_does_not_exist(username, password):
    user_info = exec_get_one(f"""
    SELECT name, password
    FROM library.users
    WHERE name = '{username}' 
    AND
    password = '{password}' 
    """)
    # if user doesn't exist then return true
    if (user_info == None): return True
    return False

def insert_sesion_key(user_id):
    exec_commit(f"""
    UPDATE library.users 
    SET session_key = '{secrets.token_hex(16)}'
    WHERE id = {user_id}
    """)

def get_session_key(user_id):
    return exec_get_one(f"SELECT session_key FROM library.users WHERE id = {user_id}")

def get_user_id(username, password):
    return exec_get_one(f"SELECT id FROM library.users WHERE name = '{username}' AND password = '{password}'")

def add_user(username, password):
    if (user_does_not_exist(username, password)):
        exec_commit(f"""
        INSERT INTO library.users(name, password)VALUES ('{username}', '{password}');""")
        user_id = get_user_id(username,password)
        insert_sesion_key(user_id[0])
    return BAD_REQUEST

def update_user_name(username, session_key, id):
    if (user_id_existence(id) is not None): 
        exec_commit(f"""
        UPDATE library.users 
        SET name = '{username}'
        WHERE session_key = '{session_key}' 
        AND id = {id}
        """)
    return BAD_REQUEST

def update_user_password(password, session_key, id):
    if (user_id_existence(id) is not None): 
        exec_commit(f"""
        UPDATE library.users 
        SET password = '{password}'
        WHERE session_key = '{session_key}' 
        AND id = {id}
        """)
    return BAD_REQUEST

def delete_user(session_key, id):   
    if (user_id_existence(id) == None): return BAD_REQUEST

    exec_commit(f"""
    DELETE FROM library.users 
    WHERE session_key='{session_key}'
    AND id = {id};
    """)

def get_checkout_for_user(user_id):
    # Session key is generated for those logged in, if not logged in return error
    #if (get_session_key(user_id)[0] == None): return UNAUTHORIZED
    return exec_get_all(f"""SELECT title, inventory.library_location, author FROM library.inventory INNER JOIN library.checkout 
    ON library.inventory.book_id = library.checkout.book_checked_out_id 
    WHERE library.checkout.user_id = {user_id}""")

def login_user(user_name, password):
    # if user tries to log in without a valid account, return 401
    if (user_does_not_exist(user_name,password)):
        return UNAUTHORIZED
    user_id = get_user_id(user_name, password)
    insert_sesion_key(user_id[0])
    return get_session_key(user_id[0])[0]

def user_checkout(user_id, book_checked_out_id, checked_out_date, library_location):
    # print(type(user_id))
    # print("BACKEND DEBUG: " + str(user_id))
    if (get_session_key(user_id) == None): return UNAUTHORIZED

    checkout_date_new = datetime.strptime(checked_out_date, '%Y-%m-%d').date() 

    exec_commit(f"""
        INSERT INTO library.checkout(user_id, book_checked_out_id, checked_out_date, library_location)VALUES
        ({user_id}, {book_checked_out_id}, '{checkout_date_new}', {library_location})""")




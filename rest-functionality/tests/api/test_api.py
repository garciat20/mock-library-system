from http.client import BAD_REQUEST, UNAUTHORIZED
import unittest
from src.db.db_utils import exec_get_one
from tests.test_utils import *

class TestExample(unittest.TestCase):

    def setUp(self):
        exec_sql_file('src/db/schema.sql')
        insert_test_data()

    def test_list_all_users(self):
        actual_output = len(get_rest_call(self, 'http://localhost:4999/users'))
        #print(actual_output)
        #print(get_rest_call(self, 'http://localhost:4999/users'))
        expected_output = 4
        self.assertEqual(actual_output,expected_output)

    def test_list_all_books(self):
        actual_output = len(get_rest_call(self, 'http://localhost:4999/books'))
        expected_output = 6
        self.assertEqual(actual_output,expected_output)

    def test_search_book_criteria_fiction(self):
        actual_output = len(get_rest_call(self, 'http://localhost:4999/books/fiction'))
        expected_output = 3
        self.assertEqual(actual_output,expected_output)

    def test_search_book_criteria_existing_author(self):
        get_output = get_rest_call(self, 'http://localhost:4999/books/Fyodor Dostoevsky')
        # print("DEBUG EXISTING AUTHOR: " )
        library = 'Pittsford'
        copies = 4
        author = 'Fyodor Dostoevsky'
        expected_output = [library, copies, author]
        actual_output = []
        for item in get_output:
            if 'location' in item[0]:
                actual_output.append(item[0].get('location'))
            if 'copies' in item[0]:
                actual_output.append(item[0].get('copies'))
            if 'author' in item[0]:
                actual_output.append(item[0].get('author'))
        self.assertEqual(actual_output,expected_output)
    
    def test_search_book_criteria_nonexistent_author(self):
        #should return empty list
        actual_output = get_rest_call(self, 'http://localhost:4999/books/Fake Author')
        expected_output = []
        self.assertEqual(actual_output,expected_output)
    
    def test_add_user_success(self):
        #SHA CALCULATOR ALSO SHOWS ITS CORRECT PASS
        response = post_rest_call(self, 'http://localhost:4999/users',{'username': 'testname', 'password': 'testpass'}) 
        new_length_of_users = (len(get_rest_call(self, 'http://localhost:4999/users')))
        expected_length_of_users = 5
        self.assertEqual(new_length_of_users, expected_length_of_users, 'og # of users was 4, if not 5, then this failed')

    def test_add_user_fail(self):
        #print(len(get_rest_call(self, 'http://localhost:4999/users')))
        response_user_one = post_rest_call(self, 'http://localhost:4999/users',{'username': 'testname', 'password': 'testpass'})
        response_user_one_repeated = post_rest_call(self, 'http://localhost:4999/users',{'username': 'testname', 'password': 'testpass'})  
        length_of_users = (len(get_rest_call(self, 'http://localhost:4999/users')))
        # expected_length_of_users = 5
        # print(length_of_users)
        # print(exec_get_all("SELECT * FROM library.users"))
        self.assertEqual(BAD_REQUEST, response_user_one_repeated, 'One user was added, but a duplicate was made so dont add a duplicate to sql table')

    def test_edit_user_name(self):
        # new_user = post_rest_call(self, 'http://localhost:4999/users/add',{'username': 'newname', 'password': 'newpass', 'session_key': 'session_key_test'})
        # print(exec_get_all("SELECT session_key FROM library.users WHERE id = 5"))
        # session_key = exec_get_all("SELECT session_key FROM library.users WHERE id = 5")
        # session_key = session_key[0][0]
        # user_id = exec_get_one(f"SELECT id FROM library.users WHERE session_key = '{session_key}'")
        edit_user_name = put_rest_call(self, 'http://localhost:4999/users/1', {'username': 'newnameada', 'session_key': 'testkeyada'})
       # print(exec_get_one(f"SELECT name FROM library.users WHERE id = {user_id[0]}"))
        #print(edit_user_name)
        expected = 'newnameada'
        actual = exec_get_one("SELECT name FROM library.users WHERE session_key = 'testkeyada'")    
        self.assertEqual(expected, actual[0])
        #print(exec_get_all("SELECT * FROM library.users"))

    def test_edit_user_name_failure(self):
        edit_user_name = put_rest_call(self, 'http://localhost:4999/users/12398', {'username': 'newnameada', 'session_key': 'testkeyada'})
        self.assertEqual(BAD_REQUEST, edit_user_name)

    def test_edit_user_password(self):
        edit_user_password = put_rest_call(self, 'http://localhost:4999/users/1', {'password': 'newpassada', 'session_key': 'testkeyada'})
        expected = 'newpassada'
        actual = exec_get_one("SELECT password FROM library.users WHERE session_key = 'testkeyada'")    
        self.assertEqual(expected, actual[0])
        #print(exec_get_all("SELECT * FROM library.users"))

    def test_edit_user_password_failure(self):
        edit_user_password = put_rest_call(self, 'http://localhost:4999/users/123487', {'password': 'newpassada', 'session_key': 'testkeyada'})       
        self.assertEqual(BAD_REQUEST, edit_user_password)


    def test_delete_user_success(self):
        #print(exec_get_all("SELECT * FROM library.users"))
        session_key = 'testkeyada'
        delete_call = delete_rest_call(self, f"http://localhost:4999/users/1?session_key={session_key}")
      
        expected_length = 3
        actual_length = len(get_rest_call(self, 'http://localhost:4999/users'))
        # print(exec_get_all("SELECT * FROM library.users"))
        self.assertEqual(actual_length,expected_length)

    def test_delete_user_failure(self):
        session_key = '123hgy3evwudbinjoNONEEXISTENTKEY_______'
        delete_call = delete_rest_call(self, f"http://localhost:4999/users/1?session_key={session_key}")
        actual_length = len(get_rest_call(self, 'http://localhost:4999/users'))
        expected_length = 4
        self.assertEqual(actual_length,expected_length)
    
    def test_get_checkout_for_user(self):
        rest_output = get_rest_call(self, f"http://localhost:4999/users/{2}")
        expected_length = 2 
        actual_length = len(rest_output)
        self.assertEqual(actual_length,expected_length)

    def test_user_login_success(self):
        rest_output = put_rest_call(self, f"http://localhost:4999/users/login", {'username': 'Ada Lovelace', 'password':'testpassada'})
        expected_output = 32
        # ada = 'Ada Lovelace'
        # print(exec_get_all(f"SELECT * FROM library.users WHERE name = '{ada}'"))
        self.assertEqual(len(rest_output), expected_output, 'expected session_key length should be 32 after logging in')
    
    def test_user_login_failure(self):
        rest_output = put_rest_call(self, f"http://localhost:4999/users/login", {'username': 'NOT A REAL USER', 'password':'h923u'})
        expected_output = UNAUTHORIZED
        # print("BRU")
        # print("DEBUG THIS REST OUTPUT BRU: " + str(rest_output))
        self.assertEqual(rest_output, expected_output, 'UNAUTHORIZED should be returned since user doesnt exist')
    
    def test_user_checkout_success(self):
        rest_output = put_rest_call(self, f"http://localhost:4999/users/checkout-book", {'library_location': "'Fairport'", 'checked_out_date':'2022-11-11', 'book_id': 1, 'user_id': 1})
        #print("DEBUG OUTPUT : " + str(rest_output))
        rest_output2 = get_rest_call(self, f"http://localhost:4999/users/{1}")[0]  
        checked_out_user_list = ['Let Me Tell You What I Mean', 'Fairport', 'Joan Didion']
        self.assertEqual(rest_output2, checked_out_user_list)

    def test_user_checkout_failure(self):
        rest_output = put_rest_call(self, f"http://localhost:4999/users/checkout-book", {'library_location': "'Fairport'", 'checked_out_date':'2022-11-11', 'book_id': 1, 'user_id': 456})
        self.assertEqual(rest_output, UNAUTHORIZED)







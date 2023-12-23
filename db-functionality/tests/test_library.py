import datetime
import unittest
from src.db_utils import *
from src.library import *

class TestLibrary(unittest.TestCase):
    
    def setUp(self):
        rebuild_tables()

    def test_rebuild_tables(self):
        """Build the tables"""
        conn = connect()
        cur = conn.cursor()
        rebuild_tables()
        cur.execute('SELECT * FROM library.users')
        self.assertEqual([], cur.fetchall(), "no rows in library.users table")
        conn.close()

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuild_tables()
        rebuild_tables()
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM library.users')
        self.assertEqual([], cur.fetchall(), "no rows in library.users table")
        conn.close()

    def test_insert_data_from_csv(self):
        # adding books to database
        # Comment code out, and uncomment code in library.py if u want to see table in pgAdmin
        # Save list within a tuple of all data and can loop thru it to test stuff
        insert_data_from_csv('db-functionality/tests/library.csv')
        expected_output = 19
        actual_output = get_all_book_count()
        #print(actual_output) added a is_available option to books
        self.assertEqual(expected_output, actual_output[0][0], 'something wrong about book data')

    def test_number_of_users(self):
        exec_sql_file('tests/schema_creation_test.sql')
        #Check correct number of users in rows
        actual_users = get_all_users()
        expected_users = [(1, 'Ada Lovelace'), (2, 'Mary Shelley'), 
        (3, 'Jackie Gleason'), (4, 'Art Garfunkel')]
        self.assertEqual(expected_users, actual_users, 'expected users not in table')

    def test_art_has_book(self):
        exec_sql_file('tests/schema_creation_test.sql')
        expected_output = []
        actual_output = get_Art_user_books()
        self.assertEqual(expected_output, actual_output, 'expected empty list from art')

    def test_gleason_books(self):
        #indexing tuple to get book
        exec_sql_file('tests/schema_creation_test.sql')
        actual_output = get_user_id_books(3)[0]
        expected_output = "The Count of Monte Cristo"
        self.assertEqual(expected_output, actual_output, 'expected "The Count of Monte Cristo" to be checked out by Gleason')

    def test_get_all_checked_books(self):
        # maybe should have indexed book titles and made more specific tests individualy?
        exec_sql_file('tests/schema_creation_test.sql')
        actual_output = get_all_checked_out_books()
        expected_output = [('Let Me Tell You What I Mean',), ('The Count of Monte Cristo',), ('The Right Stuff',)]
        self.assertEqual(expected_output, actual_output, 'expected books to be in order by username')

    def test_get_all_nonfiction_and_quantity(self):
        exec_sql_file('tests/schema_creation_test.sql')
        actual_output = get_nonfiction_books_and_quantity()
        expected_output = [('Let Me Tell You What I Mean', 'nonfiction', 3), ('The Right Stuff', 'nonfiction', 8), ('Dispatches', 'nonfiction', 7)]
        self.assertEqual(expected_output, actual_output, 'expected')
    
    def test_add_new_user(self):
        # add_user creates a new person into the databse
        exec_sql_file('tests/schema_creation_test.sql')
        add_new_user('Christopher Marlowe', 'MarloweC@email.com')
        add_new_user('Francis Bacon', 'BaconF@email.com')
        actual_output = exec_get_all("""
        SELECT * FROM library.users WHERE name =\'Christopher Marlowe\'
        """)
        actual_output2 = exec_get_all("""
        SELECT * FROM library.users WHERE name =\'Francis Bacon\'
        """)
        #print(actual_output)
        expected_output = [(5, 'Christopher Marlowe', 'MarloweC@email.com', True)]
        expected_output2 = [(6, 'Francis Bacon', 'BaconF@email.com', True)]
        self.assertEqual(actual_output, expected_output)
        self.assertEqual(actual_output2, expected_output2)

    def test_delete_user(self):
        # deleting a user should return an empty list when you look that user up
        add_new_user('John Smith', 'SmithJ@email.com')
        delete_user('John Smith')
        actual_output = exec_get_all("""
        SELECT * FROM library.users WHERE name =\'John Smith\'
        """)
        expected_output = []
        self.assertEqual(actual_output, expected_output)


    def test_gleason_reserve_book_failure(self):
        #adding books to data
        insert_data_from_csv('db-functionality/tests/library.csv') 
        #Ada Lovelace out a book with 1 copy
        user_id_gleason = get_user_id('Jackie Gleason')
        book_id = get_book_id('In Cold Blood', 'Truman Capote')
        book_copies = get_book_copies(book_id[0])
        # is this the right way to test for the a failure
        with self.assertRaises(Exception) as cannot_reserve:
            reserve_book(book_copies[0] ,user_id_gleason[0], book_id[0])
            self.assertTrue('Gleason cannot reserve a book' in cannot_reserve.exception)

    def test_gleason_reserve_book_success(self):
        #adding books to data
        insert_data_from_csv('db-functionality/tests/library.csv')
        exec_sql_file('tests/schema_creation_test.sql')
        # checking out a book so the inventory updates to 0 copies (doesnt work lol)
        # user_checkout(1,16,'2020-03-14')
        add_book_old('TestBook', 'nonfiction', 2022, 'Placeholder Name', 0)
        user_id_gleason = get_user_id('Jackie Gleason')
        book_id = get_book_id('TestBook','Placeholder Name')
        book_copies = get_book_copies(book_id[0])
        reserve_book(book_copies[0] ,user_id_gleason[0], book_id[0])
        actual_output = exec_get_all(f"""
        SELECT library.users.name, library.inventory.title FROM library.users
        INNER JOIN library.reserve ON library.reserve.user_id = library.users.id
        INNER JOIN library.inventory ON library.inventory.book_id = library.reserve.reservation_book_id
        ORDER BY library.users.name ASC
        """)
        actual_output = actual_output
        expected_output = [('Jackie Gleason', 'TestBook')]
        self.assertEqual(actual_output, expected_output, 'No books reserved')
    
    def test_garfunkel_return_book(self):
        exec_sql_file('tests/schema_creation_test.sql')
        #Art Garfunkel returns a copy of “Frankenstein” three days after he borrowed it.
        add_book_old('Frankenstein', 'fiction', 1818, 'Mary Shelley', 1)
        user_id_garfunkel = get_user_id('Art Garfunkel')
        book_id = get_book_id('Frankenstein', 'Mary Shelley')

        user_checkout(user_id_garfunkel[0], book_id[0], '2000/09/20')


        return_book(user_id_garfunkel[0],book_id[0],'2000/09/23')


        actual_output = exec_get_one(f"""SELECT library.users.name, library.inventory.title,  
        library.checkout.checked_out_date, library.return.return_book_date FROM library.users, library.checkout, library.return
        INNER JOIN library.inventory ON library.inventory.book_id = library.return.return_book_id
        """)
        time1 = datetime.date(2000, 9, 20)
        time2 = datetime.date(2000, 9, 23)
        expected_output = ('Art Garfunkel', 'Frankenstein', time1, time2)
        self.assertEqual(actual_output,expected_output, 'wrong info')

    def test_search_book_delete_account(self):
        exec_sql_file('tests/schema_creation_test.sql')
        add_book_old('The Last Man', 'fiction', 1826, 'Mary Shelley', 0)
        book_id = get_book_id('The Last Man', 'Mary Shelley')
        user_id = get_user_id('Mary Shelley')
        book_copies = get_book_copies(book_id[0])
        if (book_copies[0] == 0): delete_user('Mary Shelley')
        actual_output = get_user_info(user_id[0])
        expected_output = []
        self.assertEqual(actual_output, expected_output, 'mary shelley should be deleted')

    def test_checked_out_book_info_all(self):
        exec_sql_file('tests/schema_creation_test.sql')
        #adjust OLD TESTS (UPDATE SCHEMA_CREATION_TEST.SQL)
        actual_output = get_checked_out_books_all_info()
        #print(actual_output)
        expected_output = [('Jackie Gleason', 'The Count of Monte Cristo', 5), ('Ada Lovelace', 'Let Me Tell You What I Mean', 3), ('Mary Shelley', 'The Right Stuff', 8)]
        self.assertEqual(actual_output,expected_output, 'wrong info')

    def test_add_libraries(self):
        exec_sql_file('tests/schema_creation_test.sql')
        actual_output = get_all_libraries()
        library_list = []
        for location in actual_output:
            library_list.append(location[0])
        expected_output = ['Penfield', 'Pittsford', 'Henrietta','Fairport']
        self.assertEqual(library_list, expected_output, 'not correct libraries')

    def test_late_checkout_and_return(self):
        #
        # Can break this test into multiple smaller tests later
        # Everything below are checkouts and returns that occured
        # At the Fairport Library.
        #
        exec_sql_file('tests/schema_creation_test.sql')
       
        # Part 1 of big test

        add_book("The Winds of Winter", "fiction", "George R.R. Martin",1,'Fairport',2023)
        mary_user_id = get_user_id('Mary Shelley')[0]
        book_id = get_book_id("The Winds of Winter", "George R.R. Martin")[0]

        # part 2 of big test
        user_checkout(mary_user_id, book_id, '2022-01-02', 'Fairport')
        # mary returns 8 days later

        return_book(mary_user_id, book_id,'2022-01-10', 'Fairport')

        ada_user_id = get_user_id('Ada Lovelace')[0]

        # part 3 of big test
        user_checkout(ada_user_id, book_id, '2022-01-13', 'Fairport')
        # part 4 of big test, Ada tries to check out another book after 15 days of 

        add_book('Ada Cannot Checkout','nonfiction','Thomas Garcia', 1, 'Fairport',2023)

        old_checkout_date = get_checkout_date_of_book(book_id, ada_user_id)[0]
        ada_first_checkout = parse_datetime_day(old_checkout_date)
        # print("DEBUG ::: : :: : : : " + str(compare_two_checkout_dates('2022-01-28', ada_first_checkout)))
        # print(get_max_lend_time())

        checkout_additional_book(ada_user_id,get_book_id('Ada Cannot Checkout','Thomas Garcia')[0],'2022-01-28',ada_first_checkout, 'Fairport')
        return_book(ada_user_id, book_id,'2022-01-31', 'Fairport') #ada returns book 18 days late

        # HER ACCOUNT IS DISABLED BECAUSE OF THIS
        jackie_id = get_user_id('Jackie Gleason')[0]
        user_checkout(jackie_id,book_id,'2022-03-01','Fairport')
        return_book(jackie_id,book_id,'2022-03-31','Fairport')

        # since ada returned a book late her account is disabled
        # Ada, and Jackie return books late so there should b 2 books
        actual_output = get_all_late_book_count()[0][0]
        expected_output = 2
        self.assertEqual(actual_output,expected_output,'Expected 2 late books')

    def test_book_donation_to_libraries(self):
        exec_sql_file('tests/schema_creation_test.sql')
        add_book('The Wines of Winter','fiction','WineExpress', 2,'Pittsford', 2022)
        add_book('The Wines of Winter','fiction','WineExpress', 2,'Henrietta', 2022)
        actual_output = get_all_books_at_locations()
        expected_output = [('The Wines of Winter','WineExpress', 2,'Pittsford'), ('The Wines of Winter', 'WineExpress', 2, 'Henrietta')]
        self.assertEqual(actual_output,expected_output)
        
    def test_book_donations_to_Fairport(self):
        add_book('The Winds of Winter','fiction','George R.R. Martin', 3,'Fairport', 2022)

        actual_output = get_books_by_location('Fairport')
        expected_output = [('The Winds of Winter', 'George R.R. Martin', 3, 'Fairport')]
        self.assertEqual(actual_output,expected_output, 'wrong location, book, etc')

    def test_get_all_book_location_info(self):
        exec_commit("""
        INSERT INTO library.inventory(title, book_type, publish_date, author, 
        book_copies, library_location)VALUES
        ('Let Me Tell You What I Mean', 'nonfiction', 2021, 'Joan Didion', 3, 'Fairport'),
        ('The Count of Monte Cristo', 'fiction', 1846, 'Alexandre Dumas', 5, 'Fairport'),
        ('The Right Stuff', 'nonfiction', 1979, 'Tom Wolfe', 8, 'Henrietta'),
        ('Crime and Punishment', 'fiction', 1866, 'Fyodor Dostoevsky', 4, 'Pittsford'),
        ('Dispatches', 'nonfiction', 1991, 'Michael Herr', 7, 'Henrietta'),
        ('Little Red Riding Hood', 'fiction', 1697, 'Charles Perrault', 8, 'Fairport');
        """)

        exec_commit("""
        INSERT INTO library.libraries(library_location)VALUES
        ('Penfield'),
        ('Pittsford'),
        ('Henrietta'),
        ('Fairport');
        """)

        exec_commit("""
        INSERT INTO library.libraries(library_book_id)VALUES
        (1),
        (2),
        (3),
        (4),
        (5),
        (6);
        """)
        
        actual_output =  get_books_locations()
        #print(actual_output)
        expected_output = [(3, 'Fairport'), (2, 'Henrietta'), (1, 'Pittsford')]
        self.assertEqual(actual_output,expected_output, 'wrong number of books at certain location')




    
        
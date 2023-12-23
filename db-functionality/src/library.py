from src.db_utils import *
import csv

def rebuild_tables():
    exec_sql_file('src/schema_creation.sql')
    # exec_sql_file('tests/schema_creation_test.sql')
    #insert_data_from_csv('tests/library.csv') #uncomment to see table in pgAdmin

def get_all_users():
    users = exec_get_all('SELECT id, name FROM library.users ORDER BY id ASC')
    return users

def get_Art_user_books():
    books = exec_get_all("""SELECT title FROM library.inventory INNER JOIN library.checkout 
    ON library.inventory.book_id = library.checkout.book_checked_out_id WHERE library.checkout.user_id = 4""")
    return books

def get_user_id_books(user_id):
    books = exec_get_one(f"""SELECT title FROM library.inventory INNER JOIN library.checkout 
    ON library.inventory.book_id = library.checkout.book_checked_out_id 
    WHERE library.checkout.user_id = {user_id}""")
    return books

def get_all_checked_out_books():
    # need to do the 2nd to last function
    books = exec_get_all("""
    SELECT library.inventory.title FROM library.users
    INNER JOIN library.checkout ON library.checkout.user_id = library.users.id
    INNER JOIN library.inventory ON library.inventory.book_id = library.checkout.book_checked_out_id
    ORDER BY library.users.name ASC
    """)
    return books

def get_nonfiction_books_and_quantity():
    books_and_quantity = exec_get_all("""
    SELECT library.inventory.title, library.inventory.book_type, library.inventory.book_copies FROM 
    library.inventory WHERE library.inventory.book_type = 'nonfiction'
    """)
    return books_and_quantity

def add_new_user(name, contact_info):
    # inserts a new user into the sql database
    return exec_commit(f"INSERT INTO library.users(name, contact_info)VALUES('{name}', '{contact_info}');")
    
def delete_user(name):
    # deletes a specfic user from the databse
    return exec_commit(f"DELETE FROM library.users WHERE library.users.name = '{name}';")

def insert_data_from_csv(filename):
    with open(filename, 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) #skip header
        for record in csvreader:
            book_title = record[0]
            # probz a better way to replace "'" with an escape character
            if ("'" in book_title): book_title = book_title.replace("'", "\'\'")
            author = record[1]
            if ("'" in author): author = author.replace("'", "\'\'")
            summary = record[2]
            if ("'" in summary): summary = summary.replace("'", "\'\'")
            category = record[3]
            sub_category = record[4]
            book_copies = record[5]
            publish_date = record[6]
            # If a book, author, etc has a single quote (') use regex to find (') and escape character it
            sql_command = f"""INSERT INTO library.inventory(title, book_type, publish_date, author, 
            book_copies, book_sub_type, book_summary)VALUES
            ('{book_title}', '{category}', {publish_date}, '{author}', {book_copies}, '{sub_category}', '{summary}');
            """
            exec_commit(sql_command)

def reserve_book(book_copies, user_id, book_id, author=''):
    #default parameter for author incase same book title but different authors
    # user_id = get_user_id(name)
    # book_id = get_book_id(title)
    # book_copies = get_book_copies(book_id[0])
    # might need to make a if so program doesnt crash
    reserve_book = f"""INSERT INTO library.reserve(reserved_book_copies, user_id, reservation_book_id)VALUES
    ({book_copies}, '{user_id}', '{book_id}'); 
    """
    #^^^
    return exec_commit(reserve_book)

def get_all_books():
    return exec_get_all(f"SELECT * FROM library.inventory;")

def get_user_id(name):
    return exec_get_one(f"SELECT id FROM library.users WHERE name = '{name}'")

def get_book_id(title, author):
    return exec_get_one(f"SELECT book_id FROM library.inventory WHERE library.inventory.title = '{title}' AND library.inventory.author = '{author}'")

def get_book_copies(book_id):
    return exec_get_one(f"SELECT book_copies FROM library.inventory WHERE library.inventory.book_id= {book_id}")

def user_checkout(user_id, book_checked_out_id, checked_out_date, library_location=''):

    # get specific member_status 
    member_status = exec_get_one(f"""SELECT member_active_status FROM library.users
    WHERE id = {user_id}""")[0]
    # print("Member status: ")
    # print(isinstance(member_status,bool))
   # print("book copies before checkout: " + str(get_book_copies(book_checked_out_id)[0]))
    if (member_status == True):

        exec_commit(f"""
        INSERT INTO library.checkout(user_id, book_checked_out_id, checked_out_date, library_location)VALUES
        ({user_id}, {book_checked_out_id},'{checked_out_date}', '{library_location}');""")

        # update book copies on specific book id 
        exec_commit("""UPDATE library.inventory SET book_copies = (book_copies - 1)
        FROM library.checkout WHERE is_available = true AND 
        %s = book_id;""",(book_checked_out_id,))

        # if book_copies on a specific book id == 0, then set is_available to false cuz no copies left
        exec_commit(f"""UPDATE library.inventory SET is_available = false WHERE book_copies = 0
        AND book_id = {book_checked_out_id};""")


def return_book(user_id, book_id, date_returned, library_location=''):
    #insert data into return table
    exec_commit(f"""INSERT INTO library.return(return_book_id, return_book_date, user_id, library_location)VALUES
    ({book_id}, '{date_returned}', {user_id}, '{library_location}');""")
    
    # delete book from library.checkout where user_id once checked it out

    # extract datetime value
    day_checked_out_datetime = exec_get_one(f"""SELECT checked_out_date FROM library.checkout, library.users WHERE
    library.checkout.book_checked_out_id = {book_id} AND users.id = {user_id};""")

    # its a tuple so index it
    day_checked_out_datetime = day_checked_out_datetime[0]
    
    #print("datetime : " + day_checked_out_datetime.strftime('%d'))

    # Get only the day
    day_checked_out = day_checked_out_datetime.strftime('%d')
  
    #print("day_checked_out: " + day_checked_out)
    # if the day is for example: "01", "05", then simply index the 2nd element to get a single digit
    if day_checked_out[0] == '0': day_checked_out = day_checked_out[1]
    # print("day checked out: " + day_checked_out)
    # print("day returned: " + date_returned[-2:]) # just get the last 2 elements

    # Subtract the the days it took to return the book
    length_to_return_book = abs(int(day_checked_out)) - abs(int(date_returned[-2:]))
    length_to_return_book = abs(length_to_return_book)
    #print(length_to_return_book)
    # max_lend_time = get_max_lend_time()

    # if time to return book is longer than the lend time, disable the users account
    # HOW TO AVOID USING GLOBAL VARIABLE 
    if (length_to_return_book > get_max_lend_time()[0]):  # index tuple
        update_late_book_history(book_id,date_returned) # Add late book to library.lend and the date it was returned
        disable_user_account(user_id) # disable user from checking out more books

    exec_commit("""
    UPDATE library.inventory SET book_copies = (book_copies + 1) FROM    
    library.return WHERE book_id = %s""",(book_id,))

    # After u add 1 to the book, then the book will be available again since it will be a nonzero number
    exec_commit("""
    UPDATE library.inventory SET is_available = true;
    """)

    # at the end u want to delete the relationship between users and checkout since
    # they no longer check out the book (cuz they returned it)???

    # exec_commit(f"""
    # DELETE FROM library.checkout WHERE checkout.book_checked_out_id = {book_id};
    # """)


def add_book_old(title, book_type, publish_date, author, book_copies):
    return exec_commit(f"""
        INSERT INTO library.inventory(title, book_type, publish_date, author, 
        book_copies) VALUES
        ('{title}', '{book_type}', '{publish_date}', '{author}',{book_copies});
        """)

def get_user_info(user_id):
    return exec_get_all(f"""
    SELECT * FROM library.users WHERE library.users.id = {user_id};
    """)

def get_checked_out_books_all_info():
    # only prints out, name, title, copies
    # How to get return date + update copies going down in schema_creation?
    return exec_get_all(f"""
        SELECT library.users.name, library.inventory.title,library.inventory.book_copies 
        FROM library.users
        INNER JOIN library.checkout ON library.users.id = library.checkout.user_id 
        INNER JOIN library.inventory ON library.checkout.book_checked_out_id = library.inventory.book_id
        ORDER BY library.inventory.author,library.inventory.book_type ASC
        """)

def get_all_book_count():
    return exec_get_all(f"""
    SELECT COUNT(library.inventory.title) AS num_of_books FROM 
    library.inventory
    """)

def get_all_libraries():
    return exec_get_all(f"""
    SELECT library_location FROM library.libraries;
    """)
  
def get_max_lend_time():
    args = {
        'max lend time': 'placeholder'
    } 
    return exec_get_one("SELECT max_lending_time FROM library.lend", args)

def disable_user_account(user_id):
    return exec_commit("UPDATE library.users SET member_active_status = false WHERE id = %s",(user_id,))

def update_late_book_history(book_id, late_date):
    exec_commit(f"INSERT INTO library.lend(late_book_id, late_date)VALUES ({book_id}, '{late_date}');")

def get_checkout_date_of_book(book_id, user_id):
        return exec_get_one(f"""SELECT checked_out_date FROM library.checkout, library.users WHERE
        library.checkout.book_checked_out_id = {book_id} AND checkout.user_id = {user_id}""")

def length_of_time(day1, day2):
    length_to_return_book = abs(int(day1)) - abs(int(day2))
    length_to_return_book = abs(length_to_return_book)
    return length_to_return_book

# if object recieved is datetime, use this to parse only the day, i dont remmeber if it works
def parse_datetime_day(day):
    day_not_parsed =  day.strftime('%d')
    parsed_day = day_not_parsed[-2:]
    if (parsed_day[0] == 0): parsed_day = [1]
    parsed_day = str(parsed_day)
    return parsed_day

# combine many helpers into 1 to just return length of days between 2 checkout dates
def compare_two_checkout_dates(new_checkout_date, old_checkout_date):
    parsed_new_date = new_checkout_date[-2:]
    # if the date is like 01 or 04, then we just want the single digit 
    if (parsed_new_date[0] == 0): parsed_new_date = [1]

    parsed_old_checkout_date = old_checkout_date[-2:]
    if (parsed_old_checkout_date[0] == 0): parsed_old_checkout_date = [1]

    # return length of time between checked out dates
    return length_of_time(parsed_new_date,parsed_old_checkout_date) 

def checkout_additional_book(user_id, book_id, new_checkout_date, old_checkout_date, library_location):
    #if user wants to check out an additional book
    parsed_new_date = new_checkout_date[-2:]
    # if the date is like 01 or 04, then we just want the single digit 
    if (parsed_new_date[0] == 0): parsed_new_date = [1]

    parsed_old_checkout_date = old_checkout_date[-2:]
    if (parsed_old_checkout_date[0] == 0): parsed_old_checkout_date = [1]

    # HOW TO COMPARE WITH MAX LENGTH TIME INSTEAD OF GLOBAL VARIABLLE

    if (length_of_time(parsed_new_date,parsed_old_checkout_date) <= get_max_lend_time()[0]):user_checkout(user_id,book_id,new_checkout_date, library_location)
    
def get_all_checkout_dates():
    return exec_get_all(f"""SELECT id, name, checked_out_date FROM library.inventory
        INNER JOIN library.checkout ON library.inventory.book_id = checkout.book_checked_out_id
        INNER JOIN library.users ON library.checkout.user_id = users.id""")

def get_all_late_book_count():
    return exec_get_all("""
    SELECT COUNT(late_book_id) FROM library.lend
    """)


def get_member_status(user_id):
    return exec_get_one(f"""SELECT member_active_status FROM library.users WHERE
        users.id = {user_id}""")

def add_book(title, genre,author, copies, location, publish_date):
    exec_commit(f"""
    INSERT INTO library.inventory(title, author, book_copies, library_location, publish_date, book_type) VALUES
    ('{title}', '{author}', {copies},'{location}', {publish_date}, '{genre}');
    """)

def get_books_by_location(location):
    return exec_get_all(f"""
    SELECT title, author, book_copies, inventory.library_location FROM library.inventory WHERE library.inventory.library_location = '{location}'
    """)

def get_all_books_at_locations():
    return exec_get_all("""
    SELECT title, author, book_copies, library.inventory.library_location FROM library.inventory
    INNER JOIN library.libraries ON libraries.library_location = inventory.library_location
    """)

def get_books_locations():
    return exec_get_all("""SELECT COUNT(book_id), library.inventory.library_location FROM 
    library.inventory INNER JOIN library.libraries ON libraries.library_location = inventory.library_location
    GROUP BY inventory.library_location
    ORDER BY COUNT(book_id) DESC""")

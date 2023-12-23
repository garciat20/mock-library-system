INSERT INTO library.users(name, session_key, password) VALUES
    ('Ada Lovelace', 'testkeyada', 'testpassada'),
    ('Mary Shelley', 'testkeymary', 'testpassmary'),
    ('Jackie Gleason', 'testkeyjackie', 'testpassjackie'),
    ('Art Garfunkel', 'testkeyart', 'testpassart');

-- below can add library location and subgenre
INSERT INTO library.inventory(title, book_type, publish_date, author, 
book_copies, library_location) VALUES
    ('Let Me Tell You What I Mean', 'nonfiction', 2021, 'Joan Didion', 3, 'Fairport'),
    ('The Count of Monte Cristo', 'fiction', 1846, 'Alexandre Dumas', 5, 'Fairport'),
    ('The Right Stuff', 'nonfiction', 1979, 'Tom Wolfe', 8, 'Henrietta'),
    ('Crime and Punishment', 'fiction', 1866, 'Fyodor Dostoevsky', 4, 'Pittsford'),
    ('Dispatches', 'nonfiction', 1991, 'Michael Herr', 7, 'Penfield'),
    ('Little Red Riding Hood', 'fiction', 1697, 'Charles Perrault', 8, 'Penfield');

INSERT INTO library.lend(max_lending_time)VALUES
    (14);

INSERT INTO library.libraries(library_location)VALUES
 
    ('Penfield'),
    ('Pittsford'),
    ('Henrietta'),
    ('Fairport');

INSERT INTO library.checkout(user_id,book_checked_out_id,checked_out_date)VALUES

    (2,2,'2021-02-03'),
    (2,3,'2021-03-04');
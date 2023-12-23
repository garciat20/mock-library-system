INSERT INTO library.users(name, session_key, password) VALUES
    ('Ada Lovelace', 'testkeyada', 'testpassada'),
    ('Mary Shelley', 'testkeymary', 'testpassmary'),
    ('Jackie Gleason', 'testkeyjackie', 'testpassjackie'),
    ('Art Garfunkel', 'testkeyart', 'testpassart');

-- below can add library location and subgenre
INSERT INTO library.inventory(title, book_type, publish_date, author, 
book_copies) VALUES
    ('Let Me Tell You What I Mean', 'nonfiction', 2021, 'Joan Didion', 3),
    ('The Count of Monte Cristo', 'fiction', 1846, 'Alexandre Dumas', 5),
    ('The Right Stuff', 'nonfiction', 1979, 'Tom Wolfe', 8),
    ('Crime and Punishment', 'fiction', 1866, 'Fyodor Dostoevsky', 4),
    ('Dispatches', 'nonfiction', 1991, 'Michael Herr', 7),
    ('Little Red Riding Hood', 'fiction', 1697, 'Charles Perrault', 8);

INSERT INTO library.lend(max_lending_time)VALUES
    (14);

INSERT INTO library.libraries(library_location)VALUES
    -- why does everything crash when i use double quotes?
    ('Penfield'),
    ('Pittsford'),
    ('Henrietta'),
    ('Fairport');
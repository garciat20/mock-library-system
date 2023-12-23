INSERT INTO library.users(name, contact_info) VALUES
    ('Ada Lovelace', 'LovelaceA@email.com'),
    ('Mary Shelley', 'ShelleyM@email.com'),
    ('Jackie Gleason', 'GleasonJ@email.com'),
    ('Art Garfunkel', 'GarfunkelA@email.com');

-- Below are books with no summaries, by default they have empty string 
INSERT INTO library.inventory(title, book_type, publish_date, author, 
book_copies) VALUES
    ('Let Me Tell You What I Mean', 'nonfiction', 2021, 'Joan Didion', 3),
    ('The Count of Monte Cristo', 'fiction', 1846, 'Alexandre Dumas', 5),
    ('The Right Stuff', 'nonfiction', 1979, 'Tom Wolfe', 8),
    ('Crime and Punishment', 'fiction', 1866, 'Fyodor Dostoevsky', 4),
    ('Dispatches', 'nonfiction', 1991, 'Michael Herr', 7),
    ('Little Red Riding Hood', 'fiction', 1697, 'Charles Perrault', 8);

INSERT INTO library.checkout(user_id, book_checked_out_id, checked_out_date)VALUES
-- year/month/day
    (1, 1, '2000-09-20'),
    (2, 3, '2000-02-03'),
    (3, 2, '2000-04-05');

INSERT INTO library.checkout(user_id)VALUES
    (4);

INSERT INTO library.lend(max_lending_time)VALUES
    (14);

INSERT INTO library.libraries(library_location)VALUES
    -- why does everything crash when i use double quotes?
    ('Penfield'),
    ('Pittsford'),
    ('Henrietta'),
    ('Fairport');

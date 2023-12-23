DROP SCHEMA IF EXISTS library CASCADE;
CREATE SCHEMA library;

CREATE TABLE library.users (
    id SERIAL NOT NULL PRIMARY KEY,
    name text NOT NULL,
    password text,
    session_key text DEFAULT NULL,
    -- contact_info text NOT NULL,
    member_active_status BOOLEAN DEFAULT true NOT NULL 
);

CREATE TABLE library.inventory (
    book_id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL, --
    book_type text DEFAULT '' NOT NULL, --
    book_sub_type text DEFAULT '' NOT NULL,
    publish_date INTEGER NOT NULL, --
    author text NOT NULL, --
    book_copies INTEGER DEFAULT 0 NOT NULL, --
    book_summary text DEFAULT '' NOT NULL,
    library_location text DEFAULT '' NOT NULL,
    is_available BOOLEAN DEFAULT true NOT NULL,
    is_late BOOLEAN DEFAULT false NOT NULL
);

CREATE TABLE library.checkout (
    checkout_id SERIAL NOT NULL PRIMARY KEY,
    book_checked_out_id INTEGER, 
    user_id INTEGER,
    late_book_status BOOLEAN DEFAULT false NOT NULL,
    checked_out_date DATE,
    library_location text DEFAULT '' NOT NULL, 
    return_book_date DATE UNIQUE, 
    late_fee DECIMAL DEFAULT 0.0,
    FOREIGN KEY(user_id) REFERENCES library.users(id) ON DELETE CASCADE,
    FOREIGN KEY(book_checked_out_id) REFERENCES library.inventory(book_id)
);

CREATE TABLE library.reserve (
    reservation_id SERIAL NOT NULL PRIMARY KEY,
    reservation_book_id INTEGER,
    user_id INTEGER,
    reserved_book_copies INTEGER, 
    library_location text DEFAULT '' NOT NULL,
    CHECK (reserved_book_copies = 0),
    FOREIGN key (user_id) REFERENCES library.users(id) ON DELETE CASCADE, 
    FOREIGN key (reservation_book_id) REFERENCES library.inventory(book_id) 
);

CREATE TABLE library.return(
    return_id SERIAL NOT NULL PRIMARY KEY,
    return_book_id INTEGER,
    return_book_date DATE UNIQUE, 
    user_id INTEGER,
    late_fee DECIMAL DEFAULT 0.0,
    library_location text DEFAULT '' NOT NULL,
    FOREIGN key (user_id) REFERENCES library.users(id) ON DELETE CASCADE,
    FOREIGN key (return_book_id) REFERENCES library.inventory(book_id)
);

CREATE TABLE library.libraries(
    library_id SERIAL NOT NULL PRIMARY KEY,
    library_location text DEFAULT '' NOT NULL,
    library_book_id INTEGER,
    FOREIGN key (library_book_id) REFERENCES library.inventory(book_id)
);

CREATE TABLE library.lend(
    lend_id SERIAL NOT NULL PRIMARY KEY,
    late_book_id INTEGER,
    max_lending_time INTEGER DEFAULT 14 NOT NULL,
    late_date DATE, 
    FOREIGN KEY (late_date) REFERENCES library.return(return_book_date),
    FOREIGN KEY (late_book_id) REFERENCES library.inventory(book_id)
);
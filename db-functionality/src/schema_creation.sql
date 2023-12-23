DROP SCHEMA IF EXISTS library CASCADE;
CREATE SCHEMA library;

CREATE TABLE library.users (
    id SERIAL NOT NULL PRIMARY KEY,
    name text NOT NULL,
    contact_info text NOT NULL,
    member_active_status BOOLEAN DEFAULT true NOT NULL -- false for lock account, if locked cant checkout
    -- once user returns books, account will be unlocked
);

CREATE TABLE library.inventory (
    book_id SERIAL NOT NULL PRIMARY KEY,
    title text NOT NULL,
    book_type text DEFAULT '' NOT NULL,
    book_sub_type text DEFAULT '' NOT NULL,
    publish_date INTEGER NOT NULL,
    author text NOT NULL,
    book_copies INTEGER DEFAULT 0 NOT NULL, -- new value to get indiiv
    book_summary text DEFAULT '' NOT NULL, -- default summary is no summary
    library_location text DEFAULT '' NOT NULL,
    is_available BOOLEAN DEFAULT true NOT NULL,
    is_late BOOLEAN DEFAULT false NOT NULL
);

CREATE TABLE library.checkout (
    checkout_id SERIAL NOT NULL PRIMARY KEY,
    book_checked_out_id INTEGER, -- the book id u want to check out
    user_id INTEGER,
    late_book_status BOOLEAN DEFAULT false NOT NULL,
    checked_out_date DATE, -- year/month/day
    library_location text DEFAULT '' NOT NULL, 
    -- max_lending_time INTEGER DEFAULT 14 NOT NULL,
    FOREIGN KEY(user_id) REFERENCES library.users(id) ON DELETE CASCADE,
    FOREIGN KEY(book_checked_out_id) REFERENCES library.inventory(book_id)
);

CREATE TABLE library.reserve (
    reservation_id SERIAL NOT NULL PRIMARY KEY,
    reservation_book_id INTEGER,
    user_id INTEGER,
    reserved_book_copies INTEGER, -- Subsitute for CHECK in the meantime
    library_location text DEFAULT '' NOT NULL,
    CHECK (reserved_book_copies = 0),
    --CHECK (library.inventory.CheckAvailability() = 0),
    FOREIGN key (user_id) REFERENCES library.users(id) ON DELETE CASCADE, -- maybe also delete on cascade
    FOREIGN key (reservation_book_id) REFERENCES library.inventory(book_id) -- was original book.checkout.book_checked_out_id UNIQUE but it gave error
);

CREATE TABLE library.return(
    return_id SERIAL NOT NULL PRIMARY KEY,
    return_book_id INTEGER,
    return_book_date DATE UNIQUE, --when user returns book and its over max_lending_time (14 days)
    user_id INTEGER,
    library_location text DEFAULT '' NOT NULL,
    --late_return DATE, -- when user returns book and its over max_lending_time (14 days)
    FOREIGN key (user_id) REFERENCES library.users(id) ON DELETE CASCADE,-- maybe also delete on cascade
    FOREIGN key (return_book_id) REFERENCES library.inventory(book_id) -- MAYBE ISSUE OG MADE BOOK_CHECKED_OUT_ID UNIQUE IN CHECKOUT TABLE
    -- make foreign key and references to other tables
);

CREATE TABLE library.libraries(
    library_id SERIAL NOT NULL PRIMARY KEY,
    library_location text DEFAULT '' NOT NULL,
    -- as long as book_id matches the one in the inventory
    library_book_id INTEGER,
    FOREIGN key (library_book_id) REFERENCES library.inventory(book_id)
);

CREATE TABLE library.lend(
    lend_id SERIAL NOT NULL PRIMARY KEY,
    late_book_id INTEGER,
    max_lending_time INTEGER DEFAULT 14 NOT NULL,
    late_date DATE, --when user returns book and its over max_lending_time (14 days)
    FOREIGN KEY (late_date) REFERENCES library.return(return_book_date),
    FOREIGN KEY (late_book_id) REFERENCES library.inventory(book_id)
);

## mock-library-system

## Description

Created a mock library systems with mock data for books, library locations, and users. I then validated that actions such as checking out a book at a certain location, or only a logged in user can perform a certain action, or securely storing a password, etc. is done properly via pytests.

## Installation

Optional: pgAdmin installed for a nice GUI to use to see data in schema/ database: https://www.pgadmin.org/download/
Needed: Installation of Postgres.app to easily use project: https://postgresapp.com/ 
Needed: Python 3, and installing requirements.txt 
```
pip install -r requirements.txt
```
or
```
pip3 install -r requirements.txt
```
Needed: find your *pg_hba.conf* file and modify the method part to "trust" so no credentials are required to connct to local database.
```
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     trust
```

Once installed and *pg_hba.conf* is modified, start running the server and create a database using the psql tool via the terminal
```
psql
```
```
create database library;
```
```
\c library
```

## Usage
Once installations are complete, and the database is created/ connected, you may now run the tests for both the database, and restful side of this project to check functionality

#for database side:
```python3 -m pytest db-functionality/tests/test_library.py```

#for restful side:
* Run the server first: ```python3 rest-functionality/src/server.py```
* Once server is running, run tests to validate that restful commands of project work: ```python3 -m pytest db-functionality/tests/test_library.py```


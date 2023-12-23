import unittest
from src.db.example import *
from tests.test_utils import *

class TestDBSchema(unittest.TestCase):

    def test_rebuild_tables(self):
        """Rebuild the tables"""
        exec_sql_file('src/db/schema.sql')
        assert_sql_count(self, "SELECT * FROM library.users", 0)

    def test_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        exec_sql_file('src/db/schema.sql')
        exec_sql_file('src/db/schema.sql')
        assert_sql_count(self, "SELECT * FROM library.users", 0)

    def test_seed_data_works(self):
        """Attempt to insert the seed data"""
        exec_sql_file('src/db/schema.sql')
        insert_test_data()
        assert_sql_count(self, "SELECT * FROM library.users", 4)
        assert_sql_count(self, "SELECT * FROM library.libraries", 4)
        assert_sql_count(self, "SELECT * FROM library.inventory", 6)
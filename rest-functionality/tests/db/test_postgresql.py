import unittest
from src.db.db_utils import connect

class TestPostgreSQL(unittest.TestCase):

    def test_can_connect(self):
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT VERSION()')
        self.assertTrue(cur.fetchone()[0].startswith('PostgreSQL'))
        conn.close()
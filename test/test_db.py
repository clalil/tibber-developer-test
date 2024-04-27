import pytest
import sqlite3

SQL = '''CREATE TABLE IF NOT EXISTS robot 
        (timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')), 
        commands INT, 
        result INT, 
        duration REAL)'''
        
SAMPLE_DATA =[('2018-05-12 12:45:10.851596', 2, 4, 0.000123), ('2018-05-10 12:45:10.851596', 3, 2, 0.000123)]

@pytest.fixture
def create_cursor():
    conn = sqlite3.connect("test_db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(SQL)
        yield conn
        conn.rollback()


def test__when_initialized__should_be_empty(create_cursor):
    assert len(list(create_cursor.execute('SELECT * FROM robot'))) == 0

def test__when_data_is_inserted__should_store_data(create_cursor):
    create_cursor.executemany('INSERT INTO robot VALUES(?,?,?,?)', SAMPLE_DATA)
    assert len(list(create_cursor.execute('SELECT * FROM robot'))) == 2

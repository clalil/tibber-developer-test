import pytest
import sqlite3
import pdb

SQL = '''CREATE TABLE IF NOT EXISTS robot 
        (timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')), 
        commands INT, 
        result INT, 
        duration REAL)'''
        
SAMPLE_DATA =[('2018-05-12 12:45:10.851596', 2, 4, 0.000123), ('2018-05-10 12:45:10.851596', 3, 2, 0.000123)]

@pytest.fixture
def create_connection():
    conn = sqlite3.connect("test_db")
    with conn:
        cursor = conn.cursor()
        cursor.execute(SQL)
        yield conn
        conn.rollback()


def test__when_initialized__should_be_empty(create_connection):
    cursor = create_connection.cursor()
    assert len(list(cursor.execute('SELECT * FROM robot'))) == 0


def test__when_called_upon__should_store_data(create_connection):
    cursor = create_connection.cursor()
    cursor.executemany('INSERT INTO robot VALUES(?,?,?,?)', SAMPLE_DATA)
    assert len(list(cursor.execute('SELECT * FROM robot'))) == 2


def test__when_values_are_inserted__should_successfully_populate(create_connection):
    cursor = create_connection.cursor()
    cursor.execute('INSERT INTO robot VALUES(?,?,?,?)', ('2018-05-12 12:45:10.851596', 2, 4, 0.000123))
    cursor.execute('SELECT * FROM robot')
    rows = cursor.fetchall()
    for row in rows:
        assert row == ('2018-05-12 12:45:10.851596', 2, 4, 0.000123)

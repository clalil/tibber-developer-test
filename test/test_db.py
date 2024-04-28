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
def db():
    conn = sqlite3.connect("test_db")
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(SQL)
        except sqlite3.Error as e:
            print(f"Error: Database could not be initialized. Due to {e}")
            conn.rollback()
        yield conn
        conn.rollback()


def test__when_initialized__should_be_empty(db):
    assert len(list(db.execute('SELECT * FROM robot'))) == 0


def test__when_called_upon__should_store_data(db):
    db.executemany('INSERT INTO robot VALUES(?,?,?,?)', SAMPLE_DATA)
    assert len(list(db.execute('SELECT * FROM robot'))) == 2


def test__when_values_are_inserted__should_successfully_populate(db):
    db.execute('INSERT INTO robot VALUES(?,?,?,?)', ('2018-05-12 12:45:10.851596', 2, 4, 0.000123))
    db.execute('SELECT * FROM robot')
    cursor_for_traversing = db.cursor()
    rows = cursor_for_traversing.fetchall()
    for row in rows:
        assert row == ('2018-05-12 12:45:10.851596', 2, 4, 0.000123)

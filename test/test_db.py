import pytest
import sqlite3
import pdb

SQL = '''CREATE TABLE IF NOT EXISTS robot (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
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
        yield conn
        conn.rollback()


def test__when_initialized__should_be_empty(db):
    assert len(list(db.execute('SELECT * FROM robot'))) == 0


def test__when_called_upon__should_store_data(db):
    db.executemany('INSERT INTO robot (timestamp, commands, result, duration) VALUES(?,?,?,?)', SAMPLE_DATA)
    assert len(list(db.execute('SELECT * FROM robot'))) == 2


def test__when_values_are_inserted__should_successfully_populate(db):
    db.execute('INSERT INTO robot (timestamp, commands, result, duration) VALUES(?,?,?,?)', ('2018-05-12 12:45:10.851596', 2, 4, 0.000123))
    rows = db.execute('SELECT * FROM robot').fetchall()
    assert rows == [(1, '2018-05-12 12:45:10.851596', 2, 4, 0.000123)]

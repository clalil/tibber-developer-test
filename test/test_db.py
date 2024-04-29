import pytest
import sqlite3
from src.api import DataBase
from unittest.mock import patch


SQL = '''CREATE TABLE IF NOT EXISTS robot (
        id INTEGER PRIMARY KEY,
        timestamp DATETIME DEFAULT (strftime('%Y-%m-%d %H:%M:%f', 'now', 'localtime')),
        commands INT,
        result INT,
        duration REAL)'''

SAMPLE_DATA =[('2018-05-12 12:45:10.851596', 2, 4, 0.000123), ('2018-05-10 12:45:10.851596', 3, 2, 0.000123)]


@pytest.fixture
def fixture_db():
    conn = sqlite3.connect("test_db")
    with conn:
        try:
            cursor = conn.cursor()
            cursor.execute(SQL)
        except sqlite3.Error as e:
            print(f"Error: Database could not be initialized. Due to {e}")
        yield conn
        conn.rollback()


def test__when_initialized__should_be_empty(fixture_db):
    assert len(list(fixture_db.execute('SELECT * FROM robot'))) == 0


def test__when_called_upon__should_store_data(fixture_db):
    fixture_db.executemany('INSERT INTO robot (timestamp, commands, result, duration) VALUES(?,?,?,?)', SAMPLE_DATA)
    assert len(list(fixture_db.execute('SELECT * FROM robot'))) == 2


def test__when_values_are_inserted__should_successfully_populate(fixture_db):
    fixture_db.execute('INSERT INTO robot (timestamp, commands, result, duration) VALUES(?,?,?,?)', ('2018-05-12 12:45:10.851596', 2, 4, 0.000123))
    rows = fixture_db.execute('SELECT * FROM robot').fetchall()
    assert rows == [(1, '2018-05-12 12:45:10.851596', 2, 4, 0.000123)]


def test_existing_name(capsys):
    with patch('src.api.sqlite3') as mock_sqlite3:
        with mock_sqlite3.connect(":memory:") as conn:
            conn.execute(SQL)
            db = DataBase('2018-05-12 12:45:10.851596', 2, 4, 0.000123)
            db.save_to_db()

    captured = capsys.readouterr()
    # Note: print() function has default argument end='\n', which is responsible for the end of line
    assert captured.out == "Successfully entered values into Database\n"
    assert db.response["status_code"] == 201

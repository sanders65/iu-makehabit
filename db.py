import sqlite3


def get_db(name='main.db'):
    db = sqlite3.connect(name)
    create_tables(db)
    return db

def create_tables(db):
    cur = db.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS habits (
        name TEXT PRIMARY KEY, 
        periodicity TEXT, 
        creation_date DATE, 
        streak INTEGER)""")

    cur.execute("""CREATE TABLE IF NOT EXISTS tracking (
        habitName TEXT, 
        checkoff_date DATE, 
        streak INTEGER,
        FOREIGN KEY (habitName) REFERENCES habits(name))""")

    db.commit()

def add_habit_data(db, name, periodicity, creation_date, streak):
    cur = db.cursor()
    cur.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, periodicity, creation_date, streak))
    db.commit()

def remove_habit_data(db, name, periodicity, creation_date, streak):
    cur = db.cursor()
    cur.execute("DELETE FROM habits VALUES (?, ?, ?, ?)", (name, periodicity, creation_date, streak))
    db.commit()

def add_tracking_data(db, name, checkoff_date, streak):
    cur = db.cursor()
    cur.execute("INSERT INTO tracking VALUES (?, ?, ?)", (name, checkoff_date, streak))
    db.commit()

def get_habit_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name=?", (name,))
    return cur.fetchall()

def get_all_habit_data(db):
    cur = db.cursor()
    cur.execute("SELECT * FROM habits")
    return cur.fetchall()

def get_tracking_data(db, name):
    cur = db.cursor()
    cur.execute("SELECT * FROM tracking WHERE habitName=?", (name,))
    return cur.fetchall()

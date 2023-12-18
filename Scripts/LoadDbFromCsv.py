import csv
import sqlite3

db_file = "Database\ProgramDetail.db"
csv_file = "CSV\\university.csv"

# Function to create a database connection
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn

# Function to create a table in the database
def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS programs (
                prog TEXT PRIMARY KEY,
                program TEXT,
                fee REAL,
                duration TEXT,
                no_of_seat INTEGER,
                hod TEXT
            )
        ''')
        conn.commit()
    except sqlite3.Error as e:
        print(e)

# Function to populate the database from CSV
def populate_database(db_file, csv_file):
    conn = create_connection(db_file)
    if conn:
        create_table(conn)
        try:
            cursor = conn.cursor()
            with open(csv_file, 'r',  newline='', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    prog = row['prog']
                    program = row['program']
                    fee = row['fee']
                    duration = row['duration']
                    no_of_seat = row['no_of_seat']
                    hod = row['hod']
                    cursor.execute('''
                        INSERT INTO programs (prog,program, fee, duration, no_of_seat, hod)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (prog,program, fee, duration,no_of_seat, hod))
            conn.commit()
            print("Data inserted successfully into the database.")
        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


# Call the function to populate the database
populate_database(db_file, csv_file)

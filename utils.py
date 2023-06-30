# utils.py

# create database knowledge.db if it doesn't already exist

# create the table OLKG with two columns: id (int, autoincrement) and label (text)
# it should have the following rows: Nairobi, United States, Miami Dolphins

import sqlite3
from config import PATH_DB

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    conn.close()

def create_table(db_name, table_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    create_table_query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT
        )
    '''
    cursor.execute(create_table_query)

    conn.commit()
    conn.close()

def insert_rows(db_name, table_name, rows):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    for row in rows:
        insert_row_query = f'''
            INSERT INTO {table_name} (label) VALUES (?)
        '''
        cursor.execute(insert_row_query, (row,))

    conn.commit()
    conn.close()

def create_table_entities():
    db_name = PATH_DB
    table_name = 'OLKG'
    rows = ['Nairobi', 'United States', 'Miami Dolphins']

    create_table(db_name, table_name)
    insert_rows(db_name, table_name, rows)

def create_table_ignored():
    db_name = PATH_DB
    table_name = 'OIGN'
    rows = ['i', 'you', 'he', 'she', 'they', 'we', 'it', 'who', 'which', 'that']

    create_table(db_name, table_name)
    insert_rows(db_name, table_name, rows)

if __name__ == '__main__':
    db_name = PATH_DB

    create_database(db_name)
    create_table_entities()
    create_table_ignored()

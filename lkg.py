import sqlite3
from config import PATH_DB

# tools for interacting with the local knowledge base
def get_all_entities():
    # Connect to the SQLite database using 'with' statement
    with sqlite3.connect(PATH_DB) as conn:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute the query to retrieve ignored phrases
        cursor.execute('SELECT label FROM OLKG')

        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()

        # Extract the items from the rows and store them in a list
        ignored_phrases = [row[0] for row in rows]

    return ignored_phrases

if __name__ == "__main__":
    entities = get_all_entities()
    for entity in entities:
        print(entity)
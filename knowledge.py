import requests
import xml.etree.ElementTree as ET
from functools import lru_cache
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from collections import defaultdict
from urllib.parse import unquote
from datetime import datetime 
from dictionary import get_dic_info
from config import PATH_DB
import colorama
from colorama import Fore, Back, Style

# Initialize colorama
colorama.init(autoreset=True)

DBPEDIA_API = "http://lookup.dbpedia.org/api/search/KeywordSearch"
DBPEDIA_ONTOLOGY_API = "http://dbpedia.org/sparql"
global ignored_phrases

def parse_dbpedia_result(result):
    return {
        "label": result.find("Label").text,
        "uri": result.find("URI").text,
        "description": result.find("Description").text,
        "classes": [
            {"label": cls.find("Label").text, "uri": cls.find("URI").text}
            for cls in result.find("Classes")
        ],
        "categories": [
            {"uri": cat.find("URI").text}
            for cat in result.find("Categories")
        ],
    }

def satisfy_query_dbpedia(query, result):
    if result['label']:
        return query.lower() in result["label"].lower()

@lru_cache(maxsize=None)
def search_dbpedia(query, limit=10):
    response = requests.get(
        DBPEDIA_API,
        headers={"Accept": "application/xml"},
        params={"QueryString": query, "MaxHits": limit},
    )
    if response.status_code == 200:
        root = ET.fromstring(response.content)
        results = [parse_dbpedia_result(result) for result in root.findall("Result")]
        return results
    else:
        return []

@lru_cache(maxsize=None)
def find(query):
    results = search_dbpedia(query)
    response = []

    for result in results:
        if satisfy_query_dbpedia(query, result):
            res = {
                'label': result['label']
            }
            response.append(res)
            
            # If there is an exact match, return immediately
            if res['label'].lower() == query.lower():
                return [res]

    return response if response != [] else None

import sqlite3
import csv

PATH_DB = 'knowledge.db'
TABLE_LKG = 'OLKG'
PATH_PHRASES = 'phrases.csv'

def get_phrases():
    unique_items = set()  # Create an empty set to store unique items

    # Open the CSV file in read mode
    with open(PATH_PHRASES, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)

        # Iterate over each row in the CSV file
        for row in reader:
            # Assuming each row contains a single item
            item = row[0]

            # Add the item to the set of unique items
            unique_items.add(item)

    return list( unique_items )

def is_in_ignore_list(term):
    return term.lower() in ignored_phrases

def search_in_local_kg(phrase):
    with sqlite3.connect(PATH_DB) as conn:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Search for the given phrase in the local knowledge graph using the OLKG table
        select_query = """
                        SELECT      *
                        FROM        OLKG
                        WHERE       label = ?
                        """

        cursor.execute(select_query, (phrase,))
        results = cursor.fetchall()

    if not results:
        return 
    elif len( results ) == 1:
        return results[0][0] # id of the entry in the kg
    else:
        raise Exception(f"multiple entries found in local kg: {phrase}")

def add_to_kg(label):
    """
    Add a label the local knowledge graph.
    """

    with sqlite3.connect(PATH_DB) as conn:
        cursor = conn.cursor()

        # Insert the label into the Labels table if it doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO OLKG (label)
            VALUES ( ? )
        """, (label,))

        # Get the ID of the label we just inserted or retrieved
        cursor.execute("""
            SELECT id
            FROM OLKG
            WHERE label = ?
        """, (label,))
        label_id = cursor.fetchone()[0]

        # Commit the changes
        conn.commit()
        return label_id

def process_foreign_kg( phrase ):
    """
    To process phrase through foreign knowledge graph
    """
    results = find( phrase )
    idKg = None 
    if results:
        if len( results ) == 1:
            for result in results:
                idKg = add_to_kg( phrase )
                    
    # return the id to the knowledge graph entry
    return idKg

@lru_cache(maxsize=None)  # Unbounded cache
def check_kgs(phrase):
    idKg = search_in_local_kg(phrase)
    
    # if no results (idKg is None), search foreign kg
    if not idKg:
        idKg = process_foreign_kg( phrase )

    # return the id
    return idKg
 
def trim(phrase):
    """
    Returns the phrase less its first word. If a single worded phrase is given, return None.
    """
    words = phrase.split()
    if len(words) == 1:
        return None
    return " ".join(words[1:])

def get_last_word( phrase ):
    """
    Returns the the last word of a phrase 
    """
    if phrase:
        return phrase.split()[-1]
    else:
        return None
   
def process_phrase(noun_phrase):
    """
    💪 center of the sequence. to check for phrase in our knowledge base - kgs, dics
    """
    # Exclude if in our ignore list
    if is_in_ignore_list(noun_phrase):
        print(f'\tphrase in ignore list: {noun_phrase}')
        return True

    # Test the function with a noun phrase
    noun_phrase = noun_phrase.lower()

    # --- LOCAL KG --- 
    # check in local kg 
    idKg = search_in_local_kg(noun_phrase)

    # --- FOREIGN KG --- 
    # if no results (idKg is None), search foreign kg
    if idKg:
        print(Fore.GREEN + f"Discovered in local kg: {noun_phrase}, lkg id: {idKg}")
        return True # return in case of recursive function
    else:
        idKg = process_foreign_kg( noun_phrase )

    if idKg:
        print(Fore.BLUE + f"Discovered in foreign kg: {noun_phrase}, new lkg id: {idKg}")
        return True # return in case of recursive function
    
    # --- TRIM --- 
    # if still no results, check if one words and check in dictionary
    noun_phrase_trimmed = trim( noun_phrase )

    # --- DICTIONARY --- 
    # if phrase is one word, check in dictionary
    if noun_phrase_trimmed is None:
        res_dic = get_dic_info(noun_phrase)
        if res_dic["isDicEntry"]:
            print(Back.BLACK + Fore.WHITE + f'Discovered in dic: {get_last_word(noun_phrase)}' + Style.RESET_ALL)
            return True
        else:
            print(Fore.RED + f'phrase not found in knowledge base: {noun_phrase}')
            return False 

    # --- REPEAT ---
    solution_found = False  # Flag variable to track if a solution is found
    while noun_phrase_trimmed is not None:
        if process_phrase(noun_phrase_trimmed):  # Process the trimmed phrase recursively
            solution_found = True  # Set the flag to indicate a solution is found
            break  # Exit the while loop
        noun_phrase_trimmed = trim(noun_phrase_trimmed)  # Update the value of noun_phrase_trimmed

    if solution_found:
        return True  # Return True to propagate the solution up the recursive call stack

    # Return False if no solution is found at this level or higher levels
    return False  

# Main function
def main():
    global ignored_phrases
    # get all lables from otrc that don't have a checkmark as being inspected
    # get subject labels first
    phrases = get_phrases()
    ignored_phrases = get_ignored()

    for phrase in phrases:
        try:
            # check if phrase is in ignored phrases
            phrase_lower = phrase.lower()
            if is_in_ignore_list(phrase_lower):
                print(f'\tphrase in ignore list: {phrase}')
                continue

            # if not in ignored phrases, proceed for checks 
            process_phrase( phrase )

        except Exception as e:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"Error occurred at {now}: {e}")

def get_ignored():
    # Connect to the SQLite database using 'with' statement
    with sqlite3.connect(PATH_DB) as conn:
        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Execute the query to retrieve ignored phrases
        cursor.execute('SELECT label FROM OIGN')

        # Fetch all the rows as a list of tuples
        rows = cursor.fetchall()

        # Extract the items from the rows and store them in a list
        ignored_phrases = [row[0] for row in rows]

    return ignored_phrases


if __name__ == "__main__":
    main()

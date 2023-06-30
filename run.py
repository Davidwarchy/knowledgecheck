# main function
import subprocess

def install_requirements():
    try:
        subprocess.check_call(['pip', 'install', '-r', 'requirements.txt'])
        print("Requirements installed successfully.")
    except subprocess.CalledProcessError:
        print("Failed to install requirements.")

install_requirements()

from lkg import get_all_entities
from knowledge import main
from utils import create_database, create_table_entities, create_table_ignored
from config import PATH_DB

# create a new database and update it with items
def create_lkg():
    db_name = PATH_DB
    print(f'creating database: {db_name}')
    create_database(db_name)
    create_table_entities()
    create_table_ignored()


# first print out the entities currently in our lkg
def show_lkg():
    """
    display all items currently in our simple knowledge graph
    """
    entities = get_all_entities()
    for entity in entities:
        print(entity)

def run_main():
    """
    run the sequence for checking items from knowledge graph
    """
    main()

# create a simple local knowledge graph
create_lkg()

# show the current items in our knowledge graph
show_lkg()

# run the knowledge checks
run_main()

# show the entities in our updated knowledge graph
show_lkg()
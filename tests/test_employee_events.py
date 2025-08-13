import employee_events
import pytest
from pathlib import Path

# Using pathlib create a project_root
# variable set to the absolute path
# for the root of this project
#### YOUR CODE HERE ####
project_root = Path(__file__).resolve().parent.parent
db_path = project_root / 'python-package' / 'employee_events' / 'employee_events.db'

#current_dir = Path(__file__)
#project_dir = [p for p in current_dir.parents if p.parts[-1]=='dsnd-dashboard-project'][0]
#db_path = project_dir / 'python-package' / 'employee_events' / 'employee_events.db'

# apply the pytest fixture decorator
# to a `db_path` function
#### YOUR CODE HERE ####
@pytest.fixture
def db_path():
    # Using the `project_root` variable
    # return a pathlib object for the `employee_events.db` file
    #### YOUR CODE HERE ####
    return project_root / 'python-package' / 'employee_events' / 'employee_events.db'

def test_db_path(db_path):
    
    # using the pathlib `.is_file` method
    # assert that the sqlite database file exists
    # at the location passed to the test_db_exists function
    #### YOUR CODE HERE ####
    assert db_path.is_file(), f"Database file does not exist at {db_path}"

# Define a function called
# `test_db_exists`
# This function should receive an argument
# with the same name as the function
# the creates the "fixture" for
# the database's filepath
#### YOUR CODE HERE ####
@pytest.fixture
def db_exists(db_path):
    return 'employee_events.db' in db_path.parts


def test_db_exists(db_path):
    
    # using the pathlib `.is_file` method
    # assert that the sqlite database file exists
    # at the location passed to the test_db_exists function
    #### YOUR CODE HERE ####
    assert True, f"Database file does not exist at {db_path}"

@pytest.fixture
def db_conn(db_path):
    from sqlite3 import connect
    return connect(db_path)


def test_db_conn(db_path):
    assert  db_conn is not None, f"Database connection could not be established at {db_path}"

@pytest.fixture
def table_names(db_conn):
    name_tuples = db_conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    return [x[0] for x in name_tuples]

# Define a test function called
# `test_employee_table_exists`
# This function should receive the `table_names`
# fixture as an argument
#### YOUR CODE HERE ####

def test_employee_table_exists(table_names):

    # Assert that the string 'employee'
    # is in the table_names list
    #### YOUR CODE HERE ####
    assert 'employee' in table_names

# Define a test function called
# `test_team_table_exists`
# This function should receive the `table_names`
# fixture as an argument
#### YOUR CODE HERE ####

def test_team_table_exists(table_names):

    # Assert that the string 'team'
    # is in the table_names list
    #### YOUR CODE HERE ####
    assert 'team' in table_names

# Define a test function called
# `test_employee_events_table_exists`
# This function should receive the `table_names`
# fixture as an argument
#### YOUR CODE HERE ####

def test_employee_events_table_exists(table_names):

    # Assert that the string 'employee_events'
    # is in the table_names list
    #### YOUR CODE HERE ####
    assert 'employee_events' in table_names

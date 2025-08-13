from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Using pathlib, create a `db_path` variable
# that points to the absolute path for the `employee_events.db` file

#project_root = Path(__file__).resolve().parent.parent
#db_path = project_root / 'python-package' / 'employee_events' / 'employee_events.db'
current_dir = Path(__file__)
project_dir = [p for p in current_dir.parents if p.parts[-1]=='dsnd-dashboard-project'][0]
db_path = project_dir / 'python-package' / 'employee_events' / 'employee_events.db'

# Leave this code unchanged
def query(func):
    """
    Decorator that runs a standard sql execution
    and returns a list of tuples
    """

    @wraps(func)
    def run_query(*args, **kwargs):
        query_string = func(*args, **kwargs)
        connection = connect(db_path)
        cursor = connection.cursor()
        result = cursor.execute(query_string).fetchall()
        connection.close()
        return result
    
    return run_query

# OPTION 1: MIXIN
# Define a class called `QueryMixin`
class QueryMixin:
    
    # Define a method named `pandas_query`
    # that receives an sql query as a string
    # and returns the query's result
    # as a pandas dataframe
    #### YOUR CODE HERE ####
    def pandas_query(self, sql_query:str) -> pd.DataFrame:
        with connect(db_path) as conn:
            df = pd.read_sql_query(sql_query, conn)
        return df

    # Define a method named `query`
    # that receives an sql_query as a string
    # and returns the query's result as
    # a list of tuples. (You will need
    # to use an sqlite3 cursor)
    #### YOUR CODE HERE ####
    @query
    def query(self, sql_query: str) -> list[tuple]:
        return query(sql_query)

        



# Import any dependencies needed to execute sql queries
# YOUR CODE HERE ####
from employee_events.sql_execution import QueryMixin, query
from sqlite3 import connect
from pathlib import Path
from functools import wraps
import pandas as pd

# Define a class called QueryBase
# Use inheritance to add methods
# for querying the employee_events database.
# YOUR CODE HERE ####
class QueryBase(QueryMixin):

    # Create a class attribute called `name`
    # set the attribute to an empty string
    # YOUR CODE HERE ####
    def __init__(self, name=''):
        self.name = name

    
    # Define a `names` method that receives
    # no passed arguments
    # YOUR CODE HERE ####
    def names(self):
        
        # Return an empty list
        # YOUR CODE HERE ####
        return []


    # Define an `event_counts` method
    # that receives an `id` argument
    # This method should return a pandas dataframe
    # YOUR CODE HERE ####
    def event_counts(self, id):

        # QUERY 1
        # Write an SQL query that groups by `event_date`
        # and sums the number of positive and negative events
        # Use f-string formatting to set the FROM {table}
        # to the `name` class attribute
        # Use f-string formatting to set the name
        # of id columns used for joining
        # order by the event_date column
        query1 = f"""
                SELECT event_date AS event_date,
                    SUM(positive_events) AS positive_events,
                    SUM(negative_events) AS negative_events
                FROM employee_events
                WHERE {self.name}_id = {id}
                GROUP BY event_date
                ORDER BY event_date
            """

        return self.pandas_query(query1)

    # Define a `notes` method that receives an id argument
    # This function should return a pandas dataframe
    # YOUR CODE HERE ####
    def notes(self, id):

        # QUERY 2
        # Write an SQL query that returns `note_date`, and `note`
        # from the `notes` table
        # Set the joined table names and id columns
        # with f-string formatting
        # so the query returns the notes
        # for the table name in the `name` class attribute
        # YOUR CODE HERE ####
        query2 = f"""
                SELECT note_date AS note_date,
                    note AS note
                FROM notes
                WHERE {self.name}_id = {id}
                ORDER BY note_date
            """

        return self.pandas_query(query2)

# Import the QueryBase class
#### YOUR CODE HERE ####
from employee_events.query_base import QueryBase
from employee_events.sql_execution import QueryMixin, query
import pandas as pd
import pytest
from sqlite3 import connect
from pathlib import Path
from functools import wraps


# Define a subclass of QueryBase
# called Employee
#### YOUR CODE HERE ####
class Employee(QueryBase):

    # Set the class attribute `name`
    # to the string "employee"
    #### YOUR CODE HERE ####
    def __init__(self):
        super().__init__("employee")

    # Define a method called `names`
    # that receives no arguments
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE ####
    @query
    def names(self):
        # Query 3
        # Write an SQL query
        # that selects two columns 
        # 1. The employee's full name
        # 2. The employee's id
        # This query should return the data
        # for all employees in the database
        #### YOUR CODE HERE ####
        return f"""
                    SELECT first_name || ' ' || last_name AS full_name
                         , {self.name}_id
                    FROM {self.name}
                """
    
    # Define a method called `username`
    # that receives an `id` argument
    # This method should return a list of tuples
    # from an sql execution
    #### YOUR CODE HERE ####
    @query
    def username(self, id):
        
        # Query 4
        # Write an SQL query
        # that selects an employees full name
        # Use f-string formatting and a WHERE filter
        # to only return the full name of the employee
        # with an id equal to the id argument
        #### YOUR CODE HERE ####
        return f"""
                    SELECT first_name || ' ' || last_name AS full_name
                    FROM {self.name}
                    WHERE {self.name}_id = {id}
                """


    # Below is method with an SQL query
    # This SQL query generates the data needed for
    # the machine learning model.
    # Without editing the query, alter this method
    # so when it is called, a pandas dataframe
    # is returns containing the execution of
    # the sql query
    #### YOUR CODE HERE ####
    def model_data(self, id):

        pd_query = f"""
                    SELECT SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                """
        # Use the pandas_query method
        # from the QueryMixin class
        # to return the query's result
        # as a pandas dataframe
        return self.pandas_query(pd_query)
# Import the QueryBase class
# YOUR CODE HERE ####
from employee_events.query_base import QueryBase

# Import dependencies for sql execution
#### YOUR CODE HERE ####
from employee_events.sql_execution import QueryMixin, query

# Create a subclass of QueryBase
# called  `Team`
#### YOUR CODE HERE ####
class Team(QueryBase):

    # Set the class attribute `name`
    # to the string "team"
    #### YOUR CODE HERE ####
    def __init__(self):
        super().__init__("team")


    # Define a `names` method
    # that receives no arguments
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE ####
    @query
    def names(self):

        # Query 5
        # Write an SQL query that selects
        # the team_name and team_id columns
        # from the team table for all teams
        # in the database
        #### YOUR CODE HERE ####
        #print(f"DEBUG: self.name = '{self.name}'")
        #query5 = f"""
        #            SELECT team_name, team_id
        #            FROM {self.name}
        #        """

        #return self.pandas_query(query5)
        return f"""
            SELECT team_name, team_id
            FROM {self.name}
        """

    # Define a `username` method
    # that receives an ID argument
    # This method should return
    # a list of tuples from an sql execution
    #### YOUR CODE HERE ####
    def username(self, id):

        # Query 6
        # Write an SQL query
        # that selects the team_name column
        # Use f-string formatting and a WHERE filter
        # to only return the team name related to
        # the ID argument
        #### YOUR CODE HERE ####
        #query6 = f"""
        #            SELECT team_name
        #            FROM {self.name}
        #            WHERE team_id = {id}
        #        """
        #return self.pandas_query(query6)
        return f"""
            SELECT team_name
            FROM {self.name}
            WHERE team_id = {id}
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

        query7 = f"""
            SELECT positive_events, negative_events FROM (
                    SELECT employee_id
                         , SUM(positive_events) positive_events
                         , SUM(negative_events) negative_events
                    FROM {self.name}
                    JOIN employee_events
                        USING({self.name}_id)
                    WHERE {self.name}.{self.name}_id = {id}
                    GROUP BY employee_id
                   )
                """
        return self.pandas_query(query7)
    
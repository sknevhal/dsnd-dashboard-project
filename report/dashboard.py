from fasthtml.common import *
from matplotlib import cm
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
#### YOUR CODE HERE ####
from employee_events.query_base import QueryBase
from employee_events.employee import Employee
from employee_events.team import Team

# import the load_model function from the utils.py file
from utils import load_model
import pandas as pd

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
#### YOUR CODE HERE ####
class ReportDropdown(Dropdown):

    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    #### YOUR CODE HERE ####
    def build_component(self, entity_id, model):

        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = getattr(model, "name", None) or "Select an option"
     
        # Return the output from the
        # parent class's build_component method
        return super().build_component(entity_id, model)

        
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    #### YOUR CODE HERE ####
    def component_data(self, entity_id, model):
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        return model.names()
        


# Create a subclass of base_components/BaseComponent
# called `Header`
#### YOUR CODE HERE ####
class Header(BaseComponent):

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    #### YOUR CODE HERE ####
    def build_component(self, entity_id, model):
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        #### YOUR CODE HERE ####
        if model.name == "employee":
            title_text = "Employee Performance"
        elif model.name == "team":
            title_text = "Team Performance"
        else:
            title_text = "Performance Overview"  # default fallback

        return H1(title_text, cls="header-title")
        #return H1(model.name, cls='header-title')
        
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
#### YOUR CODE HERE ####
class LineChart(MatplotlibViz):
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    #### YOUR CODE HERE ####
    def visualization(self, entity_id, model):
        ###return super().visualization(entity_id, model)

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        #### YOUR CODE HERE ####
        df = model.event_counts(entity_id)
        
        if df.empty:
            print(f"No events found for employee_id={entity_id}", flush=True)

        x = df["event_date"]
        y = (df["positive_events"] + df["negative_events"])

        # Use the pandas .fillna method to fill nulls with 0
        #### YOUR CODE HERE ####
        x.fillna(0, inplace=True)
        y.fillna(0, inplace=True)

        # Create a new dataframe using the x and y variables
        #### YOUR CODE HERE ####
        df = pd.DataFrame({'event_date': x.index, 'event_count': y.values})

        # Convert the 'event_date' column to datetime
        #### YOUR CODE HERE ####
        df['event_date'] = pd.to_datetime(df['event_date'])

        # Set the 'event_date' column as the index
        # and sort the index
        # User the pandas .set_index method to set
        # the date column as the index
        #### YOUR CODE HERE ####
        df.set_index('event_date', inplace=True)

        # Sort the index
        #### YOUR CODE HERE ####
        df.sort_index(inplace=True)

        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        #### YOUR CODE HERE ####
        # Keep a copy of the original counts
        df_original = df.copy()
        # Make cumulative version
        df_cum = df_original.cumsum()

        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        #### YOUR CODE HERE ####
        df['Positive'] = df['event_count'].where(df['event_count'] > 0, 0)
        df['Negative'] = df['event_count'].where(df['event_count'] < 0, 0)
        df = df[['Positive', 'Negative']]
        # Reset the index
        df.reset_index(inplace=True)

        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        #### YOUR CODE HERE ####
        fig, axes = plt.subplots(2, 1, figsize=(10, 8))
        
        # call the .plot method for the
        # cumulative counts dataframe
        #### YOUR CODE HERE ####
        #df.plot(ax=axes[0], title='Cumulative Event Counts')
        #df.plot(ax=axes[1], kind='bar', title='Event Counts')
        # Cumulative line plot
        df_cum.plot(ax=axes[0], title='Cumulative Event Counts')

        # Original counts bar plot
        df_original.plot(ax=axes[1], kind='bar', title='Event Counts')
        # Date formatting & rotation
        import matplotlib.dates as mdates
        for ax in axes:
            ax.xaxis.set_major_locator(mdates.AutoDateLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))  
            ax.tick_params(axis='x', rotation=45)  

        plt.tight_layout()

        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        #### YOUR CODE HERE ####
        self.set_axis_styling(axes[0], bordercolor='black', fontcolor='black')
        self.set_axis_styling(axes[1], bordercolor='black', fontcolor='black')
        
        # Set title and labels for x and y axis
        #### YOUR CODE HERE ####
        axes[0].set_title("Cumulative Event Counts", fontsize=20)
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel("Count")

        axes[1].set_title("Event Counts", fontsize=20)
        axes[1].set_xlabel('Date')
        axes[1].set_ylabel("Count")


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
#### YOUR CODE HERE ####
class BarChart(MatplotlibViz):

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    #### YOUR CODE HERE ####
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    #### YOUR CODE HERE ####
    def visualization(self, asset_id, model):

        import matplotlib.cm as cm
        import matplotlib.colors as mcolors

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        #### YOUR CODE HERE ####
        model_data = model.model_data(asset_id)

        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        #### YOUR CODE HERE ####
        predict_proba_output = self.predictor.predict_proba(model_data)        
        
        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        #### YOUR CODE HERE ####
        predict_proba_output = predict_proba_output[:, 1]

        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        #### YOUR CODE HERE ####
        if model.name == "team":
            pred = predict_proba_output.mean()

        # Otherwise set `pred` to the first value
        # of the predict_proba output
        #### YOUR CODE HERE ####
        else:
            pred = predict_proba_output[0]

        # Initialize a matplotlib subplot
        #### YOUR CODE HERE ####
        fig, ax = plt.subplots(figsize=(10, 5))

        # --- Color scale mapping ---
        cmap = cm.get_cmap("RdYlGn_r")  # reversed so red=high, green=low
        norm = mcolors.Normalize(vmin=0, vmax=1)
        bar_color = cmap(norm(pred))

        ax.barh([''], [pred], color=bar_color)
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)

        # Add colorbar legend
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, orientation="horizontal", fraction=0.12, pad=0.1)
        cbar.set_label("Recruitment Risk Probability")

        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        #### YOUR CODE HERE ####
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        

# Create a subclass of combined_components/CombinedComponent
# called Visualizations
#### YOUR CODE HERE ####
class Visualizations(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    #### YOUR CODE HERE ####
    children = [
        LineChart(),
        BarChart()
    ]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
#### YOUR CODE HERE ####
class NotesTable(DataTable):

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    #### YOUR CODE HERE ####
    def component_data(self, entity_id, model):

        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        #### YOUR CODE HERE ####
        return model.notes(entity_id)

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
#### YOUR CODE HERE ####
class Report(CombinedComponent):

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    #### YOUR CODE HERE ####
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize a fasthtml app
#### YOUR CODE HERE ####
from fasthtml import FastHTML
app = FastHTML()

# Initialize the `Report` class
#### YOUR CODE HERE ####
report = Report()

# Create a route for a get request
# Set the route's path to the root
#### YOUR CODE HERE ####
@app.get('/')
def get():
    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
    #### YOUR CODE HERE ####
    return report(1, Employee()) #[("Alice Smith", 1), ("Subhash Nevhal", 2)] 

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
#### YOUR CODE HERE ####
@app.route('/employee/{id}')
def get(id:str):

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    #### YOUR CODE HERE ####
    return report(id, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
#### YOUR CODE HERE ####
@app.get('/team/{id}')
def get_team(id:str):

    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    #### YOUR CODE HERE ####
    return report(id, Team())

# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)
    


serve()

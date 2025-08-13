from base_components.base_component import BaseComponent
from fasthtml.common import Select, Label, Div, Option

class Dropdown(BaseComponent):


    def __init__(self, id="selector", name="entity-selection", label=""):
        self.id = id
        self.name = name
        self.label = label

    def build_component(self, entity_id, model):
        options = []
        for display_text, value in self.component_data(entity_id, model):
            is_selected = str(value) == str(entity_id)
            options.append(
                Option(display_text, value=value, selected=is_selected)
            )


        dropdown_settings = {
            'id': self.id,
            'name': self.name
        }

        # if model.name:
        #     dropdown_settings['disabled'] = 'disabled'
        

        selector = Select(
            *options,
            **dropdown_settings
            )
        
        
        return selector
    
    def outer_div(self, child):

        return Div(
            Label(self.label, _for=self.id),
            child,
            id=self.id,
        )
    
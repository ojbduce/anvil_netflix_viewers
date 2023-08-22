from ._anvil_designer import View_DataTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class View_Data(View_DataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.selected_file = None
    self.show_files_dropdown()
    if self.drop_down_1.selected_value:
      self.label_1.text = self.drop_down_1.selected_value
  def show_files_dropdown(self, **event_args):
    #self.drop_down_1.items = [row['path'] for row in app_tables.files.search()]
    files = app_tables.files.search()
    #self.drop_down_1.items = [(f['path'], f) for f in files]
    self.drop_down_1.items = [(f['version'], f) for f in files]
    

  #def form_show(self, **event_args):
   # """This method is called when the column panel is shown on the screen"""
    #self.drop_down_1.items = [row['path'] for row in app_tables.files.search()]
  
# Method to set self.selected_file
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    self.label_1.text = self.drop_down_1.selected_value['path']
    selected_row = self.drop_down_1.selected_value
    self.selected_file = selected_row['file']
    print(self.selected_file) #Ok but what file?

  def button_inspect_file_click(self, **event_args):
    """This method is called when the button is clicked"""
    file = self.selected_file
    anvil.server.call('csv_to_dataframe_bytes', file)

  def button_inspect_data_location_click(self, **event_args):
    """This method is called when the button is clicked"""
    version_id = self.drop_down_1.selected_value['version']
    anvil.server.call('csv_to_dataframe_version', version_id)
    


    



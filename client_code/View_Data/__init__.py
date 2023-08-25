
from ._anvil_designer import View_DataTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class View_Data(View_DataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.plot_1.visible = False
    self.plot_2.visible = False
    self.plot_3.visible = False
    self.selected_file = None
    self.show_files_dropdown()
    if self.drop_down_1.selected_value:
      self.label_1.text = self.drop_down_1.selected_value
  def show_files_dropdown(self, **event_args):
    #self.drop_down_1.items = [row['path'] for row in app_tables.files.search()]
    files = app_tables.files.search()
    # look at SearchIterator as list to understand what we are getting back.
    files_as_list = list(files)
    print("Getting files from Data Table:  ")
    for row in files_as_list:
      print(row)
    self.drop_down_1.items = [(f['path'], f) for f in files]
    #self.drop_down_1.items = [(f['version'], f) for f in files]
    

  #def form_show(self, **event_args):
   # """This method is called when the column panel is shown on the screen"""
    #self.drop_down_1.items = [row['path'] for row in app_tables.files.search()]
  
# Method to set self.selected_file
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    try:
      self.label_1.text = self.drop_down_1.selected_value['path']
      selected_row = self.drop_down_1.selected_value
      self.selected_file = selected_row['file']
      print(self.selected_file) #Ok but what file?
    except TypeError:
      alert("Please select a data source from the drop-down box")

  def button_inspect_file_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.drop_down_1.selected_value is not None:
      file = self.selected_file
      anvil.server.call('load_data_from_file', file)
    else:
      alert("Please select a data source from the drop-down box")

  def button_inspect_data_location_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.drop_down_1.selected_value is not None:
      version_id = self.drop_down_1.selected_value['version']
      anvil.server.call('inspect_data_from_version', version_id)
    else:
      alert("Please select a data source from the drop-down box")
      

  

  def button_process_data_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.plot_1.visible = True
    self.plot_2.visible = True
    self.plot_3.visible = True
    if self.drop_down_1.selected_value is not None:
      version_id = self.drop_down_1.selected_value['version']
      category = self.drop_down_1.selected_value['category']
      fig1, fig2, fig3 = anvil.server.call('data_pipeline', version_id, category)
      self.plot_1.figure = fig1
      self.plot_2.figure = fig2
      self.plot_3.figure = fig3
      
    else:
      alert("Please select a data source from the drop-down box")


    


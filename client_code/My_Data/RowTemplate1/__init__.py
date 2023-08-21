from ._anvil_designer import RowTemplate1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class RowTemplate1(RowTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    # Assuming each row has a unique 'version' column
    print(event_args)
    #version = event_args['row']['version']
    
    # Get the file associated with this version ID
    #file_row = app_tables.my_table_name.get(version=version)
    
    # Trigger the file download
    #anvil.server.download(file_row['file'])

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    #print(event_args) - doesn't get version data from row
    version = self.item['version']
    #print(version) - OK!
    file_row = app_tables.files.get(version=version)
    anvil.media.download(file_row['file'])





  

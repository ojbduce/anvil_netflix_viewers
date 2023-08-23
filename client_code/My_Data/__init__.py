from ._anvil_designer import My_DataTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class My_Data(My_DataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_file_category.items = None
  

  

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    file = file
    anvil.server.call('upload_a_file_to_database',file)
    Notification("File uploaded successfully!", timeout=3).show()

  def button_refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = anvil.server.call('show_uploaded_files')

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    pass

  def form_show_drop_down_categories(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    categories = app_tables.files.search()





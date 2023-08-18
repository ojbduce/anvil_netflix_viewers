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
    self.show_files_dropdown()()
  def show_files_dropdown(self, **event_args):
    self.drop_down_1.items = [row['path'] for row in app_tables.files.search()]






    # Any code you write here will run before the form opens.

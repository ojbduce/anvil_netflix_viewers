from ._anvil_designer import My_DataTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

'''move the category choice in upload to a notification popup launched on click event of uploader'''

class My_Data(My_DataTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_file_category.placeholder = "Please Select Category"
  def form_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    categories = app_tables.files.search()
    #self.drop_down_file_category.items = [c['category']for c in categories]
    self.drop_down_file_category.items = ['netflix','other']
    self.repeating_panel_1.items = anvil.server.call('show_uploaded_files')

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    if self.drop_down_file_category.selected_value is not None:
      category = self.drop_down_file_category.selected_value
      file = file
      anvil.server.call('upload_a_file_to_database',file, category)
      Notification("File uploaded successfully!", timeout=3).show()
    else:
      alert("Missing category designation. Please select a category from the drop-down box.")
      self.drop_down_file_category.focus()
      

  def button_refresh_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.repeating_panel_1.items = anvil.server.call('show_uploaded_files')
    # if dropdown.selected_value == x:
    #show x else show y

  

  def drop_down_file_category_change(self, **event_args):
    """This method is called when an item is selected"""
    pass


  





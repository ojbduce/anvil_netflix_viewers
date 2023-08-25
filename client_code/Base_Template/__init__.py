from ._anvil_designer import Base_TemplateTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..View_Data import View_Data
from ..My_Data import My_Data

class Base_Template(Base_TemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    
    
    

    # Any code you write here will run before the form opens.

  # Navigation 

  # "Home"

  def content_panel_show(self, **event_args):
    """This method is called when the column panel is shown on the screen"""
    self.content_panel.add_component(View_Data())

  # Links
  def link_admin_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(My_Data())

  def button_view_report_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.content_panel.clear()
    self.content_panel.add_component(View_Data()())

  def link_home_click(self, **event_args):
    self.content_panel.clear()
    self.content_panel.add_component(View_Data())

  




  


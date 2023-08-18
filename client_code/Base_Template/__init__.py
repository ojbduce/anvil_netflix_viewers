from ._anvil_designer import Base_TemplateTemplate
from anvil import *

class Base_Template(Base_TemplateTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.

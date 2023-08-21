import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import uuid 
import pandas as pd

@anvil.server.callable #why not?
def generate_unique_id():
    return str(uuid.uuid4())

@anvil.server.callable
def upload_a_file_to_database(file):
  version = generate_unique_id()
  # add file. file is media object, path is name attribute of file, version is return from above
  app_tables.files.add_row(file=file, path=file.name, version=version)
  
  
@anvil.server.callable
def show_uploaded_files():
  return app_tables.files.search()

def csv_to_dataframe(file):
  file = file
  dataframe = pd.read_csv(file)
  print (dataframe)
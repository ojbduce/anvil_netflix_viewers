import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import uuid 

@anvil.server.callable #why not?
def generate_unique_id():
    return str(uuid.uuid4())

@anvil.server.callable
def upload_a_file_to_database(file):
  version = generate_unique_id()
  # add file. file is media object, path is name attribute of file, version is return from above
  app_tables.files.add_row(file=file, path=file.name, version=version)
  anvil.Notification("File uploaded successfully!", timeout=3).show()
  
@anvil.server.callable
def show_uploaded_files():
  return app_tables.files.search()
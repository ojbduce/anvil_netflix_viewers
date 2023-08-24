import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import uuid 
import pandas as pd
from io import BytesIO

@anvil.server.callable #why not?
def generate_unique_id():
    return str(uuid.uuid4())

@anvil.server.callable
def upload_a_file_to_database(file, category):
  category = category
  print(category)
  version = generate_unique_id()
  # add file. file is media object, path is name attribute of file, version is return from above
  app_tables.files.add_row(file=file, path=file.name, version=version, category=category)
  
  
@anvil.server.callable
def show_uploaded_files():
  return app_tables.files.search()

@anvil.server.callable
def csv_to_dataframe_bytes(file):
  file_like_object = BytesIO(file.get_bytes())
  dataframe = pd.read_csv(file_like_object)
  pd.set_option('display.max_columns', None)
  print (dataframe.head)

@anvil.server.callable
def csv_to_dataframe_version(version_id):
  row = app_tables.files.get(version = version_id)
  file = row['file']
  file_like_object = BytesIO(file.get_bytes())
  dataframe = pd.read_csv(file_like_object)
  #pd.set_option('display.width', 0)
  pd.set_option('display.max_columns', None)
  print (dataframe.head)

@anvil.server.callable
def process_data(data, category):
    if category == 'netflix':
      print(category)
      return process_netflix_data(data)
    elif category == 'other':
      print(category)
      print("Nothing available. Please check later.")
        #return process_youtube_data(data)
    # ... other categories
    else:
        raise ValueError(f"Unknown data category: {category}")
      
# choose file or version and archive the other function
def process_netflix_data(file):
  netflix_df = csv_to_dataframe_bytes(file)
  netflix_df = netflix_df.loc[:,['type', 'country', 'date_added']]
  netflix_df = netflix_df.dropna(subset=['country'])
  #netflix_df['Country'] = netflix_df['Country'].fillna('International')
  netflix_df['country'] = [countries[0] for countries in netflix_df['country'].str.split(',')]
  country_counts = pd.DataFrame(netflix_df['country'].value_counts().rename_axis('countries').reset_index(name='counts')).sort_values(by=['countries'])
  netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'])
  return netflix_df, country_counts


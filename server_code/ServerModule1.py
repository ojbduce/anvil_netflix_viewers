import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import uuid 
import pandas as pd
from io import BytesIO
import plotly.graph_objects as go

# Database Functions
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
  
# Data Processing

  # Load user-selected data
@anvil.server.callable
def load_data_from_version(version_id):
  print("Loading version of your file")
  row = app_tables.files.get(version = version_id)
  file = row['file']
  file_like_object = BytesIO(file.get_bytes())
  dataframe = pd.read_csv(file_like_object)
  return dataframe

  # Inspect version. Print df.head
@anvil.server.callable
def inspect_data_from_version(version_id):
  dataframe = load_data_from_version(version_id)
  #pd.set_option('display.width', 0)
  pd.set_option('display.max_columns', None)
  print (dataframe.head)


  # Check category. Extend to Data Factory
@anvil.server.callable
def data_pipeline(version_id, category):
    if category == 'netflix':
      print(category)
      return process_netflix_data(version_id)
      # print(process_netflix_data(data))
    elif category == 'other':
      print(category)
      print("Nothing available. Please check later.")
        
    # ... other categories
    else:
        raise ValueError(f"Unknown data category: {category}")
      
  # Process according to category type
@anvil.server.callable
def process_netflix_data(version_id):
  print("Processing Netflix data. Inside function process...")
  netflix_df = load_data_from_version(version_id)
  print("Version found")
  print(netflix_df)
  netflix_df = netflix_df.loc[:,['type', 'country', 'date_added']]
  print(".loc not the issue?")
  netflix_df = netflix_df.dropna(subset=['country'])
  #netflix_df['Country'] = netflix_df['Country'].fillna('International')
  netflix_df['country'] = [countries[0] for countries in netflix_df['country'].str.split(',')]
  country_counts = pd.DataFrame(netflix_df['country'].value_counts().rename_axis('countries').reset_index(name='counts')).sort_values(by=['countries'])
  netflix_df['date_added'] = netflix_df['date_added'].str.strip().astype(str)
  #netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'], format="%B %d, %Y")
  netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'], errors='coerce')
  #netflix_df['date_added'] = pd.to_datetime(netflix_df['date_added'])
  print(netflix_df, country_counts)
  #return netflix_df, country_counts
  return create_plots(netflix_df,country_counts)

@anvil.server.callable
def create_plots(netflix_df, country_counts):
  print("Creating plots...")
  fig1 = go.Figure(
    go.Scattergeo(
      locations=sorted(netflix_df['country'].unique().tolist()), 
      locationmode='country names',  
      text = country_counts['counts'],
      marker= dict(size= country_counts['counts'], sizemode = 'area')))
  fig2 = go.Figure(
    go.Pie(
    labels=netflix_df['type'], 
    values=netflix_df['type'].value_counts()
    ))
  
  fig3 = go.Figure(
    go.Scatter(
      x=netflix_df['date_added'].dt.year.value_counts().sort_index().index, 
      y=netflix_df['date_added'].dt.year.value_counts().sort_index()
    ))

  return fig1, fig2, fig3






# Ancillary - another option for inspecting, by file. Simpler but less robust
@anvil.server.callable
def load_data_from_file(file):
  file_like_object = BytesIO(file.get_bytes())
  dataframe = pd.read_csv(file_like_object)
  pd.set_option('display.max_columns', None)
  print (dataframe.head)
  print()
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
      marker= dict(
        size= country_counts['counts'],
        line_width = 0,
        sizeref = 2,
        sizemode = 'area',
        color='#6750A4' # Making the map bubbles tertiary
      ))
  )
  fig2 = go.Figure(
    go.Pie(
    labels=netflix_df['type'], 
    values=netflix_df['type'].value_counts(),
    marker=dict(colors=['#7D5260', '#FFD8E4']), # Making the pie chart two different shades of red
    hole=.4, # Adding a hole to the middle of the chart
    textposition= 'inside', 
    textinfo='percent+label'
  ))
    
  
  fig3 = go.Figure(
    go.Scatter(
      x=netflix_df['date_added'].dt.year.value_counts().sort_index().index, 
      y=netflix_df['date_added'].dt.year.value_counts().sort_index(),
      line=dict(color='#6750A4', width=3)
    ))
  fig1.update_layout(
  title='Production countries',
  font=dict(family='Roboto', color='#1C1B1F'), # Customizing the font
  margin=dict(t=60, b=30, l=0, r=0), # Changing the margin sizes of the figure
  paper_bgcolor='#E7E0EC', # Setting the card color to grey
  plot_bgcolor='#E7E0EC', # Setting background of the figure to grey
  hoverlabel=dict(font_size=14, font_family='Roboto'),
  geo=dict(
    framecolor='rgba(0,0,0,0)',
    bgcolor='rgba(0,0,0,0)',
    landcolor='#7D7D7D',
    lakecolor = 'rgba(0,0,0,0)',))

  fig2.update_layout(
  title='Content breakdown by type',
  margin=dict(t=60, b=30, l=10, r=10),
  showlegend=False,
  paper_bgcolor='#E7E0EC',
  plot_bgcolor='#E7E0EC',
  font=dict(family='Roboto', color='#1C1B1F'))

  fig3.update_layout(
  title='Content added over time',
  margin=dict(t=60, b=40, l=50, r=50),
  paper_bgcolor='#E7E0EC',
  plot_bgcolor='#E7E0EC',
  font=dict(family='Roboto', color='#1C1B1F'),
  hoverlabel=dict(font_size=14, font_family='Roboto'))


  return fig1, fig2, fig3






# Ancillary - another option for inspecting, by file. Simpler but less robust
@anvil.server.callable
def load_data_from_file(file):
  file_like_object = BytesIO(file.get_bytes())
  dataframe = pd.read_csv(file_like_object)
  pd.set_option('display.max_columns', None)
  print (dataframe.head)
  print()
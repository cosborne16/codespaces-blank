                                    
#This is for Part 1.2 of lab!
import pandas as pd

def get_unique_water_sites(csv_path='station.csv'):
    df = pd.read_csv(csv_path)

    site_info = df[[
        'MonitoringLocationIdentifier',
        'MonitoringLocationName',
        'LatitudeMeasure',
        'LongitudeMeasure',
        'MonitoringLocationDescriptionText'
    ]]

    unique_sites = site_info.drop_duplicates(subset=['MonitoringLocationIdentifier'])

    for _, row in unique_sites.iterrows():
        print(f"Site ID: {row['MonitoringLocationIdentifier']}")
        print(f"Name: {row['MonitoringLocationName']}")
        print(f"Location: ({row['LatitudeMeasure']}, {row['LongitudeMeasure']})")
        description = row['MonitoringLocationDescriptionText']
        if pd.notna(description):
            print(f"Description: {description}")
        print("-" * 40)



# This is for Part 1.3 for th lab to create my coooool map!!

import pandas as pd
import plotly.express as px



def plot_station_map(csv_path='station.csv'):
    # Load the data
    df = pd.read_csv(csv_path)

    # Filter and clean
    stations = df.drop_duplicates(subset=['MonitoringLocationIdentifier'])
    stations = stations.dropna(subset=['LatitudeMeasure', 'LongitudeMeasure'])

    # Create the interactive map
    fig = px.scatter_mapbox(
        stations,
        lat='LatitudeMeasure',
        lon='LongitudeMeasure',
        hover_name='MonitoringLocationName',
        hover_data={'LatitudeMeasure': False, 'LongitudeMeasure': False},
        zoom=5,
        height=600
    )

    # Use open Mapbox style (no token required)
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r':0, 't':0, 'l':0, 'b':0})

    # Show map
    fig.show()

# Usage
plot_station_map('station.csv')

# This is for Part 2.2 to create a graph with just one variable
import pandas as pd
import plotly.express as px

def plot_station_map_to_html(csv_path='station.csv', output_html='station_map.html'):
    # Load the CSV
    df = pd.read_csv(csv_path)

    # Drop duplicates and missing coordinates
    stations = df.drop_duplicates(subset=['MonitoringLocationIdentifier'])
    stations = stations.dropna(subset=['LatitudeMeasure', 'LongitudeMeasure'])

    # Create interactive map using scatter_map
    fig = px.scatter_map(
        stations,
        lat='LatitudeMeasure',
        lon='LongitudeMeasure',
        color='MonitoringLocationIdentifier',
        hover_name='MonitoringLocationName',
        hover_data={'LatitudeMeasure': True, 'LongitudeMeasure': True},
        zoom=5,
        height=600,
        title='Monitoring Sites Map'
    )

    # Set open map style and layout
    fig.update_layout(mapbox_style='open-street-map')
    fig.update_layout(margin={'r': 0, 't': 30, 'l': 0, 'b': 0})

    # Export to HTML
    fig.write_html(output_html)
    print(f"✅ Map saved to: {output_html}")

# Usage:
plot_station_map_to_html('station.csv', 'station_map.html')




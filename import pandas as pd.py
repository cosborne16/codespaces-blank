                                    
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
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

def plot_precipitation_timeseries(csv_path='narrowresult.csv'):
    # Load data
    df = pd.read_csv(csv_path)

    # Filter for precipitation in inches
    is_precip = df['CharacteristicName'].str.contains("precipitation", case=False, na=False)
    is_inches = df['ResultMeasure/MeasureUnitCode'].str.lower() == 'in'
    filtered = df[is_precip & is_inches]

    # Parse dates
    filtered['ActivityStartDate'] = pd.to_datetime(filtered['ActivityStartDate'])

    # Prepare plot
    sns.set_theme(style="whitegrid", palette="pastel")

    plt.figure(figsize=(12, 6))

    # Plot each station
    for station, group in filtered.groupby("MonitoringLocationIdentifier"):
        group = group.sort_values("ActivityStartDate")
        plt.plot(group["ActivityStartDate"], group["ResultMeasureValue"],
                 label=station, linewidth=2)

    # Format plot
    plt.title("Precipitation Over Time by Station", fontsize=16)
    plt.xlabel("Date")
    plt.ylabel("Precipitation (inches)")
    plt.legend(title="Station", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.grid(True)

    # Show plot
    plt.show()

# Run the function
plot_precipitation_timeseries('narrowresult.csv')









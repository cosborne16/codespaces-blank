                                    
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

def plot_precipitation_by_station(csv_path='narrowresult.csv'):
    # Load the dataset
    df = pd.read_csv(csv_path)

    # Debug: print unique values to help verify correct filtering (optional)
    print("Unique Characteristic Names:")
    print(df['CharacteristicName'].unique())
    print("\nUnique Measure Unit Codes:")
    print(df['ResultMeasure/MeasureUnitCode'].unique())

    # Filter: Only precipitation measurements in inches (allow for common variants)
    is_precip = df['CharacteristicName'].str.contains('precipitation', case=False, na=False)
    is_inches = df['ResultMeasure/MeasureUnitCode'].str.lower().isin(['in', 'inches'])
    df_filtered = df[is_precip & is_inches].copy()

    # Debug: check the number of rows after filtering
    print("\nNumber of rows after filtering:", df_filtered.shape[0])
    if df_filtered.empty:
        print("No data matched your filtering conditions for precipitation. Please adjust the filtering criteria.")
        return

    # Drop rows with missing critical info
    df_filtered = df_filtered.dropna(subset=['MonitoringLocationIdentifier', 'ResultMeasureValue', 'ActivityStartDate'])

    # Convert the date strings to datetime objects
    df_filtered['ActivityStartDate'] = pd.to_datetime(df_filtered['ActivityStartDate'])

    # Sort by date for consistent line plotting
    df_filtered = df_filtered.sort_values(by='ActivityStartDate')

    # Set up the pastel theme using Seaborn
    sns.set(style='whitegrid', palette='pastel')

    # Create the figure
    plt.figure(figsize=(14, 7))

    # Generate a list of unique pastel colors (one for each unique station)
    pastel_colors = sns.color_palette("pastel", n_colors=df_filtered['MonitoringLocationIdentifier'].nunique())

    # Plot each station as a separate line
    for i, (station, group) in enumerate(df_filtered.groupby('MonitoringLocationIdentifier')):
        plt.plot(group['ActivityStartDate'], group['ResultMeasureValue'],
                 label=station,
                 color=pastel_colors[i % len(pastel_colors)],
                 linewidth=2)

    # Formatting the plot
    plt.title('Precipitation Over Time by Monitoring Station', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Precipitation (inches)', fontsize=12)
    plt.legend(title='Station', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
    plt.tight_layout()
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the plot as a PNG file
    plt.savefig("precipitation_plot.png", dpi=300, bbox_inches="tight")
    print("Saved the plot as precipitation_plot.png")

    # Show the plot
    plt.show()

# Run the function
plot_precipitation_by_station('narrowresult.csv')



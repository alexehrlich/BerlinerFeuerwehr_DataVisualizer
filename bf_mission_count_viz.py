import pandas as pd
import requests
import os
import matplotlib.pyplot as plt
import geopandas as gpd
from matplotlib.patches import Ellipse
from matplotlib.widgets import Slider
from geopy.geocoders import Nominatim
import re
import array
import io


def set_geo_data(df):
    """
        Load location data for every district with geopy and write it to
        the data frame. Some locations are not found which stay NaN.
    """
    print("Loading the Geodata. This may take a while but only on the first run. The locations will then be safed!")
    print("Fetch locations . . .\n")
    df['longitude'] = float('nan')
    df['latitude'] = float('nan')

    geolocator = Nominatim(user_agent="geo_locator")
    districts = df.index.to_list()

    for district in districts:
        location = geolocator.geocode(f"{district}, Berlin, Germany", timeout=10)
        if location:
            print(f"{district}: Longitude:{location.longitude}, Latitude:{location.latitude}\n")
            df.loc[district, ['longitude', 'latitude']] = [location.longitude, location.latitude]
        else:
            print(f"{district} NOT FOUND\n")
    

def load_csv_data():
    """
        Tries to load every file from Berliner Feuerwehr github Regional Data. Starts with 2018
        and stops when no content can be fetched. Create a new data frame which only stores
        the mission_count_all from every district(index) per year (column)
    """
    print("Load public data from Berliner Feuerwehr . . .")
    df = None
    year = 2018
    while True:
        url = f"https://raw.githubusercontent.com/Berliner-Feuerwehr/BF-Open-Data/refs/heads/main/Datasets/Regional_Data/{str(year)}/BFw_district_area_data_{str(year)}.csv"
        response = requests.get(url)
        buffer = io.StringIO(response.text)

        if response.status_code != 200:
            print(f"Successfully loaded data from 2018 to {year - 1}\n")
            return df

        if df is None:
            df = pd.read_csv(buffer)
            df = df.loc[:, 'district_area_name':'mission_count_all']
            df.rename(columns={'mission_count_all': '2018'}, inplace=True)
        else:
            temp = pd.read_csv(buffer)
            df[str(year)] = temp['mission_count_all']

        year += 1



def plot_circles(year, ax, df):
    """
        Plots circles with diameter proportional to mission_Count_all
        for a specific year. Users Ellipses becuase of the aspect ratio
        of longitude and latitude.
    """
    for patch in ax.patches:
        patch.remove()

    for index in df.index:
        longitude = df.loc[index, 'longitude']
        latitude = df.loc[index, 'latitude']
        if float(longitude) != float('nan'):
            circle_center = (longitude, latitude) 
            initial_radius_x = df.loc[index, str(year)] / 600000 
            initial_radius_y = initial_radius_x / ax.get_aspect()
            if str(year) == df.columns[1:-2].to_list()[-1]:
                color = 'orange'
            else:
                color = 'red'
            ellipse = Ellipse(circle_center, width=initial_radius_x * 2, height=initial_radius_y * 2, color=color, alpha=0.5)
            ax.add_patch(ellipse)
    
def plot_districts(ax):
    berlin_districts_coordinates = {
    "Mitte": {"latitude": 52.5200, "longitude": 13.35050},
    "Friedrichshain-\nKreuzberg": {"latitude": 52.5020, "longitude": 13.4250},
    "Pankow": {"latitude": 52.6, "longitude": 13.42},
    "Charlottenburg-\nWilmersdorf": {"latitude": 52.5030, "longitude": 13.22},
    "Spandau": {"latitude": 52.5373, "longitude": 13.1975},
    "Steglitz-Zehlendorf": {"latitude": 52.44, "longitude": 13.2},
    "Tempelhof-\nSchöneberg": {"latitude": 52.4670, "longitude": 13.3546},
    "Neukölln": {"latitude": 52.4722, "longitude": 13.4258},
    "Treptow-Köpenick": {"latitude": 52.4444, "longitude": 13.5725},
    "Marzahn-\nHellersdorf": {"latitude": 52.53, "longitude": 13.5492},
    "Lichten-\nberg": {"latitude": 52.5156, "longitude": 13.48},
    "Reinickendorf": {"latitude": 52.6, "longitude": 13.25},
    }
    for key, cord in berlin_districts_coordinates.items():
        ax.text(cord['longitude'], cord['latitude'], 
            key, fontsize=5, color='white', alpha=0.5)




def clean_names(name):
    """
        Very specific function to trim all the district names to
        get as much results from geopy as possible.
    """
    delete = ['Südliche', 'Nördliche', 'Ost', 'Süd', 'West', 'Nord', 'Nordwest', 'Nordost', 'Südwest', 'Südost', 'FK', 'Zentrum', 'Mitte']

    # Create a regex pattern that matches any of the words in the delete list, case-insensitive
    pattern = r'\b(?:' + '|'.join(delete) + r')\b'
    
    # Replace words in the delete list with an empty string (case-insensitive)
    name = re.sub(pattern, "", name, flags=re.IGNORECASE).strip()

    # Replace "MV" with "Märkisches Viertel"
    name = re.sub(r"\bMV\b", "Märkisches Viertel", name).strip()

    name = re.sub(r"\bNeuköllner\b", "Neukölln", name).strip()

    # If there's a hyphen, take the part after the first hyphen
    if ' - ' in name:
        name = name[name.index(" - ") + 3:].strip()
    
    if '/' in name:
        name = name.split('/')[0].strip()
    
    if ',' in name:
        name = name.split(',')[0].strip()
    
    if name.endswith('-'):
        name = name[:-1]

    return name

    
def main():
    """
        Automated fetch of data sets from Berliner Feuerwehr starting from 2018
        to visualize the number of missions on a Berlin map and per year in a
        bar chart.
    """
    #Only load all the data if needed
    if not os.path.exists('merged_mission_count_years.csv'):
        df = load_csv_data()

        #Clean the district names before the geo data fetch for better results
        df['district_area_name'] = df['district_area_name'].apply(clean_names)
        df.set_index('district_area_name', inplace=True)
        
        #Group districts together: 
        #Prenzlauer Berg Nord and Prenzlauer Berg Süd become Prenzlauer Berg
        df = df.groupby(df.index).sum()
        set_geo_data(df)

        #Safe for later
        df.to_csv('merged_mission_count_years.csv')
    else:
        df = pd.read_csv('merged_mission_count_years.csv', index_col=0, header=0)

 
    # Plot all layers
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
    ax[0].set_title("Berlin Feuerwehr missions")

    #Read in der Berlin Map
    gdf = gpd.read_file('./bezirksgrenzen/bezirksgrenzen.shp')
    gdf.plot(ax=ax[0], color='black')

    #Plot the bar chart for missions per year, make the current year orange
    colors = ['lightblue' for year in df.columns.tolist()[:-2]]
    colors[-1] = 'orange'
    ax[1].grid(axis='y')
    ax[1].set_axisbelow(True)
    ax[1].bar(df.columns.tolist()[:-2], [df[year].sum() / 100000 for year in df.columns.tolist()[:-2]], color=colors)
    ax[1].set_title('Missions Berlin total in 100 Tsd.')


    # Add a slider for the circle diameter
    ax_slider = plt.axes([0.1, 0.02, 0.35, 0.03])  # Position of the slider
    slider = Slider(ax_slider, "Year", 2018, int(df.columns[1:-2].tolist()[-1]), valinit=2018, valstep=1)

    # Update function for the slider
    def update(val):
        plot_circles(val, ax[0], df)
        fig.canvas.draw_idle()
    slider.on_changed(update)

    plot_districts(ax[0])

    plot_circles(2018, ax[0], df)
    plt.show()


if __name__ == '__main__':
    main()
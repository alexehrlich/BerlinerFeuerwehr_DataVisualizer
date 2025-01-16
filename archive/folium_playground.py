import pandas as pd
import requests
import folium
from geopy.geocoders import Nominatim
import os
import webview
from ipywidgets import interact
import ipywidgets as widgets
import matplotlib.pyplot as plt
import time


def set_geo_data(df):
    # Initialize geolocator
    geolocator = Nominatim(user_agent="geo_locator")

    # Example: List of districts
    print(df.index.to_list())
    districts = df.index.to_list()

    # Retrieve coordinates
    geo_data = {}
    for district in districts:
        print("Requested: ", district)
        location = geolocator.geocode(f"{district}, Berlin, Germany", timeout=10)
        if location:
            #print(f"Location: {location}, {location.longitude}, {location.latitude}\n")
            #geo_data[district] = (location.latitude, location.longitude)
            df.loc[district, ['longitude', 'latitude']] = [location.longitude, location.latitude]
        else:
            print(f"{location} not found\n")
    


def load_csv_data() -> pd.DataFrame:
    data = {}
    for year in range(2018, 2025):
        url = f"https://raw.githubusercontent.com/Berliner-Feuerwehr/BF-Open-Data/refs/heads/main/Datasets/Regional_Data/{str(year)}/BFw_district_area_data_{str(year)}.csv"
        response = requests.get(url)
        with open(f"{year}.csv", 'wb') as f:
            f.write(response.content)

        data[year] = pd.read_csv(f"{year}.csv")[['district_area_name', 'mission_count_all']]

    df_merged = pd.DataFrame(columns=data.keys(), index=data[2018]['district_area_name'])

    for year in data.keys():
        for district in data[2018]['district_area_name']:
            df_merged.loc[district, year] = data[year].loc[data[year]['district_area_name'] == district, 'mission_count_all'].values[0]
    
    return df_merged

 # Function to update the map based on the selected year

def update_map(year, webview_window, df, m):
    # Clear all markers
    # for marker in list(m._children.values()):
    #     if isinstance(marker, folium.vector_layers.Circle):
    #         m.remove_child(marker)

    # Add new markers based on the selected year
    for index, row in df.iterrows():
        if pd.notna(row['longitude']) and pd.notna(row['latitude']):
            diameter = row[str(year)] / 10  # Scale the diameter (adjust this factor as needed)
            
            folium.Circle(
                location=[row['latitude'], row['longitude']],
                radius=diameter,
                color='blue',
                fill=True,
                fill_color='blue'
            ).add_to(m)

    # Save the updated map to an HTML file
    m.save("district_map_with_slider.html")
    
    # If the webview window already exists, just update its URL
    if webview_window is not None:
        webview_window.load_url('district_map_with_slider.html')
    else:
        # Otherwise, create a new webview window
        webview_window = webview.create_window('District Map', 'district_map_with_slider.html')
        webview.start()

def test():
    print("Hello")

def main():
    #df = load_csv_data()
    
    #set_geo_data(df)

    #df.to_csv('merged.csv')
    test = 5
    webview_window = None
    df = pd.read_csv('merged.csv')

    # Create a map centered around Berlin
    map_center = [52.5200, 13.4050]  # Berlin coordinates
    m = folium.Map(location=map_center, zoom_start=10)

    print("2018")
    update_map(2018, webview_window, df, m)




    
if __name__ == '__main__':
    main()
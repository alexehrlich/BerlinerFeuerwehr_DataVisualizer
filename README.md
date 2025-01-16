# Berlin Feuerwehr Regional Mission Visualization

This project automatically downloads all available regional mission data and process and groups districts to then
plot a graphical representation of the mission frequency per year in proprtional circles on the berlin map.
The map is a public available shapefile of Berlin. The location data is retreived by OpenStreetMAp.org via geopy. 

On the first execution the geo data for every district is fetched which takes a while. The data is then stored. The
next executions won't need to fetch the data and will be much faster.


## Demo
![](https://github.com/alexehrlich/BerlinerFeuerwehr_DataVisualizer/tree/main/img/demo.gif)

## Requirements
- Python 3.6 or higher
- dependecies which get installed in the venv in the section below


## Setup Instructions

- `git clone https://github.com/alexehrlich/BerlinerFeuerwehr_DataVisualizer.git` 
- `cd`to that folder
- `make setup`to automatically create virtual environment and install dependecies
- `make run`to run the code

If you don't have make you can create the venv manually and install the dependencies from requirements.txt manually.

## Resources
- Berliner Feuerwehr Data: https://github.com/Berliner-Feuerwehr/BF-Open-Data/tree/main/Datasets/Regional_Data
- Berlin Shapefiles: https://daten.odis-berlin.de
- Location Data: OpenStreetMap.org

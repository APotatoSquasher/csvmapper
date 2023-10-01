import streamlit as st
import csv
import folium
from streamlit_folium import folium_static

st.title("CSV File to Map")
filevar = st.file_uploader("Upload CSV files", accept_multiple_files=True)
       
if filevar:
    for x in filevar:
        data = x.read().decode("utf-8")  # Decode bytes to string
        st.write(x.name)
        
        if ".csv" in str(x.name):
            st.write("CSV file detected.")

            loninput = st.text_input("Enter the column number for longitude (starting from 0):")
            latinput = st.text_input("Enter the column number for latitude (starting from 0):")
            catinput = st.text_input("(Optional) Add column for the label of a particular point (starting from 0):")
            submit_button = st.button(label="Submit")
            if (submit_button) and loninput and latinput:
                try:
                    
                    lon_col = int(loninput)
                    lat_col = int(latinput)
                    listofthings = []
                    filler = []
                    st.write("Creating map...")
                    m = folium.Map(location=[0, 0], zoom_start=2)
                    latlist = []
                    lonlist = []

                        # Read CSV rows and add markers to the map
                    csv_reader = csv.reader(data.splitlines())
                    next(csv_reader)  # Skip header row
                        
                    for row in csv_reader:
                        try:
                            lat = float(row[lat_col])
                            latlist.append(lat)
                            lon = float(row[lon_col])
                            lonlist.append(lon)
                                
                            if catinput is not None:
                                category = float(row[int(catinput)])
                                listofthings.append(category)
                                

                        except (ValueError, IndexError):
                            st.write("Invalid data at row(s):", row)
                            continue
                    color = "blue"
                    if catinput is not None:
                        for j in range(len(latlist)):
                            label = listofthings[j]
                            folium.CircleMarker([lonlist[j], latlist[j]], radius=1, color=color, fill=True,popup=label).add_to(m)
                        folium_static(m)
                    else:
                        st.write("No categories selected.")
                        folium.CircleMarker([lonlist[j], latlist[j]], radius=1, color=color, fill=True,).add_to(m)
                            
                    folium_static(m)
                except ValueError:
                    st.write("Please enter valid integer values for column numbers.")
                
        else:
            st.write("This file is not a .csv file. Please remove this file.")


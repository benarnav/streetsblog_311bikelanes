import streamlit as st
import leafmap.foliumap as leafmap
from sodapy import Socrata
import pandas as pd

st.set_page_config(page_title="NYC 311 Bike Lane Complaints since Oct 2016", layout="wide")


client = Socrata("data.cityofnewyork.us", db_token, timeout=100000000)
results = client.get("erm2-nwe9", complaint_type="Illegal Parking", status="Closed", descriptor='Blocked Bike Lane', limit=2500000)
df = pd.DataFrame.from_records(results)

#Converts these two columns from str to float
df['latitude'] = df['latitude'].astype(float)
df['longitude'] = df['longitude'].astype(float)
df = df.dropna(subset=['latitude', 'longitude'])
df['value'] = 1

m = leafmap.Map(center=(40.72975524648407, -73.96071485734623), zoom=12, tiles="stamentoner")
m.add_heatmap(
    df,
    latitude="latitude",
    longitude="longitude",
    value='value',
    name="Heat map",
    radius=13,
)

m.to_streamlit(height=1000)

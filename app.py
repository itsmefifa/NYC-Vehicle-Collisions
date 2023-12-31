import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
#import plotly
import plotly.express as px
import requests
import pandas as pd
from io import StringIO

# Your GitHub details
ORGANISATION = "itsmefifa"
REPOSITORY = "NYC-Vehicle-Collisions"
OID = "02b59ff75d4eedc98ceb3f776fab98a5bb160085738b252a681d97ad32584d5c"
SIZE = "189611673"

# Construct the LFS API URL
LFS_API_URL = f"https://github.com/{ORGANISATION}/{REPOSITORY}.git/info/lfs/objects/batch"

# Create the JSON payload for the API request
payload = {
    "operation": "download", 
    "transfer": ["basic"], 
    "objects": [
        {"oid": OID, "size": int(SIZE)}
    ]
}

# Define headers for the API request
headers = {
    "Accept": "application/vnd.git-lfs+json",
    "Content-Type": "application/json"
}

# Send the API request
response = requests.post(LFS_API_URL, json=payload, headers=headers)

# Check if the request was successful (HTTP Status Code 200)
if response.status_code == 200:
    # Extract the download URL from the API response
    download_url = response.json()['objects'][0]['actions']['download']['href']

# Set Streamlit theme
st.set_page_config(
    page_title="NYC Vehicle Collisions",
    page_icon="🚗",
    layout="wide",
)

# Add a header image
image_url = "https://raw.githubusercontent.com/itsmefifa/NYC-Vehicle-Collisions/main/Castle%20Crashers.png"
st.image(image_url, use_column_width=True)

# Add a beautiful title
st.title("🌟 Explore NYC Vehicle Collisions 🌟")

# Add a subtitle
st.markdown("An interactive dashboard for analyzing motor vehicle collisions in NYC")

# Load the data
DATA_URL = download_url

# Load data using Streamlit's caching
@st.cache_data(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(100000)

# Section 5: Show Raw Data
if st.checkbox("Show Raw Data", False):
    st.subheader('📄 Raw Data')
    st.write(data)

# Section 1: Map of Injured People
st.header("🚑 Where are the most people injured in NYC? 🌇")
injured_people = st.slider("Select the number of injured persons", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how='any'))

# Section 2: Collisions by Time of Day
st.header("🕒 Collisions by Time of Day 🌞")
hour = st.slider("Select an hour to explore", 0, 23)
data = data[data['date/time'].dt.hour == hour]

st.markdown(f"Vehicle collisions between {hour}:00 and {(hour + 1) % 24}:00")
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.pydeck_chart(
    pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        initial_view_state={
            "latitude": midpoint[0],
            "longitude": midpoint[1],
            "zoom": 11,
            "pitch": 50,
        },
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data[["date/time", 'latitude', 'longitude']],
                get_position=['longitude', 'latitude'],
                radius=100,
                extruded=True,
                pickable=True,
                elevation_scale=4,
                elevation_range=[0, 1000],
            ),
        ]
    )
)

# Section 3: Breakdown by Minutes
st.subheader(f"📊 Breakdown by minutes between {hour}:00 and {(hour + 1) % 24}:00 🕒")
filtered = data[(data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes': hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)', marker_line_width=1.5)
st.plotly_chart(fig)

# Section 4: Top 5 Dangerous Streets
st.header("🔥 Top 5 dangerous streets by affected type 🔍")
select = st.selectbox("Select an affected type of people", ['Pedestrians', 'Cyclists', 'Motorists'])

if select == 'Pedestrians':
    st.write(data.query("injured_pedestrians >= 1")[["on_street_name", "injured_pedestrians"]]
             .sort_values(by=['injured_pedestrians'], ascending=False)
             .dropna())
elif select == 'Cyclists':
    st.write(data.query("injured_cyclists >= 1")[["on_street_name", "injured_cyclists"]]
             .sort_values(by=['injured_cyclists'], ascending=False)
             .dropna())
else:
    st.write(data.query("injured_motorists >= 1")[["on_street_name", "injured_motorists"]]
             .sort_values(by=['injured_motorists'], ascending=False)
             .dropna())

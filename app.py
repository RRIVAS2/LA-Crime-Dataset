import streamlit as st
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt


st.title('LA Crime Data')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv('Crime_Data_from_2020_to_Present.csv', nrows=nrows, converters={'time occ': str})
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data['date occ'] = pd.to_datetime(data['date occ'])
    return data

data = load_data(1000)

# Convert column to string and pad with leading zeros
data['hour occ'] = data['time occ'].astype(str).str.zfill(4).str[:2]



if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# Define filter options with "All" as the default value
all_areas = ['All'] + data['area name'].unique().tolist()
all_crime_desc = ['All'] + data['crm cd desc'].unique().tolist()

# Filter by area name
selected_area = st.selectbox("Select Area Name", all_areas)

# Filter by crime description
selected_crime_desc = st.selectbox("Select Crime Description", all_crime_desc)


# Apply filters
if selected_area != 'All':
    data = data[data['area name'] == selected_area]
if selected_crime_desc != 'All':
    data = data[data['crm cd desc'] == selected_crime_desc]



# Preprocess data to calculate counts for each hour
hourly_counts = data['hour occ'].value_counts().sort_index()



# Create histogram
st.write("## Hourly Occurrences Histogram")
plt.figure(figsize=(10, 6))
plt.bar(hourly_counts.index, hourly_counts, color='skyblue')
plt.xlabel('Hour of Occurrence')
plt.ylabel('Count')
plt.title('Hourly Occurrences Histogram')
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
# Display the plot in Streamlit app
st.pyplot(plt)

st.subheader('Map of crime occurances')





st.map(data[['lat','lon']])


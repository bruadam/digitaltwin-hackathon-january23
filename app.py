import streamlit as st
import pandas as pd

# Load the data
data_climify = pd.read_excel('data_climify.xlsx')
data_skylab = pd.read_excel('data_skylab.xlsx')


# Define all attributes contained in the columns locationid from the data
locationid = data_climify['locationid'].unique()

# Create the Streamlit app
st.title('Room Occupancy Dashboard')

# Display a subtitle and a selectbox for the locationid
locationid_selected = st.selectbox('Location', locationid)



# Add a date picker for the chosen date
chosen_date = st.date_input('Select a date')

# Add a time picker for the chosen time
chosen_time = st.time_input('Select a time')

# Convert the chosen date and time to a datetime object
chosen_datetime = pd.to_datetime(chosen_date.strftime('%Y-%m-%d') + ' ' + chosen_time.strftime('%H:%M:%S'))

# Convert the chosen datetime to a interger
chosen_datetime = int(chosen_datetime.value / 10**9)

# Convert the _time column to a list of integers
data_climify['_time'] = data_climify['_time'].apply(lambda x: int(x.value / 10**9))

# Convert the _time column to a datetime for the skylab data
data_skylab['_time'] = data_skylab['_time'].apply(lambda x: pd.to_datetime(x))
# Convert the _time column to a list of integers for the skylab data
data_skylab['_time'] = data_skylab['_time'].apply(lambda x: int(x.value / 10**9))

# Filter the data for the closest datetime to the chosen datetime
filtered_data_climify = data_climify[data_climify['_time'].sub(chosen_datetime).abs() == data_climify['_time'].sub(chosen_datetime).abs().min()]
filtered_data_skylab = data_skylab[data_skylab['_time'].sub(chosen_datetime).abs() == data_skylab['_time'].sub(chosen_datetime).abs().min()]

# Display a title for the filtered data
st.subheader('Occupancy data for the chosen date and time')

# Conditionally display the filtered data on the occupancy_pred column from the climify data and occupancy column from the skylab data
if filtered_data_climify['occupancy_pred'].values[0] == 1 and filtered_data_skylab['occupancy'].values[0] == 1: 
    st.write('The room is occupied')
    # Display the background color of the streamlit app to red
    st.markdown("""<style>body {background-color: #FF0000;}</style>""", unsafe_allow_html=True)
    # Display a rectangle with the color red
    st.markdown("""<style>div.Widget.row-widget.stRadio > div:nth-child(2) > div > label:nth-child(1) {background-color: #FF0000;}</style>""", unsafe_allow_html=True)
elif filtered_data_climify['occupancy_pred'].values[0] == 0 and filtered_data_skylab['occupancy'].values[0] == 0:
    st.write('The room is not occupied')
    # Display the background color of the streamlit app to green
    st.markdown("""<style>body {background-color: #00FF00;}</style>""", unsafe_allow_html=True)
    # Display a rectangle with the color green
    st.markdown("""<style>div.Widget.row-widget.stRadio > div:nth-child(2) > div > label:nth-child(2) {background-color: #00FF00;}</style>""", unsafe_allow_html=True)
elif filtered_data_climify['occupancy_pred'].values[0] == 1 and filtered_data_skylab['occupancy'].values[0] == 0:
    st.write('The room is not booked but occupied')
    # Display the background color of the streamlit app to yellow
    st.markdown("""<style>body {background-color: #FFFF00;}</style>""", unsafe_allow_html=True)
    # Display a rectangle with the color orange
    st.markdown("""<style>div.Widget.row-widget.stRadio > div:nth-child(2) > div > label:nth-child(3) {background-color: #FFFF00;}</style>""", unsafe_allow_html=True)
elif filtered_data_climify['occupancy_pred'].values[0] == 0 and filtered_data_skylab['occupancy'].values[0] == 1:
    # Display the text 'The room is booked but not occupied' in orange font color
    st.markdown('<p style="color:orange;">The room is booked but not occupied</p>', unsafe_allow_html=True)
    # Display the background color of the streamlit app to yellow
    st.markdown("""<style>body {background-color: #FFFF00;}</style>""", unsafe_allow_html=True)
    # Display a rectangle with the color orange
    st.markdown("""<style>div.Widget.row-widget.stRadio > div:nth-child(2) > div > label:nth-child(3) {background-color: #FFFF00;}</style>""", unsafe_allow_html=True)

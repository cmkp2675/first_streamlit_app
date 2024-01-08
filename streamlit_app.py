import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# Streamlit app setup
st.header('Breakfast Menu')
st.text('🥣Omega 3 & Blueberry Oatmeal')
st.text('🥗Kale, Spinach & Rocket Smoothie')
st.text('🐔Hard-Boiled Free-Range Egg')
st.text('🥑🍞Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# Read data from CSV file
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Multiselect for fruit selection
fruits_selected = st.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
st.dataframe(fruits_to_show)

# New section to display Fruityvice API response
st.header("Fruityvice Fruit Advice!")

def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    
    # Check if the request was successful (status code 200)
    if fruityvice_response.status_code == 200:
        # Check if the response has content (not None)
        if fruityvice_response.content:
            # Attempt to normalize the JSON response
            fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
            return fruityvice_normalized
        else:
            st.error("Empty response from Fruityvice API")
    else:
        st.error(f"Fruityvice API request failed with status code: {fruityvice_response.status_code}")
    return None

try:
    fruit_choice = st.text_input('What fruit would you like information about?')
    if not fruit_choice:
        st.error("Please select the fruit to get information")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        if back_from_function is not None:
            st.dataframe(back_from_function)
except URLError as e:
    st.error(e)
    
# Snowflake related function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
         return my_cur.fetchall()

# Allow the end user to add fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO FRUIT_LOAD_LIST (FRUIT_NAME) VALUES (?)", (new_fruit,))
        return f"Thanks for adding {new_fruit}"

add_my_fruit = st.text_input('What fruit would you like to add?')
if st.button('Add a Fruit to List'):    
   my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
   back_from_function = insert_row_snowflake(add_my_fruit)
   st.text(back_from_function) 

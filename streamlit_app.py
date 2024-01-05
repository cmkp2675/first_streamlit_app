import streamlit

streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") #We want pandas to read our CSV file from that S3 bucket so we use a pandas function called read_csv  to pull the data into a dataframe we'll call my_fruit_list. 
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries']) 
fruits_to_show = my_fruit_list.loc[fruits_selected] #To show only Avocado & Strawberries

# Display the table on the page
streamlit.dataframe(fruits_to_show)


streamlit.header("Fruityvice Fruit Advice!")

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "Kiwi")
#streamlit.text(fruityvice_response.json()) #writes data in JSON format

fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) #take the json version of the response and normalize it

streamlit.dataframe(fruityvice_normalized) #display o/p as a table

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

'''import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.text("The fruit load list contains:")
streamlit.text(my_data_row)'''

import snowflake.connector
import streamlit as st

# Assuming streamlit.secrets is properly configured with your Snowflake credentials

try:
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_cur = my_cnx.cursor()
    my_cur.execute('SELECT * FROM fruit_load_list')

    st.text("The fruit load list contains:")
    
    # Fetch all rows and display them
    for row in my_cur.fetchall():
        st.text(row)

except snowflake.connector.errors.ProgrammingError as e:
    st.error(f"Snowflake query execution error: {e.msg}")

finally:
    # Close the cursor and connection in the finally block to ensure it happens even if an exception occurs
    if my_cur:
        my_cur.close()
    if my_cnx:
        my_cnx.close()

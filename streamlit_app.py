import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

# streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 % Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt") # S3 데이터 가지고 오기
my_fruit_list = my_fruit_list.set_index('Fruit') # 과일 이름으로 선택할 수 있도록 index 설정

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
# streamlit.dataframe(my_fruit_list) # 저장된 S3 데이터를 데이터프레임으로 설정
streamlit.dataframe(fruits_to_show) # 픽스 데이터가 설정된 버전으로 변경


# create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalized(fruityvice_response.json())
  return fruityvice_normalized

# New Section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
      streamlit.error("Please select a fruit to get information.")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
      
except URLError as e:  # 에러 발생 시 스탑
    # don't run anything past here while we troubleshoot
    streamlit.stop()

streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from fruit_load_list")  # DB 데이터 가져오기
         return my_cur.fetchall()  # 전체 결과 불러오기
# Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  # DB 연결
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
         return "Thanks for adding " + new_fruit
 
add_my_fruit = streamlit.text_input('What fruit would you like to add?') # 텍스트 입력 상자

streamlit.header("View Our Fruit List-Add Your Favorites!")
if streamlit.button('Get Fruit List'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   streamlit.write(insert_row_snowflake(add_my_fruit))
   my_data_rows = get_fruit_load_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
 
# streamlit.write('Thanks for adding ', add_my_fruit)

import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('피비스 캠페인 내역 관리')

# my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
# my_cur = my_cnx.cursor()
# my_cur.execute("select * from cj.public.Cam_History")
# my_data_row = my_cur.fetchone()
# streamlit.text("캠페인 내역")
# streamlit.dataframe(my_data_row)


streamlit.header("캠페인 내역 확인하기:")
def get_Campaign_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from cj.public.Cam_History")
         return my_cur.fetchall()
if streamlit.button('캠페인 List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into cj.public.Cam_History values ('" + new_fruit + "')")
         return "Thanks for adding " + new_fruit
 
add_campaign = streamlit.text_input('캠페인명')

streamlit.header("추가된 캠페인 확인하기")
if streamlit.button('캠페인 List 확인'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   streamlit.write(insert_row_snowflake(add_campaign))
   my_data_rows = get_Campaign_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
 
# streamlit.write('Thanks for adding ', add_campaign)

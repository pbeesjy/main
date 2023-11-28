import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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
         my_cur.execute("select * from cj.public.Cam_History order by num desc")
         return my_cur.fetchall()
if streamlit.button('캠페인 List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

# Allow the end user to add a fruit to the list
def insert_row_table(new_cam):
    with my_cnx.cursor() as my_cur:
         my_cur.execute("insert into cj.public.Cam_History values (BASE_DATE)")
         return "Thanks for adding " + new_cam
 
add_1 = streamlit.text_input('의뢰 날짜')
add_2 = streamlit.text_input('회사명')
add_3 = streamlit.text_input('캠페인명')
add_4 = streamlit.text_input('CJ 견적')
add_5 = streamlit.text_input('안내 견적')
add_6 = streamlit.text_input('수익')
add_7 = streamlit.text_input('페이지수')
add_8 = streamlit.text_input('개발 구분')
add_9 = streamlit.text_input('URL')

if streamlit.button('업로드'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   streamlit.write(insert_row_table(add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9))
   my_data_rows = get_Campaign_list()
   my_cnx.close()
   streamlit.dataframe(my_data_rows)
 
# streamlit.write('Thanks for adding ', add_campaign)

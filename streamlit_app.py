import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('피비스 캠페인 내역 관리')
streamlit.text("캠페인 내역 확인하기:")
def get_Campaign_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from cj.public.Cam_History order by num desc")
         return my_cur.fetchall()
if streamlit.button('캠페인 List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


def insert_row_table(add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("""
            INSERT INTO cj.public.Cam_History 
            (BASE_DATE, COMPANY, CAM_NAME, CJ_ESTIMATE, GUIDE_ESTIMATE, PROFIT, PAGE, DEVELOPMENT, CAM_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9))
    return "Thanks for adding the campaign."


add_1 = streamlit.text_input('의뢰 날짜')
company = ['록시땅', '서양네트웍스', '컬럼비아', '신영와코루']
add_2 = streamlit.selectbox('회사 선택', company)
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

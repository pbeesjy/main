import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('피비스 캠페인 내역 관리')

streamlit.text("캠페인 내역:")

my_data_rows = []

def get_Campaign_list():
    with my_cnx.cursor() as my_cur:
         my_cur.execute("select * from cj.public.Cam_History order by num desc")
         my_data_rows  = my_cur.fetchall()
         return my_data_rows
# streamlit.button('캠페인 List'):
# streamlit.text("캠페인 List")
streamlit.expander('캠페인 List')
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

col1,col2,col3 = streamlit.columns([2,2])
company = ['록시땅', '서양네트웍스', '컬럼비아', '신영와코루']
development = ['오픈률 집계', '기본코딩', '개인화 출력', '스크레치', '설문']
with col1 :
    add_1 = streamlit.date_input('의뢰 날짜')
    add_2 = streamlit.selectbox('회사 선택', company)
add_3 = streamlit.text_input('캠페인명')
with col2 :
    add_4 = streamlit.text_input('CJ 견적')
    add_5 = streamlit.text_input('안내 견적')
with col3 :
    add_6 = streamlit.text_input('수익')
    add_7 = streamlit.text_input('페이지수')
add_8 = streamlit.selectbox('개발 선택', development)
add_9 = streamlit.text_input('URL')

if streamlit.button('업로드'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.write(insert_row_table(add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9))
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)




def update_campaign_url(campaign_name, new_url):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("""
            UPDATE cj.public.Cam_History
            SET CAM_URL = %s
            WHERE CAM_NAME = %s
        """, (new_url, campaign_name))
    my_cnx.commit()
    return f"Updated URL for {campaign_name} to {new_url}"

update_campaign_name_options = [row[3] for row in my_data_rows]
update_campaign_name = streamlit.selectbox('캠페인명 (업데이트용)', update_campaign_name_options)
new_url = streamlit.text_input('업데이트 URL')
if streamlit.button('캠페인 업데이트'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.write(update_campaign_url(update_campaign_name, new_url))
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

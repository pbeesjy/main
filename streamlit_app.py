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



company = ['록시땅', '서양네트웍스', '컬럼비아', '신영와코루']
development = ['오픈률 집계', '기본코딩', '개인화 출력', '스크레치', '설문']

add_1 = streamlit.date_input('의뢰 날짜')
add_2 = streamlit.selectbox('회사 선택', company)
add_3 = streamlit.text_input('캠페인명', key="campaign_name")
add_8 = streamlit.selectbox('개발 선택', development)
add_9 = streamlit.text_input('URL', key="url")
col1,col2 = streamlit.columns([2,2])
with col1 :
    add_4 = streamlit.text_input('CJ 견적', key="cj_estimate")
    add_5 = streamlit.text_input('안내 견적', key="guide_estimate")
with col2 :
    add_6 = streamlit.text_input('수익', key="profit")
    add_7 = streamlit.text_input('페이지수', key="page")


if streamlit.button('업로드'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.write(insert_row_table(add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9))
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)


streamlit.header('캠페인 수정')

def update_campaign(new_url, new_cj_estimate, new_guide_estimate, new_profit, new_page, new_campaign_name):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("""
            UPDATE CJ.PUBLIC.CAM_HISTORY
            SET CAM_URL = %s, CJ_ESTIMATE = %s, GUIDE_ESTIMATE = %s, PROFIT = %s, PAGE = %s, CAM_NAME = %s
            WHERE NUM = %s
        """, (new_url, new_cj_estimate, new_guide_estimate, new_profit, new_page, new_campaign_name))
    my_cnx.commit()
    return f"Updated URL for {campaign_name} to {new_url}, CJ_ESTIMATE to {new_cj_estimate}, GUIDE_ESTIMATE to {new_guide_estimate}, PROFIT to {new_profit}, PAGE to {new_page}, CAM_NAME to {new_campaign_name}"




update_campaign_name_options = [row[0] for row in my_data_rows]
update_campaign_name = streamlit.selectbox('캠페인 번호', update_campaign_name_options)
new_campaign_name = streamlit.text_input('캠페인명')
new_url = streamlit.text_input('업데이트 URL', key="update_url")
col3,col4 = streamlit.columns([2,2])
with col3 :
    new_cj_estimate = streamlit.text_input('CJ 견적', key="update_cj_estimate")
    new_guide_estimate = streamlit.text_input('안내 견적', key="update_guide_estimate")
with col4 :
    new_profit = streamlit.text_input('수익', key="update_profit")
    new_page = streamlit.text_input('페이지수', key="update_page")

if streamlit.button('캠페인 업데이트'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.write(update_campaign(new_campaign_name, new_url, new_cj_estimate, new_guide_estimate, new_profit, new_page))
    my_data_rows = get_Campaign_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

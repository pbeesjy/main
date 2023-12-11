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
         my_cur.execute("select Cam_no, Base_Date, Cam_Code from cj.public.CAM_MASTER order by cam_no desc")
         my_data_rows  = my_cur.fetchall()
         return my_data_rows
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_data_rows = get_Campaign_list()
my_cnx.close()
streamlit.dataframe(my_data_rows)

def insert_row_table(add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9):
    add_4 = add_4 if add_4 else 0
    add_5 = add_5 if add_5 else 0
    add_6 = add_6 if add_6 else 0
    add_7 = add_7 if add_7 else 0
    add_9 = add_9 if add_9 else 'aaa'
    with my_cnx.cursor() as my_cur:
        my_cur.execute("""
            INSERT INTO cj.public.CAM_MASTER 
            (BASE_DATE, COMPANY, CAM_NAME, CJ_ESTIMATE, GUIDE_ESTIMATE, PROFIT, PAGE, DEVELOPMENT, CAM_URL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (add_1, add_2, add_3, add_4, add_5, add_6, add_7, add_8, add_9))
    return "캠페인 정보가 추가되었습니다."



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

def get_campaign_data_by_no(campaign_no):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM CJ.PUBLIC.CAM_MASTER WHERE CAM_NO = %s", (campaign_no,))
        data = my_cur.fetchone()
        return {'CAM_URL': data[9], 'CJ_ESTIMATE': data[4], 'GUIDE_ESTIMATE': data[5], 'PROFIT': data[6], 'PAGE': data[7], 'CAM_NAME': data[3]}

def update_campaign(new_campaign_name, new_url, new_cj_estimate, new_guide_estimate, new_profit, new_page):

    old_data = get_campaign_data_by_no(campaign_no)

    new_url = new_url if new_url else old_data['CAM_URL']
    new_cj_estimate = new_cj_estimate if new_cj_estimate else old_data['CJ_ESTIMATE']
    new_guide_estimate = new_guide_estimate if new_guide_estimate else old_data['GUIDE_ESTIMATE']
    new_profit = new_profit if new_profit else old_data['PROFIT']
    new_page = new_page if new_page else old_data['PAGE']
    new_campaign_name = new_campaign_name if new_campaign_name else old_data['CAM_NAME']
    
    with my_cnx.cursor() as my_cur:
        my_cur.execute("""
            UPDATE CJ.PUBLIC.CAM_MASTER
            SET CAM_URL = %s, CJ_ESTIMATE = %s, GUIDE_ESTIMATE = %s, PROFIT = %s, PAGE = %s, CAM_NAME = %s, Timestamp = TO_TIMESTAMP_NTZ(CONVERT_TIMEZONE('Asia/Seoul', CURRENT_TIMESTAMP()))
            WHERE CAM_NO = %s
        """, (new_url, new_cj_estimate, new_guide_estimate, new_profit, new_page, new_campaign_name, campaign_no))
    my_cnx.commit()
    return f"{campaign_no}의 정보가 {new_url}, {new_cj_estimate}, {new_guide_estimate}, {new_profit}, {new_page}, {new_campaign_name}로 수정 되었습니다."


update_campaign_no_options = [row[0] for row in my_data_rows]
campaign_no = streamlit.selectbox('캠페인 번호', update_campaign_no_options)
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

import streamlit
import snowflake.connector

streamlit.title('피비스 캠페인 내역 관리')
streamlit.text('캠페인 내역')


my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from cj.public.Cam_History")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

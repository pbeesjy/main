import streamlit as st
import snowflake.connector as sf

st.title('피비스 캠페인 내역 관리')
st.text('캠페인 내역')


my_cnx = sf.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)

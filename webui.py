import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image

def ui_display(file_path):
    df = pd.read_csv(file_path)
    df1 = df.dropna(axis=0,how='all')
    st.set_page_config(page_title='结果')  # 网页标题
    st.title('华南师范大学校友录')  # 标题

    st.dataframe(df1)


    # --- 筛选条件
    department = df1['毕业院校'].unique().tolist()


    department_selection = st.multiselect('毕业院校:',
                                          department,
                                          default=department)


    # --- 基于条件筛选的过滤
    mask = (df1['毕业院校'].isin(department_selection))
    number_of_result = df1[mask].shape[0]
    st.markdown(f'*人数: {number_of_result}*')

    # --- 筛选后的数据
    df_grouped = df1[mask].groupby(by=['毕业院校']).count()
    df_grouped = df_grouped.rename(columns={'姓名': "人数"})
    df_grouped = df_grouped.reset_index()

    st.table(df_grouped)


ui_display('data/alumni.csv')
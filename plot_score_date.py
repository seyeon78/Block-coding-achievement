import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
import plotly.graph_objects as go
import tkinter.ttk as ttk



## 날짜별 그래프 ##
def plot_score_date(df_projectScore, user_id, score_type, title):
    # 해당 사용자의 프로젝트 데이터 가져오기
    user_data = df_projectScore[df_projectScore['userid'] == user_id]

    # 날짜와 시간을 무시하고 날짜만 추출하여 그룹화
    user_data['date'] = pd.to_datetime(user_data['date']).dt.date

    # score_type에 따라 y값 선택
    y_column = f"{score_type}Score"

    # score_type 점수를 date 별로 나타내는 산점도 그래프
    fig = px.scatter(user_data, x='date', y=y_column, title=title, height=300, width=500)

    # 각 산점도의 점을 선으로 연결하고 마커 표시
    fig.update_traces(mode='lines+markers')

    fig.update_layout(plot_bgcolor='#f5f7fa', font=dict(size=14))  # 그래프 배경색 및 글씨 크기 조절
    st.plotly_chart(fig, use_container_width=True)

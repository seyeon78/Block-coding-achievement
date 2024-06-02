import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
import plotly.graph_objects as go
import tkinter.ttk as ttk

## 학급 내 논리성, 구현성, 창의성, 적극성 1등, 꼴등 시각화 함수 ##
def plot_logi_feas_creat_poss(df, rate_column, title, max_users_label, min_users_label):
    max_score = df[rate_column].max()
    min_score = df[rate_column].min()
    max_users = df[df[rate_column] == max_score]['userid'].tolist()
    min_users = df[df[rate_column] == min_score]['userid'].tolist()

    fig = px.bar(df[df['userid'].isin(max_users + min_users)], 
                 y='userid', 
                 x=rate_column, 
                 orientation='h', 
                 title=title,
                 labels={'userid': '학생', rate_column: rate_column})
    
    rate_mean = df[rate_column].mean()
    fig.add_vline(x=rate_mean, line_dash="dot", line_color="red", 
                  annotation_text=f'평균: {rate_mean:.2f}', 
                  annotation_position="bottom right", 
                  annotation=dict(font=dict(color="black")))

    fig.update_layout(xaxis=dict(range=[0, 20]))  # x축 범위 설정
    fig.update_layout(height=250, font=dict(size=15), plot_bgcolor='#f5f7fa')  # 세로 크기 조정

    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f"<div style='font-weight: bold; background-color: #e9ecef; color: black; padding: 10px;'>우리반 {title} 1등: <span style='font-weight: bold; color: black;'>{', '.join(max_users)}</span></div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-weight: bold; background-color: #e9ecef; color: black; padding: 10px;'>우리반 {title} 꼴등: <span style='font-weight: bold; color: black;'>{', '.join(min_users)}</span></div>", unsafe_allow_html=True)

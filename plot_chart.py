import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pyparsing import empty
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
import plotly.graph_objects as go
import tkinter.ttk as ttk

## 성취도, 조회수를 이용한 그래프 함수 ##
def plot_chart(df, metric, title, user_id=None, top_bottom=False):
    df_sorted = df.sort_values(by=metric)
    
    fig = px.bar(df_sorted, x='userid', y=metric, title=title, labels={metric: '성취도 점수' if metric == 'achievementScore' else '방문 횟수'})
    fig.update_layout(height=400, width=700, font=dict(color="black", size=15), plot_bgcolor='#f5f7fa')

    avg_metric_value = df_sorted[metric].mean()
    
    fig.add_hline(y=avg_metric_value, line_dash="dash", line_color="red", annotation_text=f'<span style="color:white">평균: {avg_metric_value:.2f}</span>', annotation_position="bottom right")
    
    if user_id:
        user_score = df_sorted[df_sorted['userid'] == user_id][metric].values[0]
        user_rank = len(df_sorted[df_sorted[metric] > user_score]) + 1
        total_students = len(df_sorted)
        
        fig.update_traces(marker_color=['skyblue' if userid == user_id else '#0068C9' for userid in df_sorted['userid']], selector=dict(type='bar'))
        
        return fig, f'<div style="color:black; background-color: #e9ecef; font-weight: bold; padding: 5px;">"{user_id}" 학생의 {metric} 점수는 {user_score:.2f}점이며, {total_students}명 중 {user_rank}등입니다.</div>'
    else:
        if top_bottom:
            max_value = df_sorted[metric].max()
            min_value = df_sorted[metric].min()
            
            top_performer = df_sorted[df_sorted[metric] == max_value]['userid'].values[0]
            bottom_performer = df_sorted[df_sorted[metric] == min_value]['userid'].values[0]
            
            return fig, f"<div style='font-weight: bold; background-color: #e9ecef; padding: 10px;'>1등: {top_performer} (점수: {max_value})<br><br>꼴등: {bottom_performer} (점수: {min_value})</div>"
        else:
            return fig, None

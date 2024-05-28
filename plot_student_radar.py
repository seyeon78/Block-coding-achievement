import streamlit as st
import pandas as pd
import plotly.express as px


## 레이더 차트 함수 ##
def plot_student_radar(df_achievement, user_id):
    st.markdown(f'**1. "{user_id}" 학생의 평가지표**')
    student_data = df_achievement[df_achievement['userid'] == user_id].iloc[0][['logicalScore','feasibilityScore','creativityScore','positivenessScore']]

    # 높은 값과 낮은 값을 찾기
    highest_index = student_data.idxmax()
    lowest_index = student_data.idxmin()
    highest_value = student_data.max()
    lowest_value = student_data.min()

    # 레이더 차트 그리기
    fig_radar = px.line_polar(student_data, r=student_data.values, theta=student_data.index, line_close=True)
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],  # 범위를 0부터 100까지 설정
                tickfont=dict(color='black')
            ),
            bgcolor='#f5f7fa'  # 레이더 차트의 배경색 설정
        ),
        height=300, width=500, font=dict(size=20)  # 크기 및 텍스트 크기 조절
    )

    # 최고값과 최저값 출력
    st.markdown(
        f"<div style='background-color: #e9ecef; color: black; padding: 10px;'>"
        f"<b>가장 높은 항목: <span style='color: black;'>{highest_index} ({highest_value})</span></b><br>"
        f"<b>가장 낮은 항목: <span style='color: black;'>{lowest_index} ({lowest_value})</span></b>"
        "</div>",
        unsafe_allow_html=True
    )

    st.plotly_chart(fig_radar, use_container_width=True)

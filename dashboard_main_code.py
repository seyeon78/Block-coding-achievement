# 라이브러리 import
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pyparsing import empty
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
import tkinter.ttk as ttk

#def code import
from plot_logi_feas_creat_poss import plot_logi_feas_creat_poss
from plot_chart_achieve_view import plot_chart_achieve_view
from set_title import set_title
from plot_score_date import plot_score_date
from plot_student_radar import plot_student_radar

COLUMN = 'column'  # 실제 사용되는 상수 값을 확인하여 적절히 정의



# 데이터프레임 로드
df_achievement  = pd.read_csv('achivement_user.csv')
df_projectScore = pd.read_csv('achivement_project.csv')


# 'userid' 열의 데이터 타입을 문자열(string)로 설정
df_achievement['userid'] = df_achievement['userid'].astype(str)

# "성취도"는 "논리성", "구현성", "창의성", "적극성"의 Rate의 합을 새로운 achievementScore 칼럼에 저장
df_achievement['achievementScore'] = df_achievement.groupby('userid')[['logicalRate','feasibilityRate','creativityRate','positivenessRate']].transform('sum').sum(axis=1)
df_projectScore['achievementScore'] = df_projectScore.groupby('projectid')[['logicalScore','feasibilityScore','creativityScore']].transform('sum').sum(axis=1)

# 첫 번째 행의 groupid 값 추출
first_groupid = df_achievement.loc[0, 'groupid']


st.set_page_config(layout='wide')


# 대시보드 페이지의 공백 설정
empty1,col1,empty2 = st.columns([0.5,1.0,0.5])
empty1, col2, col3, empty2 = st.columns([0.5, 1.0, 1.0, 0.5])
empty1, col4, col5, empty2 = st.columns([0.5, 1.0, 1.0, 0.5])
empty1, col6, col7, empty2 = st.columns([0.5, 1.0, 1.0, 0.5])


empty1,col8,empty2 = st.columns([0.5,1.0,0.5])
empty1,col9,col10,empty2 = st.columns([0.25,0.5,0.5,0.25])
empty1,col11,empty2 = st.columns([0.5,1.0,0.5])
empty1,col12,col13,col14, empty2= st.columns([0.5,0.6,0.6,0.6,0.5])
empty1,col15,empty2 = st.columns([0.5,1.0,0.5])



### 각 페이지 기능 정의 ###
## 반 전체 대시보드 페이지 ##
def main_page():
    with empty1:
        empty()

    with col1: 
        set_title(f"{first_groupid}의 성취도 대시보드", is_sidebar=True)


    with col2:
        st.markdown("## 학급 전체 인원의 성취도 그래프 ##")
        fig, _ = plot_chart_achieve_view(df_achievement, 'achievementScore', "전체 성취도", top_bottom=True)
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.markdown("## 반에서 가장 조회수를 많이 받은 학생 그래프 ##")
        fig, _ = plot_chart_achieve_view(df_achievement, 'visit', "우리반 조회수 1등")
        st.plotly_chart(fig, use_container_width=True)

    with col4:  # 학급 내 논리성 점수 시각화
        plot_logi_feas_creat_poss(df_achievement, 'logicalRate', '논리성', 'logicalRate', 'logicalRate')
        
    with col5:  # 학급 내 구현성 점수 시각화
        plot_logi_feas_creat_poss(df_achievement, 'feasibilityRate', '구현성', 'feasibilityRate', 'feasibilityRate')
        
    with col6: # 학급 내 창의성 점수 시각화
        plot_logi_feas_creat_poss(df_achievement, 'creativityRate', '창의성', 'creativityRate', 'creativityRate')
        
    with col7:  # 학급 내 적극성 점수 시각화
        plot_logi_feas_creat_poss(df_achievement, 'positivenessRate', '적극성', 'positivenessRate', 'positivenessRate')

    with empty2:
        empty() 

        

# 각 사용자 페이지 생성 함수 정의
def create_user_page(user_id):
    def user_page():
        with empty1:
            st.empty() 

        with col8:
            set_title(f"{user_id}의 세부 평가지표 대시보드")
                   
        with col9:  # 학생 점수 레이더 차트 시각화
            plot_student_radar(df_achievement, user_id)
    
        with col10:  # 학생 성취도 점수, 등수 시각화
            st.markdown(f'**2. "{user_id}" 학생의 등수**')
            fig, result_text = plot_chart_achieve_view(df_achievement, 'achievementScore', "반 전체 성취도 점수", user_id=user_id)
            st.plotly_chart(fig, use_container_width=True)
            if result_text:
                st.markdown(result_text, unsafe_allow_html=True)

          
        with col11:
            st.markdown(f'**3. "{user_id}" 학생의 날짜 별 평가지표 점수 추이**')
        
        with col12:
            # logicalScore 점수를 date 별로 나타내는 산점도 그래프
            plot_score_date(df_projectScore, user_id, 'logical', f"{user_id}의 논리성 점수 추이")

   
        with col13:
            # feasibilityScore 점수를 date 별로 나타내는 산점도 그래프
            plot_score_date(df_projectScore, user_id, 'feasibility', f"{user_id}의 구현성 점수 추이")


        with col14:
            # creativityScore 점수를 date 별로 나타내는 산점도 그래프
            plot_score_date(df_projectScore, user_id, 'creativity', f"{user_id}의 창의성 점수 추이")

        with empty2:
            empty()

    return user_page




# 페이지 이름을 사용자 ID로 매핑하는 딕셔너리 생성
user_pages = {user_id: create_user_page(user_id) for user_id in df_achievement['userid'].unique()}

# 사용자 ID 리스트 생성
user_ids = list(user_pages.keys())

# 기본 페이지와 사용자 페이지들을 합쳐서 페이지 선택 박스에 표시할 모든 페이지 목록 생성
page_names = {'학급 페이지': main_page, **{f'{user_id}의 성취도 페이지': user_pages[user_id] for user_id in user_ids}}

# 페이지 선택 박스 생성
selected_page = st.sidebar.selectbox('학생 페이지 선택하기', list(page_names.keys()))

# 선택된 페이지 함수 실행
page_names[selected_page]()

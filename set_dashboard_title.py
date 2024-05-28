import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import seaborn as sns
import plotly.graph_objects as go
import tkinter.ttk as ttk

## 제목과 사이드바 함수 ##
def set_dashboard_title(title, is_sidebar=False):
    header_html = f"<h{'3' if is_sidebar else '2'} style='text-align: center; color: black; background-color: #e9ecef; padding: 10px;'>{title}</h{'3' if is_sidebar else '2'}>"
    st.markdown(header_html, unsafe_allow_html=True)
    if is_sidebar:
        st.sidebar.title(title)
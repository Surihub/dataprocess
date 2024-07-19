import streamlit as st
import os
import importlib.util

# 페이지 디렉토리 설정
pages_dir = 'pages'
pages = [f.replace('.py', '') for f in os.listdir(pages_dir) if f.endswith('.py')]

# 앱 제목과 소개글
st.title("데이터 기반 현장연구를 위한 앱")
st.warning("""
이 앱은 데이터 기반 현장 연구를 위한 다양한 도구와 리소스를 제공합니다.
사이드바의 페이지를 클릭하여 각 페이지로 이동할 수 있습니다.
""")

# 목차 생성 및 페이지 링크
for page in pages:
    st.markdown(f"### {page[3:]}")

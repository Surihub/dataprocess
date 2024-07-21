import streamlit as st
import os
import importlib.util

# 페이지 디렉토리 설정
pages_dir = 'pages'
pages = [f.replace('.py', '') for f in os.listdir(pages_dir) if f.endswith('.py')]

# 앱 제목과 소개글
st.title("📊 학교에서 데이터 활용하기")
st.warning("""
이 앱은 데이터 기반 현장 연구를 위한 다양한 도구와 리소스를 제공합니다.
사이드바의 페이지를 클릭하여 각 페이지로 이동할 수 있습니다.
           \n**made by 황수빈**
           [👩🏻‍💻github](https://github.com/Surihub), 📧 sbhath17@gmail.com
           """, icon="🚀")

# 목차 생성 및 페이지 링크
st.subheader("페이지 바로가기")
for page in pages:
    page_url = page.replace(" ", "_")
    st.link_button(f"{page[1:]}", page_url[1:])

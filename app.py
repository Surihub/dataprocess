import streamlit as st
import pandas as pd
import random
import string
from faker import Faker

fake = Faker()

def generate_random_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def pseudonymize_value():
    return fake.first_name() + " " + fake.last_name()

def custom_id_generator(base_string, index):
    return f"{base_string}{index}"

def pseudonymize_columns(df, columns, method, custom_id_base=None):
    if method == "영문 숫자 혼용된 문자열":
        for column in columns:
            df[column] = df[column].apply(lambda x: generate_random_string())
    elif method == "커스텀 ID":
        if custom_id_base is None:
            custom_id_base = "id"
        for column in columns:
            df[column] = [custom_id_generator(custom_id_base, i) for i in range(1, len(df) + 1)]
    elif method == "랜덤 이름":
        for column in columns:
            df[column] = df[column].apply(lambda x: pseudonymize_value())
    return df

def main():
    st.title("CSV 열 익명 처리")

    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv", "xlsx"])
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file, encoding='euc-kr')
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file)
        st.write("원본 데이터:")
        st.write(df)

        columns_to_pseudonymize = st.multiselect(
            "익명 처리할 열 선택", df.columns)

        method = st.selectbox(
            "익명 처리 방법 선택",
            ("영문 숫자 혼용된 문자열", "커스텀 ID", "랜덤 이름")
        )

        custom_id_base = None
        if method == "커스텀 ID":
            custom_id_base = st.text_input("ID 기본 문자열 입력", value="id")

        if st.button("익명 처리"):
            if columns_to_pseudonymize:
                df_pseudonymized = pseudonymize_columns(df, columns_to_pseudonymize, method, custom_id_base)
                st.write("익명 처리된 데이터:")
                st.write(df_pseudonymized)
                
                csv = df_pseudonymized.to_csv(index=False).encode('euc-kr')
                st.download_button(
                    "익명 처리된 CSV 다운로드",
                    data=csv,
                    file_name="pseudonymized_data.csv",
                    mime='text/csv',
                )
            else:
                st.warning("익명 처리할 열을 하나 이상 선택하세요.")

if __name__ == "__main__":
    main()

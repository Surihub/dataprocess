import streamlit as st
import pandas as pd
import random
import string
from faker import Faker

fake = Faker()

def generate_random_name():
    return fake.name()

def generate_random_string(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

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
            df[column] = df[column].apply(lambda x: generate_random_name())
    return df

def main():
    st.title("📇 데이터 익명 처리 앱")
    st.info("개인정보가 포함된 데이터를 여러 옵션으로 익명화할 수 있습니다. \n데이터(csv 파일)를 업로드 한 후 옵션을 설정하여 익명처리 합니다. 올바르게 익명처리가 되었다면 다운로드 받기 버튼을 클릭해주세요. 업로드된 데이터는 별도의 서버에 저장되지 않습니다. ", icon = "👩🏻‍💻")
    uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv", "xlsx"])
    if uploaded_file is not None:
        encoding_options = ['utf-8', 'euc-kr', 'latin-1']
        encoding = st.radio("인코딩 오류가 날 경우, 다른 옵션으로 선택해보세요!", encoding_options, index=0)
        if uploaded_file.name.endswith('.csv'):
            try:
                df = pd.read_csv(uploaded_file, encoding=encoding)
            except UnicodeDecodeError:
                st.error(f"파일을 읽는 도중 인코딩 에러가 발생했습니다. 선택한 인코딩({encoding})이 맞는지 확인해주세요.")
                return
        elif uploaded_file.name.endswith('.xlsx'):
            df = pd.read_excel(uploaded_file, error_bad_lines=False)
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
                
                csv = df_pseudonymized.to_csv(index=False).encode('utf-8')
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
else:
    st.warning("익명 처리할 열을 하나 이상 선택하세요.")


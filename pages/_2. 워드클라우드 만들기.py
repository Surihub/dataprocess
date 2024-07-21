import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
from kiwipiepy import Kiwi

# 형태소 분석기 초기화
kiwi = Kiwi()

# 한글 컬러맵과 실제 컬러맵 이름 매칭
colormap_dict = {
    "녹색": "viridis",
    "다채로운": "plasma",
    "불꽃색": "inferno",
    "용암색": "magma",
    "황색": "cividis",
    "파란색": "Blues",
    "초록색": "Greens",
    "빨간색": "Reds",
    "보라색": "Purples"
}

def extract_nouns(text):
    tokens = kiwi.analyze(text)
    nouns = [word.form for sentence in tokens for word in sentence[0] if word.tag.startswith('NN')]
    return ' '.join(nouns)

def generate_wordcloud(text, colormap, width, height, margin):
    font_path = './NanumSquareNeo.ttf'  # 폰트 파일이 있는 경로
    wordcloud = WordCloud(font_path=font_path, background_color='white', colormap=colormap, width=width, height=height, margin=margin).generate(text)
    plt.figure(figsize=(15, 15))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

def main():
    st.title("☁️ 워드클라우드 생성 앱")
    st.info("아래에 텍스트를 입력하면 워드클라우드가 생성됩니다.", icon = "👩🏻‍💻")

    text = st.text_area("워드클라우드에 사용할 텍스트를 여기에 입력하세요.")
    
    colormap_kor = st.selectbox(
        "컬러맵 선택",
        ["다채로운(플라즈마)", "불꽃(인페르노)", "용암(마그마)", "황색(시비디스)", "파란색", "초록색", "빨간색", "보라색"]
    )

    colormap = colormap_dict[colormap_kor]

    width = 1000
    height = 1000
    margin = 1

    if st.button("워드클라우드 생성"):
        if text:
            try:
                # 원본 텍스트로 워드클라우드 생성
                buf_original = generate_wordcloud(text, colormap, width, height, margin)
                
                # 형태소 분석으로 명사 추출 후 워드클라우드 생성
                nouns_text = extract_nouns(text)
                buf_nouns = generate_wordcloud(nouns_text, colormap, width, height, margin)
                
                # 워드클라우드 두 가지 버전 병렬로 표시
                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("원본 텍스트")
                    st.image(buf_original, use_column_width=True)
                    st.download_button(
                        label="PNG로 다운받기",
                        data=buf_original,
                        file_name="wordcloud_original.png",
                        mime="image/png"
                    )

                with col2:
                    st.subheader("명사만 추출")
                    st.image(buf_nouns, use_column_width=True)
                    st.download_button(
                        label="PNG로 다운받기",
                        data=buf_nouns,
                        file_name="wordcloud_nouns.png",
                        mime="image/png"
                    )

            except OSError:
                st.error("OS 오류가 발생했습니다. NanumSquareNeo.ttf 폰트 파일이 있는지 확인하세요.")
        else:
            st.warning("텍스트를 입력하세요.")

if __name__ == "__main__":
    main()
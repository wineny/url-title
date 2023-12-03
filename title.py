import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup

def extract_title(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        if soup.title:
            # 제목에서 " | GPTers 그룹" 부분을 제거
            title = soup.title.text.strip()
            return title.rsplit(' | GPTers 그룹', 1)[0]
        else:
            return 'No title found'
    except Exception as e:
        return f'Error: {e}'

def process_file(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'URL' in df.columns:
            with st.spinner('제목을 추출 중입니다. 잠시만 기다려주세요...'):
                df['Title'] = df['URL'].apply(extract_title)
            return df
        else:
            st.error('CSV 파일에 URL 열이 없습니다.')
            return None

def main():
    st.title("URL로 제목 추출하기🌎")
    st.caption("url을 csv 파일로 저장하면 한 번에 제목을 뽑아줍니다.")

    with st.sidebar:
        st.header("만든 사람")
        st.markdown("😄 지피터스 커뮤니티 리더 윤누리")
        st.markdown("📗 누리의 브런치 : [링크](https://brunch.co.kr/@wine-ny)")

    uploaded_file = st.file_uploader("CSV 파일을 첨부하세요. 가장 위 헤더는 'URL'이어야 합니다.", type="csv")
    if uploaded_file is not None:
        df_processed = process_file(uploaded_file)
        if df_processed is not None:
            for _, row in df_processed.iterrows():
                st.markdown(f"[{row['Title']}]({row['URL']})")

# main 함수 호출
if __name__ == "__main__":
    main()

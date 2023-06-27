import streamlit as st
from functions import ask_chatgpt

st.title('あなたへのおすすめ')
st.write('作品を入力するとそれに基づいた他作品の紹介を行います')

with st.form(key='recommend_form'):
    # テキストボックス
    work1 = st.text_input('好きな作品1', key='work1')
    work2 = st.text_input('好きな作品2', key='work2')
    work3 = st.text_input('好きな作品3', key='work3')

    # ボタン
    submit_btn = st.form_submit_button('送信')

    if submit_btn:
        works = [work1, work2, work3]
        for i, work in enumerate(works):
            st.text(f'あなたの好きな作品{i+1}：『{work}』')
        
        recommendation = ask_chatgpt(works)
        for i, work in enumerate(recommendation):
            st.text(f'あなたにおすすめの作品{i+1}：『{work}』')
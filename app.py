import streamlit as st
from functions import make_question, ask_chatgpt, answer_to_list
import os
from dotenv import load_dotenv
load_dotenv('.env') 
PASSWORD = os.environ.get("PASSWORD")

# タイトル及び説明文
st.title('あなたへのおすすめ')
st.write('作品を入力するとそれに基づいた他作品の紹介を行います')

# テキストボックスでパスワード入力を求める(簡易的なログイン)
password = st.text_input('パスワードを入力してください')

# セレクトボックスでジャンルを決める
genre = st.selectbox(
    'ジャンル',
    ['アニメ', '漫画', '小説', '映画', 'ドラマ']
)

# スライダーで入力する作品の個数を決める
num_fav_works = st.slider('入力したい作品の数を選んでください', 3, 10, 3)

with st.form(key='recommend_form'):
    # テキストボックスでユーザーに好きな作品の入力を求める
    favorite_works = []
    st.write(f'あなたの好きな{genre}を入力してください')
    for i in range(num_fav_works):
        favorite_works.append(st.text_input(f'好きな{genre} {i+1}個目', key=f'work{i+1}'))

    # 送信ボタン
    submit_btn = st.form_submit_button('送信')

    # ボタンが押された際の処理
    if submit_btn and password == PASSWORD:
        st.write('あなたの入力内容')
        st.text(f'あなたが選んだジャンル：{genre}')
        for i, work in enumerate(favorite_works):
            st.text(f'あなたの好きな{genre} {i+1}個目：『{work}』')
        st.write('\n')
        
        # 入力した値からGPTに投げる質問を作る
        question = make_question(genre, favorite_works)
        # デバッグ用
        st.write('ChatGPTに投げた質問')
        st.write(question)
        
        # 得た答えを扱いやすいように加工する
        answer = ask_chatgpt(question)
        similarities, recommend_works = answer_to_list(answer)
        
        st.write(f'あなたが好きな{genre}の共通点')
        for i, similarity in enumerate(similarities):
            st.text(f'共通点{i+1}')
            st.text(similarity)
            
        st.write('あなたへのおすすめ')
        for i, work in enumerate(recommend_works):
            st.text(f'あなたにおすすめの{genre}{i+1}：{work[0]}')
            st.text(f'おすすめの理由\n{work[1]}')
    
    elif submit_btn and password != PASSWORD:
        st.text('パスワードが違います')
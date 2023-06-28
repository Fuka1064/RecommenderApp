import streamlit as st
from functions import make_question, ask_chatgpt, answer_to_list

st.title('あなたへのおすすめ')
st.write('作品を入力するとそれに基づいた他作品の紹介を行います')

num_fav_works = st.slider('入力したい作品の数を選んでください', 3, 10, 3)

with st.form(key='recommend_form'):
    # テキストボックス
    favorite_works = []
    st.write('好きな作品を入力してください')
    for i in range(num_fav_works):
        favorite_works.append(st.text_input(f'好きな作品{i+1}', key=f'work{i+1}'))

    # ボタン
    submit_btn = st.form_submit_button('送信')

    if submit_btn:
        st.write('あなたの入力内容')
        for i, work in enumerate(favorite_works):
            st.text(f'あなたの好きな作品{i+1}：『{work}』')
        st.write('\n')
        
        # 入力した値からGPTに投げる質問を作る
        question = make_question(favorite_works)
        
        # 得た答えを扱いやすいように加工する
        answer = ask_chatgpt(question)
        similarities, recommend_works = answer_to_list(answer)
        
        st.write('あなたが好きな作品の共通点')
        for i, similarity in enumerate(similarities):
            st.text(f'共通点{i+1}')
            st.text(similarity)
            
        st.write('あなたへのおすすめ')
        for i, work in enumerate(recommend_works):
            st.text(f'あなたにおすすめの作品{i+1}：{work[0]}')
            st.text(f'おすすめの理由\n{work[1]}')
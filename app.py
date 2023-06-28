import streamlit as st
from functions import make_question, ask_chatgpt, answer_to_list
import os
from dotenv import load_dotenv
load_dotenv('.env') 
PASSWORD = os.environ.get("PASSWORD")

# タイトル及び説明文
st.title('あなたへのおすすめ')
st.write('\n\n')
st.markdown('#### 0. 使い方')
st.write('まずはジャンルを選択し、そのジャンルであなたが好きな作品をいくつか入力してください。')
st.write('AIがそれらの共通点を考えたうえで他の作品を紹介してくれます。')
st.write('ただし、入力によってはエラーになってしまったり、存在しない作品をおすすめされてしまったりすることがあります。')
st.write('上記にご了承のうえでの使用をお願いします。')
st.write('\n\n')

# テキストボックスでパスワード入力を求める(簡易的なログイン)
st.markdown('#### 1. パスワードを入力して下さい')
password = st.text_input('パスワード：')
if password == PASSWORD:
    st.text('認証に成功しました')
elif password != '' and password != PASSWORD:
    st.text('パスワードが違います')
st.write('\n\n')

# セレクトボックスでジャンルを決める
st.markdown('#### 2. ジャンルと入力する作品数を決めてください')
genre = st.selectbox(
    'ジャンル',
    ['アニメ', '漫画', '小説', '映画', 'ドラマ']
)

# スライダーで入力する作品の個数を決める
num_fav_works = st.slider('入力したい作品の数を選んでください (最小で3個, 最大で10個)', 3, 10, 3)

st.markdown(f'#### 3. あなたの好きな{genre}を入力してください')
with st.form(key='recommend_form'):
    # テキストボックスでユーザーに好きな作品の入力を求める
    favorite_works = []
    
    for i in range(num_fav_works):
        favorite_works.append(st.text_input(f'好きな{genre} {i+1}個目', key=f'work{i+1}'))

    # 送信ボタン
    submit_btn = st.form_submit_button('送信')
    st.write('\n\n')

    # ボタンが押された際の処理
    if submit_btn and password == PASSWORD and '' not in favorite_works:
        st.markdown('### あなたの入力内容')
        st.write(f'選んだジャンル：{genre}')
        for i, work in enumerate(favorite_works):
            st.write(f'好きな{genre} {i+1}個目：『{work}』')
        st.write('\n\n')
        
        # 入力した値からGPTに投げる質問を作る
        question = make_question(genre, favorite_works)
        
        # 得た答えを扱いやすいように加工する
        answer = ask_chatgpt(question)
        similarities, recommend_works = answer_to_list(genre, answer)
        
        st.markdown(f'### あなたが好きな{genre}の共通点')
        st.write('\n')
        for i, similarity in enumerate(similarities):
            st.markdown(f'##### 共通点{i+1}')
            st.write(similarity)
            st.write('\n')
        st.write('\n')
            
        st.write('### あなたへのおすすめ')
        st.write('\n')
        for i, work in enumerate(recommend_works):
            st.markdown(f'##### おすすめの{genre}{i+1}：{work[0]}')
            st.write(f'おすすめの理由：\n{work[1]}')
            st.write('\n')
    
    elif submit_btn and password != PASSWORD:
        st.text('パスワードが違います')
        
    elif submit_btn and '' in favorite_works:
        st.text(f'好きな{genre}入力欄はすべて埋めてください')
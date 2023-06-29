import streamlit as st
import openai

openai.api_key = st.secrets["API_KEY"]

genre_to_eng = {'アニメ':'anime', 
                '漫画':'comic', 
                '小説':'novel', 
                '映画':'movie', 
                'ドラマ':'drama', }

def make_question(genre, works, num_recommend_works):
    # 受け取った作品リストをもとに質問を作る
    question = f"Here are the titles of the {genre_to_eng[genre]} I like:\n"
    for work in works:
        question += f"  『{work}』\n"
    question += f"\nPlease point out the characteristics common to the {genre_to_eng[genre]}s listed above. Also, please recommend similar {genre_to_eng[genre]}s that exhibit similar characteristics. As a reminder, please be sure to introduce actual {genre_to_eng[genre]}s, even if they are difficult to guess.\n"
    question += "Please answer in Japanese according to the following format:\n\n"
    question += "【共通点】\n   (1) 共通点1\n   (2) 共通点2\n   (3) 共通点3\n\n"
    question += f"【おすすめの{genre}】\n"
    for i in range(num_recommend_works):
        question += f"   ({i+1}) 「タイトル」\n       おすすめの理由\n"

    return question

def ask_chatgpt(question):
    # 引数として受け取った質問をChatGPTに投げてその返答を返す

    answer = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": question
            },
        ],
    )
    
    # デバッグ用
    # print(answer)
    # print(answer["choices"][0]["message"]["content"])

    return answer["choices"][0]["message"]["content"]

def answer_to_list(genre, answer):
    # 空のリストを初期化
    similarities = []
    recommend_works = []

    # テキストを行に分割する
    lines = answer.split('\n')
    lines = [i for i in lines if i != '']

    # 共通点とおすすめの作品のセクションの開始と終了のインデックスを見つける
    start_index_similarities = lines.index("【共通点】") + 1
    end_index_similarities = lines.index(f"【おすすめの{genre}】")
    start_index_recommend = lines.index(f"【おすすめの{genre}】") + 1

    # 共通点を抽出する
    for i in range(start_index_similarities, end_index_similarities):
        similarity = lines[i].split(') ')[1]
        similarities.append(similarity)

    # おすすめの作品を抽出する
    for i in range(start_index_recommend, len(lines)-1, 2):
        recommend_work = [lines[i].strip(), lines[i+1].strip()]
        if ') ' in recommend_work[0]:
            recommend_work[0] = recommend_work[0].split(') ')[1]
        
        if 'おすすめの理由' in recommend_work[1]:
            recommend_work[1] = recommend_work[1].split('おすすめの理由')[1][1:]
            
        recommend_works.append(recommend_work)

    return similarities, recommend_works
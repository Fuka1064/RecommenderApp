import os
from dotenv import load_dotenv
load_dotenv('.env') 
API_KEY = os.environ.get("API_KEY")

genre_to_eng = {'アニメ':'anime', 
                '漫画':'comic', 
                '小説':'novel', 
                '映画':'movie', 
                'ドラマ':'drama', }

def make_question(genre, works):
    # 受け取った作品リストをもとに質問を作る
    question = f"Here are the titles of the {genre_to_eng[genre]} I like:\n"
    for work in works:
        question += f"  『{work}』\n"
    question += f"\nPlease point out the characteristics common to the {genre_to_eng[genre]}s listed above. Also, please recommend similar {genre_to_eng[genre]}s that exhibit similar characteristics. As a reminder, please be sure to introduce actual {genre_to_eng[genre]}s, even if they are difficult to guess.\n"
    question += "Please answer in Japanese according to the following format:\n\n"
    question += "【共通点】\n   (1) 共通点1\n   (2) 共通点2\n   (3) 共通点3\n\n"
    question += f"【おすすめの{genre}】\n"
    for i in range(3):
        question += f"   ({i+1}) 「タイトル」\n       おすすめの理由\n"

    return question

def ask_chatgpt(question):
    # 引数として受け取った質問をChatGPTに投げてその返答を返す
    answer = """【共通点】
(1) シュール: 奇妙な場所や出来事が描かれたりします。

(2) 異世界的: 現実とは異なる異世界的な要素を含んでいます。

(3) 対比: 過酷な状況や困難な試練に直面することもあります。

【おすすめのアニメ】
(1) 『ブラック』
おすすめの理由: 医療の現場でのドラマや人間模様が描かれています。

(2) 『少女革命』
おすすめの理由: 哲学的なストーリーが特徴です。

(3) 『ハウル』
おすすめの理由: スタジオジブリの作品である。"""

    return answer

def answer_to_list(answer):
    # 空のリストを初期化
    similarities = []
    recommend_works = []

    # テキストを行に分割する
    lines = answer.split('\n')
    lines = [i for i in lines if i != '']

    # 共通点とおすすめのアニメのセクションの開始と終了のインデックスを見つける
    start_index_similarities = lines.index("【共通点】") + 1
    end_index_similarities = lines.index("【おすすめのアニメ】")
    start_index_recommend = lines.index("【おすすめのアニメ】") + 1

    # 共通点を抽出する
    for i in range(start_index_similarities, end_index_similarities):
        similarity = lines[i].split(') ')[1]
        similarities.append(similarity)

    # おすすめのアニメを抽出する
    for i in range(start_index_recommend, len(lines)-1, 2):
        recommend_work = [lines[i].strip(), lines[i+1].strip()]
        recommend_work[0] = recommend_work[0].split(') ')[1]
        recommend_work[1] = recommend_work[1].split('おすすめの理由: ')[1]
        recommend_works.append(recommend_work)

    return similarities, recommend_works
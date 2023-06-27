def make_prompt(works):
    text = f"""Here are the titles of the works I like:
        "{works[0]}"\n
        "{works[1]}"\n
        "{works[2]}"\n
        Could you point out any shared characteristics among these pieces and recommend similar works that exhibit those qualities? Even if it's difficult, I would appreciate your input.\n
        Please answer in Japanese according to the following format:\n
        【共通点】
        (1) 共通点その1\n
        (2) 共通点その2\n
        (3) 共通点その3\n
        【おすすめのアニメ】\n
        1. 「タイトル」
        おすすめの理由\n
        2. 「タイトル」
        おすすめの理由\n
        3. 「タイトル」
        おすすめの理由\n
    """
    return text

def ask_chatgpt(text):
    # ここで作品の処理やおすすめの計算を行う
    recommendations = [] 
    return recommendations
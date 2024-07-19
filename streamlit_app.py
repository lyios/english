import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st

# セッション状態の初期化
if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False  # デフォルト値で初期化

st.set_page_config(page_title="英検準二級英単語ガチャ")

def quest():
    st.title('クエストへようこそ!')
    st.write("あなたは岐路に立っている。どの道を選ぶのか？")
    option = st.radio(
        "道を選ぶ:",
        ("左へ", "右へ")
    )

    if option == "左へ":
        st.write("親切な商人に出会う.")
        action = st.selectbox(
            "どうする?",
            ("何かを買う", "無視して続ける")
        )
        if action == "何かを買う":
            st.write("魔法の剣を買った!")
        else:
            st.write("あなたは旅を続ける")

    elif option == "右へ":
        st.write("宝箱を見つける")
        action = st.selectbox(
            "どうする?",
            ("チェストを開ける", "そのままにする")
        )
        if action == "チェストを開ける":
            st.write("あなたは隠された都市への地図を見つけた!")
        else:
            st.write("そのままにしておく.")
def main():
    st.header("Quest Maker App")
    st.subheader("Create your own interactive quest!")
    quest()

if st.session_state.get('quest_completed', False):
    st.title('英検準二級英単語ガチャ')

    def draw_gacha():
        st.write('英単語をランダムに表示して、勉強をサポートします！')
        st.write('がんばってください！')

    # Load the data
    @st.cache
    def load_data():
        return pd.read_excel("a.xlsx")

    words_df = load_data()

    # ガチャ機能
    if st.button('ガチャを引く！'):
        rarity_probs = {
            'N': 0.4,
            'R': 0.3,
            'SR': 0.2,
            'SSR': 0.1
        }
        chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
        subset_df = words_df[words_df['レア度'] == chosen_rarity]
        selected_word = subset_df.sample().iloc[0]
    
        # セッションステートに選択された単語を保存
        st.session_state.selected_word = selected_word
        st.session_state.display_meaning = False

    if 'selected_word' in st.session_state:
        st.header(f"単語名: {st.session_state.selected_word['単語']}")
        st.subheader(f"レア度: {st.session_state.selected_word['レア度']}")
   
        # 意味を確認するボタンを追加
        if st.button('意味を確認する'):
            st.session_state.display_meaning = True

        if st.session_state.display_meaning:
            st.write(f"日本語訳: {st.session_state.selected_word['日本語訳']}")

            if st.button('英文を見る'):
                st.session_state.display_meaning = 'english'

        if st.session_state.display_meaning == 'english':
            if '英文' in st.session_state.selected_word:
                st.write(f"英文: {st.session_state.selected_word['英文']}")
            else:
                st.write("英文がありません")

            if st.button('日本文を見る'):
                st.session_state.display_meaning = 'japanese'

        if st.session_state.display_meaning == 'japanese':
            if '日本文' in st.session_state.selected_word:
                st.write(f"日本文: {st.session_state.selected_word['日本文']}")
            else:
                st.write("日本文がありません")

if __name__ == "__main__":
    main()

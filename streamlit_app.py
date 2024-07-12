import streamlit as st
import pandas as pd
import numpy as np
import streamlit as st

# セッション状態の初期化
if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False  # デフォルト値で初期化

st.set_page_config(page_title="英検準二級英単語ガチャ")

# タイトルと説明
st.title('英検準二級英単語ガチャ')

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

    if st.button('例文を見る'):
        st.session_state.display_meaning = True

    st.write("以下が例文です:")
    for index, row in df.iterrows():
        st.write(row['例文'])
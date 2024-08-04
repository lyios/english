import streamlit as st
import pandas as pd
import numpy as np
import time

# セッション状態の初期化
if 'current_word' not in st.session_state:
    st.session_state.current_word = None

if 'correct_pos' not in st.session_state:
    st.session_state.correct_pos = None
    
if 'quest_completed' not in st.session_state:
    st.session_state.quest_completed = False

if 'selected_word' not in st.session_state:
    st.session_state.selected_word = None

if 'display_meaning' not in st.session_state:
    st.session_state.display_meaning = False

if 'question_displayed' not in st.session_state:
    st.session_state.question_displayed = False


st.set_page_config(page_title="品詞クイズと英単語ガチャ")

def load_data(file_path):
    return pd.read_excel(file_path)


def draw_gacha():
        st.write('英単語をランダムに表示して、勉強をサポートします！')
        st.write('がんばってください！')

    # Load the data
        @st.cache
        def load_data():
            return pd.read_excel("a.xlsx")

        words_df = load_data()

        subset_df = pd.DataFrame() 

    # ガチャ機能
        if st.button('ガチャを引く！'):
            if st.session_state.selected_word is None:
                st.warning("品詞クイズに正解するまでガチャは引けません。")
                return
            
            rarity_probs = {
                'N': 0.4,
                'R': 0.3,
                'SR': 0.2,
                'SSR': 0.1
            }
            chosen_rarity = np.random.choice(list(rarity_probs.keys()), p=list(rarity_probs.values()))
            subset_df = words_df[words_df['レア度'] == chosen_rarity]
    
        # セッションステートに選択された単語を保存
        
            selected_word = subset_df.sample().iloc[0]
            st.session_state.selected_word = selected_word
            st.session_state.display_meaning = False
        
        if st.session_state.gacha_word is not None:
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

def load_data(file_path):
    return pd.read_excel(file_path)

def get_random_word(df):
    # ランダムに単語を選ぶ
    row = df.sample(n=1).iloc[0]
    word = row['単語']
    pos = row['品詞']
    return word, pos

def question():
    st.title('品詞クイズ')
    st.write("この単語の品詞は何でしょう？")

    # Load the data
    @st.cache
    def word_data():
        return pd.read_excel("ブック.xlsx")
    
    file_path ='ブック.xlsx'
    word_data = pd.read_excel(file_path)

    word, correct_pos = get_random_word(word_data)

    if st.session_state.current_word is None:
        st.session_state.current_word, st.session_state.correct_pos = get_random_word(word_data)


    st.write(f"単語: {word}")

    with st.spinner('少々お待ちください...'):
        time.sleep(5)  # 5秒待機


    all_pos = ['動詞', '形容詞', '副詞']
    options = list(set(all_pos) - {correct_pos})
    options.append(correct_pos)
    np.random.shuffle(options)  # 選択肢をシャッフル

    user_answer = st.radio(
        "この単語の品詞は？",
        options=options,
        key="quiz_radio"
    )

    # 回答のチェックとフィードバックを表示
    if st.button("決定"):
        if user_answer == correct_pos:
            st.success("正解です！")
            st.session_state.quest_completed = True
            st.session_state.selected_word = {'単語': word, '品詞': correct_pos}
            draw_gacha()
        
        else:
            st.error(f"不正解です。正解は「{correct_pos}」です。")

        if st.button("次の問題"):
            st.session_state.current_word = None
            st.session_state.correct_pos = None
            st.session_state.question_displayed = False



def main():
        st.header("品詞クイズに正解すると、英単語ガチャを引けます。")
        question()

if __name__ == "__main__":
        main()        


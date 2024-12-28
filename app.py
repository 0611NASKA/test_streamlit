import streamlit as st

# アプリのタイトル
st.title("My First Streamlit App")

# テキスト入力
user_input = st.text_input("名前を入力してください:")

# 結果を表示
if user_input:
    st.write(f"こんにちは、{user_input}さん！")
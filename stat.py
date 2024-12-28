import os
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import matplotlib.font_manager as fm

# .env ファイルを読み込む
load_dotenv()

api_url = os.getenv("API_URL")
font_path = os.getenv("FONT_PATH")

# 日本語フォントを設定
font_path = font_path
font_prop = fm.FontProperties(fname=font_path)
rcParams['font.family'] = font_prop.get_name()
rcParams['axes.unicode_minus'] = False

# アプリタイトル
st.title("統計データ可視化アプリ")
st.write("外部統計データベースからデータを取得して可視化します。")

# API URL のベース
BASE_URL = api_url

# 利用可能な指標コードのリスト（例: 世界銀行の主要指標）
INDICATORS = {
    "名目GDP (米ドル)": "NY.GDP.MKTP.CD",
    "人口 (総数)": "SP.POP.TOTL",
    "CO2排出量 (トン)": "EN.ATM.CO2E.KT",
    "平均寿命 (年)": "SP.DYN.LE00.IN",
    "失業率 (%)": "SL.UEM.TOTL.ZS",
}

# ユーザーから取得するパラメータ
st.sidebar.header("検索条件")
indicator_label = st.sidebar.selectbox("指標を選択してください", list(INDICATORS.keys()))
indicator = INDICATORS[indicator_label]
country = st.sidebar.text_input("国コードを入力してください (例: JP, US, CN)", value="JP")
start_year = st.sidebar.number_input("開始年", min_value=1960, max_value=2023, value=2000)
end_year = st.sidebar.number_input("終了年", min_value=1960, max_value=2023, value=2020)

# データ取得関数
def fetch_data(indicator, country, start_year, end_year):
    url = f"{BASE_URL}/country/{country}/indicator/{indicator}?date={start_year}:{end_year}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 1:
            return pd.DataFrame(data[1])
    return None

# API データの取得と表示
if st.sidebar.button("データ取得"):
    data = fetch_data(indicator, country, start_year, end_year)
    
    if data is not None and not data.empty:
        # 必要な列を抽出
        data_filtered = data[["date", "value"]].dropna()
        data_filtered["date"] = data_filtered["date"].astype(int)
        data_filtered = data_filtered.sort_values(by="date")

        st.write("### 統計データ")
        st.dataframe(data_filtered)

        st.write("### グラフ表示")
        fig, ax = plt.subplots()
        sns.lineplot(data=data_filtered, x="date", y="value", marker="o", ax=ax)
        ax.set_title(f"{indicator_label} の推移")
        ax.set_xlabel("年")
        ax.set_ylabel(indicator_label)
        st.pyplot(fig)
    else:
        st.error("データが見つかりませんでした。条件を変更して再試行してください。")

st.write("左側のサイドバーから条件を入力し、[データ取得] ボタンを押してください。")

import streamlit as st
import pandas as pd

# Excelファイル読み込み
file_path = r"C:\Users\owner\OneDrive - 朝日大学\卒論\洋画データ映画com_6月21日.xlsx"
movies = pd.read_excel(file_path, sheet_name="総データ")

# 列名の前後空白を削除
movies.columns = movies.columns.str.strip()

# アプリタイトル
st.title("🎬 洋画おすすめアプリ（映画comデータ）")

# 年代スライダー
year = st.slider(
    "年代を選んでください",
    int(movies['年代'].min()),
    int(movies['年代'].max()),
    2000
)

# 映画com評価スライダー
min_rating = st.slider(
    "最低映画com評価",
    0.0, 10.0, 7.0
)

# レビュー数スライダー（オプション）
min_review = st.number_input(
    "最低レビュー数",
    min_value=0,
    value=0,
    step=1
)

# お気に入り数スライダー（オプション）
min_fav = st.number_input(
    "最低お気に入り数",
    min_value=0,
    value=0,
    step=1
)

# 条件で絞り込み
recommended = movies[
    (movies['年代'] >= year) &
    (movies['映画com評価'] >= min_rating) &
    (movies['レビュー数'] >= min_review) &
    (movies['お気に入り数'] >= min_fav)
]

# 結果表示
st.write(f"選択条件に合う映画 {len(recommended)} 件")
st.dataframe(
    recommended[['タイトル','年代','映画com評価','レビュー数','お気に入り数','興業収入（億円）','配給会社']]
    .sort_values('映画com評価', ascending=False)
    .head(20)
)

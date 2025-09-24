import streamlit as st
import pandas as pd

# Excelファイル読み込み
file_path = "movies.xlsx"  # GitHub に置いたファイル名に合わせる
movies = pd.read_excel(file_path, sheet_name="総データ")

st.title("映画データフィルター")

# 平均値
avg_income = movies["興業収入（億円）"].mean()
avg_rating = movies["映画com評価"].mean()
avg_review = movies["レビュー数"].mean()

# --- スライダーを画面中央に配置 ---
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    st.write("### フィルタ条件")

    # 興業収入スライダー
    income_min = st.slider(
        f"興業収入（億円） (平均: {avg_income:.1f})",
        min_value=10,
        max_value=255,
        value=int(avg_income)
    )

    # 評価スライダー
    rating_min = st.slider(
        f"映画com評価 (平均: {avg_rating:.1f})",
        min_value=0.0,
        max_value=5.0,
        value=float(avg_rating),
        step=0.1
    )

    # レビュー数スライダー
    review_min = st.slider(
        f"レビュー数 (平均: {avg_review:.0f})",
        min_value=int(movies["レビュー数"].min()),
        max_value=int(movies["レビュー数"].max()),
        value=int(avg_review),
        step=10
    )

# --- フィルタリング ---
filtered = movies[
    (movies["興業収入（億円）"] >= income_min) &
    (movies["映画com評価"] >= rating_min) &
    (movies["レビュー数"] >= review_min)
]

# --- 結果表示 ---
st.subheader("検索結果")
if filtered.empty:
    st.write("条件に合う映画は見つかりませんでした。")
else:
    st.dataframe(filtered[["タイトル", "興業収入（億円）", "映画com評価", "レビュー数"]])

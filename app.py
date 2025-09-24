import streamlit as st
import pandas as pd

# ファイル読み込み
file_path = "movies.xlsx"  # Excelを同じフォルダに置く
movies = pd.read_excel(file_path, sheet_name="総データ")

st.title("洋画ソートアプリ")

# ---- 全体平均の計算（5点満点換算を含む） ----
avg_rating = (movies["映画com評価"] / 2).mean()     # 10点満点 → 5点満点に換算
avg_income = movies["興業収入（億円）"].mean()
avg_reviews = movies["レビュー数"].mean()

# ---- フィルタ ----
year = st.sidebar.selectbox("年代を選択", movies["年代"].unique())
company = st.sidebar.selectbox("配給会社を選択", movies["配給会社"].unique())

# ---- スライダー＋平均目印 ----
st.sidebar.markdown("### フィルタ条件")

# 評価スライダー
min_rating = st.sidebar.slider("最低映画評価 (0〜5)", 0.0, 5.0, 3.0, 0.1)
st.sidebar.markdown(
    f"<div style='position: relative; height: 25px;'>"
    f"<div style='position: absolute; left: {avg_rating/5*100}%; "
    f"transform: translateX(-50%); color: red; font-size: 12px;'>▼ 平均 {avg_rating:.2f}</div>"
    f"</div>",
    unsafe_allow_html=True
)

# 興行収入スライダー
min_income = st.sidebar.slider("最低興業収入（億円）", 0.0, float(movies["興業収入（億円）"].max()), 0.0, 1.0)
st.sidebar.markdown(
    f"<div style='position: relative; height: 25px;'>"
    f"<div style='position: absolute; left: {avg_income/movies['興業収入（億円）'].max()*100}%; "
    f"transform: translateX(-50%); color: red; font-size: 12px;'>▼ 平均 {avg_income:.2f}</div>"
    f"</div>",
    unsafe_allow_html=True
)

# レビュー数スライダー
min_reviews = st.sidebar.slider("最低レビュー数", 0, int(movies["レビュー数"].max()), 0, 10)
st.sidebar.markdown(
    f"<div style='position: relative; height: 25px;'>"
    f"<div style='position: absolute; left: {avg_reviews/movies['レビュー数'].max()*100}%; "
    f"transform: translateX(-50%); color: red; font-size: 12px;'>▼ 平均 {avg_reviews:.0f}</div>"
    f"</div>",
    unsafe_allow_html=True
)

# ---- データ抽出 ----
filtered = movies[
    (movies["年代"] == year) &
    (movies["配給会社"] == company) &
    (movies["映画com評価"] / 2 >= min_rating) &
    (movies["興業収入（億円）"] >= min_income) &
    (movies["レビュー数"] >= min_reviews)
]

# ---- 表示 ----
st.subheader("検索結果")
if filtered.empty:
    st.write("条件に合う映画は見つかりませんでした。")
else:
    display_cols = ["タイトル", "興業収入（億円）", "映画com評価", "レビュー数"]
    df_display = filtered[display_cols]

    # タイトル列の幅を最長タイトルに合わせる
    max_title_len = df_display["タイトル"].str.len().max()
    column_config = {
        "タイトル": st.column_config.TextColumn(
            "タイトル",
            width=max(200, max_title_len * 12)
        )
    }

    st.dataframe(df_display, use_container_width=True, column_config=column_config)

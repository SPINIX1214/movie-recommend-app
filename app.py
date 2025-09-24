import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ファイル読み込み
file_path = "movies.xlsx"  # Excelを同じフォルダに置いておく
movies = pd.read_excel(file_path, sheet_name="総データ")

st.title("映画レコメンドアプリ")

# ---- フィルタ ----
# 年代
year = st.sidebar.selectbox("年代を選択", sorted(movies["年代"].unique()))

# 配給会社
company = st.sidebar.selectbox("配給会社を選択", sorted(movies["配給会社"].unique()))

# 評価（0〜5に修正）
min_rating = st.sidebar.slider("最低映画評価 (0〜5)", 0.0, 5.0, 3.0, 0.1)

# フィルタ処理
filtered = movies[
    (movies["年代"] == year) &
    (movies["配給会社"] == company) &
    (movies["映画com評価"] / 2 >= min_rating)  # 10点満点を5点満点に変換
]

# ---- 表示 ----
st.subheader("検索結果")
if filtered.empty:
    st.write("条件に合う映画は見つかりませんでした。")
else:
    # タイトル列の最大文字数を計算して列幅調整
    max_title_len = filtered["タイトル"].str.len().max()
    column_config = {
        "タイトル": st.column_config.TextColumn(
            "タイトル",
            width=max(200, max_title_len * 12)  # 1文字12pxくらいで幅を調整
        )
    }
    st.dataframe(filtered, use_container_width=True, column_config=column_config)

    # ---- 平均値を追加したグラフ ----
    numeric_cols = ["興業収入（億円）", "映画com評価", "レビュー数", "お気に入り数"]

    for col in numeric_cols:
        st.subheader(f"{col} の分布")

        fig, ax = plt.subplots()
        ax.hist(filtered[col], bins=15, alpha=0.7, color="skyblue", edgecolor="black")

        mean_val = filtered[col].mean()
        ax.axvline(mean_val, color="red", linestyle="--", linewidth=2)
        ax.text(mean_val, ax.get_ylim()[1]*0.9, f"平均値: {mean_val:.2f}", color="red")

        st.pyplot(fig)

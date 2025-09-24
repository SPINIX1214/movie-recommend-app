import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ファイル読み込み
file_path = "movies.xlsx"
movies = pd.read_excel(file_path, sheet_name="総データ")

# 評価スケールを10 → 5 に変換
if movies["映画com評価"].max() > 5:
    movies["映画com評価"] = movies["映画com評価"] / 2

st.title("映画データフィルター")

# 平均値の算出
avg_income = movies["興業収入（億円）"].mean()
avg_rating = movies["映画com評価"].mean()
avg_review = movies["レビュー数"].mean()

# --- スライダー用の共通関数 ---
def slider_with_avg(label, min_val, max_val, avg_val, default_val):
    col1, col2, col3 = st.columns([1, 3, 1])  # 真ん中に配置
    with col2:
        st.write(f"**{label}**")
        fig, ax = plt.subplots(figsize=(6, 1))
        ax.axvline(avg_val, color="red", linestyle="--", linewidth=2)
        ax.text(avg_val, 0.5, f"平均: {avg_val:.1f}", color="red",
                ha="center", va="bottom", fontsize=9, transform=ax.get_xaxis_transform())
        ax.set_xlim(min_val, max_val)
        ax.set_ylim(0, 1)
        ax.get_yaxis().set_visible(False)
        ax.set_xticks(range(int(min_val), int(max_val)+1,
                            max(1, (int(max_val)-int(min_val))//5)))
        st.pyplot(fig)
        return st.slider(label, min_val, max_val, default_val)

# スライダー作成
income_filter = slider_with_avg("興業収入（億円）", 10, 255, avg_income, int(avg_income))
rating_filter = slider_with_avg("映画com評価", 0.0, 5.0, avg_rating, float(avg_rating))
review_filter = slider_with_avg("レビュー数", int(movies["レビュー数"].min()),
                                int(movies["レビュー数"].max()), avg_review, int(avg_review))

# フィルタリング
filtered = movies[
    (movies["興業収入（億円）"] >= income_filter) &
    (movies["映画com評価"] >= rating_filter) &
    (movies["レビュー数"] >= review_filter)
][["タイトル", "興業収入（億円）", "映画com評価", "レビュー数"]]

# タイトル列の幅調整（長いタイトルに合わせる）
st.dataframe(filtered, use_container_width=True)

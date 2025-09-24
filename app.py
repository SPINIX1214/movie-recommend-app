import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Excelファイルの読み込み
file_path = "movies.xlsx"  # GitHub に置いたファイル名に合わせて修正
movies = pd.read_excel(file_path, sheet_name="総データ")

st.title("🎬 映画データ可視化アプリ")

# --- スライダー配置（中央寄せ） ---
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    revenue_min, revenue_max = st.slider(
        "興業収入（億円）",
        min_value=10,
        max_value=255,
        value=(10, 255),
        step=5,
    )
    rating_min = st.slider(
        "映画com評価",
        min_value=0.0,
        max_value=5.0,
        value=0.0,
        step=0.1,
    )
    review_min = st.slider(
        "レビュー数",
        min_value=int(movies["レビュー数"].min()),
        max_value=int(movies["レビュー数"].max()),
        value=int(movies["レビュー数"].min()),
        step=10,
    )

# --- 平均値 ---
avg_revenue = movies["興業収入（億円）"].mean()
avg_rating = movies["映画com評価"].mean()
avg_review = movies["レビュー数"].mean()

# --- スライダーに平均値の線を追加 ---
def add_avg_line(ax, value, label, color="red"):
    ax.axvline(value, color=color, linestyle="--")
    ax.text(
        value,
        1.05,  # 少し上に表示して文字が被らないように調整
        f"平均: {value:.2f}",
        color=color,
        ha="center",
        va="bottom",
        transform=ax.get_xaxis_transform()
    )

# --- グラフ表示 ---
fig, axes = plt.subplots(3, 1, figsize=(6, 8))

# 1. 興業収入
axes[0].hist(movies["興業収入（億円）"], bins=20, color="skyblue", edgecolor="black")
axes[0].set_title("興業収入（億円）")
axes[0].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
add_avg_line(axes[0], avg_revenue, "興業収入平均")

# 2. 映画com評価
axes[1].hist(movies["映画com評価"], bins=20, color="lightgreen", edgecolor="black")
axes[1].set_title("映画com評価")
axes[1].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.1f}"))
add_avg_line(axes[1], avg_rating, "評価平均")

# 3. レビュー数
axes[2].hist(movies["レビュー数"], bins=20, color="orange", edgecolor="black")
axes[2].set_title("レビュー数")
axes[2].xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
add_avg_line(axes[2], avg_review, "レビュー平均")

st.pyplot(fig)

# --- フィルタリングされたデータ表示 ---
filtered = movies[
    (movies["興業収入（億円）"] >= revenue_min) & (movies["興業収入（億円）"] <= revenue_max) &
    (movies["映画com評価"] >= rating_min) &
    (movies["レビュー数"] >= review_min)
]

st.subheader("フィルタ後の映画データ")
st.dataframe(filtered[["タイトル", "興業収入（億円)", "映画com評価", "レビュー数"]])

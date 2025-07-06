import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import os

st.set_page_config(page_title="情绪日记", page_icon="📝")

st.title("🧘 情绪日记 App")

DATA_FILE = "diary.csv"

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["日期", "情绪", "内容"])
    df_init.to_csv(DATA_FILE, index=False)

# --- 输入区 ---
st.subheader("📌 今天的日记")
today = st.date_input("选择日期", date.today())

mood = st.radio("你的情绪", ["😊 开心", "😐 一般", "😢 难过", "😠 生气", "😴 累"])

entry = st.text_area("写下今天的想法...")

if st.button("💾 保存日记"):
    df = pd.read_csv(DATA_FILE)
    new_entry = pd.DataFrame([[today, mood, entry]], columns=["日期", "情绪", "内容"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ 日记保存成功！")

# --- 历史记录区 ---
st.subheader("📖 历史日记")

df = pd.read_csv(DATA_FILE)
if df.empty:
    st.info("还没有日记，快写一篇吧！")
else:
    df["日期"] = pd.to_datetime(df["日期"])
    df_sorted = df.sort_values(by="日期", ascending=False)
    st.dataframe(df_sorted[["日期", "情绪", "内容"]])

# --- 情绪趋势图 ---
st.subheader("📈 情绪趋势图（最近 7 天）")

if not df.empty:
    df_last7 = df[df["日期"] >= pd.to_datetime(date.today() - timedelta(days=6))]
    mood_map = {"😊 开心": 5, "😐 一般": 3, "😢 难过": 1, "😠 生气": 2, "😴 累": 2.5}
    df_last7["情绪数值"] = df_last7["情绪"].map(mood_map)

    mood_trend = df_last7.groupby("日期")["情绪数值"].mean()

    plt.rcParams['font.sans-serif'] = ['Songti SC', 'Heiti TC', 'PingFang TC', 'Arial Unicode MS']
    plt.rcParams['axes.unicode_minus'] = False
    
    fig, ax = plt.subplots()
    ax.plot(mood_trend.index, mood_trend.values, marker='o', color='teal')
    ax.set_ylabel("情绪评分（1~5）")
    ax.set_title("最近 7 天情绪趋势")
    ax.grid(True)

    st.pyplot(fig)
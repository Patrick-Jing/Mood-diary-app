import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date, timedelta
import os

st.set_page_config(page_title="Mood Journal", page_icon="📝")

st.title("🧘 Mood Journal App")

DATA_FILE = "diary.csv"

# Initialize data file
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Date", "Mood", "Content"])
    df_init.to_csv(DATA_FILE, index=False)

# --- Entry Section ---
st.subheader("📌 Today's Entry")
today = st.date_input("Select Date", date.today())

mood = st.radio("Your Mood", ["😊 Happy", "😐 Neutral", "😢 Sad", "😠 Angry", "😴 Tired"])

entry = st.text_area("Write down your thoughts...")

if st.button("💾 Save Entry"):
    df = pd.read_csv(DATA_FILE)
    new_entry = pd.DataFrame([[today, mood, entry]], columns=["Date", "Mood", "Content"])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)
    st.success("✅ Entry saved successfully!")

# --- History Section ---
st.subheader("📖 Entry History")

df = pd.read_csv(DATA_FILE)
if df.empty:
    st.info("No entries yet. Start by writing your first one!")
else:
    df["Date"] = pd.to_datetime(df["Date"])
    df_sorted = df.sort_values(by="Date", ascending=False)
    st.dataframe(df_sorted[["Date", "Mood", "Content"]])

# --- Mood Trend Chart ---
st.subheader("📈 Mood Trend (Last 7 Days)")

if not df.empty:
    df_last7 = df[df["Date"] >= pd.to_datetime(date.today() - timedelta(days=6))]
    mood_map = {
        "😊 Happy": 5,
        "😐 Neutral": 3,
        "😢 Sad": 1,
        "😠 Angry": 2,
        "😴 Tired": 2.5
    }
    df_last7["Mood Score"] = df_last7["Mood"].map(mood_map)

    mood_trend = df_last7.groupby("Date")["Mood Score"].mean()

    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    fig, ax = plt.subplots()
    ax.plot(mood_trend.index, mood_trend.values, marker='o', color='teal')
    ax.set_ylabel("Mood Score (1~5)")
    ax.set_title("Mood Trend Over the Last 7 Days")
    ax.grid(True)

    st.pyplot(fig)

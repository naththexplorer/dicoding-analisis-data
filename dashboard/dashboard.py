import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Konfigurasi visual
sns.set_theme(style='white')

def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    path_data = os.path.join(current_dir, "main_data.csv")
    df = pd.read_csv(path_data)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# Sidebar
with st.sidebar:
    st.title("Bike Sharing Analysis")
    start_date, end_date = st.date_input(
        label='Select Date Range',
        min_value=df["dteday"].min(),
        max_value=df["dteday"].max(),
        value=[df["dteday"].min(), df["dteday"].max()]
    )

# Filter
main_df = df[(df["dteday"] >= str(start_date)) & (df["dteday"] <= str(end_date))]

# Header
st.title('Bike Sharing Dashboard')
st.text('Analisis penyewaan sepeda berdasarkan tren waktu dan tipe pengguna.')

# Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rentals", value=f"{main_df.cnt.sum():,}")
with col2:
    st.metric("Casual", value=f"{main_df.casual.sum():,}")
with col3:
    st.metric("Registered", value=f"{main_df.registered.sum():,}")

st.markdown("---")

# Chart 1: Monthly Trend
st.subheader('Trend Rental (Bulanan)')
monthly_df = main_df.resample(rule='M', on='dteday').agg({"cnt": "sum"}).reset_index()
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(monthly_df["dteday"], monthly_df["cnt"], marker='o', color='#2E86C1', linewidth=2)
ax.set_ylabel("Total Count")
st.pyplot(fig)

# Chart 2: Hourly Pattern (Working Day)
st.subheader('Trend Rental Per-Jam: Casual vs Registered')
if 'hr' in main_df.columns:
    workingday_df = main_df[main_df["workingday"] == 1]
    hourly_df = workingday_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(hourly_df['hr'], hourly_df['registered'], label='Registered', color='#2E86C1', lw=2)
    ax2 = ax.twinx() # Gunakan twinx agar skala sebanding jika perlu, atau tetap satu axis
    ax.plot(hourly_df['hr'], hourly_df['casual'], label='Casual', color='#AED6F1', lw=2)
    ax.set_xticks(range(0, 24))
    ax.set_xlabel("Hour of Day")
    ax.legend()
    st.pyplot(fig)
else:
    st.error("Column 'hr' not found. Please use the hour.csv data for main_data.csv")

st.markdown("---")
st.caption('Created by: Firdaus Akmal Budiman')
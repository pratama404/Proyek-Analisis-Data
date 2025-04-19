import streamlit as st
import pandas as pd
import plotly.express as px
import os
import folium
from streamlit_folium import folium_static

# Load dataset
data_file = os.path.join(os.path.dirname(__file__), "data.csv")

def load_data():
    if not os.path.exists(data_file):
        raise FileNotFoundError(f"File data tidak ditemukan: {data_file}")

    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df['weekday'] = df['date'].dt.weekday  # 0 = Senin, 6 = Minggu
    df['season'] = df['month'].apply(lambda x: "Winter" if x in [12, 1, 2] else 
                                                 "Spring" if x in [3, 4, 5] else 
                                                 "Summer" if x in [6, 7, 8] else "Fall")
    return df

df = load_data()

# Sidebar - Filter Parameter
st.sidebar.header("Filter Parameter")
polutan_list = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3"]
selected_polutan = st.sidebar.selectbox("Pilih Polutan", polutan_list)
selected_year = st.sidebar.slider("Pilih Tahun", min_value=2013, max_value=2017, value=(2013, 2017))
st.sidebar.header("Filter Lokasi")
station_list = df["station"].unique()
selected_station = st.sidebar.multiselect("Pilih Stasiun", station_list, default=station_list)

df_filtered = df[
    (df['year'] >= selected_year[0]) & (df['year'] <= selected_year[1]) & (df["station"].isin(selected_station))
]

# **Dashboard Visualisasi Data**
st.title("📊 Dashboard Kualitas Udara Beijing")
st.write(f"Analisis **{selected_polutan}** dari tahun **{selected_year[0]}** hingga **{selected_year[1]}**")

# **1️⃣ Tren Polusi di Aotizhongxin Per Musim**
st.subheader("📆 Tren Polusi di Aotizhongxin Per Musim")
df_aoti = df_filtered[df_filtered["station"] == "Aotizhongxin"]
fig_season = px.box(df_aoti, x="season", y=selected_polutan, color="season", 
                     title=f"Distribusi {selected_polutan} di Aotizhongxin per Musim")
st.plotly_chart(fig_season, use_container_width=True)

# **2️⃣ Waktu Polusi Tertinggi di Aotizhongxin**
st.subheader("⏳ Polusi Tertinggi di Aotizhongxin")
df_aoti_hourly = df_aoti.groupby("hour")[selected_polutan].mean().reset_index()
fig_hourly = px.line(df_aoti_hourly, x="hour", y=selected_polutan, title=f"Rata-rata {selected_polutan} di Aotizhongxin per Jam")
st.plotly_chart(fig_hourly, use_container_width=True)

highest_hour = df_aoti_hourly.loc[df_aoti_hourly[selected_polutan].idxmax()]
st.write(f"⏰ **Jam dengan polusi tertinggi:** {highest_hour['hour']} dengan rata-rata {selected_polutan}: **{highest_hour[selected_polutan]:.2f} µg/m³**")

# **3️⃣ Hubungan Polusi dengan Faktor Meteorologi**
st.subheader("🌡️ Hubungan Polusi dengan Faktor Meteorologi")
weather_factors = ["TEMP", "PRES", "DEWP", "RAIN", "WSPM"]
selected_weather = st.sidebar.selectbox("Pilih Faktor Cuaca", weather_factors)
fig_weather = px.scatter(df_filtered, x=selected_weather, y=selected_polutan, color="station",
                         title=f"Korelasi {selected_polutan} dengan {selected_weather}")
st.plotly_chart(fig_weather, use_container_width=True)

correlation = df_filtered[[selected_polutan, selected_weather]].corr().iloc[0, 1]
st.write(f"📉 **Korelasi antara {selected_polutan} dan {selected_weather}: {correlation:.2f}**")


# **4️⃣ Perbedaan Polusi Antara Hari Kerja dan Akhir Pekan**
st.subheader("📅 Perbedaan Kualitas Udara antara Hari Kerja dan Akhir Pekan")
df_filtered["workday"] = df_filtered["weekday"].apply(lambda x: "Weekday" if x < 5 else "Weekend")
fig_workday = px.box(df_filtered, x="workday", y=selected_polutan, color="workday", 
                      title=f"Perbandingan {selected_polutan} antara Hari Kerja dan Akhir Pekan")
st.plotly_chart(fig_workday, use_container_width=True)

weekday_avg = df_filtered[df_filtered["workday"] == "Weekday"][selected_polutan].mean()
weekend_avg = df_filtered[df_filtered["workday"] == "Weekend"][selected_polutan].mean()
st.write(f"📊 **Rata-rata {selected_polutan} di Hari Kerja:** {weekday_avg:.2f} µg/m³")
st.write(f"📊 **Rata-rata {selected_polutan} di Akhir Pekan:** {weekend_avg:.2f} µg/m³")

# **5️⃣ Dampak Kebijakan Lingkungan terhadap Polusi**
st.subheader("📜 Dampak Kebijakan terhadap Polusi")
policy_events = {
    "2014": "Peluncuran Rencana Aksi Udara Bersih",
    "2016": "Pembatasan Kendaraan Bermotor"
}

fig_policy = px.line(df_filtered.groupby("year")[selected_polutan].mean().reset_index(), x="year", y=selected_polutan,
                     title=f"Tren {selected_polutan} dan Kebijakan Lingkungan")
for year, event in policy_events.items():
    fig_policy.add_vline(x=int(year), line_dash="dash", annotation_text=event)
st.plotly_chart(fig_policy, use_container_width=True)

# **Geospatial Analysis - Peta Polusi**
st.subheader("🗺️ Peta Distribusi Kualitas Udara")
stations_geo = {
    "Aotizhongxin": [39.985, 116.498],
    "Changping": [40.220, 116.234],
    "Dingling": [40.290, 116.220],
    "Dongsi": [39.929, 116.417],
    "Guanyuan": [39.929, 116.339],
    "Gucheng": [39.911, 116.184],
    "Huairou": [40.375, 116.630],
    "Nongzhanguan": [39.934, 116.455],
    "Shunyi": [40.125, 116.655],
    "Tiantan": [39.886, 116.418],
    "Wanliu": [39.963, 116.290],
    "Wanshouxigong": [39.878, 116.339]
}
# m = folium.Map(location=[39.9, 116.4], zoom_start=10)
# for station, coords in stations_geo.items():
#     if station in selected_station:
#         avg_polutan = df_filtered[df_filtered['station'] == station][selected_polutan].mean()
#         folium.CircleMarker(location=coords, radius=avg_polutan / 10, color="red", fill=True, fill_opacity=0.6,
#                             popup=f"{station}: {avg_polutan:.2f}").add_to(m)
# folium_static(m)
m = folium.Map(location=[39.9, 116.4], zoom_start=10)
for station, coords in stations_geo.items():
    if station in selected_station:
        avg_polutan = df_filtered[df_filtered['station'] == station][selected_polutan].mean()
        folium.CircleMarker(
            location=coords, radius=avg_polutan / 10, color="red", fill=True, fill_opacity=0.6,
            popup=f"{station}: {avg_polutan:.2f}"
        ).add_to(m)
folium_static(m)

# **Clustering - Manual Binning**
st.subheader("🔍 Clustering Polutan dengan Binning")
df_filtered["pollution_level"] = pd.cut(df_filtered[selected_polutan], bins=[0, 50, 100, 150, 200, 300],
                                         labels=["Baik", "Sedang", "Tidak Sehat", "Sangat Tidak Sehat", "Berbahaya"])
clustering_counts = df_filtered["pollution_level"].value_counts()
st.bar_chart(clustering_counts)

# **RFM Analysis - Simulasi**
st.subheader("📊 Simulasi RFM Analysis")
st.write("RFM biasa digunakan dalam analisis pelanggan. Di sini, kita coba menerapkan konsepnya ke data polusi:")
df_rfm = df_filtered.groupby("station").agg(
    Recency=("date", lambda x: (df_filtered["date"].max() - x.max()).days),
    Frequency=(selected_polutan, "count"),
    Monetary=(selected_polutan, "mean")
).reset_index()
st.dataframe(df_rfm)

st.write("📌 **Catatan:** RFM Analysis di sini hanya simulasi karena data ini bukan data transaksi pelanggan.")

# **Footer**
st.write("📌 **Note**: Data diambil dari PRSA Dataset (2013-2017)")
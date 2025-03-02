import streamlit as st
import pandas as pd
import plotly.express as px
import os
import folium
from streamlit_folium import folium_static

# Folder tempat semua file CSV disimpan
data_folder = "data.csv"

# Load semua dataset
@st.cache_data
def load_data():
    all_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]
    df_list = []
    
    for file in all_files:
        df = pd.read_csv(os.path.join(data_folder, file))
        station_name = file.split("_")[2]  # Ambil nama stasiun dari nama file
        df["station"] = station_name
        df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
        df_list.append(df)
    
    return pd.concat(df_list, ignore_index=True)

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

# **Line Chart**
st.subheader("📈 Tren Polutan dari Tahun ke Tahun")
fig1 = px.line(df_filtered, x="date", y=selected_polutan, color="station", title=f"Tren {selected_polutan} per Tahun")
st.plotly_chart(fig1, use_container_width=True)

# **Distribusi Polutan**
st.subheader("📊 Distribusi Nilai Polutan")
fig2 = px.histogram(df_filtered, x=selected_polutan, nbins=50, title=f"Distribusi {selected_polutan}")
st.plotly_chart(fig2, use_container_width=True)

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
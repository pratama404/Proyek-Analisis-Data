# Dashboard Kualitas Udara Beijing

Dashboard ini dibuat menggunakan Streamlit untuk menganalisis dan memvisualisasikan data kualitas udara di berbagai stasiun di Beijing dari tahun 2013 hingga 2017. Dataset yang digunakan berasal dari PRSA Data yang mencakup beberapa parameter polusi udara.

## 📌 Fitur Utama

### Filter Interaktif
- Memilih polutan yang ingin dianalisis (PM2.5, PM10, SO2, NO2, CO, O3)
- Memilih rentang tahun untuk analisis
- Memilih stasiun pemantauan udara
- Memilih metode statistik (Mean, Median, Max)

### Visualisasi Data
- **Line Chart** untuk tren polutan dari waktu ke waktu
- **Histogram** untuk distribusi nilai polutan
- **Heatmap** Korelasi antara polutan dan faktor cuaca
- **Peta Interaktif** dengan distribusi polutan berdasarkan lokasi stasiun

### Analisis Lanjutan
- **RFM Analysis** untuk melihat pola perilaku polusi berdasarkan Recency, Frequency, dan Monetary
- **Geospatial Analysis** untuk memahami pola distribusi polutan berdasarkan lokasi
- **Clustering Manual** menggunakan binning untuk mengelompokkan level polusi tanpa algoritma machine learning

## 🛠 Instalasi dan Cara Menjalankan

### 1. Clone Repository
```sh
git clone https://github.com/username/repo-name.git
cd repo-name
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

### 3. Jalankan Streamlit App
```sh
streamlit run app.py
```

## 📂 Struktur File
```
|-- data/                           # Folder untuk dataset CSV
|-- dashboard/                      # Folder untuk dashboard
|-- dashboard.py                    # File utama aplikasi Streamlit
|-- requirements.txt                # Daftar dependencies yang dibutuhkan
|-- data.csv                        # Dataset untuk streamlit
|-- README.md                       # Dokumentasi ini
```

## 📊 Sumber Data
Dataset ini berasal dari PRSA Data yang mencakup pengukuran polusi udara dari beberapa stasiun di Beijing dari 2013-2017.

## 🎯 Pengembangan Selanjutnya
- Menambahkan fitur prediksi kualitas udara berbasis tren historis
- Mengembangkan analisis lebih dalam menggunakan metode statistik
- Mengoptimalkan UI/UX agar lebih interaktif
- Menambahkan fitur analisis berbasis stasiun untuk perbandingan antar wilayah

## 🤝 Kontribusi
Jika ingin berkontribusi, silakan fork repository ini, buat perubahan, lalu buat pull request.

---

**Special: Ageng Putra Pratama 🚀**

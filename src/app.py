import streamlit as st
from halaman_utama import halaman_utama
from halaman_klasifikasi import klasifikasi_data  # Menyimpan klasifikasi data di file terpisah
from halaman_predict import predict_category
from analisis import analisis

# Menambahkan judul pada sidebar
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih Menu", ["Halaman Utama", "Analisis Data", "Klasifikasi Data", "Input Predict",])

# Menampilkan halaman utama atau halaman klasifikasi data berdasarkan pilihan
if menu == "Halaman Utama":
    halaman_utama()
elif menu == "Analisis Data":
    analisis()
elif menu == "Klasifikasi Data":
    klasifikasi_data()
elif menu == "Input Predict":
    predict_category()

# halaman_utama.py

import streamlit as st

# Fungsi untuk halaman utama
def halaman_utama():
    # Header utama
    st.title("🌟 Prediksi Kategori Produksi Daging")
    
    # Deskripsi singkat
    st.markdown("""
    **Selamat datang di aplikasi Prediksi Kategori Produksi Daging Hewan Ternak!**  
    Aplikasi ini dirancang untuk membantu Anda menganalisis dan mengklasifikasikan data produksi daging berdasarkan kategori **Rendah**, **Sedang**, atau **Tinggi**.
    """)
    
    # Informasi pembuat
    st.write("---")
    st.markdown("""
    **Oleh:**  
    📄 Ellys Rahma Putri Bintoro  
    🎓 **NIM:** 202110370311468  
    """)
    
    # Petunjuk penggunaan
    st.write("---")
    st.info("Gunakan menu di **sidebar** untuk: \n\n"
            "- 📊 **Analisis Data** : Statistik dan Distribusi Data. \n"
            "- 🔍 **Klasifikasi Data**: Pengecekan Prediksi Kategori data Produksi Anda. \n"
            "- 🔮 **Prediksi Kategori**: Masukkan data baru untuk melihat hasil prediksi.")
import pandas as pd
import os
import streamlit as st
import matplotlib.pyplot as plt

def analisis():
    """
    Menampilkan data yang telah diproses dan mengelompokkan berdasarkan kategori yang diberikan.
    """
    # Path file CSV
    file_path = r"D:\KULIAH SMT 7\Praktikum Machine Learning\UAP 2\global-meat-production-by-livestock-type.csv"
    
    # Memeriksa apakah file ada
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' tidak ditemukan. Pastikan file berada di direktori yang sama dengan skrip ini.")
        return

    # Membaca file CSV
    data = pd.read_csv(file_path)

    # Menangani nilai kosong: Mengisi dengan nilai yang paling sering muncul (mode)
    for col in data.columns:
        if data[col].isna().sum() > 0:  # Jika ada nilai kosong
            if data[col].dtype in ['float64', 'int64']:  # Jika tipe data numerik
                median_value = data[col].median()
                data[col].fillna(median_value, inplace=True)
            else:  # Jika tipe data kategorikal
                most_frequent_value = data[col].mode()[0]
                data[col].fillna(most_frequent_value, inplace=True)

    # Preprocessing: Hitung total produksi dan kategorisasi berdasarkan Total Production
    data['Total Production'] = data.iloc[:, 3:].sum(axis=1)  # Menghitung total produksi
    data['Category'] = pd.qcut(data['Total Production'], q=3, labels=["Rendah", "Sedang", "Tinggi"])  # Kategorisasi

    # Menampilkan statistik deskriptif
    st.write("### Statistik Deskriptif")
    st.dataframe(data.describe())

    # Menampilkan distribusi jumlah kategori dalam bentuk tabel
    st.write("### Distribusi Kategori Berdasarkan Jumlah")
    category_counts = data['Category'].value_counts().reset_index()
    category_counts.columns = ['Kategori', 'Jumlah']
    
    # Menampilkan tabel distribusi jumlah kategori
    st.dataframe(category_counts)

    # Menampilkan Pie Chart untuk distribusi kategori berdasarkan persen
    st.write("### Distribusi Kategori Berdasarkan Persen")
    category_percentages = data['Category'].value_counts(normalize=True) * 100  # Persentase kategori
    fig, ax = plt.subplots()
    ax.pie(category_percentages, labels=category_percentages.index, autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie chart is drawn as a circle.
    
    # Menampilkan Pie Chart di Streamlit
    st.pyplot(fig)

    # Menampilkan data berdasarkan kategori tertentu
    st.write("### Data Berdasarkan Kategori")
    selected_category = st.selectbox("Pilih kategori untuk melihat data:", ["Rendah", "Sedang", "Tinggi"])
    
    # Filter data berdasarkan kategori yang dipilih
    filtered_data = data[data['Category'] == selected_category]

    # Menampilkan data yang telah difilter berdasarkan kategori
    st.write(f"Data dengan kategori '{selected_category}':")
    st.dataframe(filtered_data)

if __name__ == "__main__":
    # Menjalankan fungsi analisis
    analisis()

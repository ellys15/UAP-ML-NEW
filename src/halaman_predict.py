import streamlit as st
import numpy as np
import pandas as pd

# Fungsi untuk menerima input dari pengguna dan memprediksi kategori
def predict_category():
    st.title("🔮 Prediksi Kategori Produksi Daging")

    # Input dari pengguna
    sheep_and_goat = st.number_input("Sheep and Goat (tonnes)", min_value=0.0)
    beef_and_buffalo = st.number_input("Beef and Buffalo (tonnes)", min_value=0.0)
    pigmeat = st.number_input("Pigmeat (tonnes)", min_value=0.0)
    wild_game = st.number_input("Wild game (tonnes)", min_value=0.0)
    duck = st.number_input("Duck (tonnes)", min_value=0.0)
    poultry = st.number_input("Poultry (tonnes)", min_value=0.0)
    horse = st.number_input("Horse (tonnes)", min_value=0.0)
    camel = st.number_input("Camel (tonnes)", min_value=0.0)
    goose_and_guinea_fowl = st.number_input("Goose and Guinea Fowl (tonnes)", min_value=0.0)

    # Membuat array fitur berdasarkan input pengguna
    user_input = np.array([sheep_and_goat, beef_and_buffalo, pigmeat, wild_game,
                           duck, poultry, horse, camel, goose_and_guinea_fowl])

    # Menghitung total produksi
    total_production = np.sum(user_input)

    # Menentukan kategori berdasarkan total produksi
    categories = ["Rendah", "Sedang", "Tinggi"]
    
    if total_production <= 100000:
        category = "Rendah"
    elif total_production <= 500000:
        category = "Sedang"
    else:
        category = "Tinggi"
    
    # Menampilkan hasil prediksi kategori berdasarkan total produksi
    st.write(f"Total Produksi: {total_production} ton")
    st.write(f"Kategori produksi untuk input ini adalah: {category}")

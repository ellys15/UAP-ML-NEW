import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from pytorch_tabnet.tab_model import TabNetClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
import torch
import os
import joblib  # Untuk menyimpan model dengan format .joblib


def klasifikasi_data():
    st.title("🤖 Prediksi Kategori Data Produksi Daging")

    # Load file CSV
    file_path = r"D:\KULIAH SMT 7\Praktikum Machine Learning\UAP 2\global-meat-production-by-livestock-type.csv"
    if not os.path.exists(file_path):
        st.error(f"File '{file_path}' tidak ditemukan. Pastikan file berada di direktori yang sama dengan skrip ini.")
        return

    # Membaca file CSV
    data = pd.read_csv(file_path)

    # Menangani nilai kosong: Mengisi dengan nilai yang paling sering muncul (mode)
    for column in data.columns:
        if data[column].isna().sum() > 0:  # Jika ada nilai kosong
            if data[column].dtype in ['float64', 'int64']:  # Jika tipe data numerik
                median_value = data[column].median()
                data[column].fillna(median_value, inplace=True)
            else:  # Jika tipe data kategorikal
                most_frequent_value = data[column].mode()[0]
                data[column].fillna(most_frequent_value, inplace=True)

    # Preprocessing: Hitung total produksi daging dan kategorisasi
    data['Total Production'] = data.iloc[:, 3:].sum(axis=1)  # Menghitung total produksi
    data['Category'] = pd.qcut(data['Total Production'], q=3, labels=["Rendah", "Sedang", "Tinggi"])  # Kategorisasi

    # Pilih fitur dan target
    fitur = [col for col in data.columns if col != 'Category']  # Semua kolom kecuali 'Category'
    target = 'Category'

    # Menampilkan pilihan fitur pada web
    st.write("### Pilih Fitur dan Target untuk Klasifikasi")

    # Membuat selectbox untuk memilih fitur
    selected_fitur = st.multiselect("Pilih kolom fitur:", fitur)

    # Membuat selectbox untuk memilih target
    selected_target = st.selectbox("Pilih kolom target:", [target])

    if not selected_fitur or not selected_target:
        st.warning("Pilih fitur dan target terlebih dahulu.")
        return

    # Memisahkan data menjadi fitur dan target
    X = data[selected_fitur]
    y_categorical = pd.Categorical(data[selected_target])  # Konversi target menjadi kategori
    y = y_categorical.codes  # Numerik
    categories = y_categorical.categories  # Simpan kategori

    # Mengonversi fitur kategorikal menjadi numerik
    X = pd.get_dummies(X)

    # Standarisasi data untuk model tertentu (misalnya Neural Network)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Membagi data menjadi training dan testing
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Pilih model untuk klasifikasi
    model_name = st.radio("Pilih Model:", ["Random Forest", "XGBoost", "TabNet"])

    if st.button("Jalankan Model"):
        model = None
        model_path = None
        y_pred = None

        if model_name == "Random Forest":
            model = RandomForestClassifier(random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            # Simpan model Random Forest dalam format .joblib
            joblib.dump(model, "random_forest_model.h5")
            st.write("Model Random Forest telah disimpan sebagai 'random_forest_model.h5'.")

        elif model_name == "XGBoost":
            model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss', random_state=42)
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            # Simpan model XGBoost dalam format .joblib
            joblib.dump(model, "xgboost_model.h5")
            st.write("Model XGBoost telah disimpan sebagai 'xgboost_model.h5'.")

        elif model_name == "TabNet":
            model_path = "tabnet_model.zip"
            X_train_np = np.array(X_train, dtype=np.float32)
            X_test_np = np.array(X_test, dtype=np.float32)
            y_train_np = np.array(y_train, dtype=np.int64)
            y_test_np = np.array(y_test, dtype=np.int64)

            model = TabNetClassifier(
                n_d=8, n_a=8, n_steps=3,
                gamma=1.3, lambda_sparse=1e-4,
                optimizer_fn=torch.optim.Adam,
                optimizer_params=dict(lr=2e-2),
                verbose=0
            )

            # Latih model TabNet
            model.fit(
                X_train_np, y_train_np,
                eval_set=[(X_test_np, y_test_np)],
                eval_metric=['accuracy'],
                max_epochs=20,
                patience=10,
                batch_size=32,
                virtual_batch_size=16
            )
            y_pred = model.predict(X_test_np)
            # Simpan model TabNet dalam format .zip
            model.save_model("tabnet_model.zip")
            st.write("Model TabNet telah disimpan sebagai 'tabnet_model.zip'.")

        # Akurasi dan laporan
        accuracy = accuracy_score(y_test, y_pred)
        st.write(f"Akurasi: {accuracy:.2f}")

        # Menampilkan perbandingan antara nilai asli dan prediksi
        comparison_df = pd.DataFrame({
            'Actual': [categories[i] for i in y_test],
            'Predicted': [categories[i] for i in y_pred]
        })
        st.write("### Perbandingan antara Kategori Asli dan Prediksi")
        st.write(comparison_df)

        st.write("### Confusion Matrix")
        plot_confusion_matrix(y_test, y_pred, categories, f"Confusion Matrix - {model_name}")
        st.write("### Classification Report")
        st.markdown(f"```\n{classification_report(y_test, y_pred, target_names=categories)}\n```")

# Fungsi untuk menampilkan confusion matrix
def plot_confusion_matrix(y_true, y_pred, categories, title):
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=categories, yticklabels=categories)
    plt.title(title)
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    st.pyplot(plt)

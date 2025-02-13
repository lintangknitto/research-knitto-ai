# Knitto AI

Knitto AI adalah sebuah proyek yang menggunakan teknologi kecerdasan buatan untuk mempermudah proses **Q&A** dengan customer. Dengan **Knitto AI**, Anda dapat membangun sistem yang dapat menangani pertanyaan dan jawaban otomatis menggunakan machine learning dan teknologi AI. Ikuti langkah-langkah berikut untuk menjalankan proyek ini di lokal Anda.

## Persyaratan Sistem

Sebelum memulai, pastikan sistem Anda memenuhi persyaratan berikut:

- **Python** versi minimal 3.x.
- Pastikan `pip` sudah terinstall di sistem Anda.

## Langkah-Langkah untuk Menjalankan Knitto AI

### 1. Clone Repositori

Langkah pertama adalah meng-clone repositori ini ke mesin lokal Anda. Gunakan perintah berikut:


Setelah repositori berhasil di-clone, masuk ke dalam folder proyek:


### 2. Membuat dan Mengaktifkan Virtual Environment (venv)

Untuk memastikan proyek berjalan dengan dependensi yang terisolasi, kita akan menggunakan **virtual environment** (`venv`).

- **Membuat virtual environment**:


- **Mengaktifkan virtual environment**:

- Di **Windows**:

  ```
  venv\Scripts\activate
  ```

- Di **MacOS/Linux**:

  ```
  source venv/bin/activate
  ```

Jika berhasil, prompt terminal Anda akan menunjukkan `(venv)` di depan nama folder, menandakan bahwa virtual environment telah aktif.

### 3. Install Dependensi

Setelah virtual environment aktif, install semua dependensi yang diperlukan oleh proyek dengan perintah berikut:


Ini akan menginstal semua paket yang tercantum dalam file `requirements.txt`.

### 4. Menjalankan Aplikasi dengan Streamlit

Proyek ini menggunakan **Streamlit** untuk antarmuka pengguna (UI). Setelah dependensi terinstal, Anda dapat menjalankan aplikasi dengan perintah berikut:


Aplikasi akan mulai berjalan, dan Streamlit akan memberi Anda URL untuk mengakses aplikasi melalui browser.

### 5. Menonaktifkan Virtual Environment

Setelah selesai bekerja dengan aplikasi, Anda dapat menonaktifkan virtual environment dengan perintah berikut:


Ini akan mengembalikan Anda ke lingkungan Python global.

## Troubleshooting

Jika Anda mengalami masalah saat instalasi atau menjalankan aplikasi, coba beberapa langkah berikut:

- **Periksa versi Python**: Pastikan Anda menggunakan versi Python yang tepat dengan menjalankan perintah:


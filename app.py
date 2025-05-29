
from flask import Flask, render_template, request, redirect, url_for, flash
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'rahasia123'
UPLOAD_FOLDER = 'laporan'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nama = request.form.get('nama')
        kontak = request.form.get('kontak')
        kategori = request.form.get('kategori')
        tanggal = request.form.get('tanggal')
        deskripsi = request.form.get('deskripsi')
        link = request.form.get('link')
        lokasi = request.form.get('lokasi')
        file = request.files.get('bukti')

        if not kategori or not tanggal or not deskripsi:
            flash('Kategori, tanggal, dan deskripsi harus diisi.', 'error')
            return redirect(url_for('index'))

        filename = None
        if file and file.filename != '':
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        laporan_path = os.path.join(UPLOAD_FOLDER, 'laporan.txt')
        with open(laporan_path, 'a', encoding='utf-8') as f:
            f.write(f"""
==============================
Tanggal Kirim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Nama         : {nama}
Kontak       : {kontak}
Kategori     : {kategori}
Tanggal Kasus: {tanggal}
Deskripsi    : {deskripsi}
Link         : {link}
Lokasi       : {lokasi}
Bukti Upload : {filename if filename else '-'}
==============================\n""")

        return render_template('sukses.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

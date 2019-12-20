#!/usr/bin/env python3
"""
TEMPLATE TP4 DDP1 Semester Gasal 2019/2020
Author: 
Ika Alfina (ika.alfina@cs.ui.ac.id)
Evi Yulianti (evi.yulianti@cs.ui.ac.id)
Meganingrum Arista Jiwanggi (meganingrum@cs.ui.ac.id)
Last update: 26 November 2019
"""

#Mengimpor fitur yang ada di file budayaKB_model.py dan beberapa fitur yang ada di module flask
from budayaKB_model import BudayaItem, BudayaCollection
from flask import Flask, request, render_template

#Membuat flask constructor dan membuat password enkripsi
app = Flask(__name__)
app.secret_key ="tp4"

#Inisialisasi objek budayaData
databasefilename = ""
budayaData = BudayaCollection()

@app.route('/')
def index():
	"""
	Merender tampilan saat tombol 'Home' diklik
	"""
	return render_template("index.html")
 	
@app.route('/imporBudaya', methods=['GET', 'POST'])
def importData():
	"""
	Implementasi fitur Impor Budaya
	Merender tampilan saat menu Impor Budaya diklik
	Melakukan pemrosesan terhadap isian form setelah tombol 'Import Data' diklik
	Menampilkan notifikasi bahwa data telah berhasi diimport
	"""

	if request.method == "GET":
		return render_template("imporBudaya.html")
	
	elif request.method == "POST":	
		f = request.files['file']
		global databasefilename
		databasefilename=f.filename
		budayaData.importFromCSV(f.filename)
		n_data = len(budayaData.koleksi)
		return render_template("imporBudaya.html", result=n_data, fname=f.filename)


@app.route('/lihatBudaya')
def lihatData():
	"""
	Implementasi fitur Lihat Budaya
	Merender tampilan saat menu Lihat Budaya diklik
	Menampilkan seluruh data yang ada di dalam program
	"""

	data = budayaData.lihat()
	jumlah_data = len(data)
	return render_template("lihatBudaya.html", data_budaya = data, jumlah_data = jumlah_data)
		
@app.route('/cariBudaya', methods=['GET', 'POST'])
def cariData():
	"""
	Implementasi fitur Cari Budaya
	Merender tampilan saat menu Cari Budaya diklik
	Memproses pencarian data berdasarkan pilihan user
	Menampilkan hasil dari pencarian data dan juga jumlahnya
	"""

	if request.method == "GET":
		return render_template("cariBudaya.html")

	elif request.method == "POST":
		pilihan = request.form['pilihan']
		target_data = request.form['target']

		if pilihan == 'Nama Budaya':
			data = budayaData.cariByNama(target_data)

		elif pilihan == 'Tipe Budaya':
			data = budayaData.cariByTipe(target_data)

		else :
			data = budayaData.cariByProv(target_data)

		jumlahData = len(data)

		if databasefilename :
			return render_template('cariBudaya.html', data_budaya = data, jumlah_budaya = jumlahData, choice = 1)

		else :
			return render_template('cariBudaya.html', data_budaya = data, jumlah_budaya = jumlahData, choice = 2)
	
@app.route('/tambahBudaya', methods=['GET', 'POST'])
def tambahData():
	"""
	Implementasi salah satu fitur Sunting Budaya
	Merender tampilan saat submenu Tambah Budaya diklik
	Memproses penambahan data dengan isian form yang diisi user ke dalam program dan menampilkan pesan hasil proses penambahan
	Mengeskpor ke dalam file jika telah memenuhi syarat
	"""

	if request.method == "GET":
		return render_template("tambahBudaya.html")
	
	elif request.method == "POST":
		namaBudaya = request.form['namaBudaya']
		tipeBudaya = request.form['tipeBudaya']
		provinsiBudaya = request.form['provinsiBudaya']
		urlReference = request.form['urlReference']

		if databasefilename:
			tambah_budaya = budayaData.tambah(namaBudaya, tipeBudaya, provinsiBudaya, urlReference)

			if tambah_budaya :
				budayaData.exportToCSV(databasefilename)
				return render_template("tambahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 1)

			else :
				return render_template("tambahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 2)

		else:
			return render_template("tambahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 3)



@app.route('/ubahBudaya', methods=['GET', 'POST'])
def ubahData():
	"""
	Implementasi salah satu fitur Sunting Budaya
	Merender tampilan saat submenu Ubah Budaya diklik
	Memproses pengubahan data dengan isian form yang diisi user ke dalam program dan menampilkan pesan hasil proses pengubahan
	Mengekspor ke dalam file jika telah memenuhi syarat
	"""

	if request.method == "GET":
		return render_template("ubahBudaya.html")
	
	elif request.method == "POST":
		namaBudaya = request.form['namaBudaya']
		tipeBudaya = request.form['tipeBudaya']
		provinsiBudaya = request.form['provinsiBudaya']
		urlReference = request.form['urlReference']

		if databasefilename:
			ubah_budaya = budayaData.ubah(namaBudaya, tipeBudaya, provinsiBudaya, urlReference)

			if ubah_budaya :
				budayaData.exportToCSV(databasefilename)
				return render_template("ubahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 1)

			else:
				return render_template("ubahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 2)

		else:
			return render_template("ubahBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 3)

@app.route('/hapusBudaya', methods=['GET', 'POST'])
def hapusData():
	"""
	Implementasi salah satu fitur Sunting Budaya
	Merender tampilan saat submenu Hapus Budaya diklik
	Memproses penghapusan data dengan isian form yang diisi user ke dalam program dan menampilkan pesan hasil proses penghapusan
	Mengekspor ke dalam fiie jika telah memenuhi syarat
	"""

	if request.method == "GET":
		return render_template("hapusBudaya.html")

	elif request.method == "POST":
		namaBudaya = request.form['namaBudaya']

		if databasefilename :
			hapus_budaya = budayaData.hapus(namaBudaya)

			if hapus_budaya:
				budayaData.exportToCSV(databasefilename)
				return render_template("hapusBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 1)

			else:
				return render_template("hapusBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 2)
				
		else :
			return render_template("hapusBudaya.html", fname = databasefilename, nama_budaya = namaBudaya, choice = 3)

@app.route('/statistikBudaya', methods = ['GET', 'POST'])
def statData():
	"""
	Implementasi fitur Statistik Budaya
	Merender tampilan saat menu Statistik Budaya diklik
	Memproses penghitungan data berdasarkan pilihan user
	Menampilkan hasil dari penghitungan data dari jumlah yang terbanyak
	"""

	if request.method == 'GET':
		return render_template('statistikBudaya.html')
	
	elif request.method == 'POST':
		pilihan = request.form['pilihan']

		if pilihan == 'Semua Budaya':
			data = budayaData.stat()

		elif pilihan == 'Tipe Budaya':
			data = budayaData.statByTipe()
			data = sorted(data.items(), key=lambda keyvalue: keyvalue[1], reverse = True)

		else :
			data = budayaData.statByProv()
			data = sorted(data.items(), key=lambda keyvalue: keyvalue[1], reverse = True)
		

		return render_template('statistikBudaya.html', pilihan = pilihan, data_budaya = data)

@app.route('/refreshProgram')
def refreshData():
	"""
	Implementasi fitur Refreh Program
	Merender tampilan saat menu Refresh Program diklik
	Menghapus file database dan koleksi data yang ada di dalam program
	"""

	budayaData.refProg()
	global databasefilename	
	databasefilename = ""
	return render_template("refreshProgram.html")

# run main app
if __name__ == "__main__":
	app.run(debug=True)

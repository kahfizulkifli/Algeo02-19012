from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from pprint import pprint
from rank import *
from terms import *
from tabel import *	

app = Flask(__name__)
UPLOAD_FOLDER = os.path.abspath('../test') # directory dokumen-dokumen
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# BukanTxt(filename) mengembalikan true apabila filename bukan merupakan nama file .txt
def BukanTxt(filename):
	return '.' not in filename or filename.rsplit('.',1)[1].lower() != 'txt' 

# HomePage adalah fungsi untuk menampilkan dan mengolah laman utama (home)
@app.route('/', methods=['GET', 'POST'])
def HomePage():
	if request.method == 'POST': # website mendapat masukan
		if 'query' in request.form: # pengguna memasukkan query
			query = request.form['query'] # ambil query pengguna
			return redirect(url_for('SearchResultsPage', query=query)) # muat laman hasil pemcarian
		elif 'upload' in request.files: # pengguna mengunggah file .txt
			file = request.files['upload'] # ambil file pengguna
			filename = secure_filename(file.filename) # buat nama file tahan serangan
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # simpan file yang diunggah pengguna
			return render_template('home.html', perihalpage=url_for('PerihalPage')) # muat laman utama (home)
	return render_template('home.html', perihalpage=url_for('PerihalPage'), scrapingpage=url_for('WebScrapingPage')) # muat laman utama (home)

# SearchResultsPage adalah fungsi untuk menampilkan dan mengolah laman hasil pencarian
@app.route('/search-<query>', methods=['GET', 'POST'])
def SearchResultsPage(query):
	if request.method == 'POST': # website mendapat masukan
		if 'query' in request.form: # pengguna memasukkan query
			query = request.form['query'] # ambil query pengguna
			return redirect(url_for('SearchResultsPage', query=query)) # muat laman hasil pemcarian
		elif 'upload' in request.files: # pengguna mengunggah file
			file = request.files['upload'] # ambil file pengguna
			filename = secure_filename(file.filename) # buat nama file tahan serangan
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # simpan file yang diunggah pengguna
		return render_template('home.html', perihalpage=url_for('PerihalPage'), scrapingpage=url_for('WebScrapingPage')) # muat laman utama (home)
	
	# convert string query ke list of terms
	queryTermsStem = GetTermsStem(query)
	queryTermsNonStem = GetTermsNonStem(query)
	# tabel term
	tabel = GetTabel(query)
	# cosine sim & rank
	rank = GetRank(queryTermsStem)
	rank2 = []
	for (filename, cntword, score, firstSentence) in rank:
		rank2.append((filename, url_for('DisplayPage', filename=filename), cntword, round(score*100,2), firstSentence))
	return render_template('search_results.html',  terms=queryTermsNonStem, rank=rank2, query=query, tabel=tabel, perihalpage=url_for('PerihalPage'), scrapingpage=url_for('WebScrapingPage'))

# DisplayPage adalah fungsi untuk menampilkan dan mengolah laman tampilan dokumen
@app.route('/display-<filename>')
def DisplayPage(filename):
	file = open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # buka file yang diminta pengguna
	return render_template('display.html', text=file.read()) # muat laman tampilan dokumen

# PerihalPage adalah fungsi untuk menampilkan dan mengolah laman perihal
@app.route('/perihal')
def PerihalPage():
	return render_template('perihal.html', homepage=url_for('HomePage'), scrapingpage=url_for('WebScrapingPage')) # muat laman perihal

# WebScrapingPage adalah fungsi untuk menampilkan dan mengolah laman web scraping
@app.route('/webscraping', methods=['GET', 'POST'])
def WebScrapingPage():
	if request.method == 'POST': # website mendapat masukan
		url = request.form['query'] # ambil url
		namafile = request.form['namafile']
		text = WebScrappingKontenByUrl(url) # dapatkan string dokumen
		file = open(os.path.join(app.config['UPLOAD_FOLDER'],namafile),'w')
		file.write(text)
		file.close()
		return redirect(url_for('HomePage'))
	return render_template('webscraping.html', homepage=url_for('HomePage'))
if __name__ == '__main__':
  app.run()

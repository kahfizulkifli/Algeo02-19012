import io 
import re
import string
import os
from newspaper import Article
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
from pprint import pprint

#konstanta
FOLDER = os.path.abspath("docs")

#Fungsi untuk melakukan ekstraksi konten web (Web Scrapping) berupa berita yang ada di laman web
def WebScrappingKontenByUrl(url): #Parameter yang dimasukan adalah string yang merujuk ke alamat laman berita
	article = Article(url) #Instantiate object article dengan kelas Article
	article.download() #Melakukan download konten laman
	article.parse()
	return article.text #Mengembalikan string berupa berita yang telah di scrapping dari laman web

#Mastiin nama filenya sesuai format (.txt)
def FormatNamaFile(namaFile):
	if ((namaFile[(len(namaFile))-4:len(namaFile)]) != ".txt"):
		namaFile += ".txt"
	namaFile = os.path.join(FOLDER,namaFile)
	return namaFile

#Save string ke file .txt
def SaveKontenTxt(namaFile, konten): #Parameter berupa nama file tempat ingin melakukan save, dan konten (string) yang mau disave
	fileTxt = open(FormatNamaFile(namaFile),"w") #Membaca file yang memiliki nama namaFile (format .txt) dalam mode write
	fileTxt.write(konten) #Menuliskan/save string (konten) yang ingin disimpan dalam file
	fileTxt.close() #Menutup file

#Membaca isi sebuah file .txt dan mengembalikannya dalam bentuk string
def BacaKontenTxt(namaFile):
	f = open(FormatNamaFile(namaFile))
	isiFileString = f.read()
	return isiFileString

#Menggunakan regular expression untuk melakukan pembersihan terhadap string yang akan diolah
def RegexCleaning(stringKotor):
	#Hilangkan Unicode
	stringBersih = re.sub(r'[^\x00-\x7F]+', ' ', stringKotor)
	#Hilangkan Mentions
	stringBersih = re.sub(r'@\w+', '', stringBersih)
	#Ubah jadi Lowercase
	stringBersih = stringBersih.lower()
	#Hilangkan punctuations
	stringBersih = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', stringBersih)
	#Lowercase numbers
	stringBersih = re.sub(r'[0-9]', '', stringBersih)
	#Hilangkan double space
	stringBersih = re.sub(r'\s{2,}', ' ', stringBersih)

	return stringBersih

#Mengubah String menjadi Array. Di mana tiap indeks array diisi oleh tiap kata dalam string.
def StringToArray(stringAwal):
	return word_tokenize(stringAwal)

#Melakukan stemming terhadap array of kata (string)
def StemmingKonten(arrayOfKata):
	porter = PorterStemmer() #Menggunakan PorterStemmer
	arrayKataSudahStemming = [] #Array kosong untuk menyimpan kata-kata yang sudah di stemming

	for kata in arrayOfKata: 
		arrayKataSudahStemming.append(porter.stem(kata)) #Melakukan append kata yang sudah di stem ke dalam array
	return arrayKataSudahStemming

#Menghilangkan stopwords dari array of kata (string)
def StopWordsRemove(arrayOfKata):
	stop_words = set(stopwords.words('english')) #Menginisiasi daftar stopwrd dengan menggunakan library nltk
	arrayKataTanpaStopWords = [] #Array kosong untuk menyimpan kata-kata yang sudah di remove stopwordsnya

	for kata in arrayOfKata:
		if kata not in stop_words: #Melakukan pengecekan. Bila kata bukan stopwords, makan dilakukan append ke array 
			arrayKataTanpaStopWords.append(kata)
	return arrayKataTanpaStopWords

#Mengambil kalimat pertama
def firstsentence():
	arroffirstsentence = []
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	for namaFile in namaFiles:
		konten = BacaKontenTxt(namaFile)
		sentences = sent_tokenize(konten)
		arroffirstsentence.append(sentences[0])
	return arroffirstsentence

#Fungsi yang menggabungkan fungsi-fungsi sebelumnya. Menerima parameter berupa namafile dan akan mengembalikan array of kata yang sudah bersih (sudah stem, remove stopwords)
def ArrayIsiFileSiapOlah(namaFile):
	stringDariFile = BacaKontenTxt(namaFile)
	arrayBersih = StopWordsRemove(StemmingKonten(StringToArray(RegexCleaning(stringDariFile))))
	return arrayBersih

def ArrayIsiFileSiapOlahNonStem(namaFile):
	stringDariFile = BacaKontenTxt(namaFile)
	arrayBersih = StopWordsRemove(StringToArray(RegexCleaning(stringDariFile)))
	return arrayBersih

#Fungsi yang mengembalikan kamus kata dalam bentuk array. Kamus kata adalah daftar kata unik dari dokumen yang dimasukkan
def KataDalamKamus(): #Parameter berupa banyaknya dokumen yang ingin dibaca
	kamus = [] #Array kosong untuk menyimpan kata unik
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	for namaFile in namaFiles: 
		arrTemp = ArrayIsiFileSiapOlah(namaFile) #Memanggil fungsi ArrayIsiFileSiapOlah untuk mendapakan kata bersih dari masing-masing dokumen
		kamus += arrTemp #Menggabungkan kata-kata tiap dokumen
		kamus = list(set(kamus)) #Memanggil set agar elemen menjadi unik (tidak duplikat), kemudian memanggil list agar berubah menjadi array kembali
		kamus.sort() #Mengurutkan dari a-z, elemen  dalam kamus
	return kamus

def KataDalamKamusNonStem(): #Parameter berupa banyaknya dokumen yang ingin dibaca
	kamus = [] #Array kosong untuk menyimpan kata unik
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	for namaFile in namaFiles: 
		arrTemp = ArrayIsiFileSiapOlahNonStem(namaFile) #Memanggil fungsi ArrayIsiFileSiapOlah untuk mendapakan kata bersih dari masing-masing dokumen
		kamus += arrTemp #Menggabungkan kata-kata tiap dokumen
		kamus = list(set(kamus)) #Memanggil set agar elemen menjadi unik (tidak duplikat), kemudian memanggil list agar berubah menjadi array kembali
		kamus.sort() #Mengurutkan dari a-z, elemen  dalam kamus
	return kamus

#Fungsi yang mengembalikan array yang berisi kata-kata yang muncul pada setiap dokumen (tidak unik)
def KataDalamDokumen():
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	kataDiDokumen = [[] for i in range(len(namaFiles))] #Inisiasi array of array yang berisi elemen sebanyak dokumen yang ingin dibaca
	i = 0
	for namaFile in namaFiles:
		arrTemp = ArrayIsiFileSiapOlah(namaFile) #menyiapkan kata-kata dalam dokumen 
		kataDiDokumen[i] = arrTemp #Menyimpan kata-kata dalam dokumen ke dalam variabel kataDiDokumen
		i += 1
	return kataDiDokumen

def KataDalamDokumenNonStem():
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	kataDiDokumen = [[] for i in range(len(namaFiles))] #Inisiasi array of array yang berisi elemen sebanyak dokumen yang ingin dibaca
	i = 0
	for namaFile in namaFiles:
		arrTemp = ArrayIsiFileSiapOlahNonStem(namaFile) #menyiapkan kata-kata dalam dokumen 
		kataDiDokumen[i] = arrTemp #Menyimpan kata-kata dalam dokumen ke dalam variabel kataDiDokumen
		i += 1
	return kataDiDokumen

#Fungsi yang mengembalikan dictionary yang memiliki format {(Kata,No.Dokumen): FrekuensiKata}
def KamusDokumen(banyakDokumen, kamusKata, kataDiDokumen):
	kamusKataDokumen = {} #Dictionary kosong
	for kata in kamusKata:
		for dokumen in range(banyakDokumen):
			kamusKataDokumen[(kata,dokumen)] = kataDiDokumen[dokumen].count(kata)
	return kamusKataDokumen

#Fungsi yang mengembalikan array yang berisi kata-kata yang muncul pada setiap dokumen (tidak unik)
def KataDalamDokumen2():
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	kataDiDokumen = {} #Inisiasi dict
	for namaFile in namaFiles:
		arrTemp = ArrayIsiFileSiapOlah(namaFile) #menyiapkan kata-kata dalam dokumen 
		kataDiDokumen[namaFile] = arrTemp #Menyimpan kata-kata dalam dokumen ke dalam variabel kataDiDokumen
	return kataDiDokumen

def KataDalamDokumenNonStem2():
	namaFiles = os.listdir(FOLDER) #Membaca seluruh nama file dalam folder test dan menyimpannya dalam bentuk array
	kataDiDokumen = {} #Inisiasi dict
	for namaFile in namaFiles:
		arrTemp = ArrayIsiFileSiapOlahNonStem(namaFile) #menyiapkan kata-kata dalam dokumen 
		kataDiDokumen[namaFile] = arrTemp #Menyimpan kata-kata dalam dokumen ke dalam variabel kataDiDokumen
	return kataDiDokumen

#Fungsi yang mengembalikan dictionary yang memiliki format {(Kata,namafile): FrekuensiKata}
def KamusDokumen2(namaFiles, kamusKata, kataDiDokumen):
	kamusKataDokumen = {} #Dictionary kosong
	for kata in kamusKata:
		for dokumen in namaFiles:
			kamusKataDokumen[(kata,dokumen)] = kataDiDokumen[dokumen].count(kata)
	return kamusKataDokumen


# GetTermsStem menerima string query dari pengguna
# dan mengembalikan dictionary dengan key:value pairnya = [KATA]:[KEMUNCULAN KATA]
def GetTermsStem(s):
	sBersih = StopWordsRemove(StemmingKonten(StringToArray(RegexCleaning(s))))
	terms = {}
	for kata in sBersih:
		if not kata in terms:
			terms[kata] = sBersih.count(kata)
	return terms

# GetTermsStem menerima string query dari pengguna
# dan mengembalikan dictionary dengan key:value pairnya = [KATA]:[KEMUNCULAN KATA]
def GetTermsNonStem(s):
	sBersih = StopWordsRemove(StringToArray(RegexCleaning(s)))
	terms = {}
	for kata in sBersih:
		if not kata in terms:
			terms[kata] = sBersih.count(kata)
	return terms


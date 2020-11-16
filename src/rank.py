# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"
from terms import *
import collections

# konstanta
FOLDER = os.path.abspath("../test")

query = {'american': 2, 'president': 3}

def GetRank(query):
	# GetRank(query) menerima dictionary dengan 
	# keys bentuk (string query, dokumen ke-i)
	# value berisi jumlah kemunculan 
	# dan mengembalikan array/list berisi tuple
	# (nama file dokumen,
	# jumlah kata semuanya di dokumen, 
	# tingkat kemiripan dokumen dengan query,
	# kalimat pertama dari dokumen)

	# semua kata di lower case dan dibuat list kata2 unik secara berurutan

	# dicopas oleh Wibi dari tabel.py
	kamusKata = KataDalamKamus()
	kataDiDokumen = KataDalamDokumen()
	kalimatPertama = firstsentence()
	banyakDokumen = len(os.listdir(FOLDER))
	kamusDokumen = KamusDokumen(banyakDokumen, kamusKata, kataDiDokumen)

	newdict = dict([((s,i),value) for (i,s),value in kamusDokumen.items()])
	new = collections.OrderedDict(sorted(newdict.items()))
	final = dict([((s,i),value) for (i,s),value in new.items()])

	queryvector = []
	docvector = [[] for i in range(banyakDokumen)]
	simvector = []
	arrmagdocvector = []
	arroftupleresult = []

	count = 0
	dotproduct = 0
	magdocvector = 0
	sim = 0
	prec = 0
	magqueryvector = 0
	iterate = 0
	banyakdokumen = 100

	berlebih = False

	for i in query.values():
		queryvector.append(i)
	for i in queryvector:
		magqueryvector += i ** 2
	magqueryvector = magqueryvector ** 0.5

	iterate = len(queryvector)

	for i in range(banyakDokumen):
		for k in query:
			if (k,i) in final:
				docvector[i].append(final[k,i])
			else:
				docvector[i].append(0)

	for s,i in final:
		if i == prec:
			magdocvector += final[(s,i)] ** 2
		else:
			magdocvector = magdocvector ** 0.5
			arrmagdocvector.append(magdocvector)
			magdocvector = 0
			prec += 1
	arrmagdocvector.append(magdocvector)

	for i in range(banyakDokumen):
		for j in range(len(queryvector)):
			dotproduct += queryvector[j] * docvector[i][j]
		sim = dotproduct/(magqueryvector * arrmagdocvector[i])
		simvector.append(sim)
		dotproduct = 0
		sim = 0


	nkata = kataDiDokumen
	arrfirstsentence = kalimatPertama
	namaFiles = os.listdir(FOLDER)

	for i in range(banyakDokumen):
		arroftupleresult.append((namaFiles[i],len(nkata[i]),simvector[i],arrfirstsentence[i]))
	
	arroftupleresult.sort(key=lambda tup: tup[2], reverse = True)
	return arroftupleresult
	# print(arroftupleresult)

#(GetRank(query))

	# Misal query = 'big big car'

	# {(big, 0): 1, (big, 0): 1}
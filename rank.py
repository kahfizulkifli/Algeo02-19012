# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"
from terms import *
import collections

query = {'equip': 2, 'ethic': 1}

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
	kamusKata = KataDalamKamus(BANYAK_DOKUMEN)
	kataDiDokumen = KataDalamDokumen(BANYAK_DOKUMEN)
	kalimatPertama = firstsentence(BANYAK_DOKUMEN)
	kamusDokumen = KamusDokumen(BANYAK_DOKUMEN, kamusKata, kataDiDokumen)

	newdict = dict([((s,i),value) for (i,s),value in kamusDokumen.items()])
	new = collections.OrderedDict(sorted(newdict.items()))
	final = dict([((s,i),value) for (i,s),value in new.items()])

	queryvector = []
	docvector = []
	simvector = []
	arroftupleresult = []

	count = 0
	dotproduct = 0
	magdocvector = 0
	sim = 0
	prec = 0
	magqueryvector = 0
	iter = 0
	banyakdokumen = 100

	for i in query.values():
		queryvector.append(i)
	for i in queryvector:
		magqueryvector += i ** 2
	magqueryvector = magqueryvector ** 0.5

	iter = len(queryvector)

	for s,i in final:
		for k in query:
			if s == k:
				docvector.append(final[(s,i)])
				count += 1
				if count == iter:
					for j in range(iter):
						dotproduct += queryvector[j] * docvector[j]
					count = 0
		if (i == prec):
			magdocvector += final[(s,i)] ** 2
		else:
			magdocvector = magdocvector ** 0.5
			sim = dotproduct/(magqueryvector * magdocvector)
			simvector.append(sim)
			dotproduct = 0
			sim = 0
			docvector.clear()
			prec += 1
	magdocvector = magdocvector ** 0.5
	sim = dotproduct/(magqueryvector * magdocvector)
	simvector.append(sim)		
	prec += 1

	nkata = kataDiDokumen
	arrfirstsentence = kalimatPertama

	for i in range(prec):
		arroftupleresult.append((('hasil'+str(i+1)+'.txt'),len(nkata[i]),simvector[i],arrfirstsentence[i]))
	
	arroftupleresult.sort(key=lambda tup: tup[2], reverse = True)
	return arroftupleresult
	# print(arroftupleresult)

#GetRank(query, testdata)

	# Misal query = 'big big car'

	# {(big, 0): 1, (big, 0): 1}
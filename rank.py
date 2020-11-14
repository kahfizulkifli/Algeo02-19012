# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"
from tabel import KataDalamDokumen, firstsentence, KamusDokumen, KataDalamKamus, kamusDokumen, kataDiDokumen, kalimatPertama

query = {'big': 2, 'car': 1}
testdata = kamusDokumen

def GetRank(query, testdata):
	# GetRank(query) menerima dictionary dengan 
	# keys bentuk (string query, dokumen ke-i)
	# value berisi jumlah kemunculan 
	# dan mengembalikan array/list berisi tuple
	# (nama file dokumen,
	# jumlah kata semuanya di dokumen, 
	# tingkat kemiripan dokumen dengan query,
	# kalimat pertama dari dokumen)

	# semua kata di lower case dan dibuat list kata2 unik secara berurutan

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

	for i in query.values():
		queryvector.append(i)

	for i in queryvector:
		magqueryvector += i ** 2
	magqueryvector = magqueryvector ** 0.5

	iter = len(queryvector)

	for s,i in testdata:
		for k in query:
			if s == k:
				docvector.append(testdata[(s,i)])
				count += 1
				if count == iter:
					for j in range(iter):
						dotproduct += queryvector[j] * docvector[j]
					count = 0
		if (i == prec):
			magdocvector += testdata[(s,i)] ** 2
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
		print(len(nkata[i]))
		arroftupleresult.append((('hasil'+str(i+1)+'.txt'),len(nkata[i]),simvector[i],arrfirstsentence[i]))
	print(arroftupleresult)

GetRank(query, testdata)

	# Misal query = 'big big car'

	# {(big, 0): 1, (big, 0): 1}
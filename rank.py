# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"

query = {'big': 2, 'car': 1}
testdata = {('ant', 0): 7, ('big', 0): 2, ('car', 0): 1, ('ship', 0): 5, 
			('ant', 1): 5, ('big', 1): 9, ('car', 1): 7, ('ship', 1): 3}

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

	for i in query.values():
		queryvector.append(i)

	magqueryvector = 0

	for i in queryvector:
		magqueryvector += i ** 2
	magqueryvector = magqueryvector ** 0.5

	iter = len(queryvector)

	docvector = []

	count = 0
	dotproduct = 0
	magdocvector = 0
	sim = 0

	prec = 0

	for s,i in testdata:
		for k in query:
			if s == k:
				docvector.append(testdata[(s,i)])
				count += 1
				if count == iter:
					for i in range(iter):
						dotproduct += queryvector[i] * docvector[i]
		if (i == prec):
			magdocvector += testdata[(s,i)] ** 2
		else:
			magdocvector = magdocvector ** 0.5
			sim = dotproduct/(magqueryvector * magdocvector)



GetRank(query, testdata)

	# Misal query = 'big big car'

	# {(big, 0): 1, (big, 0): 1}
# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"

query = ['Donald', 'Trump', 'lost']

def GetRank(terms):
	# GetRank(query) menerima list of terms
	# dan mengembalikan array/list berisi tuple
	# (nama file dokumen,
	# jumlah kata di dokumen, 
	# tingkat kemiripan dokumen dengan query,
	# kalimat pertama dari dokumen)

	# semua kata di lower case dan dibuat list kata2 unik secara berurutan
	file = open("sample.txt", "r")
	data = file.read().lower()
	array = data.split()
	unique_words = list(set(array))
	unique_words.sort()

	
	print(unique_words)
GetRank(query)
	
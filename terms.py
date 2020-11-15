from tabel import *

# boleh nambah import atau variabel global

def GetTerms(query):
	
	queryBersih = StopWordsRemove(StemmingKonten(StringToArray(RegexCleaning(query))))
	terms = {}
	for kata in queryBersih:
		if not terms.has_key(kata):
			terms[kata] = queryBersih.count(kata)
	return terms
	# GetTerms menerima string query dari pengguna
	# dan mengembalikan dictionary dengan key:value pairnya = [KATA]:[KEMUNCULAN KATA]

from tabel import *

# boleh nambah import atau variabel global

def GetTerms(query):
    return StopWordsRemove(StemmingKonten(StringToArray(RegexCleaning(query))))
	# GetTerms menerima string query dari pengguna
	# dan mengembalikan array/list berisi string
	# term-term pada query

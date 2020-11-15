from terms import *
from pprint import pprint
# boleh nambah import atau variabel global
# dokumen-dokumen ada di directory "docs/"


#Fungsi Utama

def GetTabel(query):
    queryToken = StopWordsRemove(StringToArray(RegexCleaning(query))) #misal query = "The sponge in the woods"; hasil akhir = ["sponge","woods"] ("The" dan "in" hilang karena mereka termasuk stopwords)
    #Ga jadi di pake	#queryStemToken = StemmingKonten(queryToken) #dengan contoh yang sama, maka menghasilkan stemming terhadap kata "sponge" dan "woods"; misal hasilnya jadi ["spong","wood"]
    # print("query di GetTabel:",queryToken)
    kamusKata = KataDalamKamusNonStem(BANYAK_DOKUMEN)
    kataDiDokumen = KataDalamDokumenNonStem(BANYAK_DOKUMEN)
    kamusDokumen = KamusDokumen(BANYAK_DOKUMEN, kamusKata, kataDiDokumen)
    # pprint(kamusDokumen)
    tabelFrekuensiQuery = {}
    for i in range(len(queryToken)):
        for j in range(BANYAK_DOKUMEN+1): #+1 karena dalam dictionary ini, juga memuat nilai dari kata dalam query.
            if j == 0: #Kata-kata milik query diwakili oleh indeks j = 0
                tabelFrekuensiQuery[(queryToken[i],j)] = queryToken.count(queryToken[i])
            else: #Untuk tiap dokumen, maka j =1 melambangkan dokumen ke 1, j = 2 dokumen ke 2, dst.
                if (queryToken[i],(j-1)) in kamusDokumen:
                    tabelFrekuensiQuery[(queryToken[i],j)] = kamusDokumen[(queryToken[i],(j-1))]
                else:
                    tabelFrekuensiQuery[(queryToken[i],j)] = 0
    	    
    return tabelFrekuensiQuery
			
			
		
	
	
#Fungsi Tambahan

#-------Dummy--------------
#2 (dua) variabel di bawah ini, digunakan sebagai dummy url untuk melakukan web scrapping

url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
url1 = 'https://www.fox13now.com/news/coronavirus/local-coronavirus-news/utah-considers-thanksgiving-covid-19-recommendations-medical-experts-say-dont-gather'

arrurl = [url, url1]
############################

#-------Fungsi Mainan-------

#Cuma buat ngetes aja, fungsi ini ga kepake di main program. Bisa dihapus kalau mau
def CobaCoba(url, namaFile):
    konten = WebScrappingKontenByUrl(url)
    SaveKontenTxt(namaFile, konten)

#############################

#-------Fungsi Utama---------

#Testing
'''
i = 0
for url in arrurl:
  SaveKontenTxt("hasil"+str(i+1),WebScrappingKontenByUrl(url))
  i += 1

kamusKata = KataDalamKamus(BANYAK_DOKUMEN)
kataDiDokumen = KataDalamDokumen(BANYAK_DOKUMEN)
kalimatPertama = firstsentence(BANYAK_DOKUMEN)
kamusDokumen = KamusDokumen(BANYAK_DOKUMEN, kamusKata, kataDiDokumen)
'''
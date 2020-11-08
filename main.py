from flask import Flask, render_template
from rank.py import GetRank
from tabel.py import GetTabel	
app = Flask(__name__)

@app.route("/")
def HomePage():
	return render_template("home.html")

@app.route("/search-<query>")
def SearchResultsPage(query):
	# convert string query ke list of terms
	terms = GetTerms(query)
	# cosine sim & rank
	rank = GetRank(terms)
	# tabel term
	tabel = GetTabel(terms)
	return render_template("search_results.html", terms=terms, rank=rank, tabel=tabel)

@app.route("/perihal")
def PerihalPage():
	return render_template("perihal.html")

if __name__ == '__main__':
  app.run()
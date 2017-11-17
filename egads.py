import ads
import requests
import json
import numpy as np
from astropy.io import ascii
from astropy.table import Table, Column, MaskedColumn



def query_ads_db(year_published = 1997, rows=10):

	q = ads.SearchQuery(year=year_published, sort='citation_count+desc', database='astronomy', rows=rows)
	bibcodelist = []
	firstauthorlist = []
	publist = []
	for paper in q:
		#print(paper.title, "\t", paper.bibcode, "\t", paper.year, "\t", paper.citation_count)
		bibcodelist.append(paper.bibcode)
		firstauthorlist.append(paper.first_author)
		publist.append(paper.pub)

	return bibcodelist, firstauthorlist, publist



def query_ads_hist(bibcode, token='ept6kgoeYOkWZQDt81RPY4H1oljs4G4nYz1M9Dzw'):
	queryURL = 'https://api.adsabs.harvard.edu/v1/metrics'
	payload = {'bibcodes': [bibcode]}
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization':'Bearer %s' % token}
	r = requests.post(queryURL, data=json.dumps(payload), headers=headers)
	return r



year_published = 1985
year_today = 2017
nb_years = year_today - year_published
nb_papers = 40

# query db
#bibcodelist, keywordlist = query_ads_db(year_published, rows=nb_papers)
bibcodelist, firstauthorlist, publist = query_ads_db(year_published, rows=nb_papers)

# year list
yearlist = np.arange(year_published, year_today)


print("Author Year Citations Journal")
# curl db and add to list
#for bibcode in bibcodelist:
for bibcode, firstauthor, pub in zip(bibcodelist, firstauthorlist, publist):
	response = query_ads_hist(bibcode)#, token='yETR4I5amXo4CMD4dVOZT4FKobTqg2raUxv1sNo')
	histograms = response.json()['histograms']
	citations = histograms['citations']['refereed to refereed']
	if np.sum(np.array(citations)) != 0:
		sums = 0
		for key, value in citations.items():
			sums += value
			print(firstauthor,",", key, ",", sums,",", pub)



	




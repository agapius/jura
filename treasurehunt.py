# coding=utf-8
# is needed for reasons I don't understand
##treasurehunt

# import libraries
import urllib2
import datetime
from bs4 import BeautifulSoup

#functions:
# function readies the string that names the files, removes: non-Ascii chars, dots, and slashes
def remove_non_ascii_1(text):
	new_string = ''.join(i for i in text if ord(i)<128)
	new_string = new_string.replace('.', ' ')
	return new_string.replace('/', ' ')

##give it an overview page and it returns the number of pages
def get_number_of_pages(start):
###this link leads to page 100 (since there is no page 100, one is automatically redirected to the highest page)
	l_start = urllib2.urlopen(start).read()
	b_start = BeautifulSoup(l_start, 'html.parser')
	r_start = b_start.html.thead.tr
###find all page links on the last page (the last page link on the last page is the 'pre-last-page')
	pages = r_start.findAll('a',{"class": "pagelink"})
###pages[-1] gets us the number of the pre-last page. Convert this to an int to do then math with it (+1)
	Nofpages= int(pages[-1].get_text(strip=True))+1
	return Nofpages



##get a list of years that we can loop throuh:
###set first year
year= 2000
now = datetime.datetime.now()
print now.year



url_year="http://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en&Datum="
list_of_year_page_url= []
###loop through all years until now and concatenate a relevant link with the year_url
while year <= now.year:
	url_year="http://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/list.py?Gericht=bgh&Art=en&Datum="+str(year)
	page=0
	nofpages=get_number_of_pages(url_year+'&Seite=100')
	while page <= nofpages:
		url_year_pages= url_year+"&Seite="+str(page)
		list_of_year_page_url.append(url_year_pages)
		page += 1
	year += 1
###result is a list of all the pages in every year from 2000-2018

#loop through all the year-pages 
for url in list_of_year_page_url:
	p = urllib2.urlopen(url)
	soup = BeautifulSoup(p, 'html.parser')
# ab enthält alle download-links, die nicht direkt zum pdf doc führen, wenn '&Blank=1.pdf' angefügt wird, führt die der link direkt zum pdf
	for a in soup.find_all('a', href=True):
		ab = str(a['href']) # the link-part of the a-tag is converted to string
		if 'document' in ab and '.pdf' not in ab:	# there are more links than wanted (e.g to previous or next page).all relevant links start with document and do not end with .pdf (since we want to extract the name first)
			bgh_pdf = 'http://juris.bundesgerichtshof.de/cgi-bin/rechtsprechung/' + ab
			name = urllib2.urlopen(bgh_pdf)
			soup_name = BeautifulSoup(name, 'html.parser')
			name_box = remove_non_ascii_1(soup_name.title.string)    # funktioniert nur in 70% der Fälle, dann bringt es aber den richtigen Namen raus

			bgh_pdf_link = bgh_pdf +'&Blank=1.pdf'
			f = urllib2.urlopen(bgh_pdf_link) 
			name_final = name_box + '.pdf'
			file = open(name_final, 'wb')
			file.write(f.read())
			file.close()





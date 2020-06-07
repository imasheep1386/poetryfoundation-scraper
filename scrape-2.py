"""
PoetryFoundation Scraper

Simple web scraper that scrapes a poet's poems from the PoetryFoundation
website into a single pdf file, formatted for thermal printers.

originally by Eric Li, pdf revision and python3 update Samir Chadha
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
from html.parser import HTMLParser
from fpdf import FPDF

pdf = FPDF('P', 'mm', (60, 200))
pdf.set_auto_page_break(True, margin = 0.0)
pdf.add_font("Gibson", fname="Gibson-Regular.ttf", uni=True)
pdf.add_font("GibsonBold", fname="gibson-bold.ttf", uni=True)
pdf.add_font("Gentium", fname="GentiumPlus-R.ttf", uni=True)



poet = input('Enter a poet: ')

poet = poet.lower()
poetx = re.sub('[^a-z]+','-',poet)



#fileout = poet + ".txt"
#output = open(fileout,'w')


url = "http://www.poetryfoundation.org/bio/"+poetx+"#about"
page = requests.get(url)
soup = BeautifulSoup(page.text, features="html5lib")
parser = HTMLParser()

poems = soup.find_all('a',href=re.compile('.*/poems/[0-9]+/.*'))
poems2 = soup.find_all('a',href=re.compile('.*/poem/.*'))

poems.extend(poems2)

for poem in poems:
		poemURL = poem.get('href')
		poemPage = requests.get(poemURL)
		poemSoup = BeautifulSoup(poemPage.text, features="html5lib")
		poemTitle = poemSoup.find('h1')
		
		if poemTitle:
			pdf.add_page()
			title = parser.unescape(poemTitle.text)
			title = title.strip()
			pdf.set_font("GibsonBold", size=10)
			pdf.multi_cell(0, 4, txt=title, align="L")
#			print(poet.title())
			pdf.set_font("Gibson", size=8)
			pdf.multi_cell(0, 4, txt=poet.upper(), align="L")
			poemContent = poemSoup.find('div', {'class' : 'o-poem'})
			poemLines = poemContent.findAll('div')
			poemBlocks = poemContent.findAll('p')
			for line in poemLines:
				
				text = parser.unescape(line.text)
				pdf.set_font("Gentium", size=8)
				
				l = text
				l = l.strip()
				pdf.multi_cell(0, 4, txt=l, align="L")
				
			for line in poemBlocks:
				para = parser.unescape(line.text)
				pdf.set_font("Gentium", size=8)
				p = para.strip()
				pdf.multi_cell(0, 4, txt=p, align="L")
			filename = poetx + ".pdf"
			filename = filename.encode('utf-8')
			pdf.output(filename, 'F')
#			lp -o fit-to-page filename
				


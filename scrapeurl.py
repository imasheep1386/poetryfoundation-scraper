"""
PoetryFoundation Scraper

Simple web scraper that scrapes a poet's poems from the PoetryFoundation
website into a single pdf file, formatted for thermal printers.

originally by Eric Li, pdf revision, switch to url, and python3 update Samir Chadha
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
from html.parser import HTMLParser
import html
from fpdf import FPDF
import os

pdf = FPDF('P', 'mm', (60, 200))
pdf.set_auto_page_break(True, margin = 0.0)
pdf.add_font("Gibson", fname="Gibson-Regular.ttf", uni=True)
pdf.add_font("GibsonBold", fname="gibson-bold.ttf", uni=True)
pdf.add_font("Gentium", fname="GentiumPlus-R.ttf", uni=True)

url = input('What poem do you want printed? ')
parser = HTMLParser()



poemPage = requests.get(url)
poemSoup = BeautifulSoup(poemPage.text, features="html5lib")
poemTitle = poemSoup.find('h1')
poet = poemSoup.find(class_="c-txt c-txt_attribution")
poet = poet.a.string

if poemTitle:
	pdf.add_page()
	title = html.unescape(poemTitle.text)
	title = title.strip()
	pdf.set_font("GibsonBold", size=10)
	pdf.multi_cell(0, 4, txt=title, align="L")
	pdf.set_font("Gibson", size=8)
	pdf.multi_cell(0, 4, txt=poet.upper(), align="L")
	poemContent = poemSoup.find('div', {'class' : 'o-poem'})
	poemLines = poemContent.findAll('div')
	poemBlocks = poemContent.findAll('p')
	for line in poemLines:
		text = html.unescape(line.text)
		pdf.set_font("Gentium", size=8)
		l = text
		l = l.strip()
		pdf.multi_cell(0, 4, txt=l, align="L")
		
	for line in poemBlocks:
		para = parser.unescape(line.text)
		pdf.set_font("Gentium", size=8)
		p = para.strip()
		pdf.multi_cell(0, 4, txt=p, align="L")
	filenam = title.replace(" ", "") + ".pdf"
	filename = filenam.encode('utf-8')
	pdf.output(filename)
	os.system('lp -o ' + str(filenam))
		


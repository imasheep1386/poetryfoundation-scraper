"""
PoetryFoundation Scraper

Simple web scraper that scrapes a poet's poems from the PoetryFoundation
website into a single txt file.

Eric Li
"""

from __future__ import print_function
from bs4 import BeautifulSoup
import requests
import re
from html.parser import HTMLParser

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
			print(parser.unescape(poemTitle.text))
			print(poet.title())
			poemContent = poemSoup.find('div', {'class' : 'o-poem'})
			poemLines = poemContent.findAll('div')
			poemBlocks = poemContent.findAll('p')
			for line in poemLines:
				
				text = parser.unescape(line.text)
				print(str(text))
			for line in poemBlocks:
				para = parser.unescape(line.text)
				print(str(para)) 
				

"""
for poem in poems:

    poemURL = poem.get('href')
    poemPage = requests.get(poemURL)
    poemSoup = BeautifulSoup(poemPage.text, features="html5lib")
    
    poemTitle = poemSoup.find('h1')
    
    if poemTitle:
        print(parser.unescape(poemTitle.text).encode('utf8'),file=output)
        
        poemContent = poemSoup.find('div',{'class':'o-poem'})
        poemLines = poemContent.findAll('div')
        for line in poemLines:
            text = parser.unescape(line.text)
            out = text.encode('utf8')
            print(out,file=output)
      
        """  

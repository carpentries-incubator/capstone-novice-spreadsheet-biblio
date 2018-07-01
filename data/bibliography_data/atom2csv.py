#!/usr/bin/env python3


from lxml import etree

ns = {"atom": "http://www.w3.org/2005/Atom"}


parser = etree.XMLParser(remove_blank_text=True) 

doc = etree.parse("share.osf.io.xml", parser)
root = doc.getroot()

allEntries=[]
count=0
for x in doc.xpath('//atom:entry', namespaces=ns):
	entry={}
	count+=1
	entry["title"]=x[0].text
	entry["link"]=x[1].get("href")
	entry["author"]='; '.join([name.text for name in x[4]])
	allEntries.append(entry)
	
print(len(entry), count)	
print(entry)

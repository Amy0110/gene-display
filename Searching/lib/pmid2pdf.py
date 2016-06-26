import requests
import os
import sys
import re
import codecs
from bs4 import BeautifulSoup


class P2P:
	def __init__(self, PMDID):
		if not re.match("^\d+$", PMDID):
			raise TypeError("Not a PMDID!")
		self.PMDID = PMDID
	
	def __linkout(self):
		self.url = "http://www.ncbi.nlm.nih.gov/pubmed/" + self.PMDID
		r = requests.get(self.url)
		soup = BeautifulSoup(r.text, 'html.parser')
		#get title
		title = soup.find("div", {"class":"cit"})
		self.title = ""
		if title:
			print "true"
			self.title = title.find_next_sibling("h1").string.strip()
		#get abstract
		abstr = soup.find("div", {"class":"abstr"})
		self.abstr = ""
		if abstr:
			print "true"
			for string in abstr.strings:
				self.abstr += string.strip()
			if self.abstr.startswith("Abstract"):
				self.abstr.lstrip("Abstract")
		#check if provides free full text
		if not soup.find(text = re.compile("(Free full text)|(Free PMC Article)")):
			print "Free full text not provided!"
			return {}
		Linkout = {}
		t1 = soup.find("h4", text = re.compile("Full Text Sources"))
		t2 = t1.find_next_sibling("ul") if t1 else None
		if t2:
			for t3 in t2.find_all("a"):
				name = t3.string.strip()
				Linkout[name] = t3['href']
		return Linkout
	
	def __path2url(self, url, path):
		return re.match("https?://[\w\.]+", url).group(0) + path

	def __fromdb(self, db, url, fd):
		if db == "Wiley":
			return self.__fromWiley(url, fd)
		try:
			args, kwargs = self.__pattern(db)
		except ValueError:
			print "%s not include." % db
		  	return False	
		r = requests.get(url, verify = False)
		soup = BeautifulSoup(r.text, 'html.parser')
		link = soup.find(args, kwargs)
		if link:
			link = link['href']
			#fix if not a url
			if not link.startswith("http"):
				link = self.__path2url(r.url, link)
			#fix link which ends with "html"
			if link.endswith(".pdf+html"):
				link = link.rstrip("+html")
			print link
			r = requests.get(link, stream = True)
			for chunk in r.iter_content():
				if chunk:
					fd.write(chunk)
			return True
		else:
			print "pattern not found."
			return False

	def __pattern(self, db):
		if db == "Public Library of Science":
			return "a", {"id":"downloadPdf"}
		elif db.startswith("PubMed Central"):
			return "a", {"href":re.compile("/pmcc?/articles/\S+\.pdf$")}
		#27178303
		elif db == "BioMed Central":
			return "a", {"id":"articlePdf"}
		#27178246
		elif db.startswith("HighWire"):
			return "a", {"href":re.compile("\.full\.pdf")}
		#27177090
		elif db == "Impact Journals, LLC":
			return "a", {"href":re.compile("op=download")}
		#27175853
		elif db == "eLife Sciences Publications, Ltd":
			return "a", {"href":re.compile("download\.pdf")}
		else:
			raise ValueError
	
	def __fromWiley(self, url, fd):
		r = requests.get(url)
		soup = BeautifulSoup(r.text, 'html.parser')
		t = soup.find(href = re.compile("/pdf"))
		if t:
			link = t['href']
			if not link.startswith("http"):
				link = self.__path2url(r.url, link)
		r = requests.get(link)
		pdflink = re.search('src="(\S+\.pdf\S+)"', r.text).group(1)
		r2 = requests.get(pdflink, stream = True)
		for chunk in r2.iter_content():
			if chunk:
				fd.write(chunk)
		return True

	def __call__(self):
		filename = "%s.pdf" % self.PMDID
		filepath = "./pdf/" + filename
		if os.path.exists(filepath):
			print "%s already exists!" % filename
			return
		try:
			fd = open(filepath, "wb")
			print "downloading pubmed article : %s" % self.PMDID
			success = False
			Linkout = self.__linkout()
			for name, url in Linkout.items():
				if not success:
					print "try access from %s......" % name
					success = self.__fromdb(name, url, fd)
				else:
					break
		finally:
			fd.close()
			with codecs.open("info.txt", "a", encoding="utf-8") as f:
				f.write(self.PMDID + "\t" + self.title + "\t" + self.url + "\t" + self.abstr +"\n")
			if not success:
				print "download not succeed."
				os.remove(filepath)
			else:
				print "download succeed."

if __name__ == "__main__":
	assert len(sys.argv) == 2
	PMDIDs = sys.argv[1].split(",")
	for ID in PMDIDs:
		P2P(ID)()
			

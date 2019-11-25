from queue import Queue
from threading import  Thread
import requests
from bs4 import BeautifulSoup
import dateparser
from lxml import etree

from flights import flights
import os

def processZodiacs(lib_dir):
    lib = lib_dir
    xslt_files = [f for f in os.listdir(lib) if os.path.isfile(os.path.join(lib, f)) and f.rfind('.xslt')]
    for f in xslt_files:
        libpath = "%s/%s" % (lib, f)
        xslt = etree.parse(libpath)
        uri_template = xslt.find("{http://www.w3.org/1999/XSL/Transform}variable[@name='uri']").text.strip()
        zodiacs = xslt.find("{http://www.w3.org/1999/XSL/Transform}variable[@name='zodiacs']").text.strip()
        for z in zodiacs.split(" "):
            yield [uri_template % z, xslt]

def scraper_worker(q, data):
    task = q.get()
    try:
        scrape_result = scrape(task)
        data.append(scrape_result)
    except FileNotFoundError:
        print(task["url"] + " not found")

def scrape(task):
    url = task["url"]
    r = requests.get(url)
    if r.status_code != 200:
        raise FileNotFoundError

    html = r.text
    soup = BeautifulSoup(html, 'lxml')
    data = {}
    try:
        date_element = soup.select_one(task["date"]["css"])
        date_string = task["date"]["parse"](date_element.text)
        date = dateparser.parse(date_string, languages=[task["lang"]])
        data["date"] = date
    except AttributeError:
        print("Error: %s date not found" % url)

    return data

def main_scraper(flights):
  print("main scraper was called, got: ")
  print(flights)
  data = []
  q = Queue()
  for flight in flights:
      q.put(flight)
  for i in range(0,  5):
      t = Thread(target = scraper_worker, args = (q, data))
      t.daemon = True
      t.start()
  q.join()
  return data

if __name__ == "__main__":
    main_scraper(flights)

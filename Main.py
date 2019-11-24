from queue import Queue
from threading import  Thread
import requests
from bs4 import BeautifulSoup
import dateparser
from flights import flights


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

import sys
import time
from unittest import mock

import pytest
from unittest.mock import MagicMock, patch
from queue import Queue
from bottle import get, static_file, run
import requests
import os
from Main import flights, scrape
from threading import  Thread
from urllib import parse


def download_and_save(uri):
    parsed_uri = parse.urlparse(uri)
    uri = parse.urlunparse(parsed_uri)
    r = requests.get(uri)
    if (r.status_code != 200):
        parsed_uri = parsed_uri._replace(scheme="http")
        uri = parse.urlunparse(parsed_uri)
        r = requests.get(uri)
    if(r.status_code != 200):
        raise FileNotFoundError

    filename = os.path.basename("html/%s/%s" % (parsed_uri.netloc, parsed_uri.path.strip('/')))
    path = os.path.dirname("html/%s/%s" % (parsed_uri.netloc, parsed_uri.path.strip('/')))
    os.makedirs(path, 0o777, True)
    file = open(path + '/' + filename, "wb")
    file.write(r.content)
    file.close()

def replace_url(url):
    parsed_uri = parse.urlparse(url)
    replaced = parsed_uri._replace(scheme="http", netloc="localhost:8088/" + parsed_uri.netloc)
    return  parse.urlunparse(replaced).rstrip('/')

def setup_module(module):
    for f in flights:
        f["url"] = replace_url(f["url"])

    @get("/")
    def index():
        return static_file("index.html", root="html")

    @get("/<provider>/<uri:path>/")
    @get("/<provider>/<uri:path>")
    def cache(provider, uri):
        path_file = "html/%s/%s" % (provider, uri)
        path = os.path.dirname(path_file)
        filename = os.path.basename(path_file)
        if not os.path.isfile(path_file):
             download_and_save("https://%s/%s" % (provider, uri))
        return static_file(filename, root=path)

    def start_proxy():
        run(host='127.0.0.1', port=8088, debug=True)

    global proxy_thread
    proxy_thread = Thread(target=start_proxy)
    proxy_thread.start()
    time.sleep(0.2)

def teardown_module():
    global proxy_thread
    print ("Press CTRL+C to stop")
    proxy_thread.join()

def test_downloadAndSave():
    for f in flights:
        r = requests.get(f["url"])
        assert r.status_code == 200

def test_CacheAllSites():
    results = {}
    for f in flights:
        try:
            scrape_result = scrape(f)
            results[f["name"]] = scrape_result
        except FileNotFoundError:
            pytest.fail(f["url"] + " not found")
    pass

import time
import pytest
from bottle import get, static_file, run
import requests
import os
from threading import  Thread
from urllib import parse
from lxml import etree
from bs4 import BeautifulSoup

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

    filename = os.path.basename("html/%s/%s.html" % (parsed_uri.netloc, parsed_uri.path.strip('/')))
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
    @get("/")
    def index():
        return static_file("index.html", root="static")

    @get("/<file>")
    def index(file):
        return static_file(file, root="static")

    @get("/<provider>/<uri:path>/")
    @get("/<provider>/<uri:path>")
    def cache(provider, uri):
        path_file = "html/%s/%s.html" % (provider, uri)
        path = os.path.dirname(path_file)
        filename = os.path.basename(path_file)
        if not os.path.isfile(path_file):
             download_and_save("https://%s/%s" % (provider, uri))
        return static_file(filename, root=path)

    def start_proxy():
        run(host='127.0.0.1', port=8088)

    global proxy_thread
    proxy_thread = Thread(target=start_proxy)
    proxy_thread.start()
    time.sleep(0.2)

def teardown_module():
    global proxy_thread
    print ("Press CTRL+C to stop")
    proxy_thread.join()

def test_transformXSLTforOne():
    base_url = replace_url("https://www.horoscope.com/us/horoscopes/general/horoscope-general-daily-today.aspx?sign=12")
    xslt = etree.parse('../lib/horoscopecom.xslt')
    from Main import downloadAndTransform
    newdom_string = downloadAndTransform(base_url, xslt)

    os.makedirs("transformed", 0o777, True)
    f = open("transformed/out.html", "w")
    f.write(newdom_string)
    f.close()

#@pytest.mark.skip()
def test_downLoadAllZodiacsFromXSLTVariable():
    from Main import processZodiacs
    for uri, xslt in processZodiacs('../lib'):
        u = replace_url(uri)
        from Main import downloadAndTransform
        newdom_string = downloadAndTransform(u, xslt)

        uri = parse.urlparse(uri)
        fs_path = ("transformed/%s/%s.html" % (uri.netloc,uri.path)).lstrip('/')
        fs_dir = os.path.dirname(fs_path).lstrip('/')

        if not os.path.isdir(fs_dir):
            os.makedirs(fs_dir, mode=0o777, exist_ok=True)

        f = open(fs_path, 'w')
        f.write(newdom_string)
        f.close()
        assert os.path.getsize(fs_path) > 0

    pass
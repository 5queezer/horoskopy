import time
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
        return static_file("index.html", root="html")

    @get("/<file>")
    def index(file):
        return static_file(file or "index.html", root="html")

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

def test_transformXSLTforOneHoroskope():
    base_url = replace_url("https://www.astroportal.com/tageshoroskope/fische/")
    r = requests.get(base_url)
    assert r.status_code == 200

    html_soup = BeautifulSoup(r.text, 'lxml')
    html = str(html_soup).strip()
    assert len(html) > 0

    dom = etree.HTML(html, base_url=base_url)
    xslt = etree.parse('../lib/astroportal.xslt')
    transform = etree.XSLT(xslt)
    newdom = transform(dom, origin="'%s'" % base_url)
    newdom_string = str(newdom)

    os.makedirs("transformed", 0o777, True)
    f = open("transformed/out.html", "w")
    f.write(newdom_string)
    f.close()
    f = open("transformed/aw.html", "wb")
    f.write(etree.tostring(dom, pretty_print=True))
    f.close()

def test_downLoadAllZodiacsFromXSLTVariable():
    from Main import processZodiacs
    for uri, xslt in processZodiacs('../lib'):
        # build url and download
        u = replace_url(uri)
        r = requests.get(u)
        assert r.status_code == 200

        # load html into xml parser
        html_soup = BeautifulSoup(r.text, 'lxml')
        html = str(html_soup).strip()
        assert len(html) > 0

        # load xslt and transform to xml
        dom = etree.HTML(html, base_url=uri)
        transform = etree.XSLT(xslt)
        newdom = transform(dom, origin="'%s'" % uri)
        newdom_string = str(newdom)
        assert len(newdom_string) > 0

        uri = parse.urlparse(uri)
        fs_path = ("transformed/%s/%s/.html" % (uri.netloc,uri.path)).lstrip('/')
        fs_dir = os.path.dirname(fs_path).lstrip('/')

        if not os.path.isdir(fs_dir):
            os.makedirs(fs_dir, mode=0o777, exist_ok=True)

        f = open(fs_path, 'w')
        f.write(newdom_string)
        f.close()
        assert os.path.getsize(fs_path) > 0

    pass
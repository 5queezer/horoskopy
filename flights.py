
flights = [
    {
        "name": "Astrolantis daily",
        "url": "https://www.astrolantis.de/tageshoroskop-fische.php",
        "lang": "de",
        "title": None,
        "date": {
            "css": ".horoscope-item-date",
            "parse": (lambda string: string.replace('Tageshoroskop für den ',''))
        }
    },
    {
        "name": "Astroportal daily",
        "url": "https://www.astroportal.com/tageshoroskope/fische/",
        "lang": "de",
        "date": {
            "css": "#c23 > div:nth-child(1) > h2:nth-child(6)"  ,
            "parse": (lambda string: string.replace('für ',''))
        }
    }
]
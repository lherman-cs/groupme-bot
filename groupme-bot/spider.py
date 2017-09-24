from os.path import dirname, abspath, join
from os import getcwd

from bs4 import BeautifulSoup
import requests


class Spider():
    search_engine_url = 'https://stackoverflow.com'
    search_url_template = search_engine_url + '/search?q={}'

    def __init__(self):
        pass

    def result_links(self, sentence):
        r = requests.get(self.search_url_template.format(sentence))

        if r.status_code == 200:
            raw = r.text
            bs = BeautifulSoup(raw, "lxml")
            for result in bs.select("div.summary > div.result-link > span > a"):
                yield result.get("href")

    def collect(self, sentence):
        cntr = 0
        results = []
        for result_link in self.result_links(sentence):
            if cntr == 3:
                break
            results.append(self.search_engine_url + result_link)
            cntr += 1

        return results

import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from pathlib import Path

headers = {
    'Accept-Language': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
}

class WebPage:


    def __init__(self, url):
        self.url = url
        self.content = self.get_content(url)


    def get_pdf_urls(self):
        _refs = self.content.find_all('a', href=True)
        _prd_refs = [urljoin(self.url, ref['href']) for ref in _refs if '.pdf' in ref['href'].lower()]
        logging.info(f'{len(_prd_refs)} pdfs found')
        print(f'{len(_prd_refs)} pdfs found')
        return _prd_refs

    def download_pdf(self, ref, directory='.'):
        if not os.path.exists(directory):
            os.makedirs(directory)
        _fname = os.path.basename(ref).split('?')[0]
        _fpath = os.path.join(directory, _fname)
        response = requests.get(ref, headers=headers)
        with open(_fpath, 'wb') as pdf:
            pdf.write(response.content)

    @staticmethod
    def get_content(url):
        response = requests.get(url, headers=headers)
        if not response.ok:
            logging.error(response.status_code, response.text)
            return
        return BeautifulSoup(response.content, 'html.parser')


if __name__ == '__main__':
    webpage = WebPage('https://www.hslu.ch/de-ch/technik-architektur/studium/bachelor/digital-construction/')
    urls = webpage.download_pdfs(directory='/Users/oliviergisiger/Desktop/hslu-pdfs')
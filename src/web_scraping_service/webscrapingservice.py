from typing import Generator, Union, Tuple, List
import bs4
import requests
from datetime import datetime
from src.web_scraping_service.iwebscarpingservice import IWebScrapingService


class WebScrapingService(IWebScrapingService[bs4.BeautifulSoup]):
    def __init__(self, url: str):
        self.__url = url
        self.__soup = self.conectar_url()
        self.__ano_atual = datetime.now().year

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url

    def conectar_url(self) -> Tuple[bool, Union[bs4.BeautifulSoup, str]]:
        try:
            response = requests.get(self.__url)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            return True, soup
        except Exception as e:
            return False, 'Erro'

    def obter_lista_sites(self, dados_site: bs4.BeautifulSoup) -> Generator[str, None, None]:
        if isinstance(dados_site, bs4.BeautifulSoup):
            sites = dados_site.find_all('li')

            lista_sites = [
                link['href']
                for site in sites
                if isinstance(site, bs4.Tag)
                   and (link := site.find("a"))
                   and isinstance(link, bs4.Tag)
                   and 'href' in link.attrs
                   and isinstance(link['href'], str)
                   and link['href'].startswith('https://')
            ]
            print(len(lista_sites))

            yield from lista_sites

    def obter_links_csv(
            self,
            dados_site: bs4.BeautifulSoup,
            flag_carga_completa: bool = True) \
            -> Generator[str, None, None]:
        lista_links = dados_site.find_all(
            'a',
            class_='resource-url-analytics',

        )

        links_csv = [
            link['href']
            for link in lista_links
            if isinstance(link, bs4.element.Tag)
               and isinstance(link['href'], str)
               and link['href'].endswith('csv')
        ]

        yield from links_csv


if __name__ == '__main__':
    wss = WebScrapingService(
        url='https://dados.ons.org.br/dataset/balanco-energia-subsistema'
    )

    flag, soup = wss.conectar_url()

    for link_csv in wss.obter_links_csv(dados_site=soup):
        print(link_csv)

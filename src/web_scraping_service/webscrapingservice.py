from typing import Generator, Union, Tuple, List
import bs4
import re
import requests
from datetime import datetime
from src.web_scraping_service.iwebscarpingservice import IWebScrapingService


class WebScrapingService(IWebScrapingService[bs4.BeautifulSoup]):
    def __init__(self, url: str):
        self.__url = url
        self.__soup = self.conectar_url()
        self.__data = datetime.now()

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str):
        self.__url = url

    def conectar_url(self) -> Tuple[bool, Union[bs4.BeautifulSoup, str]]:
        """
            Método para conectar na url
            :return: Retorna uma flag indicando sucesso ou falha e a conexão Beautifull soup junto com alguma mensagem
            :rtype: Tuple[bool, Union[bs4.BeautifulSoup, str]]
        """
        try:
            response = requests.get(self.__url)
            html = response.text
            soup = bs4.BeautifulSoup(html, 'html.parser')
            return True, soup
        except Exception as e:
            return False, 'Erro'

    def obter_lista_sites(self, dados_site: bs4.BeautifulSoup) -> Generator[str, None, None]:
        """
            Obtem a lista de sites
        :param dados_site: a conexão obtida usando beautifull soup
        :type dados_site: bs4.BeautifulSoup
        :return: Um generator com as urls
        :rtype: Generator[str, None, None]
        """

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

    def __verifica_url(self, url):
        padrao_dia = r"_\d{4}_\d{2}_\d{2}\."
        padrao_ano_mes = r"_\d{4}_\d{2}\."
        padrao_ano = r"_\d{4}\."

        if re.search(padrao_dia, url):
            return 1
        elif re.search(padrao_ano_mes, url):
            return 2
        elif re.search(padrao_ano, url):
            return 3
        else:
            return 4

    def obter_links_csv(
            self,
            dados_site: bs4.BeautifulSoup,
            flag_carga_completa: bool = True) \
            -> Generator[str, None, None]:
        lista_links = dados_site.find_all(
            'a',
            class_='resource-url-analytics',

        )
        """
            Método para obter os links de conexão em csv
            :param dados_site: dados da conexão Beautiful soup
            :type dados_site: bs4.BeautifulSoup
            :param flag_carga_completa: Flag para indicar carga completa True para carga completa e falso para alterados
            :type flag_carga_completa: bool
            :return: Um generator com os links csv
            :rtype: Generator[str, None, None]
        """

        links_csv = [
            link['href']
            for link in lista_links
            if isinstance(link, bs4.element.Tag)
               and isinstance(link['href'], str)
               and link['href'].endswith('csv')
               and (
                       (
                           f'{self.__data.year}' in link['href']
                           if self.__verifica_url(url=link['href']) == 3
                           else (
                               f'{self.__data.year}' in link['href'] and
                               f'{self.__data.month}' in link['href']
                               if self.__verifica_url(url=link['href']) == 2
                                  and str(self.__data.month).zfill(2) in link['href']
                               else (
                                   f'{self.__data.year}' in link['href'] and
                                   f'{self.__data.month}' in link['href'] and
                                   f'{self.__data.day}' in link['href']
                                   if self.__verifica_url(url=link['href']) == 1
                                      and str(self.__data.month).zfill(2) in link['href']
                                      and str(self.__data.day).zfill(2) in link['href'] else
                                   (
                                       link['href']
                                       if self.__verifica_url(url=link['href']) == 4
                                       else ''
                                   )
                               )
                           )
                       )
                       or flag_carga_completa
               )
        ]
        yield from links_csv


# if __name__ == '__main__':
#     lista_urls = [
#         'https://dados.ons.org.br/dataset/balanco-energia-subsistema',
#         'https://dados.ons.org.br/dataset/disponibilidade_usina',
#         'https://dados.ons.org.br/dataset/geracao-usina-2',
#         'https://dados.ons.org.br/dataset/programacao_diaria',
#         'https://dados.ons.org.br/dataset/ind_confiarb_ccal'
#     ]
#     for url in lista_urls:
#         print('*' * 10)
#         print(url)
#         wss = WebScrapingService(
#             url=url
#         )
#
#         flag, soup = wss.conectar_url()
#
#         for link_csv in wss.obter_links_csv(dados_site=soup, flag_carga_completa=False):
#             print(link_csv)

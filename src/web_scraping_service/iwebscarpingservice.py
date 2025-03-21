from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Generator, Tuple, Union, Optional
import requests

T = TypeVar('T')


class IWebScrapingService(ABC, Generic[T]):


    @abstractmethod
    def conectar_url(self) -> T:
        pass

    @abstractmethod
    def obter_lista_sites(self, dados_site: T) -> Generator[str, None, None]:
        pass

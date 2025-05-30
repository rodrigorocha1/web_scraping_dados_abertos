import pyodbc
from src.banco_service.idb_config import IDBConfig
from src.banco_service.dbconfigsqlserver import DbConfigSQLServer
from src.banco_service.iconexao import IConexao


class ConexaoBanco(IConexao[pyodbc]):
    """
    Classe para conectar no banco
    """
    _instancia = None

    def __new__(cls, config: IDBConfig, *args, **kwargs, ) -> "ConexaoBanco":
        """
        Método para controlar a conexão do banco de dados

        :param config: Recebe a string de conexão de qualquer banco
        :type config: IDBConfig
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        """

        if cls._instancia is None:
            cls._instancia = super(ConexaoBanco, cls).__new__(cls)
            try:
                cls._instancia.conexao = pyodbc.connect(config.obter_conexao_string())  # type: ignore
            except pyodbc.Error as e:
                return f"Falha na conexão com o banco de dados: {e}"

        return cls._instancia

    def obter_conexao(self) -> pyodbc.Connection:
        """
            Método pra obter a conexão
        :return: Retorna a conexão
        :rtype: pyodbc.Connection
        """

        return self.conexao  # type: ignore


if __name__ == "__main__":
    a = ConexaoBanco(DbConfigSQLServer())
    a.obter_conexao()

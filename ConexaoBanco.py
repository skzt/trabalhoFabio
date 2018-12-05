import pymysql as sql
from json import load as jsonLoad


class ConexaoBanco:
    def __new__(cls):
        """
        Singleton que garante que apenas uma instacia de ConexaoBanco seja criada.
        Caso já exista uma instancia, ela é retornada e não é criada uma nova.

        :return: A unica instancia de ConxaoBanco.
        """
        # Caso não haja uma instancia de singleton, criar uma nova.
        if hasattr(cls, '_instancia') is False:
            cls._instancia = super(ConexaoBanco, cls).__new__(cls)
            with open("config.json", 'r') as file:

                configs = jsonLoad(file)
                cls._DB = sql.connect(configs["hostBanco"],
                                      configs["loginBanco"],
                                      configs["senhaBanco"],
                                      configs["dataBase"])
                file.close()
        # Retorna uma instancia nova, caso ela tenha sido criada
        # Ou retorna a unica instancia que já foi criada.
        return cls._instancia

    def cursor(self):
        return self._DB.cursor()

    def close(self):
        self._DB.close()

    def commit(self):
        self._DB.commit()

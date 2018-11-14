import pymysql as sql
from Config import getDBinfo


class ConexaoBanco:
    def __new__(cls):
        # Caso não haja uma instancia de singleton, criar uma nova.
        if hasattr(cls, '_instancia') is False:
            cls._instancia = super(ConexaoBanco, cls).__new__(cls)

        # Retorna uma instancia nova, caso ela tenha sido criada
        # Ou retorna a unica instancia que já foi criada.
        return cls._instancia

    def __init__(self):
        dbinfo = getDBinfo()
        self._DB = sql.connect(dbinfo[0], dbinfo[1], dbinfo[2], dbinfo[3])

    def cursor(self):
        return self._DB.cursor()

    def close(self):
        self._DB.close()

    def commit(self):
        self._DB.commit()

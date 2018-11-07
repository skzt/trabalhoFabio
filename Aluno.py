from Matricula import Matricula


class Aluno:
    def __init__(self, janelaPrincipal, idAluno, nome, cpf, dataNasc, curso):
        self.janelaPrincipal = janelaPrincipal
        self.__idAluno = idAluno
        self.__nome = nome
        self.__cpf = cpf
        self.__dataNasc = dataNasc
        self.__curso = curso
        self.__matriculado = Matricula(self.janelaPrincipal, self.__idAluno, self.curso)
        self.__logado = False

    def solicitarMatricula(self):
        self.__matriculado.solicitarMatricula()

    def cancelarMatricula(self):
        self.__matriculado.cancelarMatricula()

    def verHistorico(self):
        self.__matriculado.verHistorico()

    def deslogar(self):
        self.janelaPrincipal = None
        self.__idAluno = None
        self.nome = None
        self.cpf = None
        self.dataNasc = None
        self.curso = None
        self.__matriculado = None
        self.logado = False

    def __del__(self):
        print("OIIII ALUNO")

    # <editor-fold desc="Property Aluno">
    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        self.__nome = nome

    @property
    def cpf(self):
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf):
        self.__cpf = cpf

    @property
    def dataNasc(self):
        return self.__dataNasc

    @dataNasc.setter
    def dataNasc(self, dataNasc):
        self.__dataNasc = dataNasc

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, curso):
        self.__curso = curso

    @property
    def logado(self):
        return self.__logado

    @logado.setter
    def logado(self, logado):
        self.__logado = logado
    # </editor-fold>

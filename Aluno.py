from Matricula import Matricula


class Aluno:
    def __init__(self, janelaPrincipal, idAluno, nome, cpf, dataNasc, curso):
        self._janelaPrincipal = janelaPrincipal
        self._idAluno = idAluno
        self._nome = nome
        self._cpf = cpf
        self._dataNasc = dataNasc
        self._curso = curso
        self._matriculado = Matricula(self._janelaPrincipal, self._idAluno, self.curso)
        self._logado = False

    def solicitarMatricula(self):
        self._matriculado.solicitarMatricula()

    def cancelarMatricula(self):
        self._matriculado.cancelarMatricula()

    def verHistorico(self):
        self._matriculado.verHistorico()

    #def deslogar(self):
     #   self._janelaPrincipal = None
      #  self._idAluno = None
       # self.nome = None
    #    self.cpf = None
    #    self.dataNasc = None
    #    self.curso = None
    ##    self._matriculado.deslogar()
    #    self._matriculado = None
    #    self.logado = False



    def __del__(self):
        del self._matriculado
        print("OIIII ALUNO")

    # <editor-fold desc="Property Aluno">
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, cpf):
        self._cpf = cpf

    @property
    def dataNasc(self):
        return self._dataNasc

    @dataNasc.setter
    def dataNasc(self, dataNasc):
        self._dataNasc = dataNasc

    @property
    def curso(self):
        return self._curso

    @curso.setter
    def curso(self, curso):
        self._curso = curso

    @property
    def logado(self):
        return self._logado

    @logado.setter
    def logado(self, logado):
        self._logado = logado
    # </editor-fold>

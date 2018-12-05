from Matricula import Matricula


class Aluno:
    def __init__(self, janelaPrincipal, idAluno, nome, cpf, dataNasc, curso):
        """
        Classe responsavel por armazenar as informações referentes ao Aluno.
        :var self._matriculado: Referencia a fachada responsavel por Manter, Processar e Apresentar as informações
        de matricula do aluno, como Historico, efetuar Matricula no semestre, etc...
        :param janelaPrincipal: Referencia a janela principal do programa.
        :param idAluno: Identificado do Aluno.
        :param nome: Nome do Aluno.
        :param cpf: CPF do Aluno.
        :param dataNasc: Data de Nascimento do Aluno.
        :param curso: Curso do Aluno.
        """
        self._janelaPrincipal = janelaPrincipal

        self._idAluno = idAluno
        self._nome = nome
        self._cpf = cpf
        self._dataNasc = dataNasc
        self._curso = curso

        self._matriculado = Matricula(self._janelaPrincipal, self._idAluno, self.curso)

    def solicitarMatricula(self):
        """
        Metodo publico, responsavel por solicitar a fachada a realização da matricula.
        :return: VOID
        """
        self._matriculado.solicitarMatricula()

    def cancelarMatricula(self):
        """
            Metodo publico, responsavel por solicitar a fachada o cancelamento da matricula em alguma disciplina.
            :return: VOID
        """
        self._matriculado.cancelarMatricula()

    def verHistorico(self):
        """
            Metodo publico, responsavel por solicitar a fachada a visualização do historico.
            :return: VOID
        """
        self._matriculado.verHistorico()

    def deslogar(self):
        """
            Metodo publico, responsavel por encerrar o processamento para encerrar a sessão.
            :return: VOID
        """
        self._matriculado.deslogar()

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

    # </editor-fold>

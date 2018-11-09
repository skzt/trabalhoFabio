import tkinter as tk
import tkinter.ttk as ttk
from time import strftime
from ConexaoBanco import ConexaoBanco
from FramesMatricula import FramesMatricula


class Matricula:
    def __init__(self, janelaPrincipal, idAluno, curso):
        self.janelaPrincipal = janelaPrincipal
        self.__curso = curso
        self.__idAluno = idAluno

        self.DB = ConexaoBanco()
        self._frameSolicitacao = None
        self._frameCancelamento = None
        self._frameHistorico = None
        self._frameHorario = None

        # self.carregarDisciplinas()

    def solicitarMatricula(self):
        metodos = {"mudarSemestre": self._mudarSemestre,
                   "confirmarSolicitacao": self._confirmarSolicitacao
                   }
        if self._frameSolicitacao is None:
            self._frameSolicitacao = FramesMatricula(self.janelaPrincipal, metodos)
        self._frameSolicitacao.frameSolicitar()
        #self._frameSolicitacao.grid(row=0, column=1, sticky='n')

    def cancelarMatricula(self):
        metodos = {"confirmarCancelamento": self._confirmarCancelamento}

        if self._frameCancelamento is None:
            self._frameCancelamento = FramesMatricula(self.janelaPrincipal, metodos)
            self._carregarProcessando()
        self._frameCancelamento.frameCancelar()
        #self._frameCancelamento.grid(row=0, column=1, sticky='n')

    def _carregarProcessando(self):
        """
        Verificar se existe alguma disciplina deste aluno com situação == PROCESSANDO
        e popula a lista _frameCancelamento._listaDisciplinas com essas disciplinas, se houver.
        :return: VOID
        """

        cursor = self.DB.cursor()

        select = ''' SELECT DISCIPLINA.codigo, DISCIPLINA.nome
        FROM DISCIPLINA
               JOIN DISCIPLINA_ALUNO
                 ON DISCIPLINA.idDisciplina = DISCIPLINA_ALUNO.idDisciplina
        WHERE DISCIPLINA_ALUNO.idAluno = %d
          AND DISCIPLINA_ALUNO.situacao = 1;''' % self.__idAluno

        cursor.execute(select)
        disciplinasProcessadas = cursor.fetchall()

        if len(disciplinasProcessadas) == 0:
            # Não possui disciplinas com status PROCESSANDO
            pass
        else:
            tmp = []
            for disciplina in disciplinasProcessadas:
                tmp.append(str(disciplina[0]) + ' - ' + disciplina[1])
            self._frameCancelamento.listaDisciplinas = tmp

        cursor.close()

    def _mudarSemestre(self, evt):
        widget = evt.widget

        mapaSemestre = {"Primeiro Semestre": 1,
                        "Segundo Semestre": 2,
                        "Terceiro Semestre": 3,
                        "Quarto Semestre": 4,
                        "Quinto Semestre": 5,
                        "Sexto Semestre": 6,
                        "Setimo Semestre": 7,
                        "Oitavo Semestre": 8,
                        "Nono Semestre": 9,
                        "Decimo Semestre": 10}

        select = '''SELECT DISCIPLINA.codigo, DISCIPLINA.nome
FROM DISCIPLINA
WHERE idDisciplina != ALL(SELECT idDisciplina
                          FROM DISCIPLINA_ALUNO
                          WHERE DISCIPLINA_ALUNO.idAluno = %d
                            AND DISCIPLINA_ALUNO.situacao != 6
                            AND DISCIPLINA_ALUNO.situacao != 7)
AND semestreGrade = %d;''' \
                 % (self.__idAluno, mapaSemestre[widget.get()])

        cursor = self.DB.cursor()
        cursor.execute(select)

        listaDisciplinas = []

        for disciplina in cursor.fetchall():
            # Cria uma lista de tuplas: (codigoDisciplina, nome)
            tmp = str(disciplina[0]) + ' - ' + disciplina[1]
            if tmp not in self._frameSolicitacao.listaSelecionados:
                listaDisciplinas.append(tmp)
            else:
                continue
        # TODO: faze sort ignorando o codigo
        cursor.close()
        listaDisciplinas.sort()
        self._frameSolicitacao.listaDisciplinas = listaDisciplinas

    def _confirmarSolicitacao(self):
        self._frameSolicitacao.focus()
        self.janelaPrincipal.fecharJanela()

        cursor = self.DB.cursor()
        for disciplina in self._frameSolicitacao.listaSelecionados:
            cursor.execute('''SELECT idDisciplina FROM DISCIPLINA WHERE codigo = %d;''' % int(disciplina[:5]))
            idDisciplina = cursor.fetchone()[0]

            semestre = strftime("%Y-%m")

            if int(semestre[5:]) > 6:
                semestre = semestre[:5] + '2'
            else:
                semestre = semestre[:5] + '1'

            cursor.execute('''SELECT idSemestreDisciplina
FROM SEMESTRE_DISCIPLINA
WHERE idDisciplina = %d AND semestre = '%s';''' % (idDisciplina, semestre))
            idSemestreDisciplina = cursor.fetchone()[0]

            insert = ''' INSERT INTO `DISCIPLINA_ALUNO` (`idDisciplina`, `idSemestreDisciplina`, `idALuno`)
            values (%d, %d, %d); ''' % (idDisciplina, idSemestreDisciplina, self.__idAluno)

            cursor.execute(insert)
            self.DB.commit()
        cursor.close()

        del self._frameSolicitacao

    def _confirmarCancelamento(self):
        self._frameCancelamento.focus()
        self.janelaPrincipal.fecharJanela()

        select = ''' select DISCIPLINA.codigo, DISCIPLINA.idDisciplina
from DISCIPLINA
       JOIN DISCIPLINA_ALUNO
         ON DISCIPLINA.idDisciplina = DISCIPLINA_ALUNO.idDisciplina
WHERE DISCIPLINA_ALUNO.situacao = 1
  AND DISCIPLINA_ALUNO.idAluno = %d;''' % self.__idAluno

        cursor = self.DB.cursor()
        cursor.execute(select)

        disciplinasCancelar = {}

        for disciplina in cursor.fetchall():
            disciplinasCancelar[disciplina[0]] = disciplina[1]

        for disciplina in self._frameCancelamento.listaSelecionados:
            delet = ''' DELETE FROM DISCIPLINA_ALUNO where idDisciplina = %d''' \
                    % disciplinasCancelar[int(disciplina[:4])]
            cursor.execute(delet)

        self.DB.commit()
        cursor.close()

        del self._frameCancelamento


    def verHistorico(self):
        pass



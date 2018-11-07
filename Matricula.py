import tkinter as tk
import tkinter.ttk as ttk
from time import strftime
from ConexaoBanco import ConexaoBanco
from FramesMatricula import FramesMatricula


class Matricula:
    # TODO: Separar Solicitação de Cancelamento de Solicitação de Matricula.
    # TODO: Criar função de cancelamento.
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

    def carregarDisciplinas(self):
        # Verifica se já existe alguma materia com situação igual a PROCESSANDO
        self.disciplinasSolicitadas.clear()
        cursor = self.DB.cursor()

        select = ''' SELECT DISCIPLINA.codigo, DISCIPLINA.nome
        FROM DISCIPLINA
               JOIN DISCIPLINA_ALUNO
                 ON DISCIPLINA.idDisciplina = DISCIPLINA_ALUNO.idDisciplina
        WHERE DISCIPLINA_ALUNO.idAluno = %d
          AND DISCIPLINA_ALUNO.situacao = 1;''' % self.__idAluno

        cursor.execute(select)
        disciplinasSelecionadas = cursor.fetchall()

        if len(disciplinasSelecionadas) == 0:
            # Não possui disciplinas com status PROCESSANDO
            pass
        else:
            for disciplina in disciplinasSelecionadas:
                self.disciplinasSolicitadas.append(str(disciplina[0]) + ' - ' + disciplina[1])
        cursor.close()

    def solicitarMatricula(self):
        metodos = {"mudarSemestre": self._mudarSemestre,
                   "confirmarSolicitacao": self._confirmarSolicitacao
                   }

        self._frameSolicitacao = FramesMatricula(self.janelaPrincipal, metodos)
        self._frameSolicitacao.frameSolicitar()
        self._frameSolicitacao.grid(row=0, column=1, sticky='n')

    def cancelarMatricula(self):
        metodos = {"confirmarCancelamento": self._confirmarCancelamento}

        self._frameCancelamento = FramesMatricula(self.janelaPrincipal, metodos)
        self._frameCancelamento.frameCancelar()
        self._frameCancelamento.grid(row=0, column=1, sticky='n')

    def _confirmarCancelamento(self):
        select = ''' SELECT idDisciplina FROM DISCIPLINA WHERE codigo = %d''' \
                 % int(self.__disciplinasSelecionadas[0][:4])

        print(select)
        cursor = self.DB.cursor()
        cursor.execute(select)

        delet = ''' DELETE FROM disciplina_aluno where idDisciplina = %d''' % cursor.fetchone()[0]

        cursor.execute(delet)

        self.DB.commit()
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
        self.janelaPrincipal.focus()
        self._frameSolicitacao.grid_remove()

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

        self.janelaPrincipal.openWindows.remove(self._frameSolicitacao)
        self._frameSolicitacao.destroy()
        del self._frameSolicitacao


    def verHistorico(self):
        self.criarJanela()

        cursor = self.DB.cursor()
        situacao = {1: "PROCESSANDO",
                    2: "CURSANDO",
                    3: "RECUSADO",
                    4: "APROVEITAMENTO DE CREDITO",
                    5: "APROVADO",
                    6: "REPROVADO",
                    7: "REPROVADO POR FALTA"}

        mapaSemestre = {1: "Primeiro Semestre",
                        2: "Segundo Semestre",
                        3: "Terceiro Semestre",
                        4: "Quarto Semestre",
                        5: "Quinto Semestre",
                        6: "Sexto Semestre",
                        7: "Setimo Semestre",
                        8: "Oitavo Semestre",
                        9: "Nono Semestre",
                        10: "Decimo Semestre"}

        semestres = {}

        historico = ttk.Treeview(self.__janelaSolicitar,
                                 columns=('Codigo', 'Disciplina', 'Periodo', 'Nota', 'Créditos', 'Situação'))
        historico['columns'] = ('Codigo', 'Disciplina', 'Periodo', 'Nota', 'Créditos', 'Situação')

        historico.column('#0', width=140)

        historico.heading('Codigo', text="Codigo")
        historico.column('Codigo', width=100, anchor='center')

        historico.heading('Disciplina', text='Disciplina')
        historico.column('Disciplina', width=250, anchor='center')

        historico.heading('Periodo', text='Periodo')
        historico.column('Periodo', width=100, anchor='center')

        historico.heading('Nota', text='Nota')
        historico.column('Nota', width=70, anchor='center')

        historico.heading('Créditos', text='Créditos')
        historico.column('Créditos', width=70, anchor='center')

        historico.heading('Situação', text='Situação')
        historico.column('Situação', width=100, anchor='center')

        select = '''select DISCIPLINA.semestreGrade,
       DISCIPLINA.codigo,
       DISCIPLINA.nome,
       SEMESTRE_DISCIPLINA.semestre,
       DISCIPLINA_ALUNO.nota,
       DISCIPLINA.numCredito,
       DISCIPLINA_ALUNO.situacao
from DISCIPLINA_ALUNO
       JOIN DISCIPLINA
         ON DISCIPLINA_ALUNO.idDisciplina = DISCIPLINA.idDisciplina
       JOIN SEMESTRE_DISCIPLINA
         ON SEMESTRE_DISCIPLINA.idDisciplina = DISCIPLINA.idDisciplina
WHERE DISCIPLINA_ALUNO.idAluno = %d;''' % self.__idAluno

        cursor.execute(select)

        for disciplina in cursor.fetchall():
            disciplina = list(disciplina)

            if disciplina[0] not in semestres:
                semestres[disciplina[0]] = historico.insert('', 'end', text=mapaSemestre[disciplina[0]])

            disciplina[6] = situacao[disciplina[6]]

            historico.insert(semestres[disciplina[0]], 'end', values=disciplina[1:])

        cursor.close()
        historico.pack()



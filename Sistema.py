import tkinter as tk
from dataEntry import DataEntry
from time import strftime
from ConexaoBanco import ConexaoBanco


class Sistema:
    def __init__(self, janelaPrincipal):
        self._janelaPrincipal = janelaPrincipal
        self.DB = ConexaoBanco()

        self._terminoMatricula = tk.StringVar()

    def iniciarMatricula(self):
        # TODO: Subistituir Entry po dataEntry (pegar no Drive)
        inicio = tk.Toplevel(self._janelaPrincipal)

        dataLabel = tk.Label(inicio)
        dataLabel['text'] = "Data de Termino"

        dataEntry = DataEntry(inicio, self._terminoMatricula)

        dataLabel.grid(row=0, column=0)
        dataEntry.grid(row=1, column=0)

        okButton = tk.Button(inicio)
        okButton['text'] = "Ok"
        okButton['command'] = inicio.destroy

    def terminarMatricula(self):
        self.terminoMatricula = strftime("%d-%m-%Y")

        listaCursando = []
        listaRecusados = []

        selectD = ''' SELECT DISTINCT idAluno FROM DISCIPLINA_ALUNO WHERE situacao = 1; '''

        cursorIdAluno = self.DB.cursor()
        cursorDependentes = self.DB.cursor()
        cursorDisciplinas = self.DB.cursor()

        cursorIdAluno.execute(selectD)

        for idAluno in cursorIdAluno.fetchall():

            selectDependentes = '''
            SELECT DISCIPLINA_ALUNO.idDisciplina,
                   DEPENDENCIAS.idDisciplina
            FROM DISCIPLINA_ALUNO
              LEFT JOIN DEPENDENCIAS
                ON DISCIPLINA_ALUNO.idDisciplina = DEPENDENCIAS.idDisciplinaDependente
            WHERE DISCIPLINA_ALUNO.idAluno = %d
              AND DISCIPLINA_ALUNO.situacao = 1;
            ''' % idAluno[0]

            cursorDependentes.execute(selectDependentes)

            selectDisciplinas = '''
            SELECT idDisciplina
            FROM disciplina_aluno
            WHERE idAluno = %d
              AND situacao IN (4, 5);
                        ''' % idAluno

            cursorDisciplinas.execute(selectDisciplinas)
            listaDisciplinas = []

            # lista as Disciplinas que o aluno já foi aprovado.
            for disciplina in cursorDisciplinas.fetchall():
                listaDisciplinas.append(disciplina[0])
            cursorDisciplinas.close()

            for disciplina in cursorDependentes.fetchall():
                # Caso não tenha dependencia
                if disciplina[1] is None:
                    # (idAluno, disciplinaSolicitada)
                    listaCursando.append((idAluno[0], disciplina[0]))
                # Caso tenha dependencia
                else:
                    if disciplina[1] in listaDisciplinas:
                        # Caso o aluno tenha cumprido o requisito
                        listaCursando.append((idAluno[0], disciplina[0]))
                    else:
                        # Caso o aluno não tenha cumprido o requisito
                        listaRecusados.append((idAluno[0], disciplina[0]))

        cursorDependentes.close()
        cursorDisciplinas.close()
        cursorIdAluno.close()

        cursor = self.DB.cursor()

        for disciplina in listaCursando:
            update = '''
        UPDATE DISCIPLINA_ALUNO
        SET situacao = 2
        WHERE idAluno = %d
          AND idDisciplina = %d;
                    ''' % (disciplina[0], disciplina[1])

            cursor.execute(update)
            self.DB.commit()

        for disciplina in listaRecusados:
                update = '''
        UPDATE DISCIPLINA_ALUNO
        SET situacao = 3
        WHERE idAluno = %d
          AND idDisciplina = %d;
                    ''' % (disciplina[0], disciplina[1])

                cursor.execute(update)
                self.DB.commit()
        cursor.close()

    @property
    def terminoMatricula(self):
        return self._terminoMatricula.get()

    @terminoMatricula.setter
    def terminoMatricula(self, data):
        self._terminoMatricula.set(data)

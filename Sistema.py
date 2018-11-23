import tkinter as tk
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

        dataEntry = tk.Entry(inicio)
        dataEntry['textvariable'] = self._terminoMatricula

        dataLabel.grid(row=0, column=0)
        dataEntry.grid(row=1, column=0)

        okButton = tk.Button(inicio)
        okButton['text'] = "Ok"
        okButton['command'] = inicio.destroy

    def terminarMatricula(self):
        self.terminoMatricula = strftime("%d-%m-%Y")

        listaCursando = []
        listaRecusados = []

        select = ''' SELECT DISTINCT idAluno FROM DISCIPLINA_ALUNO WHERE situacao = 1; '''

        cursorIdAluno = self.DB.cursor()

        cursorIdAluno.execute(select)

        for idAluno in cursorIdAluno.fetchall():
            cursor = self.DB.cursor()
            select = '''
SELECT DISCIPLINA_ALUNO.idDisciplina,
       DEPENDENCIAS.idDisciplina
FROM DISCIPLINA_ALUNO
  LEFT JOIN DEPENDENCIAS
    ON DISCIPLINA_ALUNO.idDisciplina = DEPENDENCIAS.idDisciplinaDependente
WHERE DISCIPLINA_ALUNO.idAluno = %d
  AND DISCIPLINA_ALUNO.situacao = 1;
''' % idAluno[0]

            cursor.execute(select)
            for disciplina in cursor.fetchall():
                if disciplina[1] is None:
                    listaCursando.append((idAluno[0], disciplina[0]))
                else:
                    listaRecusados.append(idAluno + disciplina)
            cursor.close()
        cursorIdAluno.close()
        cursor = self.DB.cursor()

        for disciplina in listaCursando:
            update = '''
UPDATE DISCIPLINA_ALUNO
SET situacao = 2
WHERE idAluno = %d
  AND idDisciplina = %d;
            ''' %(disciplina[0], disciplina[1])

            cursor.execute(update)
            self.DB.commit()


        for disciplina in listaRecusados:
            print(disciplina)



    @property
    def terminoMatricula(self):
        return self._terminoMatricula.get()

    @terminoMatricula.setter
    def terminoMatricula(self, data):
        self._terminoMatricula.set(data)

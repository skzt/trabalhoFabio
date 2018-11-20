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

        listaAlunos = []

        select = ''' SELECT DISTINCT idAluno FROM DISCIPLINA_ALUNO WHERE situacao = 1; '''

        cursor = self.DB.cursor()

        cursor.execute(select)

        for idAluno in cursor.fetchall():
            listaAlunos.append(idAluno[0])

        K


    @property
    def terminoMatricula(self):
        return self._terminoMatricula.get()

    @terminoMatricula.setter
    def terminoMatricula(self, data):
        self._terminoMatricula.set(data)

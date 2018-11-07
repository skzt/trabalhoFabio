import tkinter as tk
import tkinter.ttk as ttk


class FramesMatricula(tk.LabelFrame):
    """
    Esta classe fica responsavel por criar e manter os respectivos frames:
        Frame de Solicitação de Matricula
        Frame de Cancelamento de Matricula
        Frame de Visualização de Historico
        Frame de Visualização dos Horarios
    e recebe como paramentro, os metodos necessarios para o funcionamento da janela para que sejam bindados.
    master -> Referencia para janela principal.
    metodos -> Dicionario com metodos necessarios para cada tipo de frame.
    """

    # TODO: Criar menu para alternar entre janelas na GRID
    def __init__(self, master, metodos, *arg, **kwarg):
        tk.LabelFrame.__init__(self, master, labelanchor='n', *arg, **kwarg)

        self._janelaPrincipal = master
        self._metodos = metodos

        self._boxDisciplinas = None
        self._boxSelecionados = None
        self._boxSemestre = None

        self._listaDisciplinas = tk.Variable()
        self._listaSelecionados = tk.Variable()

    def frameSolicitar(self):
        # TODO: VERIFICAR SE O PERIODO DE MATRICULA ESTA EM ABERTO PERMITINDO ASSIM FAZER MATRICULA
        if self in self._janelaPrincipal.openWindows:
            # TODO: Trazer frameSolicitar para frente
            return
        else:
            self._janelaPrincipal.openWindows = self

        self['text'] = "Solicitação de Matricula"
        _labelSemestre = tk.Label(self)
        _labelSemestre['text'] = "Selecione o semestre:"

        self._boxSemestre = ttk.Combobox(self)
        self._boxSemestre['state'] = 'readonly'
        self._boxSemestre['width'] = 16
        self._boxSemestre['values'] = ["Primeiro Semestre",
                                       "Segundo Semestre",
                                       "Terceiro Semestre",
                                       "Quarto Semestre",
                                       "Quinto Semestre",
                                       "Sexto Semestre",
                                       "Setimo Semestre",
                                       "Oitavo Semestre",
                                       "Nono Semestre",
                                       "Decimo Semestre"]

        self._boxSemestre.bind("<<ComboboxSelected>>", self._metodos['mudarSemestre'])
        self._boxSemestre.current(0)

        _labelDisciplinas = tk.Label(self)
        _labelDisciplinas['text'] = "Disciplinas Disponiveis"

        self._boxDisciplinas = tk.Listbox(self)
        self._boxDisciplinas['listvariable'] = self._listaDisciplinas

        _labelSelecionados = tk.Label(self)
        _labelSelecionados['text'] = "Disciplinas a Matricular"

        self._boxSelecionados = tk.Listbox(self)
        self._boxSelecionados['listvariable'] = self._listaSelecionados

        __addButton = tk.Button(self)
        __addButton['text'] = ">>"
        __addButton['command'] = self._adicionarDisciplina

        __removerButton = tk.Button(self)
        __removerButton['text'] = "<<"
        __removerButton['command'] = self._removerDisciplina

        __confirmarButton = tk.Button(self)
        __confirmarButton['text'] = "Solicitar Matricula"
        __confirmarButton['command'] = self._metodos["confirmarSolicitacao"]

        _labelSemestre.grid(row=0, column=0)
        self._boxSemestre.grid(row=1, column=0)

        _labelDisciplinas.grid(row=2, column=0)
        self._boxDisciplinas.grid(row=3, column=0, rowspan=2)

        _labelSelecionados.grid(row=2, column=2)
        self._boxSelecionados.grid(row=3, column=2, rowspan=2)

        __addButton.grid(row=2, column=1, sticky='s')
        __removerButton.grid(row=3, column=1, sticky='n')
        __confirmarButton.grid(row=5, column=1, sticky='n')

        self._boxSemestre.event_generate("<<ComboboxSelected>>")

    def _adicionarDisciplina(self):
        index = self.boxDisciplinas.curselection()

        if len(index) == 0:
            return
        else:
            index = index[0]

            selecionado = self.listaDisciplinas[index]

            if selecionado in self.listaSelecionados:
                return
            else:
                self.boxDisciplinas.delete(index)

                disciplinasSelecionadas = self.listaSelecionados
                disciplinasSelecionadas.append(selecionado)
                disciplinasSelecionadas.sort()
                self.listaSelecionados = disciplinasSelecionadas

    def _removerDisciplina(self):
        index = self.boxSelecionados.curselection()

        if len(index) == 0:
            return
        else:
            index = index[0]
            self.boxSelecionados.delete(index)
            self.boxSemestre.event_generate("<<ComboboxSelected>>")

    def frameCancelar(self):
        # TODO: VERIFICAR SE O PERIODO DE MATRICULA ESTA EM ABERTO PERMITINDO ASSIM CANCELAR MATRICULA
        if self in self._janelaPrincipal.openWindows:
            # TODO: Trazer frameSolicitar para frente
            return
        else:
            self._janelaPrincipal.openWindows = self

        self['text'] = "Cancelar Solicitação de Matricula"

        _labelDisciplinas = tk.Label(self)
        _labelDisciplinas['text'] = "Disciplinas Solicitadas"

        self._boxDisciplinas = tk.Listbox(self)
        self._boxDisciplinas['listvariable'] = self._listaDisciplinas

        _labelSelecionados = tk.Label(self)
        _labelSelecionados['text'] = "Disciplinas a Cancelar"

        self._boxSelecionados = tk.Listbox(self)
        self._boxSelecionados['listvariable'] = self._listaSelecionados

        __addButton = tk.Button(self)
        __addButton['text'] = ">>"
        __addButton['command'] = self._adicionarDisciplina

        __removerButton = tk.Button(self)
        __removerButton['text'] = "<<"
        __removerButton['command'] = self._removerDisciplina

        __confirmarButton = tk.Button(self)
        __confirmarButton['text'] = "Cancelar Matricula"
        __confirmarButton['command'] = self._metodos["confirmarCancelamento"]

        _labelDisciplinas.grid(row=0, column=0)
        self._boxDisciplinas.grid(row=1, column=0, rowspan=3)

        _labelSelecionados.grid(row=0, column=2)
        self._boxSelecionados.grid(row=1, column=2, rowspan=3)

        __addButton.grid(row=1, column=1, sticky='s')
        __removerButton.grid(row=1, column=1, sticky='n')
        __confirmarButton.grid(row=3, column=1, sticky='s')

    def janelaHistorico(self):
        pass

    def __del__(self):
        print("oiiiiiiiiiiiiii frame")


    @property
    def boxSemestre(self):
        return self._boxSemestre

    @property
    def boxDisciplinas(self):
        return self._boxDisciplinas

    @property
    def boxSelecionados(self):
        return self._boxSelecionados

    @property
    def listaDisciplinas(self):
        return list(self._listaDisciplinas.get())

    @listaDisciplinas.setter
    def listaDisciplinas(self, lista):
        self._listaDisciplinas.set(lista)

    @property
    def listaSelecionados(self):
        return list(self._listaSelecionados.get())

    @listaSelecionados.setter
    def listaSelecionados(self, lista):
        self._listaSelecionados.set(lista)






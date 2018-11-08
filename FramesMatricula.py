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
        # TODO: Fazer bind para fechar frames com o ESC, mas não destruir a classe.

        self.focus()
        self._janelaPrincipal = master
        self._metodos = metodos
        self._janelaPrincipal.bind_class('frameMatricula', "<Escape>", lambda _: self.grid_remove())

        self._boxDisciplinas = None
        self._boxSelecionados = None
        self._boxSemestre = None

        self._listaDisciplinas = tk.Variable()
        self._listaSelecionados = tk.Variable()

    @staticmethod
    def _retag(tag, *widgets):
        """
        Adiciona uma tag especifica aos widigets passados, para bindar o evento "<Escape>" que
        esconde a janela aberta (em foco).

        :param tag: Nome da tag que sera adicionada aos widgets
        :param widgets: Widgets que iram receber a tag
        :return: VOID
        """
        for widget in widgets:
            widget.bindtags((tag,) + widget.bindtags())

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

        _addButton = tk.Button(self)
        _addButton['text'] = ">>"
        _addButton['command'] = self._adicionarDisciplina

        _removerButton = tk.Button(self)
        _removerButton['text'] = "<<"
        _removerButton['command'] = self._removerDisciplina

        _confirmarButton = tk.Button(self)
        _confirmarButton['text'] = "Solicitar Matricula"
        _confirmarButton['command'] = self._metodos["confirmarSolicitacao"]

        _labelSemestre.grid(row=0, column=0)
        self._boxSemestre.grid(row=1, column=0)

        _labelDisciplinas.grid(row=2, column=0)
        self._boxDisciplinas.grid(row=3, column=0, rowspan=2)

        _labelSelecionados.grid(row=2, column=2)
        self._boxSelecionados.grid(row=3, column=2, rowspan=2)

        _addButton.grid(row=3, column=1, sticky='n')
        _removerButton.grid(row=3, column=1, sticky='s')
        _confirmarButton.grid(row=5, column=1, sticky='n')

        self._boxSemestre.event_generate("<<ComboboxSelected>>")

        self._retag('frameMatricula',
                    self,
                    _labelSelecionados,
                    _labelDisciplinas,
                    _labelSemestre,
                    _addButton,
                    _removerButton,
                    _confirmarButton,
                    self._boxSelecionados,
                    self._boxDisciplinas,
                    self._boxSemestre)

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
        print(self.listaSelecionados)

    def _removerDisciplina(self):
        index = self.boxSelecionados.curselection()

        if len(index) == 0:
            return
        else:
            index = index[0]
            select =self.boxSelecionados.get(index)
            tmp = self.listaDisciplinas
            tmp.append(select)
            tmp.sort()
            self.listaDisciplinas = tmp
            self.boxSelecionados.delete(index)

            # if self.boxSemestre is not None:
            #             #     self.boxSemestre.event_generate("<<ComboboxSelected>>")
            #             # else:



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

        _addButton = tk.Button(self)
        _addButton['text'] = ">>"
        _addButton['command'] = self._adicionarDisciplina

        _removerButton = tk.Button(self)
        _removerButton['text'] = "<<"
        _removerButton['command'] = self._removerDisciplina

        _confirmarButton = tk.Button(self)
        _confirmarButton['text'] = "Cancelar Matricula"
        _confirmarButton['command'] = self._metodos["confirmarCancelamento"]

        _labelDisciplinas.grid(row=0, column=0)
        self._boxDisciplinas.grid(row=1, column=0, rowspan=3)

        _labelSelecionados.grid(row=0, column=2)
        self._boxSelecionados.grid(row=1, column=2, rowspan=3)

        _addButton.grid(row=1, column=1, sticky='n')
        _removerButton.grid(row=1, column=1, sticky='s')
        _confirmarButton.grid(row=3, column=1, sticky='s')

        self._retag('frameMatricula',
                    self,
                    _labelSelecionados,
                    _labelDisciplinas,
                    _addButton,
                    _removerButton,
                    _confirmarButton,
                    self._boxSelecionados,
                    self._boxDisciplinas)

    def frameHistorico(self):

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





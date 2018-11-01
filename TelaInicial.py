#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import pymysql as sql
from Config import getDBinfo
import platform as pf
from time import strftime


class TelaInicial(tk.Tk):
    def __init__(self, *arg, **kwarg):
        tk.Tk.__init__(self, *arg, **kwarg)

        __OS__ = pf.system()

        if __OS__ == 'Windows':
            self.state('zoomed')
        elif __OS__ == 'Linux':
            self.attributes('-zoomed', True)

        self.__usuarioVar = tk.StringVar()
        self.__senhaVar = tk.StringVar()
        self.__openWindows = []
        self.__alunoLogado = None
        self.__loginFrame = tk.LabelFrame(self)

        self.topmenu()
        self.loginWindow()

    def topmenu(self):

        __topMenuBar = tk.Menu(self)
        self.config(menu=__topMenuBar)
        # =======================================================================
        # Criação dos menus da barra de menus superior
        # =======================================================================

        self.__topLoginMenu = tk.Menu(self, tearoff=0)
        self.__topMatriculaMenu = tk.Menu(self, tearoff=0)
        self.__topBoletoMenu = tk.Menu(self, tearoff=0)

        # =======================================================================
        # Menu de Login
        # =======================================================================

        # self.__topLoginMenu.add_command(label="Encerrar Aplicação", command=self.encerrarAplicacao)
        __topMenuBar.add_cascade(label="Login", menu=self.__topLoginMenu)

        # =======================================================================
        # Menu de Matricula
        # =======================================================================
        __topMenuBar.add_cascade(label="Matricula", menu=self.__topMatriculaMenu)

        # =======================================================================
        # Menu de Boletos
        # =======================================================================
        __topMenuBar.add_cascade(label="Boletos", menu=self.__topBoletoMenu)

    def loginWindow(self):
        # TODO: Definir frame separado para lateral de login
        # =======================================================================
        # Janela de Login
        # =======================================================================
        __userLabel = tk.Label(self.__loginFrame)
        __userLabel['text'] = "Usuário:"

        __senhaLabel = tk.Label(self.__loginFrame)
        __senhaLabel['text'] = "Senha:"

        __usuarioEntry = tk.Entry(self.__loginFrame)
        __usuarioEntry['textvariable'] = self.__usuarioVar
        __usuarioEntry.bind("<Return>", lambda _: __usuarioEntry.tk_focusNext().focus())
        __usuarioEntry.focus()

        __senhaEntry = tk.Entry(self.__loginFrame)
        __senhaEntry['show'] = '*'
        __senhaEntry.bind("<Return>", lambda _: __senhaEntry.tk_focusNext().focus())
        __senhaEntry['textvariable'] = self.__senhaVar

        self.__loginButton = tk.Button(self.__loginFrame)
        self.__loginButton['text'] = "Iniciar Sessão"
        self.__loginButton['command'] = lambda u=__usuarioEntry: self.efetuarLogin(
            widgets=[__usuarioEntry, __senhaEntry])
        self.__loginButton.bind("<Return>",
                                lambda _, u=__usuarioEntry: self.efetuarLogin(widgets=[__usuarioEntry, __senhaEntry]))

        __sairButton = tk.Button(self.__loginFrame)
        __sairButton['text'] = "Ecerrar Aplicação"
        __sairButton['command'] = self.destroy
        __sairButton.bind("<Return>", lambda _: self.destroy())
        # TODO: Alinhar foco entre sair e demais botões (Sugestão: Tirar botões, deixar apenas no menu)
        # =======================================================================
        # Plotando a Janela de Login na Grid
        # =======================================================================
        __userLabel.grid(row=0, column=0)
        __usuarioEntry.grid(row=1, column=0)
        __senhaLabel.grid(row=2, column=0)
        __senhaEntry.grid(row=3, column=0)
        self.__loginButton.grid(row=4, column=0)
        __sairButton.grid(row=8, column=0)
        self.__loginFrame.grid(row=0, column=0, sticky='ns')
        tk.Grid.rowconfigure(self, 0, weight=1)
        # TODO: criar metodo de saida e definir como usuario logado sera guardado e usado!

    def efetuarLogin(self, widgets):
        try:
            self.__loginButton['state'] = 'disabled'
            self.alunoLogado = Login(janelaPrincipal=self,
                                     usuario=self.__usuarioVar,
                                     widgets=widgets)
        except sql.err.OperationalError as error:
            messagebox.showerror(title="Conexão ao Banco", message="Falha ao se conectar ao Banco de Dados",
                                 parent=self)

            self.__loginButton['state'] = 'normal'
            return

        if self.alunoLogado.logar(self.__senhaVar):
            # Top Menus de Login
            self.__topLoginMenu.add_command(label="Alterar Senha", command=self.alunoLogado.alterarSenhaWindow)
            self.__topLoginMenu.add_command(label="Encerrar Sessão", command=self.alunoLogado.encerrarsessao)
            self.__topMatriculaMenu.add_command(label="Solicitar Matricula",
                                                command=self.alunoLogado.aluno.solicitarMatricula)
            self.__topMatriculaMenu.add_command(label="Ver Historico", command=self.alunoLogado.aluno.verHistorico)

            # Top Menus do Aluno
            pass
        else:
            self.__loginButton['state'] = 'normal'
            self.alunoLogado = None

    def deslogar(self):
        # TODO: adicionar todos os top menus que forem adicionados após o login
        self.__topLoginMenu.delete(0, 1)
        self.__topMatriculaMenu.delete(0, 1)
        self.__loginButton['state'] = 'normal'

    @property
    def openWindows(self):
        return self.__openWindows

    @openWindows.setter
    def openWindows(self, janela):
        self.openWindows.append(janela)

    @property
    def alunoLogado(self):
        return self.__alunoLogado

    @alunoLogado.setter
    def alunoLogado(self, aluno):
        self.__alunoLogado = aluno


class Login:
    def __init__(self, janelaPrincipal, usuario, widgets):
        '''
        Classe responsavel por fazer o Login no sistema e operações relacionadas com login.
        usuario -> Variavel que observa o widget usuarioEntry
        senha -> Variavel que observa o widget senhaEntry
        widgets -> os widgets de usuario e senha, respectivamente. Utilizados para alteração de estado do widget
        '''

        self.janelaPrincipal = janelaPrincipal
        self.__widgets = widgets
        self.__usuario = usuario
        self.__aluno = None

        self.deslogarButton = None
        self.alterarSenha = None

        # Acesso ao banco
        self.DB = ConexaoBanco()

    def logar(self, senha):
        select = '''SELECT idAluno FROM LOGIN WHERE usuario = '%s' AND senha = MD5('%s');''' \
                 % (self.__usuario.get(), senha.get())

        cursor = self.DB.cursor()

        cursor.execute(select)
        idAluno = cursor.fetchone()

        if idAluno is not None:
            '''Caso exista um retorno no select, signifca que o login esta correto.
            Em caso de o login estiver correto, os dados do Aluno são consultados no banco, e se retorna True,
            indicando que houve sucesso no login.
            Em caso de o login estiver incorreto, retorna False indicando falha no Login
            Então é feito o bloqueio de digitação nos campos de usuario e senha, e aparecem os botões de:
            -Deslogar
            -Alterar senha'''

            cursor.close()
            self.__widgets[0]['state'] = 'disabled'
            self.__widgets[1]['state'] = 'disabled'
            # REMOVER APARTIR DAQUI (CASO OPTAR POR DEIXAR ESTAS OPÇÕES APENAS NO TOP MENU)
            self.deslogarButton = tk.Button(self.__widgets[0].master)
            self.deslogarButton['text'] = 'Encerrar Sessão'
            self.deslogarButton['command'] = self.encerrarsessao
            # self.deslogarButton.grid(row=5, column=0)

            self.alterarSenha = tk.Button(self.__widgets[0].master)
            self.alterarSenha['text'] = "Alterar Senha"
            self.alterarSenha['command'] = self.alterarSenhaWindow
            # self.alterarSenha.grid(row=7, column=0)
            # REMOVER ATÉ AQUI!

            cursor = self.DB.cursor()
            select = "SELECT * FROM ALUNO WHERE idAluno = %d;" % (idAluno)

            cursor.execute(select)

            tmp = cursor.fetchone()

            self.__aluno = Aluno(self.janelaPrincipal, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4])
            self.__aluno.logado = True

            return True

        else:
            messagebox.showerror(title='Login Incorreto!', message='Usuário ou senha incorreta.',
                                 parent=self.janelaPrincipal)
            cursor.close()
            return False

    def alterarSenhaWindow(self):
        __frameMudaSenha = tk.Toplevel(self.janelaPrincipal)
        self.janelaPrincipal.openWindows = __frameMudaSenha
        __senhaAtualVar = tk.StringVar()
        __novaSenhaVar = tk.StringVar()
        __confNovaSenhaVar = tk.StringVar()
        # =======================================================================
        # Labels
        # =======================================================================
        __senhaAtualLabel = tk.Label(__frameMudaSenha)
        __senhaAtualLabel['text'] = "Senha Atual"
        __novaSenhaLabel = tk.Label(__frameMudaSenha)
        __novaSenhaLabel['text'] = "Nova Senha"
        __confNovaSenhaLabel = tk.Label(__frameMudaSenha)
        __confNovaSenhaLabel['text'] = "Confirmar Senha"

        # =======================================================================
        # Entrys
        # =======================================================================
        __senhaAtualEntry = tk.Entry(__frameMudaSenha)
        __senhaAtualEntry['textvariable'] = __senhaAtualVar
        __senhaAtualEntry['show'] = '*'
        __senhaAtualEntry.focus()

        __novaSenhaEntry = tk.Entry(__frameMudaSenha)
        __novaSenhaEntry['textvariable'] = __novaSenhaVar
        __novaSenhaEntry['show'] = '*'

        __confNovaSenhaEntry = tk.Entry(__frameMudaSenha)
        __confNovaSenhaEntry['textvariable'] = __confNovaSenhaVar
        __confNovaSenhaEntry['show'] = '*'

        # =======================================================================
        # Buttons
        # =======================================================================

        __confirmar = tk.Button(__frameMudaSenha)
        __confirmar['text'] = "Confirmar"
        __confirmar['command'] = lambda sav=__senhaAtualVar, \
                                        nsv=__novaSenhaVar, \
                                        cnsv=__confNovaSenhaVar, \
                                        frame=__frameMudaSenha: self.alterarsenhacommit(sav, nsv, cnsv, frame)
        __cancelar = tk.Button(__frameMudaSenha)
        __cancelar['text'] = "Cancelar"
        __cancelar['command'] = __frameMudaSenha.destroy

        # =======================================================================
        # Grids
        # =======================================================================
        __senhaAtualLabel.grid(row=0, column=0)
        __novaSenhaLabel.grid(row=2, column=0)
        __confNovaSenhaLabel.grid(row=4, column=0)

        __senhaAtualEntry.grid(row=1, column=0)
        __novaSenhaEntry.grid(row=3, column=0)
        __confNovaSenhaEntry.grid(row=5, column=0)

        __confirmar.grid(row=6, column=0, sticky=('sw'))
        __cancelar.grid(row=6, column=0, sticky=('se'))
        return

    def alterarsenhacommit(self, senhaAtualVar, novaSenhaVar, confNovaSenhaVar, frame):
        if novaSenhaVar.get() != confNovaSenhaVar.get():
            messagebox.showerror(title="Senhas Não Conferem.",
                                 message="Nova senha e Confirmar Senha devem ser iguais.",
                                 parent=frame)
            novaSenhaVar.set("")
            confNovaSenhaVar.set("")
            return

        else:
            cursor = self.DB.cursor()

            select = '''SELECT idAluno\
                          FROM LOGIN\
                          WHERE usuario = '%s' AND senha = MD5('%s');''' \
                     % (self.__usuario.get(), senhaAtualVar.get())

            cursor.execute(select)

            if cursor.fetchone() is not None:
                '''Caso exista um retorno no select, signifca que o login esta correto.
                Então é liberado para fazer a atualização de senha.
                '''
                update = ('''UPDATE `LOGIN` SET `senha`= MD5('%s') WHERE `usuario` = '%s';'''
                          % (novaSenhaVar.get(), self.__usuario.get())
                          )
                cursor.execute(update)
                self.DB.commit()
                messagebox.showinfo(title="Sucesso!", message="Senha Alterada com suceso.", parent=frame)
                frame.destroy()
            else:
                messagebox.showerror(title='Login Incorreto!', message='Senha incorreta.', parent=frame)
                senhaAtualVar.set("")
                novaSenhaVar.set("")
                confNovaSenhaVar.set("")

    def encerrarsessao(self):
        self.__aluno.deslogar()
        self.__widgets[0]['state'] = 'normal'
        self.__widgets[0].delete(0, 'end')
        self.__widgets[1]['state'] = 'normal'
        self.__widgets[1].delete(0, 'end')

        self.alterarSenha.destroy()
        self.deslogarButton.destroy()

        del self.alterarSenha
        del self.deslogarButton

        for window in self.janelaPrincipal.openWindows:
            window.destroy()

        self.DB.close()
        self.__widgets[0].focus()
        self.janelaPrincipal.deslogar()

    @property
    def aluno(self):
        return self.__aluno


class ConexaoBanco(object):
    def __new__(cls):
        # Caso não haja uma instancia de singleton, criar uma nova.
        if hasattr(cls, '_instancia') is False:
            cls._instancia = super(ConexaoBanco, cls).__new__(cls)

        # Retorna uma instancia nova, caso ela tenha sido criada
        # Ou retorna a unica instancia que já foi criada.
        return cls._instancia

    def __init__(self):
        dbinfo = getDBinfo()
        self.__DB = sql.connect(dbinfo[0], dbinfo[1], dbinfo[2], dbinfo[3])

    def cursor(self):
        return self.__DB.cursor()

    def close(self):
        self.__DB.close()

    def commit(self):
        self.__DB.commit()


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


class Disciplina:
    def __init__(self, numCreditos, codigo, nome, horario):
        self.__alunosMatriculados = []
        self.__numCreditos = numCreditos
        self.__codigo = codigo
        self.__nome = nome
        self.__horario
        pass


class Matricula:
    def __init__(self, janelaPrincipal, idAluno, curso):
        self.janelaPrincipal = janelaPrincipal
        self.__curso = curso
        self.__idAluno = idAluno

        self.DB = ConexaoBanco()
        self.disciplinasSelecionadas = []
        self.__janelaSolicitar = None
        self.__listaDisciplinas = None
        self.__listaSelecionados = None
        self.__boxSemestre = None

        # TODO: Filtrar Materias que constam como APROVADAS para não aparecerem para seleção

    def criarJanela(self):
        self.__janelaSolicitar = tk.Toplevel(self.janelaPrincipal)
        self.janelaPrincipal.openWindows.append(self.__janelaSolicitar)
        # TODO: Modificar de TopLevel para Frame e dar Grid ao lado da GRID de login
        DX = 170
        DY = 0
        self.__janelaSolicitar.geometry(
            "+%d+%d" % (self.janelaPrincipal.winfo_x() + DX, self.janelaPrincipal.winfo_y() + DY))

    def solicitarMatricula(self):
        # TODO: VERIFICAR SE O PERIODO DE MATRICULA ESTA EM ABERTO PERMITINDO ASSIM FAZER MATRICULA
        self.criarJanela()

        self.__listaDisciplinas = tk.Listbox(self.__janelaSolicitar)
        self.__listaSelecionados = tk.Listbox(self.__janelaSolicitar)

        __labelSemestre = tk.Label(self.__janelaSolicitar)
        __labelSemestre['text'] = "Selecione o semestre:"

        self.__boxSemestre = ttk.Combobox(self.__janelaSolicitar)
        self.__boxSemestre['state'] = 'readonly'
        self.__boxSemestre['width'] = 16
        self.__boxSemestre['values'] = ["Primeiro Semestre",
                                        "Segundo Semestre",
                                        "Terceiro Semestre",
                                        "Quarto Semestre",
                                        "Quinto Semestre",
                                        "Sexto Semestre",
                                        "Setimo Semestre",
                                        "Oitavo Semestre",
                                        "Nono Semestre",
                                        "Decimo Semestre"]
        self.__boxSemestre.current(0)
        self.mudarSemestre()
        self.__boxSemestre.bind("<<ComboboxSelected>>", self.mudarSemestre)

        __addButton = tk.Button(self.__janelaSolicitar)
        __addButton['text'] = ">>"
        __addButton['command'] = self.adicionarDisciplina

        __removerButton = tk.Button(self.__janelaSolicitar)
        __removerButton['text'] = "<<"
        __removerButton['command'] = self.removerDisciplina

        __solicitarButton = tk.Button(self.__janelaSolicitar)
        __solicitarButton['text'] = "Solicitar Matricula"
        __solicitarButton['command'] = self.confirmarSolicitacao

        __labelSemestre.grid(row=0, column=0)
        self.__boxSemestre.grid(row=1, column=0)
        self.__listaDisciplinas.grid(row=2, column=0, rowspan=2)
        self.__listaSelecionados.grid(row=2, column=2, rowspan=2)
        __addButton.grid(row=2, column=1, sticky=('s'))
        __removerButton.grid(row=3, column=1, sticky=('n'))
        __solicitarButton.grid(row=4, column=1)

    def mudarSemestre(self, evt=None):
        if isinstance(evt, tk.Event):
            widget = evt.widget
        else:
            widget = self.__boxSemestre

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

        print(select)

        cursor = self.DB.cursor()
        cursor.execute(select)

        listaDisciplinas = []

        for disciplina in cursor.fetchall():
            # Cria uma lista de tuplas: (codigoDisciplina, nome)
            tmp = str(disciplina[0]) + ' - ' + disciplina[1]
            if tmp not in self.disciplinasSelecionadas:
                listaDisciplinas.append(tmp)
            else:
                continue
        # TODO: faze sort ignorando o codigo
        listaDisciplinas.sort()

        self.__listaSelecionados.delete(0, 'end')
        for disciplina in self.disciplinasSelecionadas:
            self.__listaSelecionados.insert('end', disciplina)

        self.__listaDisciplinas.delete(0, 'end')
        for disciplina in listaDisciplinas:
            self.__listaDisciplinas.insert('end', disciplina)

    def adicionarDisciplina(self):
        if len(self.__listaDisciplinas.curselection()) == 0:
            return

        selecionado = self.__listaDisciplinas.get(self.__listaDisciplinas.curselection()[0])

        if selecionado in self.disciplinasSelecionadas:
            return
        else:
            self.__listaDisciplinas.delete(self.__listaDisciplinas.curselection()[0])
            self.disciplinasSelecionadas.append(selecionado)
            self.__listaSelecionados.insert('end', selecionado)

    def removerDisciplina(self):
        # TODO: Remover solicitação do banco e da disciplinasSelecionadas
        index = self.__listaSelecionados.curselection()

        if len(index) > 0:
            index = index[0]
            self.__listaSelecionados.delete(index)
            self.disciplinasSelecionadas.remove(self.disciplinasSelecionadas[index])
            self.mudarSemestre()

        else:
            pass

    def confirmarSolicitacao(self):
        self.janelaPrincipal.openWindows.remove(self.__janelaSolicitar)
        self.__janelaSolicitar.destroy()

        cursor = self.DB.cursor()
        for disciplina in self.disciplinasSelecionadas:
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
WHERE DISCIPLINA_ALUNO.idAluno = %d;''' % (self.__idAluno)

        cursor.execute(select)

        for disciplina in cursor.fetchall():
            disciplina = list(disciplina)

            if disciplina[0] not in semestres:
                semestres[disciplina[0]] = historico.insert('', 'end', text=mapaSemestre[disciplina[0]])

            disciplina[6] = situacao[disciplina[6]]

            historico.insert(semestres[disciplina[0]], 'end', values=disciplina[1:])

        historico.pack()


if __name__ == '__main__':
    ti = TelaInicial()
    ti.mainloop()

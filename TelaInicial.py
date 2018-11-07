#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: REMOVER TODOS OS PRINTS!!!
import tkinter as tk
import platform as pf
from tkinter import messagebox
from Login import Login
from pymysql import err


class TelaInicial(tk.Tk):
    def __init__(self, *arg, **kwarg):
        tk.Tk.__init__(self, *arg, **kwarg)

        __OS__ = pf.system()

        if __OS__ == 'Windows':
            self.state('zoomed')
        elif __OS__ == 'Linux':
            self.attributes('-zoomed', True)

        self._usuarioVar = tk.StringVar()
        self._senhaVar = tk.StringVar()
        self._openWindows = []
        self._alunoLogado = None
        self._loginFrame = tk.LabelFrame(self)
        self._topLoginMenu = None
        self._topMatriculaMenu = None
        self._topBoletoMenu = None
        self._loginButton = None

        self.topmenu()
        self.loginWindow()

    def topmenu(self):

        _topMenuBar = tk.Menu(self)
        self.config(menu=_topMenuBar)
        # =======================================================================
        # Criação dos menus da barra de menus superior
        # =======================================================================

        self._topLoginMenu = tk.Menu(self, tearoff=0)
        self._topMatriculaMenu = tk.Menu(self, tearoff=0)
        self._topBoletoMenu = tk.Menu(self, tearoff=0)

        # =======================================================================
        # Menu de Login
        # =======================================================================

        # self._topLoginMenu.add_command(label="Encerrar Aplicação", command=self.encerrarAplicacao)
        _topMenuBar.add_cascade(label="Login", menu=self._topLoginMenu)

        # =======================================================================
        # Menu de Matricula
        # =======================================================================
        _topMenuBar.add_cascade(label="Matricula", menu=self._topMatriculaMenu)

        # =======================================================================
        # Menu de Boletos
        # =======================================================================
        _topMenuBar.add_cascade(label="Boletos", menu=self._topBoletoMenu)

    def loginWindow(self):
        # TODO: Definir frame separado para lateral de login
        # =======================================================================
        # Janela de Login
        # =======================================================================
        _userLabel = tk.Label(self._loginFrame)
        _userLabel['text'] = "Usuário:"

        _senhaLabel = tk.Label(self._loginFrame)
        _senhaLabel['text'] = "Senha:"

        _usuarioEntry = tk.Entry(self._loginFrame)
        _usuarioEntry['textvariable'] = self._usuarioVar
        _usuarioEntry.bind("<Return>", lambda _: _usuarioEntry.tk_focusNext().focus())
        _usuarioEntry.focus()

        _senhaEntry = tk.Entry(self._loginFrame)
        _senhaEntry['show'] = '*'
        _senhaEntry.bind("<Return>", lambda _: _senhaEntry.tk_focusNext().focus())
        _senhaEntry['textvariable'] = self._senhaVar

        self._loginButton = tk.Button(self._loginFrame)
        self._loginButton['text'] = "Iniciar Sessão"
        self._loginButton['command'] = lambda u=_usuarioEntry: self.efetuarLogin(
            widgets=[_usuarioEntry, _senhaEntry])
        self._loginButton.bind("<Return>",
                               lambda _, u=_usuarioEntry: self.efetuarLogin(widgets=[_usuarioEntry, _senhaEntry]))

        _sairButton = tk.Button(self._loginFrame)
        _sairButton['text'] = "Ecerrar Aplicação"
        _sairButton['command'] = self.destroy
        _sairButton.bind("<Return>", lambda _: self.destroy())
        # TODO: Alinhar foco entre sair e demais botões (Sugestão: Tirar botões, deixar apenas no menu)
        # =======================================================================
        # Plotando a Janela de Login na Grid
        # =======================================================================
        _userLabel.grid(row=0, column=0)
        _usuarioEntry.grid(row=1, column=0)
        _senhaLabel.grid(row=2, column=0)
        _senhaEntry.grid(row=3, column=0)
        self._loginButton.grid(row=4, column=0)
        _sairButton.grid(row=8, column=0)
        self._loginFrame.grid(row=0, column=0, sticky='ns')
        tk.Grid.rowconfigure(self, 0, weight=1)
        # TODO: criar metodo de saida e definir como usuario logado sera guardado e usado!

    def efetuarLogin(self, widgets):
        try:
            self.focus()
            self._loginButton['state'] = 'disabled'
            self.alunoLogado = Login(janelaPrincipal=self,
                                     usuario=self._usuarioVar,
                                     widgets=widgets)
        except err.OperationalError:
            messagebox.showerror(title="Conexão ao Banco", message="Falha ao se conectar ao Banco de Dados",
                                 parent=self)

            self._loginButton['state'] = 'normal'
            return

        if self.alunoLogado.logar(self._senhaVar):
            # Top Menus de Login
            self._topLoginMenu.add_command(label="Alterar Senha", command=self.alunoLogado.alterarSenhaWindow)
            self._topLoginMenu.add_command(label="Encerrar Sessão", command=self.alunoLogado.encerrarsessao)

            self._topMatriculaMenu.add_command(label="Solicitar Matricula",
                                               command=self.alunoLogado.aluno.solicitarMatricula)
            self._topMatriculaMenu.add_command(label="Cancelar Solicitação de Matricula",
                                               command=self.alunoLogado.aluno.cancelarMatricula)
            self._topMatriculaMenu.add_command(label="Ver Historico", command=self.alunoLogado.aluno.verHistorico)

            # Top Menus do Aluno
            pass
        else:
            self._loginButton['state'] = 'normal'
            self.alunoLogado = None

    def deslogar(self):
        # TODO: adicionar todos os top menus que forem adicionados após o login
        self._topLoginMenu.delete(0, 1)
        self._topMatriculaMenu.delete(0, 2)
        self._loginButton['state'] = 'normal'

    @property
    def openWindows(self):
        return self._openWindows

    @openWindows.setter
    def openWindows(self, janela):
        self.openWindows.append(janela)

    @property
    def alunoLogado(self):
        return self._alunoLogado

    @alunoLogado.setter
    def alunoLogado(self, aluno):
        self._alunoLogado = aluno


class Disciplina:
    def __init__(self, numCreditos, codigo, nome, horario):
        self._alunosMatriculados = []
        self._numCreditos = numCreditos
        self._codigo = codigo
        self._nome = nome
        self._horario = horario
        pass


if __name__ == '__main__':
    ti = TelaInicial()
    ti.mainloop()

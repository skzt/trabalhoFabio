#!/usr/bin/env python
# -*- coding: utf-8 -*-
# TODO: REMOVER TODOS OS PRINTS!!!
import tkinter as tk
import platform as pf
from tkinter import messagebox
from Login import Login
from Sistema import Sistema
from pymysql import err
from gc import collect as garbageCollector


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
        self._flagJanela = tk.IntVar()
        self._openWindows = []
        self._janelaTopo = None

        self._sistema = Sistema()
        self._alunoLogado = None
        self._frameLogin = tk.LabelFrame(self)
        self._topLoginMenu = None
        self._topMatriculaMenu = None
        self._topBoletoMenu = None
        self._topJanelaMenu = None
        self._topSistemaMenu = None
        self._loginButton = None

        self._topMenu()
        self._loginWindow()

    def _topMenu(self):

        _topMenuBar = tk.Menu(self)
        self.config(menu=_topMenuBar)
        # =======================================================================
        # Criação dos menus da barra de menus superior
        # =======================================================================

        self._topLoginMenu = tk.Menu(self, tearoff=0)
        self._topMatriculaMenu = tk.Menu(self, tearoff=0)
        self._topBoletoMenu = tk.Menu(self, tearoff=0)
        self._topJanelaMenu = tk.Menu(self, tearoff=0)
        self._topSistemaMenu = tk.Menu(self, tearoff=0)

        # =======================================================================
        # Menu de Login
        # =======================================================================

        _topMenuBar.add_cascade(label="Login", menu=self._topLoginMenu)

        # =======================================================================
        # Menu de Matricula
        # =======================================================================
        _topMenuBar.add_cascade(label="Matricula", menu=self._topMatriculaMenu)

        # =======================================================================
        # Menu de Boletos
        # =======================================================================
        _topMenuBar.add_cascade(label="Boletos", menu=self._topBoletoMenu)

        # =======================================================================
        # Menu de Controle de Janelas
        # =======================================================================
        _topMenuBar.add_cascade(label="Janelas", menu=self._topJanelaMenu)

        # =======================================================================
        # Menu de Simulação do Sistema
        # =======================================================================
        _topMenuBar.add_separator()
        _topMenuBar.add_separator()
        _topMenuBar.add_separator()
        _topMenuBar.add_cascade(label="Sistema", menu=self._topSistemaMenu)

    def _loginWindow(self):
        # =======================================================================
        # Janela de Login
        # =======================================================================
        _userLabel = tk.Label(self._frameLogin)
        _userLabel['text'] = "Usuário:"

        _senhaLabel = tk.Label(self._frameLogin)
        _senhaLabel['text'] = "Senha:"

        self._usuarioEntry = tk.Entry(self._frameLogin)
        self._usuarioEntry['textvariable'] = self._usuarioVar
        self._usuarioEntry.bind("<Return>", lambda _: self._usuarioEntry.tk_focusNext().focus())
        self._usuarioEntry.focus()

        self._senhaEntry = tk.Entry(self._frameLogin)
        self._senhaEntry['show'] = '*'
        self._senhaEntry.bind("<Return>", lambda _: self._senhaEntry.tk_focusNext().focus())
        self._senhaEntry['textvariable'] = self._senhaVar

        self._loginButton = tk.Button(self._frameLogin)
        self._loginButton['text'] = "Iniciar Sessão"
        self._loginButton['command'] = self._efetuarLogin
        self._loginButton.bind("<Return>",
                               lambda _: self._efetuarLogin())

        _sairButton = tk.Button(self._frameLogin)
        _sairButton['text'] = "Ecerrar Aplicação"
        _sairButton['command'] = self.destroy
        _sairButton.bind("<Return>", lambda _: self.destroy())

        # =======================================================================
        # Plotando a Janela de Login na Grid
        # =======================================================================
        _userLabel.grid(row=0, column=0)
        self._usuarioEntry.grid(row=1, column=0)
        _senhaLabel.grid(row=2, column=0)
        self._senhaEntry.grid(row=3, column=0)
        self._loginButton.grid(row=4, column=0)
        _sairButton.grid(row=8, column=0)
        self._frameLogin.grid(row=0, column=0, sticky='ns')
        tk.Grid.rowconfigure(self, 0, weight=1)

    def _efetuarLogin(self):
        try:
            self.focus()
            self._loginButton['state'] = 'disabled'
            self._usuarioEntry['state'] = 'disabled'
            self._senhaEntry['state'] = 'disabled'
            self.alunoLogado = Login(janelaPrincipal=self,
                                     usuario=self._usuarioVar)
        except err.OperationalError:
            messagebox.showerror(title="Conexão ao Banco", message="Falha ao se conectar ao Banco de Dados",
                                 parent=self)

            self._loginButton['state'] = 'normal'
            self._usuarioEntry['state'] = 'normal'
            self._senhaEntry['state'] = 'normal'
            return

        if self.alunoLogado.logar(self._senhaVar):
            # Top Menus de Login
            self._topLoginMenu.add_command(label="Alterar Senha", command=self.alunoLogado.alterarSenhaWindow)
            self._topLoginMenu.add_command(label="Encerrar Sessão", command=self.deslogar)

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

    def novaJanela(self, nome, janela, **kwargs):
        """

        :param nome: Nome da Nova janela.
        :param janela: Referencia para nova janela.
        :return: True -> Significa que era de fato uma janela nova.
                 False -> Significa que não era uma janela nova.
        """

        if self._janelaTopo is None:
            self._janelaTopo = janela

        if janela in self._openWindows:
            self._mudarJanela(janela, **kwargs)

            return False

        else:
            self._openWindows.append(janela)

            index = self._openWindows.index(janela)

            self._topJanelaMenu.add_radiobutton(label=nome,
                                                value=index,
                                                variable=self._flagJanela,
                                                command=lambda: self._mudarJanela(janela))
            self._mudarJanela(janela, **kwargs)

            return True

    def fecharJanela(self, evt = None):
        print("FECHAR JANELA")
        #print(evt.widget['text'])
        if self._janelaTopo is None:
            return
        else:
            print("flagJanela: ", self._flagJanela.get())
            print("topJanela Index: ", self._topJanelaMenu.index('end'))
            print("openWindows Index", self._openWindows.index(self._janelaTopo))

            self._topJanelaMenu.delete(self._flagJanela.get())

            if len(self._openWindows) > 1:
                self._openWindows.remove(self._janelaTopo)
                self._mudarJanela(self._openWindows[0])

                for index in range(self._topJanelaMenu.index('end') + 1):
                    self._topJanelaMenu.entryconfigure(index, value=index)
            else:
                self._openWindows.clear()
                self._janelaTopo.grid_remove()

    def _mudarJanela(self, janela, **kwargs):
        index = self._openWindows.index(janela)
        self._flagJanela.set(index)
        self._janelaTopo.grid_remove()
        self._janelaTopo = janela
        self._janelaTopo.grid(kwargs)

    def deslogar(self):
        # TODO: adicionar todos os top menus que forem adicionados após o login
        self._topLoginMenu.delete(0, 'end')
        self._topMatriculaMenu.delete(0, 'end')
        self._topJanelaMenu.delete(0, 'end')

        self._loginButton['state'] = 'normal'

        self._usuarioEntry['state'] = 'normal'
        self._usuarioEntry.delete(0, 'end')

        self._senhaEntry['state'] = 'normal'
        self._senhaEntry.delete(0, 'end')

        self._senhaVar.set('')
        self._usuarioVar.set('')
        self._flagJanela.set(0)

        self._openWindows.clear()
        self._janelaTopo = None

        self._alunoLogado.encerrarsessao()
        self._alunoLogado = None

        garbageCollector()

    # verificar com professor: alunoLogado é publico ou privad no diagrama de classes?
    @property
    def alunoLogado(self):
        return self._alunoLogado

    @alunoLogado.setter
    def alunoLogado(self, login):
        self._alunoLogado = login

    @property
    def terminoMatricula(self):
        return self._terminoMatricula



if __name__ == '__main__':
    ti = TelaInicial()
    ti.mainloop()

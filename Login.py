import tkinter as tk
from tkinter import messagebox
from ConexaoBanco import ConexaoBanco
from Aluno import Aluno


class Login:
    def __init__(self, janelaPrincipal, usuario, widgets):
        """ Classe responsavel por fazer o Login no sistema e operações relacionadas com login.
        usuario -> Variavel que observa o widget usuarioEntry
        senha -> Variavel que observa o widget senhaEntry
        widgets -> os widgets de usuario e senha, respectivamente. Utilizados para alteração de estado do widget."""

        self._janelaPrincipal = janelaPrincipal
        self._widgets = widgets
        self._usuario = usuario
        self._aluno = None

        # Acesso ao banco
        self.DB = ConexaoBanco()

    def logar(self, senha):
        select = '''SELECT idAluno FROM LOGIN WHERE usuario = '%s' AND senha = MD5('%s');''' \
                 % (self._usuario.get(), senha.get())

        cursor = self.DB.cursor()

        cursor.execute(select)
        idAluno = cursor.fetchone()

        if idAluno is not None:
            """
            Caso exista um retorno no select, signifca que o login esta correto.
            Em caso de o login estiver correto, os dados do Aluno são consultados no banco, e se retorna True,
            indicando que houve sucesso no login.
            Em caso de o login estiver incorreto, retorna False indicando falha no Login
            Então é feito o bloqueio de digitação nos campos de usuario e senha, e aparecem os botões de:
            -Deslogar
            -Alterar senha
            """



            select = "SELECT * FROM ALUNO WHERE idAluno = %d;" % idAluno

            cursor.execute(select)

            tmp = cursor.fetchone()
            cursor.close()
            self._aluno = Aluno(self._janelaPrincipal, tmp[0], tmp[1], tmp[2], tmp[3], tmp[4])
            self._aluno.logado = True
            return True

        else:
            messagebox.showerror(title='Login Incorreto!', message='Usuário ou senha incorreta.',
                                 parent=self._janelaPrincipal)
            cursor.close()
            return False

    def alterarSenhaWindow(self):
        __frameMudaSenha = tk.Toplevel(self._janelaPrincipal)
        self._janelaPrincipal.openWindows = ("Alterar Senha", __frameMudaSenha)
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
        __confirmar['command'] = lambda sav=__senhaAtualVar, nsv=__novaSenhaVar, cnsv=__confNovaSenhaVar, frame=\
            __frameMudaSenha: self.alterarsenhacommit(sav, nsv, cnsv, frame)
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

        __confirmar.grid(row=6, column=0, sticky='sw')
        __cancelar.grid(row=6, column=0, sticky='se')
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
                     % (self._usuario.get(), senhaAtualVar.get())

            cursor.execute(select)

            if cursor.fetchone() is not None:
                '''Caso exista um retorno no select, signifca que o login esta correto.
                Então é liberado para fazer a atualização de senha.
                '''
                update = ('''UPDATE `LOGIN` SET `senha`= MD5('%s') WHERE `usuario` = '%s';'''
                          % (novaSenhaVar.get(), self._usuario.get())
                          )
                cursor.execute(update)
                self.DB.commit()
                cursor.close()

                messagebox.showinfo(title="Sucesso!", message="Senha Alterada com suceso.", parent=frame)
                frame.destroy()
            else:
                cursor.close()
                messagebox.showerror(title='Login Incorreto!', message='Senha incorreta.', parent=frame)
                senhaAtualVar.set("")
                novaSenhaVar.set("")
                confNovaSenhaVar.set("")

    def encerrarsessao(self):
        self._aluno.deslogar()
        del self._aluno

        self._widgets[0]['state'] = 'normal'
        self._widgets[0].delete(0, 'end')
        self._widgets[1]['state'] = 'normal'
        self._widgets[1].delete(0, 'end')

        for window in self._janelaPrincipal.openWindows:
            window[1].destroy()

        self.DB.close()
        self._widgets[0].focus()
        self._janelaPrincipal.deslogar()

    def __del__(self):
        print("OIIII LOGIN")

    @property
    def aluno(self):
        return self._aluno

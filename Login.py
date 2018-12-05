import tkinter as tk
from tkinter import messagebox
from ConexaoBanco import ConexaoBanco
from Aluno import Aluno


class Login:
    def __init__(self, janelaPrincipal, usuario):
        """
        Classe responsavel por fazer o Login no sistema e operações relacionadas com login.
        Também é responsavel por manter a sessão do usuario e caminho para acesso aos dados
        do usuario (ALUNO).

        :var self._janelaPrincipal: Referencia a janela princiapl.
        :var self._usuario: Referencia a variavel que armazena o usuario digitado.
        :var self._aluno: Objeto de Aluno, contendo todos seus dados.
        :var self.DB: Referencia ao objeto de conexão ao banco de dados.

        :param janelaPrincipal: Referencia a janela principal.
        :param usuario: Referencia a variavel que armazena o usuario digitado.
        """
        """ 
        usuario -> Variavel que observa o widget usuarioEntry
        senha -> Variavel que observa o widget senhaEntry
        widgets -> os widgets de usuario e senha, respectivamente. Utilizados para alteração de estado do widget."""

        self._janelaPrincipal = janelaPrincipal
        self._usuario = usuario
        self._aluno = None

        self.DB = ConexaoBanco()

    def logar(self, senha):
        """
        Metodo publico, responsavel por efetivar o login, verificando a existencia de um
        usuario e senha compativeis com o digitado.
        :param senha: Variavel que armazena a senha digitada pelo usuario.
        :return:VOID
        """
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
        """
        Metodo publico, responsavel por gerar a janela de alteração de senha.
        :return: VOID
        """
        _frameMudaSenha = tk.Toplevel(self._janelaPrincipal)
        self._janelaPrincipal.openWindows = ("Alterar Senha", _frameMudaSenha)
        _senhaAtualVar = tk.StringVar()
        _novaSenhaVar = tk.StringVar()
        _confNovaSenhaVar = tk.StringVar()
        # =======================================================================
        # Labels
        # =======================================================================
        _senhaAtualLabel = tk.Label(_frameMudaSenha)
        _senhaAtualLabel['text'] = "Senha Atual"
        _novaSenhaLabel = tk.Label(_frameMudaSenha)
        _novaSenhaLabel['text'] = "Nova Senha"
        _confNovaSenhaLabel = tk.Label(_frameMudaSenha)
        _confNovaSenhaLabel['text'] = "Confirmar Senha"

        # =======================================================================
        # Entrys
        # =======================================================================
        _senhaAtualEntry = tk.Entry(_frameMudaSenha)
        _senhaAtualEntry['textvariable'] = _senhaAtualVar
        _senhaAtualEntry['show'] = '*'
        _senhaAtualEntry.focus()

        _novaSenhaEntry = tk.Entry(_frameMudaSenha)
        _novaSenhaEntry['textvariable'] = _novaSenhaVar
        _novaSenhaEntry['show'] = '*'

        _confNovaSenhaEntry = tk.Entry(_frameMudaSenha)
        _confNovaSenhaEntry['textvariable'] = _confNovaSenhaVar
        _confNovaSenhaEntry['show'] = '*'

        # =======================================================================
        # Buttons
        # =======================================================================

        _confirmar = tk.Button(_frameMudaSenha)
        _confirmar['text'] = "Confirmar"
        _confirmar['command'] = lambda sav=_senhaAtualVar, nsv=_novaSenhaVar, cnsv=_confNovaSenhaVar, frame=\
            _frameMudaSenha: self._alterarsenhacommit(sav, nsv, cnsv, frame)
        _cancelar = tk.Button(_frameMudaSenha)
        _cancelar['text'] = "Cancelar"
        _cancelar['command'] = _frameMudaSenha.destroy

        # =======================================================================
        # Grids
        # =======================================================================
        _senhaAtualLabel.grid(row=0, column=0)
        _novaSenhaLabel.grid(row=2, column=0)
        _confNovaSenhaLabel.grid(row=4, column=0)

        _senhaAtualEntry.grid(row=1, column=0)
        _novaSenhaEntry.grid(row=3, column=0)
        _confNovaSenhaEntry.grid(row=5, column=0)

        _confirmar.grid(row=6, column=0, sticky='sw')
        _cancelar.grid(row=6, column=0, sticky='se')
        return

    def _alterarsenhacommit(self, senhaAtualVar, novaSenhaVar, confNovaSenhaVar, frame):
        """
        Metodo privado, responsavel por conferir as senhas digitadas e efetuar
        a atualização da senha no banco de dados.

        :param senhaAtualVar: Variavel que armazena a senha digitada pelo usuario.
        :param novaSenhaVar: Variavel que armazena a nova senha digitada pelo usuario.
        :param confNovaSenhaVar: Variavel que armazena a novamente a nova
        senha digitada pelo usuario.
        :param frame: Referencia a janela de alteração de senha.
        :return: Void
        """
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
        """
        Metodo publico, responsavel por encerrar a sessão de login.
        :return: VOID
        """
        self._aluno.deslogar()

    @property
    def aluno(self):
        return self._aluno

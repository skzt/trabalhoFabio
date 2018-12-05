from time import strftime
from ConexaoBanco import ConexaoBanco
from FramesMatricula import FramesMatricula


class Matricula:
    def __init__(self, janelaPrincipal, idAluno, curso):
        """
        Classe fachada(Façade), responsavel pelo processamento necessario para:
            - Solicitar Matricula em Disciplinas;
            - Cancelar Solicitação de Matricula em Disciplinas;
            - Visualizar Historico.

        :var self._janelaPrincipal: Referencia a janela principal.
        :var self._curso : Curso do Aluno.
        :var self._idAluno: Identificado do Aluno.
        :var self.DB: Referencia a ConexaoBanco.
        :var self._frameSolicitacao: Referencia ao frame(Janela) de solicitação de matricula.
        :var self._frameCancelamento: Referencia ao frame(Janela)
        de cancelamento de solicitação de matricula.
        :var self._frameHistorico: Referencia ao frame(Janela) de historico.

        :param janelaPrincipal: Referencia a janela principal.
        :param idAluno: Identificado do Aluno.
        :param curso: Curso do Aluno.
        """
        self._janelaPrincipal = janelaPrincipal

        self._curso = curso
        self._idAluno = idAluno

        self.DB = ConexaoBanco()
        self._frameSolicitacao = None
        self._frameCancelamento = None
        self._frameHistorico = None

    def solicitarMatricula(self):
        """
        Metodo publico, responsavel por solicitar a criação de um frame e seus widgets,
        para a solicitação de matricula.
        :return: VOID
        """
        metodos = {"mudarSemestre": self._mudarSemestre,
                   "confirmarSolicitacao": self._confirmarSolicitacao
                   }
        if self._frameSolicitacao is None:
            self._frameSolicitacao = FramesMatricula(self._janelaPrincipal, metodos)
        self._frameSolicitacao.frameSolicitar()

    def cancelarMatricula(self):
        """
        Metodo publico, responsavel por solicitar a criação de um frame e seus widgets,
        para o cancelamento de solicitação de matricula.
        :return: VOID
        """
        metodos = {"confirmarCancelamento": self._confirmarCancelamento}

        if self._frameCancelamento is None:
            self._frameCancelamento = FramesMatricula(self._janelaPrincipal, metodos)
        self._carregarProcessando()
        self._frameCancelamento.frameCancelar()

    def verHistorico(self):
        """
        Metodo publico, responsavel pro solicitar a criação de um frame e seus widgets,
        para a visualização do Historico.
        :return: VOID
        """
        if self._frameHistorico is None:
            self._frameHistorico = FramesMatricula(self._janelaPrincipal)
        self._frameHistorico.frameHistorico()
        self._popularHistorico()

    def _carregarProcessando(self):
        """
        Metodo privado, responsavel por verificar se existe alguma
        disciplina deste aluno com situação == PROCESSANDO e popula
        a lista _frameCancelamento._listaDisciplinas com essas disciplinas, se houver.
        :return: VOID
        """

        cursor = self.DB.cursor()

        select = '''
        SELECT DISCIPLINA.codigo, DISCIPLINA.nome
        FROM DISCIPLINA
               JOIN DISCIPLINA_ALUNO
                 ON DISCIPLINA.idDisciplina = DISCIPLINA_ALUNO.idDisciplina
        WHERE DISCIPLINA_ALUNO.idAluno = %d
          AND DISCIPLINA_ALUNO.situacao = 1;''' % self._idAluno

        cursor.execute(select)
        disciplinasProcessadas = cursor.fetchall()

        if len(disciplinasProcessadas) == 0:
            # Não possui disciplinas com status PROCESSANDO
            pass
        else:
            tmp = []
            for disciplina in disciplinasProcessadas:
                tmp.append(str(disciplina[0]) + ' - ' + disciplina[1])
            self._frameCancelamento.listaDisciplinas = tmp

        cursor.close()

    def _mudarSemestre(self, evt):
        """
        Metodo privado, responsavel por alterar a lista de disciplinas, de acordo com o
        semestre selecionado.
        :param evt: Objeto de Event, que contem referencia ao widget ComboBox ,
        para obter o semestre escolhido.
        :return: VOID
        """
        widget = evt.widget

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

        select = '''
        SELECT DISCIPLINA.codigo,
               DISCIPLINA.nome
        FROM DISCIPLINA
        WHERE idDisciplina != ALL (
                                    SELECT idDisciplina
                                    FROM DISCIPLINA_ALUNO
                                    WHERE DISCIPLINA_ALUNO.idAluno = %d
                                      AND DISCIPLINA_ALUNO.situacao NOT IN (3, 6, 7)
                                  )
          AND semestreGrade = %d;''' \
                 % (self._idAluno, mapaSemestre[widget.get()])

        cursor = self.DB.cursor()
        cursor.execute(select)

        listaDisciplinas = []

        for disciplina in cursor.fetchall():
            # Cria uma lista de tuplas: (codigoDisciplina, nome)
            tmp = str(disciplina[0]) + ' - ' + disciplina[1]
            if tmp not in self._frameSolicitacao.listaSelecionados:
                listaDisciplinas.append(tmp)
            else:
                continue
        cursor.close()
        listaDisciplinas.sort()
        self._frameSolicitacao.listaDisciplinas = listaDisciplinas

    def _confirmarSolicitacao(self):
        """
        Metodo Privado, responsavel por finalizar a solicitação de matricula,
        salvadno no banco as disciplinas solicitadas pelo Aluno, com a situação "PROCESSANDO".
        :return: VOID
        """
        self._frameSolicitacao.focus()
        self._janelaPrincipal.fecharJanela()

        cursor = self.DB.cursor()
        for disciplina in self._frameSolicitacao.listaSelecionados:
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
            values (%d, %d, %d); ''' % (idDisciplina, idSemestreDisciplina, self._idAluno)

            cursor.execute(insert)
            self.DB.commit()
        cursor.close()

        self._frameSolicitacao = None

    def _confirmarCancelamento(self):
        """
        Metodo Privado, responsavel por finalizar o cancelamento de solicitação de matricula,
        deletando do banco as disciplinas solicitadas pelo Aluno, com a situação "PROCESSANDO".
        :return: VOID
        """
        self._frameCancelamento.focus()
        self._janelaPrincipal.fecharJanela()

        select = ''' select DISCIPLINA.codigo, DISCIPLINA.idDisciplina
from DISCIPLINA
       JOIN DISCIPLINA_ALUNO
         ON DISCIPLINA.idDisciplina = DISCIPLINA_ALUNO.idDisciplina
WHERE DISCIPLINA_ALUNO.situacao = 1
  AND DISCIPLINA_ALUNO.idAluno = %d;''' % self._idAluno

        cursor = self.DB.cursor()
        cursor.execute(select)

        disciplinasCancelar = {}

        for disciplina in cursor.fetchall():
            disciplinasCancelar[disciplina[0]] = disciplina[1]

        for disciplina in self._frameCancelamento.listaSelecionados:
            delet = ''' DELETE FROM DISCIPLINA_ALUNO where idDisciplina = %d''' \
                    % disciplinasCancelar[int(disciplina[:4])]
            cursor.execute(delet)

        self.DB.commit()
        cursor.close()
        self._frameCancelamento = None

    def _popularHistorico(self):
        """
        Metodo privado, responsavel por populas a janela de Historico com os dados das
        disciplinas cursadas e selecionadas, pelo aluno.
        :return: VOID
        """
        self._frameHistorico.treeHistorico.delete(*self._frameHistorico.treeHistorico.get_children())
        cursor = self.DB.cursor()
        situacao = {1: "PROCESSANDO",
                    2: "CURSANDO",
                    3: "RECUSADO",
                    4: "APROVEITAMENTO\nDE CREDITO",
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
                WHERE DISCIPLINA_ALUNO.idAluno = %d;''' % self._idAluno

        cursor.execute(select)
        historico = cursor.fetchall()
        for disciplina in historico:
            disciplina = list(disciplina)
            disciplina[6] = situacao[disciplina[6]]

            if disciplina[0] not in semestres:
                semestres[disciplina[0]] = []

            semestres[disciplina[0]].append(disciplina[1:])
            semestres[disciplina[0]].sort()

        for semestre in range(1, 11):

            if semestre in semestres:
                treeItem = self._frameHistorico.treeHistorico.insert('',
                                                                     'end',
                                                                     text=mapaSemestre[semestre])
                tmp = 0
                for disciplina in semestres[semestre]:
                    if tmp % 2 == 0:
                        self._frameHistorico.treeHistorico.insert(treeItem, 'end', values=disciplina, tags=('par',))
                    else:
                        self._frameHistorico.treeHistorico.insert(treeItem, 'end', values=disciplina, tags=('impar',))
                    tmp += 1
        cursor.close()

    def deslogar(self):
        """
        Metodo publico, responsavel por encerrar todas as janelas
        que a Matricula tenha aberto para finalizar a sessão.
        :return: VOID
        """
        if self._frameSolicitacao is not None:
            self._frameSolicitacao.destroy()
            del self._frameSolicitacao

        if self._frameCancelamento is not None:
            self._frameCancelamento.destroy()
            del self._frameCancelamento

        if self._frameHistorico is not None:
            self._frameHistorico.destroy()
            del self._frameHistorico

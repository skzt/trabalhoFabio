from tkinter import Entry


class DataEntry(Entry):
    def __init__(self, parent, variavel, *arg, **kwarg):
        """
        Cria uma entry especifica para digitação de datas no padrão dd/mm/aaaa

        :param parent: Widget de origem
        :param variavel: StringVar para para obter o text da Entry
        """

        Entry.__init__(self, parent, *arg, **kwarg)
        self.focus()
        self._textvariable = variavel
        self['textvariable'] = self._textvariable
        self._textvariable.set("  /  /    ")
        self._textvariable.trace_id = self._textvariable.trace('w', self._validaData)

    def _validaData(self, *_):
        """
        Metodo privado, responsavel por validar toda entrada de dados no widget e tratalo
        de maneira a se manter o padrão dd/mm/aaaa.
        :param _: Apenas ignora os paramentros passados automaticamente pelo metodo StringVar.trace()
        :return: VOID
        """
        if self.winfo_exists() == 0:
            self._textvariable.trace_vdelete('w', self._textvariable.trace_id)
            return

        if len(self._textvariable.get()) == 0:
            self._textvariable.set('  /  /    ')
            return

        if self._textvariable.get() == '  /  /    ':
            return

        data = list(self._textvariable.get())
        atual = self.index('insert')

        if len(data) < 10:
            faltando = 10 - len(data)
            for _ in range(faltando):
                data.append(' ')

            for _ in range(faltando):
                for position in range(atual, 9):
                    data[position], data[9] = data[9], data[position]

            if data.count('/') < 2:
                if data[2] == ' ':
                    data[2] = '/'
                if data[5] == ' ':
                    data[5] = '/'

        else:
            if ' ' in data:

                if data[atual].isspace():
                    data = data[:atual] + data[atual + 1:]

                elif data[atual] is '/':
                    data[atual - 1], data[atual] = data[atual], data[atual - 1]
                    self.icursor(atual + 1)

                    atual = self.index('insert')
                    if data[atual].isspace():
                        data = data[:atual] + data[atual + 1:]

            if data[2] != '/':
                if data[1] == '/':
                    data[2], data[1] = data[1], data[2]
                elif data[3] == '/':
                    data[2], data[3] = data[3], data[2]
                    self.icursor(atual + 1)

            if data[5] != '/':
                if data[4] == '/':
                    data[5], data[4] = data[4], data[5]

                elif data[6] == '/':
                    data[5], data[6] = data[6], data[5]
                    self.icursor(atual + 1)

        saida = ''
        for char in data:
            if char.isdecimal() or char in [' ', '/']:
                saida += char
            else:
                saida += ' '
        self._textvariable.set(saida[:10])

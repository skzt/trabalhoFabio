from tkinter import Entry


class DataEntry(Entry):
    def __init__(self, parent, variavel, *arg, **kwarg):
        """
        Cria uma entry especifica para digitação de datas no padrão dd/mm/aaaa

        :param parent: Widget de origem
        :param variavel: StringVar para para obter o text da Entry
        :param arg:
        :param kwarg:
        """

        Entry.__init__(self, parent, *arg, **kwarg)
        self.focus()

        self.textvariable = variavel
        self['textvariable'] = self.textvariable
        self.textvariable.set("  /  /    ")
        self.textvariable.trace('w', self.__validaData)

    def __validaData(self, *_):
        if len(self.textvariable.get()) == 0:
            self.textvariable.set('  /  /    ')
            return

        if self.textvariable.get() == '  /  /    ':
            return

        data = list(self.textvariable.get())
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
        self.textvariable.set(saida[:10])

    @property
    def textvariable(self):
        return self.__textvariable

    @textvariable.setter
    def textvariable(self, variavel):
        self.__textvariable = variavel

# import kivy
from kivy.app import App
# from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, BooleanProperty
from kivy.uix.textinput import TextInput
from kivy.metrics import dp, sp

import conv_s as conv
# from kivy.effects.opacityscroll import OpacityScrollEffect
from kivy.config import Config
from kivy.app import Factory

# Указываем пользоваться системным методом ввода, использующимся на
# платформе, в которой запущенно приложение.
# Config.set("kivy", "keyboard_mode", "system")
    # Activity баг репорта.
# https://habr.com/ru/post/300960/ -- тут пример файла main.py для сборки под ведро с логом ошибок запуска

Config.set('graphics', 'width', '480')
Config.set('graphics', 'height', '640')


def showdic(dic):
    print(f'{dic}\n{"-" * 10}')
    for k, v in dic.items():
        print(f'{k}: {v}')


class NsConv(BoxLayout):
    # ! Лучше было сделать слежение за изменением значения в тогглах, чем каждый раз проверять активный и апдейтить
    # класс
    #
    tb_inp_lst = []  # тут лежат объекты CToggButt, доступны все свойства ToggleButton
    tb_out_lst = []
    inp = StringProperty()
    out = StringProperty()
    tbg_values = {'BIN': 2, 'OCT': 8, 'DEC': 10, 'HEX': 16}
    tbg_from = ObjectProperty()
    tbg_to = ObjectProperty()
    val_inpsys = NumericProperty()
    val_outsys = NumericProperty()
    lb_debug = ObjectProperty()
    cti = ObjectProperty()
    ti = ObjectProperty()
    tifocus = BooleanProperty()


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # сделаю списки объектов CToggButt для обоих групп, для простого доступа к свойствам ToggleButton
        # вместо self.ids.tbg_from.ids.tb_xxx.property можно self.tb_inp_lst[0].property
        self.tb_inp_lst = [self.ids.tbg_from.ids[tb].__self__ for tb in self.ids.tbg_from.ids if tb.startswith('tb')]
        self.tb_inp_lst.append(self.ids.butt_ascii)
        self.tb_out_lst = [self.ids.tbg_to.ids[tb].__self__ for tb in self.ids.tbg_to.ids if tb.startswith('tb')]
        self.tb_inp_lst[2].state = 'down'
        self.tb_out_lst[0].state = 'down'
        # self.lb_debug.text = 'Info for debugging'
        # self.cti.ids['ti'].focus = True

    def ctb_released(self):
        ...

    def showdebug(self, *args):
        print(self.height, self.width)
        self.lb_debug.text = f'N:{self.height}, {self.width} -- DP:{dp(self.height)}, {dp(self.width)} -- ' \
                             f'SP:{sp(self.height)}, {sp(self.width)}'

    def clr(self):
        # self.lb_debug.text = '...'
        self.inp = ''


    def on_inp(self, instance, text):
        maxdig = conv.get_max_dig(text)
        for i, b in enumerate(self.tb_inp_lst):
            if maxdig >= b.val:  # входное число не может быть представлено в выбранной системе
                                # Например, 102 не может быть двоичным а G шестнадцатиричным
                if b.state == 'down':
                    b.state = 'normal'
                    if i + 1 < len(self.tb_inp_lst):  # активирую следующую за неактивной кнопку
                        self.tb_inp_lst[i + 1].state = 'down'
                b.disabled = True
            else:
                if all([b.disabled for b in self.tb_inp_lst[:-1]]):
                    self.tb_inp_lst[-1].state = 'down'
                b.disabled = False
        self.convert()

    def convert(self):
        # print(f'Convert {self.inp} <{self.val_inpsys}> --> <{self.val_outsys}>')

        if self.inp:
            if self.val_inpsys == 0xFFFF:
                self.out = conv.transform(self.inp, 'ascii', self.val_outsys)
            else:
                self.out = conv.transform(self.inp, self.val_inpsys, self.val_outsys)
        else:
            self.out = ''

    def on_val_inpsys(self, *args):
        self.convert()

    def on_val_outsys(self, *args):
        self.convert()


class NsConvApp(App):
    title = 'Конвертер систем счисления'

    def build(self):
        return NsConv()


if __name__ == '__main__':
    NsConvApp().run()

"""
Траблы: в текстинпуте на ведре текст микроскопического размера "+" Поставил дефолтный
большой размер АПК, мож венв исключить из компиляции, можно прописать в конфиге бильдозера "-" ХЗ почему так
появляющаяся клава скрывает кнопки преобразования "-" Возможное решение, клава появляется, когда появляется фокус в поле ввода
не удаляется первый символ в текстинпуте при нажатии бекспейса на ведровой клаве "+" уже удаляется, хз что было
Попробовать убрать размер экрана из начала файла "-" ничего не поменялось
"""
# import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty

import conv_s as conv

from kivy.config import Config

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # сделаю списки объектов CToggButt для обоих групп, для простого доступа к свойствам ToggleButton
        # вместо self.ids.tbg_from.ids.tb_xxx.property можно self.tb_inp_lst[0].property
        self.tb_inp_lst = [self.ids.tbg_from.ids[tb].__self__ for tb in self.ids.tbg_from.ids if tb.startswith('tb')]
        self.tb_inp_lst.append(self.ids.butt_ascii)
        self.tb_out_lst = [self.ids.tbg_to.ids[tb].__self__ for tb in self.ids.tbg_to.ids if tb.startswith('tb')]
        self.tb_inp_lst[2].state = 'down'
        self.tb_out_lst[0].state = 'down'

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
        # self.out = self.inp

    def convert(self):
        # print(f'Convert {self.inp} <{self.val_inpsys}> --> <{self.val_outsys}>')
        if self.inp:
            self.out = conv.transform(self.inp, self.val_inpsys, self.val_outsys)
        else:
            self.out = ''

    def on_val_inpsys(self, *args):
        # print('a')
        self.convert()

    def on_val_outsys(self, *args):
        # print('b')
        self.convert()

class NsConvApp(App):
    title = 'Конвертер систем счисления'

    def build(self):
        return NsConv()


if __name__ == '__main__':
    NsConvApp().run()

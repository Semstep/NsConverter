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


class ToggButtGroup:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        showdic(self.ids)


class NsConv(BoxLayout):
    # ! Лучше было сделать слежение за изменением значения в тогглах, чем каждый раз проверять активный и апдейтить
    # класс
    #
    tb_inp_lst = []  # тут лежат объекты CToggButt, доступны все свойства ToggleButton
    tb_out_lst = []
    inp = StringProperty()
    tbg_values = {'BIN': 2, 'OCT': 8, 'DEC': 10, 'HEX': 16}
    tbg_from = ObjectProperty()
    tbg_to = ObjectProperty()
    inpsysval: int
    outsysval: int
    val1 = NumericProperty()
    val2 = NumericProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # сделаю списки объектов CToggButt для обоих групп, для простого доступа к свойствам ToggleButton
        # вместо self.ids.tbg_from.ids.tb_xxx.property можно self.tb_inp_lst[0].property
        self.tb_inp_lst = [self.ids.tbg_from.ids[tb].__self__ for tb in self.ids.tbg_from.ids if tb.startswith('tb')]
        self.tb_inp_lst.append(self.ids.butt_ascii)
        self.tb_out_lst = [self.ids.tbg_to.ids[tb].__self__ for tb in self.ids.tbg_to.ids if tb.startswith('tb')]
        self.tb_inp_lst[2].state = 'down'
        self.tb_out_lst[0].state = 'down'

    def tgbutt_pressed(self, instance, grp, capt):
        if instance.disabled:
            return
        hdrstr = f'{"*" * 5} {grp}: {capt} {"*" * 5}'
        print(hdrstr)
        for b in self.tb_inp_lst:
            print(f'{b.text} state is {b.state}')
        print('-' * len(hdrstr))

    def on_inp(self, instance, text):
        maxdig = conv.get_max_dig(text)
        for i, b in enumerate(self.tb_inp_lst):
            # print(f'{i}: {b.val}')
            if maxdig >= b.val:
                if b.state == 'down':
                    b.state = 'normal'
                    if i + 1 < len(self.tb_inp_lst):
                        self.tb_inp_lst[i + 1].state = 'down'
                b.disabled = True
            else:
                if all([b.disabled for b in self.tb_inp_lst[:-1]]):
                    self.tb_inp_lst[-1].state = 'down'
                b.disabled = False

    def on_val1(self, *args):
        print(f'value changes on {args[1]}')

    def on_val2(self, *args):
        print(f'value changes on {args[1]}')


class NsConvApp(App):
    title = 'Конвертер систем счисления'

    def build(self):
        return NsConv()


if __name__ == '__main__':
    NsConvApp().run()

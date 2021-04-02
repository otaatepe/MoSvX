from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleview import RecycleView
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem
from kivymd.uix.tab import MDTabsBase
from kivy.properties import ListProperty

Window.size = (300, 500)

products = ['coffee', 'tea', 'milk', 'sugar', 'honey', 'cake', 'toast']


class RV(RecycleView):
    rv_products = ListProperty([{'text': x} for x in products])

    # def __init__(self, **kwargs):
    #     super(RV, self).__init__(**kwargs)
        # this code below does't update the recycleview whenever products updated.
        # self.data = [{'text': str(x)} for x in products]
        # this displays in the recycleview
        # self.data = [{'text': str(x)} for x in ['a', 'b', 'c']]


class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass


class MyLayout(BoxLayout):
    scr_mngr = ObjectProperty(None)

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen


class OpenDialog(Popup):
    pass


class MenuOSApp(MDApp):
    def __init__(self, items=[], list_items=[]):
        MDApp.__init__(self)
        self.items = items
        self.list_items = list_items

    def on_start(self):
        pass

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        print("something")

    def show_MDDialog(self, card_id):
        dlg = OpenDialog(title=card_id)
        dlg.open()

    def show_MDInput(self):
        pass

    def show_items(self):
        self.root.ids.container.clear_widgets()
        for i in range(len(products)):
            self.root.ids.container.add_widget(
                OneLineListItem(text=f"{products[i]}")
            )

    def impulse_item_clicked(self, values={}):
        products.append(values)
        self.show_items()
        print(f'impulse item clicked {values}')
        self.root.ids.rv.rv_products.append({'text': values})
        #rv_products = ListProperty([{'text': x} for x in products])
        print(self.root.ids.rv.rv_products)

    def close_spinner(self, id):
        print(id)

    def spinner_values(self, values=[]):
        print(values)


if __name__ == '__main__':
    MenuOSApp().run()
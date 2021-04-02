from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.app import MDApp
from kivy.core.window import Window
from kivymd.uix.list import OneLineListItem
from kivymd.uix.tab import MDTabsBase
from kivy.uix.recycleview import RecycleView
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label
#import StackOverflow.globalvariables as GlobalVariables

Window.size = (300, 500)


class RV(RecycleView):
    products = []

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))

class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
class MyLayout(BoxLayout):

    scr_mngr = ObjectProperty(None)
    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen


class OpenDialog(Popup):
    pass


class MenuOSApp(MDApp, RV):

    def on_start(self, items = []):

        pass

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        print("something")

    def show_MDDialog(self, card_id):
        dlg = OpenDialog(title = card_id)
        dlg.open()
    def show_MDInput(self):
        pass

    def show_items(self):
        self.root.ids.container.clear_widgets()

        for i in range(len(self.products)):
            self.root.ids.container.add_widget(
                OneLineListItem(text=f"{self.products[i]}")
            )

    def show_items_inRV(self):
        pass


    def hot_beverage_clicked(self, values = {}):

        self.products.append(values)


        self.show_items()


    def impulse_item_clicked(self, values = {}):
        self.products.append(values)
        self.show_items()

    def close_spinner(self, id):
        print(id)
    def spinner_values(self, values=[]):
        print(values)

if __name__ == '__main__':
    MenuOSApp().run()
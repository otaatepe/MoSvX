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
import pandas as pd
from datetime import datetime
import pyrebase

import smtplib
import json

Window.size = (300, 500)

products = []
# pr_items = [
#          {'SKU': '510001', 'PR_name': 'Caramel Whaffle', 'PR_price': '1.30'},
#          {'SKU': '523001', 'PR_name': 'Biscotti', 'PR_price': '1.70'},
#          {'SKU': '641301', 'PR_name': 'Mini Whaffles', 'PR_price': '2.50'}]
pr_items = []
#tr_items = [{'TRANS_DATE': '510001', 'TRANS_USER': 'Caramel Whaffle', 'TRANS_SUM': '1.30'}]
tr_items = []

class RV(RecycleView):
    rv_products = ListProperty(
        [{'sku': str(x['SKU']), 'pr_name': str(x['PR_name']), 'pr_price': x['PR_price']} for x in pr_items])


class RVH(RecycleView):
    rvh_transactions = ListProperty(
        [{'trans_date': str(t['TRANS_DATE']), 'trans_user': str(t['TRANS_USER']), 'trans_sum': str(t['TRANS_SUM'])} for
         t in tr_items])
class Tab(MDFloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    pass


class TableBasket(BoxLayout):
    pass


class TableHistory(BoxLayout):
    pass


class MyLayout(BoxLayout):
    scr_mngr = ObjectProperty(None)

    def change_screen(self, screen, *args):
        self.scr_mngr.current = screen


class OpenDialog(Popup):
    pass


class MenuOSApp(MDApp):
    # url = 'https://kivymos-default-rtdb.firebaseio.com/'
    # firebase_app = firebase.FirebaseApplication(url, None)

    config = {
        "apiKey": "apiKey",
        "authDomain": "kivymos.firebaseapp.com",
        "databaseURL": "https://kivymos-default-rtdb.firebaseio.com/",
        "storageBucket": "kivymos.appspot.com"
    }
    firebase_app = pyrebase.initialize_app(config)

    def __init__(self, items=[], list_items=[]):
        MDApp.__init__(self)
        self.items = items
        self.list_items = list_items

    def on_start(self):
        self.show_transaction_history()
        #db_history = self.firebase_app.database().child("2021-04-02 18:35:27").get()


            # for h in hist.val():
            #     print(h)
            # print(hist.key())
            # tr_user = hist.get('Username')
            # tr_sum = hist.get('Sum')
        #
        # #print(db_history.val())
        # tr_date = db_history.key()
        # print(tr_date)
        # tr_user = db_history.val().get('Username')
        # print("printing username")
        # print(tr_user)
        # print("printing username finished")
        # tr_sum = db_history.val().get('Sum')
        # print(tr_sum)
        # self.root.ids.rvh.rvh_transactions.append(
        #     {'trans_date': str(tr_date), 'trans_user': str(tr_user), 'trans_sum': str(tr_sum)})
        #
        # # printing the items of this specific child above.
        # for entry in db_history.each():
        #
        #
        #     if entry.key() == "Items":
        #         for k in entry.val():
        #             self.root.ids.rvh.rvh_transactions.append({'trans_date': str(k['sku']), 'trans_user': str(k['pr_name']), 'trans_sum': str(k['pr_price'])})
        #             #print("{} - {} - {}".format(k['sku'], k['pr_name'], k['pr_price']))
        #     if entry.key() == "Sum":
        #         print(entry.val())
        pass

    def on_tab_switch(
            self, instance_tabs, instance_tab, instance_tab_label, tab_text
    ):
        pass

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
        # append this values dict to global list 'products'
        products.append(values)

        # run show items to display it in list widget
        # self.show_items()
        # print what item is clicked
        print(f'impulse item clicked {values}')
        # append the same values dictionary to rv_products ListProperty using .kv  recycleview data 'data : self.rv_products' this will update the recycleview
        self.root.ids.rv.rv_products.append(
            {'sku': values.get('sku'), 'pr_name': values.get('pr_name'), 'pr_price': values.get('pr_price')})

        basket_items = self.root.ids.rv.rv_products
        df = pd.DataFrame(basket_items)
        # print their data types
        print("printing data types")
        print(df.dtypes)
        # create dict of what you like this rv_product data types to be
        convert_rv_products = {'sku': int, 'pr_name': str, 'pr_price': float}
        # convert it using astype()
        df = df.astype(convert_rv_products)
        # at this moment pr_price datatype changed to float. Now, get the SUM of it and print it in the console
        print("printing TOtal")
        sum_items = "%.2f" % df.pr_price.sum()
        print(sum_items)

        self.root.ids.basket_sum_text.text = "Sum : " + str("%.2f" % df.pr_price.sum())


    def close_spinner(self, id):
        print(id)

    def spinner_values(self, values=[]):
        print(values)

    def post(self, values):
        result = self.firebase_app.post(self.url, values)
        print(result)
        # to_database = json.loads(values)
        # requests.post(url=self.url, json=to_database)

    def pay_basket(self):

        # get current date time
        now = datetime.now()
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
        print("now = ", dt_string)

        basket_items = self.root.ids.rv.rv_products

        # result = self.firebase_app.post(self.url, basket_items)

        # self.pay_basket(values)
        # SUM of product price 'pr_price'

        # create a DataFrame for recycleview data which is rv_products
        df = pd.DataFrame(basket_items)

        # print their data types
        # print("printing data types")
        # print(df.dtypes)
        # create dict of what you like this rv_product data types to be
        convert_rv_products = {'sku': int, 'pr_name': str, 'pr_price': float}
        # convert it using astype()
        df = df.astype(convert_rv_products)
        # at this moment pr_price datatype changed to float. Now, get the SUM of it and print it in the console
        print("printing TOtal")
        print(df.pr_price.sum())
        # print the recycleview data which is 'self.root.ids.rv.rv_products'
        print(basket_items)
        print("rv_products finished")
        # insert (set) values into firebase RealTime Database
        db = self.firebase_app.database()
        user_name = 'Soyut'
        basket_items_with_sum = {"Username" : user_name, "Sum": float("%.2f" % df.pr_price.sum()), "Items": basket_items}
        #basket_items_with_sum = {"Sum": df.pr_price.sum(), "Items": basket_items}

        results = db.child(dt_string).set(basket_items_with_sum)
        #results = db.child(dt_string).child("Soyut").set(basket_items_with_sum)
        print(results)
        self.root.ids.rv.rv_products = {}

        self.send_transaction_email(basket_items)
        self.root.ids.basket_sum_text.text = ""
        self.show_transaction_history()

    # send transactions as an email
    def send_transaction_email(self, basket_items):
        message = ""
        for item in basket_items:
            message += item['pr_name'] + " - " + item['pr_price'] + "\n"
        #    print(message)
        print("############")
        print(message)
        print("############")

        # server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        # server.login("otaatepe@gmail.com", "Sifre$123")
        # server.sendmail("otaatepe@gmail.com","soyuty@gmail.com", message)
        # server.quit()

    def show_transaction_history(self):
        db_history2 = self.firebase_app.database().get()

        tr_user = ""
        tr_sum = ""
        for hist in db_history2.each():
            tr_date = hist.key()
            print(hist.key())
            for h in hist.val().items():
                if h[0] == "Username":
                    tr_user = h[1]
                if h[0] == "Sum":
                    tr_sum = h[1]
            print(tr_date, tr_user, tr_sum)
            self.root.ids.rvh.rvh_transactions.append(
                {'trans_date': str(tr_date), 'trans_user': str(tr_user), 'trans_sum': str(tr_sum)})


if __name__ == '__main__':
    MenuOSApp().run()

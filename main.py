from distutils.command.build import build
from turtle import getscreen
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.list import OneLineAvatarIconListItem
import sqlite3
from kivymd.uix.boxlayout import MDBoxLayout,BoxLayout
from kivymd.uix.dialog import MDDialog
kv = """
<ContentsInDialoge>:
    orientation:'vertical'
    spacing: "5dp"
    size_hint: .4, None
    height: "130"
    MDTextField:
        id:taskID
        hint_text:"Task To Do"
        text:""
        on_touch_down: if self.collide_point(*args[1].pos): self.text = ""
        
    MDRaisedButton:
        text:'Cancel'
        pos_hint:{'center_x':.5,'center_y':.5}
        on_press:app.close()
    MDRaisedButton:
        text:'Save'
        pos_hint:{'center_x':.5,'center_y':.3}
        on_press:(app.add_data_to_list(taskID.text),app.close())
<ListItemWithCheckbox>:
    id: the_list_item3
    markup: True

    IconRightWidget:
        icon: 'trash-can-outline'
        theme_text_color: "Custom"
        text_color: 1, 0, 0, 1
        on_release:
            root.delete_item(the_list_item3)
    IconLeftWidget:
    	icon:'progress-check'
Screen:
    MDLabel:
        text:'To Do List'
        halign:'center'
        pos_hint:{'center_y':.9}
    MDFloatLayout:
        # md_bg_color:1,1,0,1
        size_hint:1,.85

        ScrollView:
            # size_hint:1,.8
            MDList:
                id:list
        MDFloatingActionButton:
            icon: "plus"
            md_bg_color: app.theme_cls.primary_color
            pos_hint:{'center_x':.9,'center_y':.17}
            on_press:app.show_task_dialog()
"""
import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.Database')
        #Create a cursor 
        self.c = self.conn.cursor()
        #calling Table
        self.create_table

    #list to add

    # create a table for page 1
    def create_table(self):
        self.c.execute("""CREATE TABlE IF NOT EXISTS tab1(
            task text
        )
        """)
        self.conn.commit()
        return "Created"

    # inserting into database for page 1
    def addIntoDatabase(self,data):
        self.c.execute("INSERT INTO tab1 VALUES(?)",data,)
        self.conn.commit()

    #  Getting the values for table1 
    def fetchData(self):
        outs = self.c.execute("SELECT rowid,* FROM tab1").fetchall()
        return outs

    def deleteData(self,taskid):
        self.c.execute("DELETE FROM tab1 where rowid = ?",(taskid,) )
        self.conn.commit() 
        

class ListItemWithCheckbox(OneLineAvatarIconListItem):
    '''Custom list item'''

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        # state a pk which we shall use link the list items with the database primary keys
        self.pk = pk
    def delete_item(self, list_of_task):
        '''Delete the task'''
        self.parent.remove_widget(list_of_task)
        # Database.deleteData()# Here
        init = Database()
        delete = init.deleteData(taskid=list_of_task.pk)


class ContentsInDialoge(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class TDo(MDApp):
    dialog1 = None

    def build(self):
        self.kv = Builder.load_string(kv)
        return self.kv
    def show_task_dialog(self):
        if not self.dialog1:
            self.dialog1 = MDDialog(
                title="Create Task",
                type="custom",
                radius=[20, 7, 20, 7],
                content_cls=ContentsInDialoge(),
            )
        self.dialog1.open()
    
    def add_data_to_list(self,data):
        '''send and retrive from Database'''
        self.root.ids.list.clear_widgets()
        datas = [
            (data)
        ] 
        add = self.init.addIntoDatabase(datas)
        received = self.init.fetchData()
        for values in received:
            # ADD THE VALUE TO THE PLACEHOLDER OF ID = LIST1
            self.root.ids.list.add_widget(ListItemWithCheckbox(pk = values[0] ,text=str(values[1])))
    def close(self):
        self.dialog1.dismiss()
    def on_start(self):
        self.init = Database()
        ct = self.init.create_table()
        received = self.init.fetchData()
        for values in received:
            # ADD THE VALUE TO THE PLACEHOLDER OF ID = LIST1
            self.root.ids.list.add_widget(ListItemWithCheckbox(pk = values[0] ,text=str(values[1])))
       

TDo().run()

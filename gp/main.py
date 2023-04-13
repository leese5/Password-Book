from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.popup import Popup

import micro as microservice

class CustomDropDown(DropDown):
    pass

class GridLayoutUi(GridLayout):
    def __init__(self, **kwargs):
        super(GridLayoutUi, self).__init__(**kwargs)

        #version info UI
        self.cols = 1
        self.intro = Label(text = 'Version 1.1! You can now generate random password!', font_size = 10, size_hint_y = 0.2)
        self.add_widget(self.intro)

        #header UI (title, help)
        self.header = GridLayout(padding = 10)
        self.header.cols = 2
        self.header.add_widget(Label(text = 'My Password Book!', font_size = 50, size_hint_x = 0.8))
        self.help = Button(text = 'help', font_size = 30, size_hint_x = 0.2, size_hint_y = 0.5)
        self.help.bind(on_press = self.onHelp)
        self.header.add_widget(self.help)
        self.add_widget(self.header)

        #body UI (ID list, add ID, id and password display, delete)
        self.id = GridLayout(padding = 10)
        self.id.cols = 2
        self.idArray = self.idListing()
        self.pwArray = self.pwListing()
        #id list popup
        self.idListButton = Button(text = 'ID List', font_size = 30, size_hint_x = 0.5, size_hint_y = 0.3)
        self.id.add_widget(self.idListButton)
        self.idListButton.bind(on_press = self.idList)

        #add id popup
        self.button = Button(text = 'Add New ID', font_size = 30, size_hint_x = 0.5, size_hint_y = 0.3)
        self.button.bind(on_press = self.onAdd)
        self.id.add_widget(self.button)
        self.add_widget(self.id)
        #ID and password display UI
        self.inside = GridLayout(padding = 10)
        self.inside.cols = 2
        self.inside.add_widget(Label(text='ID: ',  font_size=30))
        self.title = Label(text='myid123',   font_size=30)
        self.inside.add_widget(self.title)
        self.inside.add_widget(Label(text='Password: ',  font_size=30))
        self.content = Label(text = 'savedPassword23!',   font_size=30)
        self.inside.add_widget(self.content)
        self.add_widget(self.inside)
        # delete popup
        self.delete = GridLayout(padding = 10)
        self.delete.cols = 1
        self.submit = Button(text='Delete',  font_size=40, size_hint_y = 0.3)
        self.submit.bind(on_press=self.pressedWarn)
        self.delete.add_widget(self.submit)
        self.add_widget(self.delete)

    def idList(self, button):
        layout = GridLayout(cols = 1, padding = 10)
        self.buttons = []
        for id in self.idArray:
            button = Button(text = id, size_hint_y = 0.3, on_press = self.getInfo)
            self.buttons.append(button)
            layout.add_widget(button)
        closeButton = Button(text = 'close', size_hint_y = 0.3)
        layout.add_widget(closeButton)
        popup = Popup(title = 'list', content = layout, size_hint = (None, None), size = (300, 300))
        popup.open()
        closeButton.bind(on_press = popup.dismiss)
        
    def getInfo(self, button):
        id = button.text
        self.title.text = id
        index = self.getIdx(id)
        pw = self.pwArray[index]
        self.content.text = pw
        layout = GridLayout(cols = 1, padding = 10)
        popupInfo = Label(text = 'ID and Password has been loaded.\nPress close button to go back to main.')
        closeButton = Button(text = 'close', size_hint_y = 0.3)
        layout.add_widget(popupInfo)
        layout.add_widget(closeButton)
        popup = Popup(title = 'done', content = layout, size_hint = (None, None), size = (300, 200))
        popup.open()
        closeButton.bind(on_press = popup.dismiss)
    
    def getIdx(self, id):
        count = 0
        for x in self.idArray:
            if id == x:
                return count
            count += 1

    def idListing(self):
        array = []
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.strip('n')
                data = data.split(',')
                array.append(data[0])
        return array
    
    def pwListing(self):
        array = []
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.strip('n')
                data = data.split(',')
                array.append(data[1])
        return array

    def pressedWarn(self, button):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel = Label(text = 'Are you sure you want to\ndelete current ID\nand password?')
        closeButton = Button(text = 'close', size_hint_y = 0.3)
        deleteButton = Button(text = 'delete', size_hint_y = 0.3)
        layout.add_widget(popupLabel)
        layout.add_widget(closeButton)
        layout.add_widget(deleteButton)
        popup = Popup(title = 'Delete ID popup', content = layout,
                        size_hint = (None, None), size = (200, 200), auto_dismiss = True)
        popup.open()
        closeButton.bind(on_press = popup.dismiss)
        deleteButton.bind(on_press= self.pressed)

    def pressed(self, instance):
        title = self.title.text
        content = self.content.text
        print('title: ', title, ' content: ', content)
        with open('password.txt', 'r') as r:
            lines = r.readlines()
            with open('password.txt', 'w') as w:
                for line in lines:
                    print(line)
                    print(title+","+content)
                    if line != title+","+content:
                        w.write(line)
        self.title.text = ''
        self.content.text =''
        self.idArray = self.idListing()
        self.pwArray = self.pwListing()
        layout = GridLayout(cols = 1, padding = 10)
        popupInfo = Label(text = 'ID and Password has been deleted.\nPress close button to go back to main.')
        closeButton = Button(text = 'close', size_hint_y = 0.3)
        layout.add_widget(popupInfo)
        layout.add_widget(closeButton)
        popup = Popup(title = 'done', content = layout, size_hint = (None, None), size = (300, 200))
        popup.open()
        closeButton.bind(on_press = popup.dismiss)
        
        

    def onAdd(self, button):
        layout = GridLayout(cols = 2, padding = 10)
        layout.add_widget(Label(text = 'ID: ', font_size = 30))
        self.addID = TextInput(text = '')
        layout.add_widget(self.addID)
        layout.add_widget(Label(text = 'Password: ', font_size = 30))
        self.addPw = TextInput(text = '')
        layout.add_widget(self.addPw)
        saveButton = Button(text = 'save')
        closeButton = Button(text = 'close')
        generatePassword = Button(text = "Generate Password")
        generatePassword.bind(on_press = self.buttonClicked)
        layout.add_widget(generatePassword)
        layout.add_widget(saveButton)
        layout.add_widget(closeButton)
        self.popup = Popup(title = 'addID popup', content = layout,
                        size_hint = (None, None), size = (500, 300), auto_dismiss = True)
        self.popup.open()
        closeButton.bind(on_press = self.popup.dismiss)
        saveButton.bind(on_press = self.doSave)
    
    def doSave(self, button):
        layout = GridLayout(cols = 1, padding = 10)
        if self.addID.text == '' or self.addPw.text == '':
            layout.add_widget(Label(text = 'ID and Password must be filled.'))
            closeButton = Button(text = 'close')
            layout.add_widget(closeButton)
            popup = Popup(title = 'Warning', content = layout, size = (100, 100))
            popup.open()
            closeButton.bind(on_press = popup.dismiss)
        else:
            f = open('password.txt', 'a')
            f.write(f"{self.addID.text}, {self.addPw.text}\n")
            f.close()
            popupInfo = Label(text = 'ID and Password has been saved.\nPress close button to go back to main.')
            closeButton = Button(text = 'close', size_hint_y = 0.3)
            layout.add_widget(popupInfo)
            layout.add_widget(closeButton)
            popup = Popup(title = 'done', content = layout, size_hint = (None, None), size = (300, 200))
            popup.open()
            closeButton.bind(on_press = popup.dismiss)
        self.idArray = self.idListing()
        self.pwArray = self.pwListing()   

    def buttonClicked(self, button):
            layout = GridLayout(cols = 1, padding = 10)
            microservice.send_pw()
            pw = microservice.receive_pw()
            password = Label(text = pw)
            closeButton = Button(text = 'close')
            layout.add_widget(password)
            layout.add_widget(closeButton)
            self.addPw.text = pw
            popup = Popup(title = 'Generated Password', content = layout, size_hint = (None, None), size = (300, 300))
            popup.open()
            closeButton.bind(on_press = popup.dismiss)

    def onHelp(self, button):
        layout = GridLayout(cols = 1, padding = 10)
        popupLabel1 = Label(text = 'Click add ID button to add another ID and password in your ID list.')
        popupLabel2 = Label(text = 'Click select ID button to see IDs saved and select an ID on the list to see ID and password.')
        popupLabel3 = Label(text = 'Click delete button to delete the current id and password info from your book.')
        popupLabel4 = Label(text = 'If you want to edit information manually, edit the file ./gp/password.txt,\nand the format has to be (id), (password).')
        closeButton = Button(text = 'close', size_hint_y = 0.1)
        layout.add_widget(popupLabel1)
        layout.add_widget(popupLabel2)
        layout.add_widget(popupLabel3)
        layout.add_widget(popupLabel4)
        layout.add_widget(closeButton)
        popup = Popup(title = 'Help', content = layout,
                        size_hint = (None, None), size = (650, 500))
        popup.open()
        closeButton.bind(on_press = popup.dismiss)

    

class gp(App):
    def build(self):
        return GridLayoutUi()
    
    
if __name__ == '__main__':
    gp().run()
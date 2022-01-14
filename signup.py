from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, FallOutTransition
from kivy.properties import ObjectProperty
from database import *
import re
import hashlib
from kivy.uix.button import Button
from kivymd.uix.button import MDFillRoundFlatButton, MDRoundFlatButton

def invalidpassword():
    pop = Popup(title='Invalid password', content=Label(text="Ensure your password:\n\nis at least 6 characters long,"
                                                             "\nhas at least one uppercase letter,\none lowercase letter,"
                                                             "\none  number\nand one special character"), size_hint=(0.3,0.4))
    pop.open()


def success():
    pop = Popup(title='Success', content=Label(text="Congratulations! \nYou have created an account!"), size_hint=(0.3,0.4), auto_dismiss=True)
    pop.open()


class Signup(Screen):
    user = ObjectProperty(None)
    official_name_title = ObjectProperty(None)
    email_address = ObjectProperty(None)
    hospital = ObjectProperty(None)
    password = ObjectProperty(None)
    repeat_new_password = ObjectProperty(None)
    info1 = ObjectProperty(None)

    def do_signup(self):
        try:

            isvalidusername = False

            mycursor.execute(f"SELECT user from users where user='{self.user.text.lower()}'")
            result_set1 = list(mycursor.fetchall())
            if len(result_set1) == 0 and len(self.user.text.strip()) > 0:
                isvalidusername = True
            elif len(self.user.text.strip()) == 0:
                self.info1.text = '[color=#FF0000]Invalid user name[/color]'
                self.user.text = ""
            if len(result_set1) > 0:
                self.info1.text = '[color=#FF0000]User Name arleady exists. \nPlease try another one[/color]'
                self.user.text = ""
                self.password.text = ""
                self.repeat_new_password.text = ""
            if isvalidusername ==True:
                email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
                if email_regex.match(f"str({self.email_address.text})"):
                    ispasswordvalid = False
                    hassixcharacters = False
                    hasdigit = False
                    hasuppercasecharacter = False
                    haslowercasecharacter = False
                    hasspecialcharacter = False

                    if len(self.password.text) >= 6:
                        hassixcharacters = True

                    for i in self.password.text:
                        if i.isdigit():
                            hasdigit = True
                        if i.isupper():
                            hasuppercasecharacter = True
                        if i.islower():
                            haslowercasecharacter = True
                        if not i.isalnum():
                            hasspecialcharacter = True

                    ispasswordvalid = hasdigit & hasuppercasecharacter & haslowercasecharacter & hasspecialcharacter & hassixcharacters

                    if self.password.text == self.repeat_new_password.text and ispasswordvalid:
                        epassword = hashlib.sha256(str(self.password.text).encode('utf-8')).hexdigest()
                        mycursor.execute(f"INSERT INTO users(user, official_name_title, hospital, email_address, password) VALUES('{self.user.text.strip()}', '{self.official_name_title.text.strip()}', '{self.hospital.text.strip()}', '{self.email_address.text}', '{epassword}')")
                        db.commit()
                        success()
                        self.reset()
                        self.manager.transition = FallOutTransition()
                        self.manager.current = 'login'
                    elif self.password.text != self.repeat_new_password.text or not ispasswordvalid:
                        invalidpassword()
                        self.password.text = ""
                        self.repeat_new_password.text = ""
                else:
                    self.info1.text = '[color=#FF0000]Invalid email[/color]'
                    self.email_address.text = ""
        except Exception as e:
            self.info1.text = "Check internet connection"

    def do_cancel(self):
        self.reset()
        self.manager.transition = FallOutTransition()
        self.manager.current = 'login'

    def reset(self):
        self.info1.text = ''
        self.user.text = ""
        self.email_address.text = ""
        self.hospital.text = ""
        self.official_name_title.text = ""
        self.password.text = ""
        self.repeat_new_password.text = ""

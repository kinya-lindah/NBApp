from kivy.app import App
from kivymd.app import MDApp
from kivymd.icon_definitions import md_icons
from kivy.config import Config
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.screenmanager import SwapTransition
from kivy.core.window import Window
from signup import *
from database import *
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.uix.button import MDRoundFlatButton, MDFillRoundFlatButton
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
import smtplib
import random
import string
from functools import partial
from datetime import datetime
from kivy.uix.dropdown import DropDown
Config.set('graphics', 'resizeable', True)
Config.write()


class Manager(ScreenManager):
    pass


manager = Manager()


class ColorA:
    def __init__(self, color):
        self.color = color
        self.colorsdict = {'purple': [.4157, 0.51, 0.6784], 'blue': [0, 0, 1], 'skyblue': [173, 216, 230],
                      'royalblue': [65, 105, 225], 'red': [1, 0, 0], 'pink': [255, 192, 203], 'peach': [255, 218, 185]}

    def light(self):
        self.colorsdict[self.color].append(0.2)

    def med(self):
        self.colorsdict[self.color].append(0.5)

    def meddark(self):
        self.colorsdict[self.color].append(0.8)

    def dark(self):
        self.colorsdict[self.color].append(1)

appemailpassword = '@!$EDSDW Eqwem2'
appemail = 'nutribaseapp@gmail.com'
emailchangesubject = "Your NutiBase app email has been changed"
emailchangebeg = "Upon your request, we have changed your email to:"
all = string.ascii_letters + string.digits + string.punctuation
digits1 = '0123456789.,'
ad = string.ascii_letters + string.digits
passwordchangesubject = 'Your NutriBase app password has been changed'
change_passworda ="Upon your request, we have changed your password to:"


def send_email(subject1, begining, username, useremail, changeditem):  # create new pasword by using random.choice
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.ehlo()
        smtp.login(appemail, appemailpassword)
        subject = subject1
        body = f"Dear {username}, \n{begining} {changeditem}\n\n If you did not request this change change. Please log onto your to your account and change your password.\nBest,\n NutriBase Team"
        msg = f'Subject: {subject}\n\n{body}'
        smtp.sendmail(appemail, useremail, msg)


class LogIn(Screen):
    user = ObjectProperty(None)
    password = ObjectProperty(None)
    info = ObjectProperty(None)
    iscorrect = False

    def do_login(self):

        if self.user.text.strip() == "" or self.password.text == "":
            self.info.text = '[color=#FF0000]username and password are required[/color]'
        try:
            mycursor.execute(f"SELECT user, password from users where user='{self.user.text.strip()}'")
            result_set2 = list(mycursor.fetchall())
            epassword1 = hashlib.sha256(str(self.password.text).encode('utf-8')).hexdigest()

            if len(result_set2) == 0 :
                self.info.text = '[color=#FF0000]User not found/Incorrect username[/color]'
                self.resetForm()
            elif len(result_set2) == 1 and epassword1 == result_set2[0][-1] :
                Connected.current = self.user.text.lower()
                mycursor.execute(
                    f"SELECT hospital, official_name_title from users where user='{self.ids.user.text.lower()}'")
                result_set3 = list(mycursor.fetchall())
                Connected.hospital = result_set3[0][0]
                Connected.offiialNameTitle = result_set3[0][1]
                LogIn.updaterv(self, result_set3[0][0])
                self.resetForm()
                self.info.text = ''
                self.manager.transition = SlideTransition()
                self.manager.current = "connected"
            elif len(result_set2) == 1 and epassword1 != result_set2[0][-1] :
                self.info.text = '[color=#FF0000]Invalid password[/color]'
                self.resetForm()
        except Exception as e:
            print(e, "on login")
            self.info.text = "No internet connection log in"

    def updaterv(self, x):
        try:
            if not Connected.isuserdeleted:
                mycursor.execute(
                    f"SELECT p_name, p_number from patient where hospital='{x}'")
                result_set4 = list(mycursor.fetchall())
                LoginApp.get_running_app().root.get_screen('connected').ids.patientlist.rows1 = result_set4

                LoginApp.get_running_app().root.get_screen('connected').ids.filterpic.source = 'images/filteroff.png'
        except Exception as e:
            print(e, "on log in rv")
            self.info.text = "No internet connection log in"

    def forgotpassword(self):
        try:
            if len(self.user.text.strip()) > 0:
                mycursor.execute(f"SELECT user, email_address, official_name_title from users where user='{self.user.text.strip()}'")
                result_set2 = list(mycursor.fetchall())
                lenpass = random.choice([6,7,8,9,10,11])
                pass1 = "".join(random.sample(all, lenpass))

                if len(result_set2) > 0:
                    try:
                        send_email(passwordchangesubject, change_passworda, result_set2[0][2], result_set2[0][1], pass1)
                        self.info.text = '[color=#FF0000]Please check your email for password reset[/color]'
                        mycursor.execute(
                            f"UPDATE users SET password=  '{hashlib.sha256(pass1.encode('utf-8')).hexdigest()}' where user='{result_set2[0][0]}'")
                        db.commit()
                    except Exception as e:
                        print(e, "login forgot password")
                        self.info.text = '[color=#FF0000]Could not send email[/color]'
                else:
                    self.info.text = '[color=#FF0000]User not found/Incorrect username[/color]'
                    self.resetForm()
            else:
                self.info.text = '[color=#FF0000]Please type in your user name then press the forgot username button[/color]'
        except Exception as e:
            print(e, "last log in ")
            self.info.text = "No internet connection log in"

    def resetForm(self):
        self.user.text = ""
        self.password.text = ""

    def do_signup(self):
        self.manager.current = "signup"

#logged in

def deletedPopup():
    try:
        mycursor.execute(f"SELECT official_name_title, hospital from users where user='{Connected.current}'")
        official = list(mycursor.fetchall())
        pop = Popup(title='User deleted', content=Label(text=f"The user  has been DELETED"), size_hint=(0.7,0.2), autodismiss = False, border=(30, 30, 30, 30))
        pop.open()

    except Exception as e:
        print(e, "deletedpopup")


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    pass
    

class SelectableLabel(RecycleDataViewBehavior, BoxLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    id_label1 = StringProperty("")
    id_label2 = StringProperty("")
    a = ''

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

    def printed(self):
        try:

            Patient2.patient = Connected.hospital + self.ids.id_label2.text
            mycursor.execute(f"SELECT hpnumber from patientmn where hpnumber='{Patient2.patient}'")
            resultset = list(mycursor.fetchall())
            mycursor.execute(f"SELECT hpnumber, p_continue from patient where hpnumber='{Patient2.patient}'")
            resultset2 = list(mycursor.fetchall())

            self.ids.buttonrv.manager = manager
            if len(resultset) == 1:
                Connected.name1 = 'nfpe2'
            elif len(resultset) == 0 and len(resultset2) == 1:
                if resultset2[0][1] == '0':
                    Connected.name1 = 'nfpe3'
                elif resultset2[0][1] == '1':
                    Connected.name1 = 'nfpe'
            self.ids.buttonrv.name_screen = Connected.name1
        except Exception as e:
            print("no internet connection log in")

    def patientpopup(self):
        SelectableLabel.a = Connected.hospital + self.ids.id_label2.text
        box = BoxLayout(orientation='vertical', padding=15, )
        box.add_widget(Label(text="Are you sure you want to delete this patient? \nOnce deleted can not be undone! Your coworkers will not be able to access this patient either",text_size=(self.width*0.4 -4, None), size_hint_y=0.94))
        popup = Popup(title='Delete Patient', title_size=30, title_align='center', content=box,
                      size_hint=(0.7, 0.4), auto_dismiss=True )

        box2 = BoxLayout(orientation="horizontal" ,  size_hint_y=0.20,spacing=8)
        box2anchor1=AnchorLayout(anchor_x='right', anchor_y='center')
        box2anchor2 = AnchorLayout(anchor_x='left', anchor_y= 'center')
        box2anchor1.add_widget(MDRoundFlatButton(line_color = (6, 39, 112,1), text_color= (1,1,1,1),  text="DELETE", on_press=SelectableLabel.delpatient, on_release=popup.dismiss))
        box2anchor2.add_widget(MDFillRoundFlatButton( line_color = (6/255, 39/255, 112/255,1), text_color= (100, 100, 120), md_bg_color= (1, 1, 1,1),text="CANCEL", on_press=popup.dismiss))
        box2.add_widget(box2anchor1)
        box2.add_widget(box2anchor2)
        box.add_widget(box2)
        popup.background_color = (6/255, 39/255, 240/255)
        popup.open()

    def delpatient(self):
        try:
            mycursor.execute(f"DELETE FROM patient WHERE hpnumber = '{SelectableLabel.a}'")
            db.commit()
            mycursor.execute(f"DELETE FROM patientmn WHERE hpnumber = '{SelectableLabel.a}'")
            db.commit()
            LogIn.updaterv(self, Connected.hospital)
        except Exception as e:
            print("no internet connection log in")


class RV(RecycleView):
    pass


class Connected(Screen):
    current = ''
    hospital = ''
    isuserdeleted = False
    dropdown1 = DropDown()
    filter_by = ''
    name1 = ""
    patientNumber = ""
    editing= False
    offiialNameTitle =""

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def change1(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'nfpe'

    def change2(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'nfpe2'

    def about(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'about'

    def filtered(self):
        try:
            if self.ids.filterpic.source == 'images/filteroff.png':
                self.ids.filterpic.source = 'images/filteron.png'
                mycursor.execute(
                    f"SELECT p_ward from patient where hospital='{Connected.hospital}'")
                result_set4 = sorted(set(list(mycursor.fetchall())))

                Connected.dropdown1 = DropDown()
                for i in result_set4:
                    word = i[0]
                    btn = Button(text=f'{i[0].upper()}', center_x=0.5, size_hint_y=None, height=40,width=20, background_color=(255, 255, 255, 1),halign="left",
                                 color=(6/255, 39/255, 112/255, 1), pos_hint={"x": 0.6, "center_y": 0.3},on_press=partial(Connected.fitered_buttons, word))
                    btn.bind(on_release=lambda btn: Connected.dropdown1.select(btn.text))
                    Connected.dropdown1.add_widget(btn)

                Connected.dropdown1.open(self.ids.filterwards)
                Connected.dropdown1.bind(on_select=lambda instance, x: setattr(self.ids.filterwards, 'text', x))
            else:
                LogIn.updaterv(self, Connected.hospital)
        except Exception as e:
            print("no internet connection cant filter")

    def fitered_buttons(self, x):
        try:
            mycursor.execute(
                f"SELECT p_name, p_number from patient where hospital='{Connected.hospital}' and p_ward='{x.text}' ")
            result_set4 = list(mycursor.fetchall())  # patients at hospital to use for recylview
            #nrv = LoginApp.get_running_app().root.get_screen('connected').ids.patientlist
            LoginApp.get_running_app().root.get_screen('connected').ids.patientlist.rows1 = result_set4
        except Exception as e:
            print("no internet connection cant filter trully")

    def search_hospital_patient(self):
        if Connected.isuserdeleted:
            Connected.back(self)
        pm1 = Connected.hospital + self.ids.patient_number.text.strip()
        Connected.searchparameters(self, pm1)

    def search_hospital_patient_text(self, text=""):
        if Connected.isuserdeleted:
            Connected.back(self)
        if not len(text):
            LogIn.updaterv(self, Connected.hospital)
        if len(text):
            try:
                if not Connected.isuserdeleted:
                    mycursor.execute(
                        f"SELECT p_name, p_number from patient where hospital='{Connected.hospital}'")
                    result_set4 = []
                    for i in list(mycursor.fetchall()):
                        if text in i[1]:
                            result_set4.append(i)
                    LoginApp.get_running_app().root.get_screen('connected').ids.patientlist.rows1 = result_set4
                    LoginApp.get_running_app().root.get_screen('connected').ids.filterpic.source = 'images/filteron.png'
            except Exception as e:
                print("no internet connection cant search")

    def searchparameters(self, x):
        try:
            mycursor.execute(f"SELECT hpnumber from patientmn where hpnumber='{x}'")
            resultset = list(mycursor.fetchall())
            mycursor.execute(f"SELECT hpnumber, p_continue from patient where hpnumber='{x}'")
            resultset2 = list(mycursor.fetchall())
            if len(resultset) == 1:
                Patient2.patient = x
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'nfpe2'
                self.ids.patient_number.text = ''
            elif len(resultset) == 0 and len(resultset2) == 1:
                Patient2.patient = x
                if resultset2[0][1] == '0':
                    self.manager.transition = SlideTransition(direction="left")
                    self.manager.current = 'nfpe'
                    self.ids.patient_number.text = ''
                elif resultset2[0][1] == '1':
                    self.manager.transition = SlideTransition(direction="left")
                    self.manager.current = 'nfpe3'
                    self.ids.patient_number.text = ''
            elif len(resultset) == 0 and len(resultset2) == 0:
                self.ids.patient_number.text = ''
                self.ids.patient_number.hint_text = "Patient Number"
        except Exception as e:
            print("no internet connection cant search paramenters")

    def new_hospital_patient(self):
        if not Connected.isuserdeleted:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'patient'
            Patient.newpatient = ''
        if Connected.isuserdeleted:
            Connected.back(self)

    def user_official_name(self):
        try:
            mycursor.execute(f"SELECT user, official_name_title from users where user='{Connected.current}'")
            if len(list(mycursor.fetchall())) > 0:
                result_set3 = list(mycursor.fetchall())[0][-1]
            else:
                result_set3 = " "
            return result_set3
        except Exception as e:
            print("no internet connection cant change official name")

    def deleting_user_popup(self):

        box = BoxLayout(orientation='vertical', padding=15)
        box.add_widget(Label(text="Are you sure you want to delete account?\nOnce deleted can not be undone!"))
        popup = Popup(title='Delete Account', title_size=30,
                      title_align='center', content=box,
                      size_hint=(0.9, 0.4),
                      auto_dismiss=True)
        box2 = BoxLayout(orientation='horizontal', size_hint_y=0.20, spacing=8)
        box2anchor1=AnchorLayout(anchor_x='right', anchor_y='center')
        box2anchor2 = AnchorLayout(anchor_x='left', anchor_y= 'center')
        box2anchor1.add_widget(MDRoundFlatButton(line_color = (6, 39, 112,1), text_color= (1,1,1,1), text="DELETE", on_press=Connected.del_user,on_release=popup.dismiss ))
        box2anchor2.add_widget(MDFillRoundFlatButton( line_color = (6/255, 39/255, 112/255,1), text_color= (100, 100, 120), md_bg_color= (1, 1, 1,1), text="CANCEL", on_press=popup.dismiss))
        self.box3 = BoxLayout(orientation='horizontal', size_hint_y=0.10)
        self.box3.add_widget(Label(text=""))
        box2.add_widget(box2anchor1)
        box2.add_widget(box2anchor2)
        box.add_widget(box2)
        box.add_widget(self.box3)
        popup.background_color = (6/255, 39/255, 240/255)
        popup.open()

    def del_user(self):
        try:
            mycursor.execute(f"DELETE FROM users WHERE user = '{Connected.current}'")
            db.commit()
            Connected.isuserdeleted = True
            Connected.hospital = 0
            LogIn.updaterv(self, Connected.hospital)
        except Exception as e:
            self.box3.text = "no internet connection cant to del user"

        # go back to log in page after this

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'

    @staticmethod
    def deleted():
        try:
            mycursor.execute(f"DELETE FROM patient WHERE hpnumber = '{Patient2.patient}'")
            db.commit()
        except Exception as e:
            pass


class Updateprofile(Screen):

    def on_pre_enter(self, *args):
        try:
            mycursor.execute(
                    f"SELECT official_name_title, hospital, email_address from users where user='{Connected.current}'")
            result_set4 = list(mycursor.fetchall())
            self.o = result_set4[0][0]
            self.h = result_set4[0][1]
            self.e = result_set4[0][2]
            self.ue = False
            self.up = False
            self.ids.usera.text = Connected.current
            self.ids.ne.text = self.e
            self.ids.nh.text = self.h
            self.ids.no.text = self.o
            self.ids.change.text = ""
            self.correctpassword = False
        except Exception as e:
            self.ids.change.text = "Check internet connection"

    def savep(self):
        updates = ''
        allok = True

        if self.ids.nh.text != self.h:
            try:
                mycursor.execute(
                    f"UPDATE users SET hospital=  '{self.ids.nh.text}' where user='{Connected.current}'")
                db.commit()
                updates += "hospital "
            except Exception as e:
                self.ids.change.text = "Check internet connection"

        if self.ids.no.text != self.o:
            try:
                mycursor.execute(
                    f"UPDATE users SET official_name_title=  '{self.ids.no.text}' where user='{Connected.current}'")
                db.commit()
                updates += "official name/title "
            except Exception as e:
                self.ids.change.text = "Check internet connection"

        if self.ids.ne.text != self.e:
            email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if email_regex.match(f"str({self.ids.ne.text.strip()})"):
                try:
                    mycursor.execute(
                        f"SELECT password from users where user='{Connected.current}'")
                    result_set2 = list(mycursor.fetchall())
                    if hashlib.sha256(self.ids.op.text.strip().encode('utf-8')).hexdigest() == result_set2[0][0]:
                        mycursor.execute(
                            f"UPDATE users SET email_address=  '{self.ids.ne.text.strip()}' where user='{Connected.current}'")
                        db.commit()
                        updates += "email "

                    else:
                        self.ids.op.text = ''
                        self.ids.change.text = f"Please input current password to confirm identity"
                        allok = False
                except Exception as e:
                    self.ids.change.text = "Check internet connection"
            else:
                self.ids.change.text = "Please check on email"
                allok = False
        if len(self.ids.np.text.strip()) > 0 or len(self.ids.op.text.strip()) > 0:
            ispasswordvalid = False
            hassixcharacters = False
            hasdigit = False
            hasuppercasecharacter = False
            haslowercasecharacter = False
            hasspecialcharacter = False
            if len(self.ids.np.text.strip()) >= 6:
                hassixcharacters = True

            for i in self.ids.np.text.strip():
                if i.isdigit():
                    hasdigit = True
                if i.isupper():
                    hasuppercasecharacter = True
                if i.islower():
                    haslowercasecharacter = True
                if not i.isalnum():
                    hasspecialcharacter = True

            ispasswordvalid = hasdigit & hasuppercasecharacter & haslowercasecharacter & hasspecialcharacter & hassixcharacters

            if not ispasswordvalid:
                self.ids.change.text = "Password should be at least 6 characters long, has 1 capital letter, 1 special character and 1 number"
                self.ids.np.text = ""
                allok = False
            if ispasswordvalid:
                try:
                    mycursor.execute(
                        f"SELECT password from users where user='{Connected.current}'")
                    result_set2 = list(mycursor.fetchall())
                    if hashlib.sha256(self.ids.op.text.strip().encode('utf-8')).hexdigest() == result_set2[0][0]:
                        mycursor.execute(
                            f"UPDATE users SET password=  '{hashlib.sha256(self.ids.np.text.strip().encode('utf-8')).hexdigest()}' where user='{Connected.current}'")
                        db.commit()
                        updates += "password "
                    else:
                        self.ids.op.text = ''
                        self.ids.change.text = f"Current password is wrong"
                        allok = False
                except Exception as e:

                    self.ids.change.text = "Check internet connection"
        if allok:
            self.ids.change.text = f"The following have been changed successfully: {updates}"
            self.ok()

    def ok(self):
        self.ids.op.text = ""
        self.ids.np.text = ""
        self.manager.transition = SwapTransition()
        self.manager.current = 'connected'

    def back(self):
        self.ids.change.text = ""
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'connected'
        self.manager.get_screen('connected')


class About(Screen):
    def on_pre_enter(self, *args):
        self.ids.a1.collapse = False
        self.ids.a2.collapse = True
        self.ids.a3.collapse = True
        self.ids.a4.collapse = True
        self.ids.a5.collapse = True
        self.ids.a6.collapse = True
        self.ids.a7.collapse = True

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'connected'
        self.manager.get_screen('connected')

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'


class Patient(Screen):
    gender = 0
    newpatient = ''
    continued = ""

    def on_enter(self, *args):
        self.ids.emptyp1.text = ""
        if Patient.newpatient != "":
            try:
                mycursor.execute(
                    f"SELECT p_ward, p_name, p_number,  p_gender, p_age, p_height,p_weight, p_continue, p_muac, p_hgs, "
                    f"p_firstimpression from patient where hpnumber='{Patient.newpatient[0][0]}'")
                self.oldpatient = list(mycursor.fetchall())

                self.ids.p_ward.text = self.oldpatient[0][0]
                self.ids.p_name.text = self.oldpatient[0][1]
                self.ids.p_number.text = self.oldpatient[0][2]
                self.ids.p_age.text = self.oldpatient[0][4]
                self.ids.p_height.text = self.oldpatient[0][5]
                self.ids.p_weight.text = self.oldpatient[0][6]
                self.ids.p_muac.text = self.oldpatient[0][8]
                self.ids.p_hgs.text = self.oldpatient[0][9]
                self.ids.p_firstimpression.text = self.oldpatient[0][10]

                Patient.continued = self.oldpatient[0][7]
                if self.oldpatient[0][3] == "Male":
                    self.ids.gender_slider.value = 0.0
                elif self.oldpatient[0][3] == "Female":
                    self.ids.gender_slider.value = 2.0
                elif self.oldpatient[0][3] == "Other":
                    self.ids.gender_slider.value = 1.0
            except Exception as e:
                print(e, "patient1 line 622")
                self.ids.emptyp1.text = "Please check internet connection "
        elif Patient.newpatient == "":
            pass

    def on_leave(self, *args):
        self.ids.emptyp1.text = ""
        if Patient.continued == 0:
            Patient.newpatient = ""

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()
        Patient.newpatient = ""
        self.clear()

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'connected'
        self.manager.get_screen('connected')
        Patient.newpatient = ""
        self.clear()

    def clear(self):
        self.ids.p_name.text = ""
        self.ids.p_ward.text = ""
        self.ids.p_number.text = ""
        self.ids.p_age.text = ""
        self.ids.p_height.text = ""
        self.ids.p_weight.text = ""
        self.ids.p_muac.text = ""
        self.ids.p_hgs.text = ""
        self.ids.p_firstimpression.text = ''

    def p_gender(self, *args):
        if int(args[-1]) == 1:
            Patient.gender = 1
        else:
            Patient.gender = 2

    def pi_checks(self):
        self.manager.transition = SlideTransition(direction="left")
        self.correct()
        if self.ids.p_height.text == "" or set(self.ids.p_height.text) == set(
                '0') or "N/A" in self.ids.p_height.text.upper():
            self.ids.p_height.text = "N/A"
            self.height1 ="N/A"
        if self.ids.p_weight.text == "" or set(self.ids.p_weight.text) == set(
                '0') or "N/A" in self.ids.p_weight.text:
            self.ids.p_weight.text = "N/A"
            self.weight = "N/A"
        if self.ids.p_muac.text == "" or set(self.ids.p_muac.text) == set('0') or "N/A" in self.ids.p_muac.text:
            self.ids.p_muac.text = "N/A"
        if self.ids.p_hgs.text == "" or set(self.ids.p_hgs.text) == set('0') or "N/A" in self.ids.p_hgs.text:
            self.ids.p_hgs.text = "N/A"


    def next(self):
        g = ""
        if Patient.gender == 0:
            g = "Male"
        elif Patient.gender == 1:
            g = "Other"
        elif Patient.gender == 2:
            g = "Female"

        if Patient.newpatient == "":  #new patient
            if self.ids.p_name.text != "" and self.ids.p_ward.text != "" and self.ids.p_number.text != "" and self.ids.p_age.text != "":
                self.pi_checks()
                self.manager.current = 'pflag'

                try:
                    Patient2.patient = str(Connected.hospital)+str(self.ids.p_number.text.strip())
                    mycursor.execute(
                        f"INSERT INTO patient(hpnumber, staff, hospital,p_ward, p_name, p_number,  p_gender, p_age, p_height, "
                        f"p_weight, p_continue, p_muac, p_hgs, p_firstimpression, p_temple, "
                        f"p_collar_bone,p_shoulder, p_scapula, p_hand, p_thigh, p_calf, p_face, p_upper_arm, p_iliac_crest,"
                        f" p_edema, p_signs, date) VALUES"
                        f"( '{Patient2.patient}', '{Connected.offiialNameTitle}', '{Connected.hospital}', '{self.ids.p_ward.text.strip()}','{self.ids.p_name.text.strip()}', "
                        f"'{self.ids.p_number.text.strip()}', '{g}', '{self.ids.p_age.text.strip()}', '{self.height1}', '{self.weight}', "
                        f"'{0}', '{self.ids.p_muac.text.strip()}', "
                        f"'{self.ids.p_hgs.text}', '{self.ids.p_firstimpression.text}','{0}','{0}','{0}','{0}','{0}', "
                        f"'{0}','{0}','{0}','{0}','{0}','{0}','{0}', '{datetime.date(datetime.now())}' )")
                    db.commit()
                    self.ids.emptyp1.text = ""
                    self.clear()
                except Exception as e:
                    print(e,  "patient 1 line 696")
                    self.ids.emptyp1.text = "Please check internet connection "
            else:
                self.ids.emptyp1.text = '[color=#FF0000]Please in ward, name, number gender, and age.[/color]'

        elif Patient.newpatient != "":  # editing patient info - maybe after

            if self.ids.p_name.text != "" and self.ids.p_ward.text != "" and self.ids.p_number.text != "" and self.ids.p_age.text != "":

                self.pi_checks()
                self.manager.current = 'pflag'

                try:
                    Patient2.patient = str(Connected.hospital)+str(self.ids.p_number.text.strip())
                    mycursor.execute(
                        f"UPDATE patient SET p_ward = '{self.ids.p_ward.text.strip()}',p_name = '{self.ids.p_name.text.strip()}', p_number = '{self.ids.p_number.text.strip()}', "
                        f"p_gender = '{g}', p_age = '{self.ids.p_age.text.strip()}', p_height = '{self.ids.p_height.text.strip()}', "
                        f"p_weight ='{self.ids.p_weight.text.strip()}', p_muac = '{self.ids.p_muac.text.strip()}', p_hgs = '{self.ids.p_hgs.text.strip()}'"
                        f", p_firstimpression = '{self.ids.p_firstimpression.text.strip()}', date ='{datetime.date(datetime.now())}' where hpnumber='{Patient2.patient}'")
                    db.commit()
                    self.ids.emptyp1.text = ""
                    self.clear()
                except Exception as e:
                    print(e, "we are tired")
                    self.ids.emptyp1.text = "Please check internet connection "
            else:
                self.ids.emptyp1.text = '[color=#FF0000]Please fill in all the questions. Make sure height and weight inputs are digits and are not 0s[/color]'

    def correct(self):
        if self.ids.h1.active:
            if self.ids.p_height.text.strip().isdigit() :
                self.height1 = self.ids.p_height.text.strip() + " cm"
        if not self.ids.h1.active:
            if self.ids.p_height.text.strip().isdigit():
                self.height1 = self.ids.p_height.text.strip() + " in"
        if self.ids.w1.active:
            if self.ids.p_weight.text.strip().isdigit():
                self.weight = self.ids.p_weight.text.strip() + " kg"
        if not self.ids.w1.active:
            if self.ids.p_weight.text.strip().isdigit():
                self.weight = self.ids.p_weight.text.strip() + " lb"

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'


class PFlag(Screen):
    totla = 0

    def on_enter(self, *args):
        mycursor.execute(
            f"SELECT p_height, p_weight from patient where hpnumber='{Patient2.patient}'")
        p3 = list(mycursor.fetchall())
        hi = 0  # height in meters
        wk = 0  # weight kg
        print(p3, "shoewef")
        if not p3 or "N/A" in p3[0][0] or "N/A" in p3[0][1]:
            self.ids.bmi.text = "N/A"
        else:
            if p3[0][0][-2:] == "in" :
                hi = float(p3[0][0][:p3[0][0].index(" ")]) * 0.0254
            if p3[0][0][-2:] == "cm":
                hi = float(p3[0][0][:p3[0][0].index(" ")]) / 100
            if p3[0][1][-2:] == "lb":
                wk = float(p3[0][1][:p3[0][1].index(" ")]) * 0.453592
            if p3[0][1][-2:] == "kg":
                wk = float(p3[0][1][:p3[0][1].index(" ")]) * 1
            print(wk, hi ,"showing wk and hi ")

            self.bmi = str(round(wk / (hi ** 2), 2))
            print(self.bmi, "show bmi")
            self.ids.bmi.text = self.bmi

        if Patient.newpatient != "" and int(Patient.continued) == 1:
            self.ids.empty3.text = "As of last check up the practitioner continued onto NFPE. You can refill the flags and view a more recent recommendation or directly go to NFPE to view previous answers"
        elif Patient.newpatient != "" and Patient.continued == 0:
            self.ids.empty3.text = "As of last check up the practitioner did not continue to teh NFPE test. You can refill the flags and view a more recent recommendation or directly go to NFPE to view previous answers"

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp2(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'patient'

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def saved1(self):
        self.checkflag()
        if PFlag.totla > 2:
            try:
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'patient2'
                mycursor.execute(
                    f"UPDATE patient SET p_continue = '{1}' where hpnumber='{Patient2.patient}'")
                db.commit()
                self.ids.empty3.text= ""
            except Exception as e:
                print(e,"pflag1")
                self.ids.empty3.text = "Check internet connection"

        else:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'nfpe3'
            try:
                mycursor.execute(
                    f"UPDATE patient SET p_continue = '{0}' where hpnumber='{Patient2.patient}'")
                db.commit()
                self.ids.empty3.text=""
                LogIn.updaterv(self, Connected.hospital)
            except Exception as e:
                print(e, "pflag2")
                self.ids.empty3.text = "Check internet connection"

    def next(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'patient2'
        try:
            mycursor.execute(
                f"UPDATE patient SET p_continue = '{1}' where hpnumber='{Patient2.patient}'")
            db.commit()
            self.ids.empty3.text=""
        except Exception as e:
            print(e, "pflag3")
            self.ids.empty3.text = "Check internet connection"

    def checkflag(self):
        try:
            self.sumf = 0
            if self.ids.ida1.active:
                self.sumf += 0
            if self.ids.ida2.active:
                self.sumf += 1
            if self.ids.ida3.active:
                self.sumf += 3
            if self.ids.idb1.active:
                self.sumf += 0
            if self.ids.idb2.active:
                self.sumf += 1
            if self.ids.idb3.active:
                self.sumf += 2
            if self.ids.idb4.active:
                self.sumf += 3
            if self.ids.idc1.active:
                self.sumf += 0
            if self.ids.idc2.active:
                self.sumf += 1
            if self.ids.idc3.active:
                self.sumf += 2
            if self.ids.idd1.active:
                self.sumf += 0
            if self.ids.idd2.active:
                self.sumf += 1
            if self.ids.ide1.active:
                self.sumf += 0
            if self.ids.ide2.active:
                self.sumf += 1
            if self.ids.ide3.active:
                self.sumf += 2
            if  'N/A' in self.ids.bmi.text or float(self.ids.bmi.text) < 19:
                self.sumf += 3
            if 'N/A' not in self.ids.bmi.text and 19 <= float(self.ids.bmi.text) < 21:
                self.sumf += 1
            if 'N/A' not in self.ids.bmi.text and 21 <= float(self.ids.bmi.text) < 23:
                self.sumf += 1
            if 'N/A' not in self.ids.bmi.text and float(self.ids.bmi.text) >= 23:
                self.sumf += 3
            PFlag.totla = self.sumf
        except Exception as e :
            PFlag.totla = 9


class Patient2(Screen):
    patient = ""

    def on_pre_enter(self, *args):

        if Patient.newpatient != "" and int(Patient.continued) == 1:
            try:
                mycursor.execute(
                    f"SELECT p_temple, p_collar_bone,p_shoulder, p_scapula, p_hand, p_thigh from patient where hpnumber"
                    f"='{Patient.newpatient[0][0]}'")
                oldpatient = list(mycursor.fetchall())

                self.ids.p_temple.text = str(oldpatient[0][0])
                self.ids.p_collar_bone.text = str(oldpatient[0][1])
                self.ids.p_shoulder.text = str(oldpatient[0][2])
                self.ids.p_scapula.text = str(oldpatient[0][3])
                self.ids.p_hand.text = str(oldpatient[0][4])
                self.ids.p_thigh.text = str(oldpatient[0][5])

            except Exception as e:
                print(e, "show e opld")
                self.ids.emptyp2.text = " Check internet connection"
        else:
            self.clear()

    def on_leave(self, *args):
        self.ids.emptyp2.text = ""

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp2(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'pflag'
        self.clear()

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def next2(self):
        a = ["0", "1", "2"]  # acceptable strings
        if self.ids.p_temple.text.strip() in a and self.ids.p_collar_bone.text.strip() in a and self.ids.p_shoulder.text.strip() \
                in a and self.ids.p_scapula.text.strip() in a and self.ids.p_hand.text.strip() in a and self.ids.p_thigh.text.strip() in a:
            try:
                mycursor.execute(f"UPDATE patient SET p_temple = '{int(self.ids.p_temple.text.strip())}', p_collar_bone = "
                                 f"'{int(self.ids.p_collar_bone.text.strip())}', p_shoulder = '{int(self.ids.p_shoulder.text.strip())}', "
                                 f"p_scapula = '{int(self.ids.p_scapula.text.strip())}', p_hand = '{int(self.ids.p_hand.text.strip())}', "
                                 f"p_thigh ='{int(self.ids.p_thigh.text.strip())}' where hpnumber ='{Patient2.patient}'")
                db.commit()
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'patient3'
                self.ids.emptyp2.text = " "
                self.clear()
            except Exception as e:
                print(e, "patient2 uodting")
                self.ids.emptyp2.text = "Check internet connection"
        else:
            self.ids.emptyp2.text = "Please make sure you have filled all the questions with a 0, 1, or 2. " \
                                    "\nIf you have comments write them at the end of the form"

    def clear(self):
        self.ids.p_temple.text = ""
        self.ids.p_collar_bone.text = ""
        self.ids.p_shoulder.text = ""
        self.ids.p_scapula.text = ""
        self.ids.p_hand.text = ""
        self.ids.p_thigh.text = ""

class Patient3(Screen):
    d = False

    def on_pre_enter(self, *args):

        if Patient.newpatient != "" and int(Patient.continued) == 1:
            try:
                mycursor.execute(
                    f"SELECT p_calf, p_face, p_upper_arm, p_iliac_crest, p_edema, p_signs, date from patient where hpnumber"
                    f"='{Patient.newpatient[0][0]}'")
                oldpatient = list(mycursor.fetchall())

                self.ids.p_calf.text = str(oldpatient[0][0])
                self.ids.p_face.text = str(oldpatient[0][1])
                self.ids.p_upper_arm.text = str(oldpatient[0][2])
                self.ids.p_iliac_crest.text = str(oldpatient[0][3])
                self.ids.p_edema.text = str(oldpatient[0][4])
                self.ids.p_signs.text = str(oldpatient[0][5])

            except Exception as e:
                print(e, "patient3")
                self.ids.empty3.text = "Check internet connection"
        else:
            self.clear()

    def on_leave(self, *args):
        self.ids.empty3.text = ""
        Patient.newpatient = ""

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp3(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'patient2'

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def finalisenfpe(self):
        a = ["0", "1", "2"]  # acceptable strings

        if self.ids.p_calf.text.strip() in a and self.ids.p_face.text.strip() in a and self.ids.p_upper_arm.text.strip() \
                in a and self.ids.p_iliac_crest.text.strip() in a and self.ids.p_edema.text.strip() in a:
            try:
                mycursor.execute(f"UPDATE patient SET p_calf = '{int(self.ids.p_calf.text.strip())}', p_face = "
                                 f"'{int(self.ids.p_face.text.strip())}', p_upper_arm = '{int(self.ids.p_upper_arm.text.strip())}', "
                                 f"p_iliac_crest = '{int(self.ids.p_iliac_crest.text.strip())}', p_edema = '{int(self.ids.p_edema.text.strip())}', "
                                 f"p_signs ='{self.ids.p_signs.text.strip()}' where hpnumber ='{Patient2.patient}'")
                db.commit()

                self.ids.empty3.text = " "
                Patient3.d = True
                LogIn.updaterv(self, Connected.hospital)
            except Exception as e:
                self.ids.empty3.text = "Check internet connection"

        else:
            self.ids.empty3.text = "Please make sure you have filled all the questions with a 0, 1, or 2. " \
                                    "\nIf you have comments write them at the slot for signs"
            Patient3.d = False

    def saved1(self):
        self.finalisenfpe()

        if Patient3.d:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'nfpe'
            self.clear()

    def next(self):

        self.finalisenfpe()
        if Patient3.d:
            self.manager.transition = SlideTransition(direction="left")
            self.manager.current = 'micronutrients'
            self.clear()

    def clear(self):
        self.ids.p_calf.text = ""
        self.ids.p_face.text = ""
        self.ids.p_upper_arm.text = ""
        self.ids.p_iliac_crest.text = ""
        self.ids.p_edema.text = ""
        self.ids.p_signs.text = ""


class Micronutrients(Screen):

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp4(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'patient3'

    @staticmethod
    def intt(x):
        if x:
            return '1'
        else:
            return '0'

    def next4(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'micronutrients2'
        mycursor.execute(f"SELECT hpnumber from patientmn where hpnumber='{Patient2.patient}'")
        newpatientmn = list(mycursor.fetchall())

        if len(newpatientmn) == 0:
            mycursor.execute(
                f"INSERT INTO patientmn(hpnumber, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16,"
                f" p17, p18, p19, p20, p21, p22, p23, p24, p25, p26, p27, p28, p29, p30, p31, p32, p33, p34, p35, p36,"
                f" p37, p38, p39, p40, p41, p42, p43, p44, p45, p46, p47, p48, p49, p50, p51, p52, p53, p54, p55, p56, "
                f"p57, p58, p59, p60, p61, p62, p63, p64, p65, p66, p67, p68, p69, p70, p71, p72, p73, p74, p75) VALUES"
                f" ('{Patient2.patient}', '{Micronutrients.intt(self.ids.p1.active)}', '{Micronutrients.intt(self.ids.p2.active)}', '{Micronutrients.intt(self.ids.p3.active)}', '{Micronutrients.intt(self.ids.p4.active)}', '{Micronutrients.intt(self.ids.p5.active)}', '{Micronutrients.intt(self.ids.p6.active)}'"
                f", '{Micronutrients.intt(self.ids.p7.active)}', '{Micronutrients.intt(self.ids.p8.active)}', '{Micronutrients.intt(self.ids.p9.active)}', '{Micronutrients.intt(self.ids.p10.active)}', '{Micronutrients.intt(self.ids.p11.active)}', '{Micronutrients.intt(self.ids.p12.active)}', '{Micronutrients.intt(self.ids.p13.active)}', '{Micronutrients.intt(self.ids.p14.active)}', '{Micronutrients.intt(self.ids.p15.active)}', '{Micronutrients.intt(self.ids.p16.active)}', '{Micronutrients.intt(self.ids.p17.active)}', '{Micronutrients.intt(self.ids.p18.active)}', '{Micronutrients.intt(self.ids.p19.active)}', '{Micronutrients.intt(self.ids.p20.active)}',"
                f" '{Micronutrients.intt(self.ids.p21.active)}', '{Micronutrients.intt(self.ids.p22.active)}', '{Micronutrients.intt(self.ids.p23.active)}', '{Micronutrients.intt(self.ids.p24.active)}', '{Micronutrients.intt(self.ids.p25.active)}', '{Micronutrients.intt(self.ids.p26.active)}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', "
                f"'{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', "
                f"'{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', "
                f"'{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}', '{0}')")
            db.commit()

        elif len(newpatientmn) == 1:

            mycursor.execute(f"UPDATE patientmn SET p1 = {Micronutrients.intt(self.ids.p1.active)}, p2 = {Micronutrients.intt(self.ids.p2.active)}, p3 = {Micronutrients.intt(self.ids.p3.active)}, p4 = {Micronutrients.intt(self.ids.p4.active)}, p5 = {Micronutrients.intt(self.ids.p5.active)}, p6 = {Micronutrients.intt(self.ids.p6.active)}, p7 = {Micronutrients.intt(self.ids.p7.active)}, p8 = {Micronutrients.intt(self.ids.p8.active)}, p9 = {Micronutrients.intt(self.ids.p9.active)}, p10 = {Micronutrients.intt(self.ids.p10.active)}, p11 = {Micronutrients.intt(self.ids.p11.active)}, p12 = {Micronutrients.intt(self.ids.p12.active)}, p13 = {Micronutrients.intt(self.ids.p13.active)}, p14 = {Micronutrients.intt(self.ids.p14.active)}, p15 = {Micronutrients.intt(self.ids.p15.active)}, p16 = {Micronutrients.intt(self.ids.p16.active)}, p17 = {Micronutrients.intt(self.ids.p17.active)}, p18 = {Micronutrients.intt(self.ids.p18.active)}, p19 = {Micronutrients.intt(self.ids.p19.active)}, p20 = {Micronutrients.intt(self.ids.p20.active)}, p21 = {Micronutrients.intt(self.ids.p21.active)}, p22 = {Micronutrients.intt(self.ids.p22.active)}, p23 = {Micronutrients.intt(self.ids.p23.active)}, p24 = {Micronutrients.intt(self.ids.p24.active)}, p25 = {Micronutrients.intt(self.ids.p25.active)}, p26 = {Micronutrients.intt(self.ids.p26.active)} where hpnumber='{Patient2.patient}'")
            db.commit()

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    #def clear(self):
    def reset_checkbox(self):
        self.ids.p1.active = False
        self.ids.p2.active = False
        self.ids.p3.active = False
        self.ids.p4.active = False
        self.ids.p5.active = False
        self.ids.p6.active = False
        self.ids.p7.active = False
        self.ids.p8.active = False
        self.ids.p9.active = False
        self.ids.p10.active = False
        self.ids.p11.active = False
        self.ids.p12.active = False
        self.ids.p13.active = False
        self.ids.p14.active = False
        self.ids.p15.active = False
        self.ids.p16.active = False
        self.ids.p17.active = False
        self.ids.p18.active = False
        self.ids.p19.active = False
        self.ids.p20.active = False
        self.ids.p21.active = False
        self.ids.p22.active = False
        self.ids.p23.active = False
        self.ids.p24.active = False
        self.ids.p25.active = False
        self.ids.p26.active = False


class Micronutrients2(Screen):

    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp4(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'micronutrients'

    @staticmethod
    def intt(x):
        if x:
            return '1'
        else:
            return '0'

    def next4(self):
        mycursor.execute(
            f"UPDATE patientmn SET p27 = {Micronutrients2.intt(self.ids.p27.active)}, p28 = {Micronutrients2.intt(self.ids.p28.active)},"
            f" p29 = {Micronutrients2.intt(self.ids.p29.active)}, p30 = {Micronutrients2.intt(self.ids.p30.active)}, "
            f"p31 = {Micronutrients2.intt(self.ids.p31.active)}, p32 = {Micronutrients2.intt(self.ids.p32.active)}, "
            f"p33 = {Micronutrients2.intt(self.ids.p33.active)}, p34 = {Micronutrients2.intt(self.ids.p34.active)}, "
            f"p35 = {Micronutrients2.intt(self.ids.p35.active)}, p36 = {Micronutrients2.intt(self.ids.p36.active)}, "
            f"p37 = {Micronutrients2.intt(self.ids.p37.active)}, p38 = {Micronutrients2.intt(self.ids.p38.active)}, "
            f"p39 = {Micronutrients2.intt(self.ids.p39.active)}, p40 = {Micronutrients2.intt(self.ids.p40.active)}, "
            f"p41 = {Micronutrients2.intt(self.ids.p41.active)}, p42 = {Micronutrients2.intt(self.ids.p42.active)},"
            f" p43 = {Micronutrients2.intt(self.ids.p43.active)}, p44 = {Micronutrients2.intt(self.ids.p44.active)}, "
            f"p45 = {Micronutrients2.intt(self.ids.p45.active)}, p46 = {Micronutrients2.intt(self.ids.p46.active)}, "
            f"p47 = {Micronutrients2.intt(self.ids.p47.active)}, p48 = {Micronutrients2.intt(self.ids.p48.active)}, "
            f"p49 = {Micronutrients2.intt(self.ids.p49.active)}, p50 = {Micronutrients2.intt(self.ids.p50.active)}, "
            f"p51 = {Micronutrients2.intt(self.ids.p51.active)}, p52 = {Micronutrients2.intt(self.ids.p52.active)},"
            f"p53 = {Micronutrients2.intt(self.ids.p53.active)},  p54 = {Micronutrients2.intt(self.ids.p54.active)}, "
            f"p55 = {Micronutrients2.intt(self.ids.p55.active)} where hpnumber='{Patient2.patient}'")
        db.commit()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'micronutrients3'

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def reset_checkbox(self):
        self.ids.p27.active = False
        self.ids.p28.active = False
        self.ids.p29.active = False
        self.ids.p30.active = False
        self.ids.p31.active = False
        self.ids.p32.active = False
        self.ids.p33.active = False
        self.ids.p34.active = False
        self.ids.p35.active = False
        self.ids.p36.active = False
        self.ids.p37.active = False
        self.ids.p38.active = False
        self.ids.p39.active = False
        self.ids.p40.active = False
        self.ids.p41.active = False
        self.ids.p42.active = False
        self.ids.p43.active = False
        self.ids.p44.active = False
        self.ids.p45.active = False
        self.ids.p46.active = False
        self.ids.p47.active = False
        self.ids.p48.active = False
        self.ids.p49.active = False
        self.ids.p50.active = False
        self.ids.p51.active = False
        self.ids.p52.active = False
        self.ids.p53.active = False
        self.ids.p54.active = False
        self.ids.p55.active = False


class Micronutrients3(Screen):
    def disconnect(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'login'
        self.manager.get_screen('login').resetForm()

    def backp4(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'micronutrients2'

    @staticmethod
    def intt(x):
        if x:
            return '1'
        else:
            return '0'

    def next4(self):
        mycursor.execute(
            f"UPDATE patientmn SET p56 = {Micronutrients3.intt(self.ids.p56.active)},"
            f" p57 = {Micronutrients3.intt(self.ids.p57.active)}, p58 = {Micronutrients3.intt(self.ids.p58.active)}, "
            f"p59 = {Micronutrients3.intt(self.ids.p59.active)}, p60 = {Micronutrients3.intt(self.ids.p60.active)}, "
            f"p61 = {Micronutrients3.intt(self.ids.p61.active)}, p62 = {Micronutrients3.intt(self.ids.p62.active)}, "
            f"p63 = {Micronutrients3.intt(self.ids.p63.active)}, p64 = {Micronutrients3.intt(self.ids.p64.active)}, "
            f"p65 = {Micronutrients3.intt(self.ids.p65.active)}, p66 = {Micronutrients3.intt(self.ids.p66.active)}, "
            f"p67 = {Micronutrients3.intt(self.ids.p67.active)}, p68 = {Micronutrients3.intt(self.ids.p68.active)}, "
            f"p69 = {Micronutrients3.intt(self.ids.p69.active)}, p70 = {Micronutrients3.intt(self.ids.p70.active)},"
            f" p71 = {Micronutrients3.intt(self.ids.p71.active)}, p72 = {Micronutrients3.intt(self.ids.p72.active)}, "
            f"p73 = {Micronutrients3.intt(self.ids.p73.active)}, p74 = {Micronutrients3.intt(self.ids.p74.active)}, "
            f"p75 = {Micronutrients3.intt(self.ids.p75.active)} where hpnumber='{Patient2.patient}'")
        db.commit()

        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'nfpe2'

    def profile(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'updateprofile'

    def reset_checkbox(self):
        self.ids.p56.active = False
        self.ids.p57.active = False
        self.ids.p58.active = False
        self.ids.p59.active = False
        self.ids.p60.active = False
        self.ids.p61.active = False
        self.ids.p62.active = False
        self.ids.p63.active = False
        self.ids.p64.active = False
        self.ids.p65.active = False
        self.ids.p66.active = False
        self.ids.p67.active = False
        self.ids.p68.active = False
        self.ids.p69.active = False
        self.ids.p70.active = False
        self.ids.p71.active = False
        self.ids.p72.active = False
        self.ids.p73.active = False
        self.ids.p74.active = False
        self.ids.p75.active = False


#actual app
class Nfpe3(Screen):
    def on_enter(self, *args):
        self.ids.date.text = ""
        Nfpe.filltopblanks(self)

    def ok(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'connected'
        LogIn.updaterv(self, Connected.hospital)

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'patient'
        try:
            mycursor.execute(
                f"SELECT hpnumber from patient where hpnumber='{Connected.hospital+self.ids.snu.text}'")
            Patient.newpatient = list(mycursor.fetchall())
        except Exception as e:
            print(e, "NFPE3 prob")


class Nfpe2(Screen):

    def on_enter(self, *args):
        self.ids.date.text = ""
        Nfpe.filltopblanks(self)
        Nfpe.fillbottomblanks(self)

    def ok(self):
        self.manager.transition = SlideTransition(direction="left")
        self.manager.current = 'micronutrientsfinal'

    def back(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'patient'
        try:
            mycursor.execute(
                f"SELECT hpnumber from patient where hpnumber='{Connected.hospital+self.ids.snu.text}'")
            Patient.newpatient = list(mycursor.fetchall())
        except Exception as e:
            print(e, "NFPE2 prob")


class Nfpe(Screen):
    def on_enter(self, *args):
        self.ids.date.text = ""
        self.filltopblanks()
        self.fillbottomblanks()

    def filltopblanks(self):
        try:
            mycursor.execute(
                f"SELECT staff, hospital, p_name, p_number,  p_gender, p_age, p_height, p_weight, "
                f"p_muac, p_hgs, p_firstimpression, date, p_ward from patient where hpnumber='{Patient2.patient}'")
            pi = list(mycursor.fetchall())
            self.ids.date.text = str(f'Summary of the NFPE done on {pi[0][11].strftime("%Y %b %d ")}')
            self.ids.ss.text = pi[0][0]
            self.ids.sh.text = pi[0][1]
            self.ids.sna.text = pi[0][2]
            self.ids.snu.text = pi[0][3]
            self.ids.sg.text = pi[0][4]
            self.ids.sa.text = pi[0][5]
            self.ids.she.text = pi[0][6]
            self.ids.sw.text = pi[0][7]
            self.ids.swa.text = pi[0][12]
            self.ids.smu.text = pi[0][8]
            self.ids.shg.text = pi[0][9]
            self.ids.sfi.text = pi[0][10]
        except Exception as e:
            self.ids.date.text = "Check your internet connection"
            print(e, "date")

    def fillbottomblanks(self):
        try:
            mycursor.execute(
                f"SELECT  p_temple, p_collar_bone,p_shoulder, p_scapula, p_hand, "
                f"p_thigh, p_calf, p_face, p_upper_arm, p_iliac_crest, p_edema, p_signs from patient where hpnumber='{Patient2.patient}'")
            pi = list(mycursor.fetchall())

            self.ids.ste.text = str(pi[0][0])
            self.ids.sco.text = str(pi[0][1])
            self.ids.ssh.text = str(pi[0][2])
            self.ids.ssc.text = str(pi[0][3])
            self.ids.sha.text = str(pi[0][4])
            self.ids.sap.text = str(pi[0][5])
            self.ids.sca.text = str(pi[0][6])
            self.ids.sfa.text = str(pi[0][7])
            self.ids.sar.text = str(pi[0][8])
            self.ids.sth.text = str(pi[0][9])
            self.ids.sed.text = str(pi[0][10])
            self.ids.ssin.text = str(pi[0][11])
            self.ids.smt.text = str(
                int(pi[0][0]) + int(pi[0][1]) + int(pi[0][2]) + int(pi[0][3]) + int(pi[0][4]) + int(pi[0][5]) + int(
                    pi[0][6]))
            self.ids.sft.text = str(int(pi[0][7]) + int(pi[0][8]) + (pi[0][9]))
            self.ids.set.text = str(pi[0][10])
        except Exception as e:
            print(e, "bottom prob")
    def ok(self):
        self.manager.transition = SwapTransition()
        self.manager.current = 'connected'
        self.manager.get_screen('connected')
        LogIn.updaterv(self, Connected.hospital)

    def back(self):

        try:
            self.manager.transition = SlideTransition(direction="right")
            self.manager.current = 'patient'

            mycursor.execute(
                f"SELECT hpnumber from patient where hpnumber='{Connected.hospital+self.ids.snu.text}'")
            Patient.newpatient = list(mycursor.fetchall())

        except Exception as e:
            print(e, "nfpe prob")
            self.ids.date.text = "Check your internet connection"


class SelectableRecycleBoxLayout2(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    pass


class SelectableLabel2(RecycleDataViewBehavior, GridLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 1

    id_label1 = StringProperty("")
    id_label2 = StringProperty("")

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel2, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel2, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected


class RV2(RecycleView):
    def __init__(self, **kwargs):
        super(RV2, self).__init__(**kwargs)
        self.data = []

    def createview(self, rows):
        self.data = [{'id_label1': str(x[0]), 'id_label2': str(x[1]), 'id_label3': str(x[2])} for x in rows]


class Micronutrientsfinal(Screen):

    def on_enter(self, *args):

        mycursor.execute(
            f"SELECT p1, p3, p5, p7, p9, p10, p12, p14, p2, p4, p6, p8, p11, p13, p15, p18, p20,p22,p24, p26, p16, p17, p19,  p21, "
            f" p23, p25, p27, p28,  p29, p31, p32, p30,  p33, p34, p36, p37, p39, p41, p35,  p38,  p40,  p42, "
            f"p44, p46, p48,  p50, p52,  p54, p43,  p45,  p47,  p49, p51,  p53,  p55, p56, p57, p58, p59, p60, p61, p62, p63, "
            f"p64, p65, p66, p67, p68, p69, p70, p71, p72, p73, p74, p75 from patientmn where hpnumber='{Patient2.patient}'")
        pi = list(mycursor.fetchall())

        self.list1 = [(" [anchor=center][b]SIGNS [/b]", "[b]POSSIBLE NUTRITION-RELATED CAUSES [/b]", "[b]POSSIBLE NON-NUTRITION-RELATED CAUSES[/b]")]
        for i in range(len(pi[0])):
            if i == 0 and (pi[0][0] == "1" or pi[0][1] == "1" or pi[0][2] == "1" or pi[0][3] == "1" or pi[0][4] == "1" or pi[0][5] == "1" or pi[0][6] == "1" or pi[0][7] == "1"):
                self.list1.append((f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/50)}[b][u]EYES[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 0 and pi[0][0] == "1":
                self.list1.append(('Xanthelasma or Circumferential Arcus',"Hyperlipidemia", "Circumferential Arcus may be normal in adults >45 years old" ))
            if i == 1 and pi[0][1] == "1":
                self.list1.append(('Angular Blepharitis', "Riboflavin, Biotin, Vitamin B6, Zinc deficiency", "Poor eye hygiene"))
            if i == 2 and pi[0][2] == "1":
                self.list1.append(('Pale Conjuctutiva', "Vitamin B6, Vitamin B12, Folate, Iron, Copper deficiency; Anemias",
                              "Non-nutritional anemia"))
            if i == 3 and pi[0][3] == "1":
                self.list1.append(('Night Blindness, dry membranes, dull or soft cornea, infected, ulcerated eye - Keratomalacia',
                             "Vitamin A deficiency", "Eye diseases; Uremia; Hypothyroidism"))
            if i == 4 and pi[0][4] == "1":
                self.list1.append(('Angular Palpebritis', "Niacin, Riboflavin, Iron, Vitamin B6 deficiency", ""))
            if i == 5 and pi[0][5] == "1":
                self.list1.append(('Ring of fine blood vessels around cornea', "General poor nutritiony", ""))
            if i == 6 and pi[0][6] == "1":
                self.list1.append(("Bitot's spots", "Vitamin A deficiency", ""))
            if i == 7 and pi[0][7] == "1":
                self.list1.append(("Opthlmoplegia", "Thiamin, Phosphorous deficiency", "Brain lesion; Grave’s disease; Stroke"))
            if i == 8 and (pi[0][8] == "1" or pi[0][9] == "1" or pi[0][10] == "1" or pi[0][11] == "1"):
                self.list1.append((f" {'.'*int(self.width*0.3/40)}", f"{'.'*int(self.width*0.3/50)}[b][u]FACE[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 8 and pi[0][8] == "1":
                self.list1.append(('Skin color loss, dark cheeks and under eyes',"Protein-calorie deficiency; Niacin, Riboflavin, and Vitamin B6 deficiency", "" ))
            if i == 9 and pi[0][9] == "1":
                self.list1.append(('Pallor',"Iron, Folate, Vitamin B12, and Vitamin C deficiency", "" ))
            if i == 10 and pi[0][10] == "1":
                self.list1.append(('Hyperpigmentation(face, eyes, neck, hands)', "Niacin deficiency", " Hormonal changes; Excessive sun exposure; Anti-seizure medications"))
            if i == 11 and pi[0][11] == "1":
                self.list1.append(('Enlarged parotid gland', "Protein deficiency; Bulimia", "Mumps; Portal cirrhosis; Sjogren’s Syndrome; Salivary duct stone"))
            if i == 12 and (pi[0][12] == "1" or pi[0][13] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/70)}[b][u]MOUTH[/u][/b]{'.'*int(self.width*0.3/70)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 12 and pi[0][12] == "1":
                self.list1.append(('Soreness, burning', "Riboflavin deficiency", "Oral candidiasis"))
            if i == 13 and pi[0][13] == "1":
                self.list1.append(("Angular Stomatitis or Cheilitis", "Riboflavin, Niacin, Iron, Vitamin B6, Vitamin B12 deficiency; Vitamin A toxicity", "Excessive salivation due to ill-fitting dentures; Dry skin; Dehydration; Herpes"))
            if i == 14 and pi[0][14] == "1":
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/50)}[b][u]LIPS[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
                self.list1.append(("Soreness, burning lips, pale", "Riboflavin deficiency", ""))
            if i == 15 and (pi[0][15] == "1" or pi[0][16] == "1" or pi[0][17] == "1" or pi[0][18] == "1" or pi[0][19] == "1" ):
                self.list1.append((  f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/70)}[b][u]TONGUE[/u][/b]{'.'*int(self.width*0.3/70)}",  f" {'.'*int(self.width*0.3/40)}"))
            if i == 15 and pi[0][15] == "1":
                self.list1.append(("Sore, swollen, scarlet, raw-beefy red tongue", "Folate, Niacin deficiency", ""))
            if i == 16 and pi[0][16] == "1":
                self.list1.append(("Soreness, burning tongue, purplish/magenta", "Riboflavin deficiency", ""))
            if i == 17 and pi[0][17] == "1":
                self.list1.append(("Smooth, beefy red tongue", "Vitamin B12, Niacin deficiency", ""))
            if i == 18 and pi[0][18] == "1":
                self.list1.append(("Glossitis (sore, swollen, red, and smooth tongue)",
                              "Riboflavin, Niacin, Vitamin B6, Vitamin B12, Folate, Severe iron deficiency",
                              "Crohn’s; Uremia; Infection; Malignancy; Anticancer therapy; Trauma"))
            if i == 19 and pi[0][19] == "1":  # there were 2 pale tongues
                self.list1.append(("Pale tongue", "Vitamin B12, Folate, Iron deficiency", ""))
            if i == 20 and (pi[0][20] == "1" or pi[0][21] == "1" or pi[0][22] == "1" or pi[0][23] == "1" or pi[0][24] == "1" or pi[0][25] == "1"):
                self.list1.append((f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/50)}[b][u]HAIR[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 20 and pi[0][20] == "1":
                self.list1.append(("Alopecia", "Iron, Zinc, Biotin, Protein deficiency", "Aging, chemotherapy or radiation; Stress; Hormonal changes; Endocrine disorders; Medications"))
            if i == 21 and pi[0][21] == "1":
                self.list1.append(("Color changes, depigmentation, lackluster", "Protein-calorie malnutrition, Manganese, Selenium, Copper deficiency", ""))
            if i == 22 and pi[0][22] == "1":
                self.list1.append(("Easily plucked with no pain; Dull, dry; Lack of natural shine", "Protein deficiency, Malnutrition, Essential fatty acid deficiency", "Over-processing of hair, excess bleaching"))
            if i == 23 and pi[0][23] == "1":
                self.list1.append(("Corkscrew hair, unemerged coiled hairs, shape of swan neck", "Vitamin C deficiency", "Menkes syndrome"))
            if i == 24 and pi[0][24] == "1":
                self.list1.append(("Flag sign (banded colors)", "Protein-calorie malnutrition", ""))
            if i == 25 and pi[0][25] == "1":
                self.list1.append(("Lanugo (very fine, soft hair)", "Calorie deficiency", ""))
            if i == 26 and pi[0][26] == "1":
                self.list1.append(( f"{'.'*int(self.width*0.3/40)}", f"{'.'*int(self.width*0.3/50)}[b][u]GUMS[/u][/b]{'.'*int(self.width*0.3/50)}", f"{'.'*int(self.width*0.3/40)}"))
                self.list1.append(("Gingivitis, swollen, spongy, bleeds easily, redness, retracted gums", "Vitamin C, Niacin, Folate, Zinc deficiency; Severe Vitamin D deficiency; Excessive Vitamin A", "Poor oral hygiene; Genetics; Smoking/chewing tobacco; Pregnancy; Diabetes; Medications"))
            if i == 27 and pi[0][27] == "1":
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/50)}[b][u]TASTE[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
                self.list1.append(("Hypogeusia; Dysgeusia (Diminished/altered taste)", "Zinc deficiency",
                              "Medications such as antineoplastic agents or sulfonylureas"))
            if i == 28 and (pi[0][28] == "1" or pi[0][29] == "1" or pi[0][30] == "1"):
                self.list1.append(( f"{'.'*int(self.width*0.3/40)}", f" {'.'*int(self.width*0.3/50)}[b][u]TEETH[/u][/b]{'.'*int(self.width*0.3/50)}",f"{'.'*int(self.width*0.3/40)}"))
            if i == 28 and pi[0][28] == "1":
                self.list1.append(("Gray-brown spots, mottling", "Increased fluoride intake", ""))
            if i == 29 and pi[0][29] == "1":
                self.list1.append(("Missing or erupting abnormally", "Generally poor nutrition", ""))
            if i == 30 and pi[0][30] == "1":
                self.list1.append(("Dental caries", "Vitamin D, Vitamin B6 deficiency; Inadequate fluoride; Excessive sugar",
                              "Poor oral hygiene"))
            if i == 31 and (pi[0][31] == "1" ):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}", f"{'.'*int(self.width*0.3/50)}[b][u]NECK[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
                self.list1.append(("Thyroid enlargement; Goiter", "Iodine deficiency",
                              "Hypo- or hyperthyroidism; Inflammatory process; Malignancy; Various cysts; Thyroiditis"))
            if i == 32 and (pi[0][32] == "1" or pi[0][33] == "1" or pi[0][34] == "1" or pi[0][35] == "1" or pi[0][36] == "1" or pi[0][37] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}",f"{'.'*int(self.width*0.3/50)}[b][u]NAILS[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 32 and pi[0][32] == "1":
                self.list1.append(("Beau’s line; horizontal grooves", " Severe zinc deficiency; Protein deficiency; Hypocalcemia", "Severe illness (i.e. MI or high fevers); Immunosuppressive therapy or chemotherapy"))
            if i == 33 and pi[0][33] == "1":
                self.list1.append(("Muehrcke’s Lines (transverse white lines)", "Malnutrition, Hypoalbuminemia", "Chronic liver or renal disease"))
            if i == 34 and pi[0][34] == "1":
                self.list1.append(("Koilonychia (spoon-shaped, concave)", "Iron, Protein deficiency; Anemia",
                              "Considered normal if seen on toenails only; Diabetes; Systemic Lupus; Raynaud’s Disease: Hypothyroidism"))
            if i == 35 and pi[0][35] == "1":
                self.list1.append(("Splinter Hemorrhage", "Vitamin C deficiency", "Bacterial endocarditis; Trichinosis; Vascular disease"))
            if i == 36 and pi[0][36] == "1":
                self.list1.append(("Brittle, soft, dry; split easily", "Magnesium deficiency; Severe malnutrition; Vitamin A and Selenium toxicity",
                              "Metabolic bone disorder; Thyroid disorder; Systemic amyloidosis; Aging"))
            if i == 37 and pi[0][37] == "1":
                self.list1.append(("Central ridges", "Iron, Folate, Protein deficiency", "Severe arterial disease"))
            if i == 38 and pi[0][38] == "1":
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}",f"[b][u]GASTROINTESTSTINAL[/u][/b]", f" {'.'*int(self.width*0.3/40)}"))
                self.list1.append(("Anorexia, flatulence, diarrhea", "Vitamin B12, Vitamin B6 deficiency", "GI disorders"))
            if i == 39 and (pi[0][39] == "1" or pi[0][40] == "1" or pi[0][41] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}", f"[b][u]SKELETAL SYSTEM[/u][/b]", f" {'.'*int(self.width*0.3/40)}"))
            if i == 39 and pi[0][39] == "1":
                self.list1.append(("Demineralization of bone", "Calcium, Phosphorus, Vitamin D deficiency; Excessive Vitamin A", ""))
            if i == 40 and pi[0][40] == "1":
                self.list1.append(("Epiphyseal enlargement of joints; Rickets", "Vitamin D deficiency", ""))
            if i == 41 and pi[0][41] == "1":
                self.list1.append(("Bone tenderness/pain", "Vitamin D deficiency", "Fractures; Arthritis; Cancer"))
            if i == 42 and (pi[0][42] == "1" or pi[0][43] == "1" or pi[0][44] == "1" or pi[0][45] == "1" or pi[0][46] == "1" or pi[0][47] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}", f"[b][u]NERVOUS SYSTEM[/u][/b]", f" {'.'*int(self.width*0.3/40)}"))
            if i == 42 and pi[0][42] == "1":
                self.list1.append(("Listlessness", "Protein-calorie deficiency", ""))
            if i == 43 and pi[0][43] == "1":
                self.list1.append(("Inability to concentrate, defective memory; Confabulation; Disorientation",
                              "Thiamin deficiency (Korsakoff’s psychosis), Vitamin B12 deficiency",
                              "Head trauma; Cerebral hemorrhage; Brain tumor; Alzheimer’s disease"))
            if i == 44 and pi[0][44] == "1":
                self.list1.append(("Seizures (Tetany), memory impairment, and behavioral disturbances", "Calcium, Magnesium, Zinc, Vitamin D deficiency", ""))
            if i == 45 and pi[0][45] == "1":
                self.list1.append(("Peripheral neuropathy with weakness and paraesthesias; Ataxia",
                              "Vitamin B12, Thiamine deficiency (Wernicke encephalopathy), Copper, Vitamin B6 deficiency",
                              ""))
            if i == 46 and pi[0][46] == "1":
                self.list1.append(("Increased weakness; impaired cognitive function; irritability; anorexia",
                              "Folate, Vitamin B12 deficiency", ""))
            if i == 47 and pi[0][47] == "1":
                self.list1.append(("Dementia", "Niacin, Vitamin B12 deficiency; Hypercalcemia; Aluminum toxicity",
                              " Disease or age-related; Medications"))
            if i == 48 and (pi[0][48] == "1" or pi[0][49] == "1" or pi[0][50] == "1" or pi[0][51] == "1" or pi[0][52] == "1" or pi[0][53] == "1" or pi[0][54] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}", f"[b][u]MUSCULAR SYSTEM[/u][/b]", f" {'.'*int(self.width*0.3/40)}"))
            if i == 48 and pi[0][48] == "1":
                self.list1.append(("Weakness","Phosphorus or potassium deficiency; Vitamin C, Vitamin D, Vitamin B6 deficiency; Anemia", ""))
            if i == 49 and pi[0][49] == "1":
                self.list1.append(("Wasted appearance", "Protein-calorie deficiency", ""))
            if i == 50 and pi[0][50] == "1":
                self.list1.append(("Calf tenderness, absent deep tendon reflexes, foot and wrist drop", "Thiamin deficiency", "Spinal cord or nerve damage"))
            if i == 51 and pi[0][51] == "1":
                self.list1.append(("Peripheral neuropathy, tingling, pins and needles", "Folate, Vitamin B6, Pantothenic acid, Phosphate, Thiamin, Vitamin B12 deficiency; Vitamin B6 toxicity", "Nerve damage"))
            if i == 52 and pi[0][52] == "1":
                self.list1.append(("Muscle twitching, convulsions, tetany", "Magnesium or Vitamin B6 excess or deficiency; Calcium, Vitamin D, Magnesium deficiency", ""))
            if i == 53 and pi[0][53] == "1":
                self.list1.append(("Muscle cramps", "Magnesium or Vitamin B6 excess or deficiency; Calcium, Vitamin D, Magnesium deficiency", ""))
            if i == 54 and pi[0][54] == "1":
                self.list1.append(("Muscle pain", "Biotin, Vitamin D deficiency", " Fibromyalgia"))
            if i == 55 and (pi[0][55] == "1" or pi[0][56] == "1" or pi[0][57] == "1" or pi[0][58] == "1" or pi[0][59] == "1" or pi[0][60] == "1" or pi[0][61] == "1" or pi[0][62] == "1" or pi[0][63] == "1" or pi[0][64] == "1" or pi[0][65] == "1" or pi[0][66] == "1" or pi[0][67] == "1" or pi[0][68] == "1" or pi[0][69] == "1"or pi[0][70] == "1" or pi[0][71] == "1" or pi[0][72] == "1" or pi[0][73] == "1" or pi[0][74] == "1"):
                self.list1.append(( f" {'.'*int(self.width*0.3/40)}", f"{'.'*int(self.width*0.3/50)}[b][u]SKIN[/u][/b]{'.'*int(self.width*0.3/50)}", f" {'.'*int(self.width*0.3/40)}"))
            if i == 55 and pi[0][55] == "1":
                self.list1.append(("Slow wound healing, decubitus ulcers", "Zinc, Vitamin C, Protein deficiency; Malnutrition; Inadequate hydration", "Poor skin care; Diabetes; Steroid use"))
            if i == 56 and pi[0][56] == "1":
                self.list1.append(("Velvety hyperpigmentation in body folds", "Obesity; Insulin resistance", "Hypothyroidism; Insulin Resistant Diabetes; Cushing’s Syndrome; Acromegaly; Metabolic syndrome"))
            if i == 57 and pi[0][57] == "1":
                self.list1.append(("Psoriasis", "Biotin deficiency", ""))
            if i == 58 and pi[0][58] == "1":
                self.list1.append(("Eczema", "Riboflavin, Zinc deficiency", "Atopic dermatitis"))
            if i == 59 and pi[0][59] == "1":
                self.list1.append(("Follicular Hyperkeratosis (goose flesh)", "Vitamin A or C deficiency", "Infection of hair follicle; Syphilis"))
            if i == 60 and pi[0][60] == "1":
                self.list1.append(("Seborrheic Dermatitis", "Biotin, Vitamin B6, Zinc, Riboflavin, Essential fatty acid deficiency; Vitamin A excess or deficiency", "Nasal drainage"))
            if i == 61 and pi[0][61] == "1":
                self.list1.append(("Petechiae (purple or red spots due to bleeding under the skin)", "Vitamin C, Vitamin K deficiency", "Abnormal blood clotting; Severe fever"))
            if i == 62 and pi[0][62] == "1":
                self.list1.append(("Purpura (purple-colored spots and patches on the skin, and in mucous membranes, including the lining of the mouth", "Vitamin C, Vitamin K deficiency; Excessive Vitamin E", "Anticoagulant therapy; Injury; Thrombocytopenia"))
            if i == 63 and pi[0][63] == "1":
                self.list1.append(("Xerosis (abnormal dryness)", "Vitamin A, Essential fatty acid deficiency", "Aging; Allergies; Hygiene; Hypothyroidism; Uremia; Ichthyosis"))
            if i == 64 and pi[0][64] == "1":
                self.list1.append(("Perifollicular Hemorrhage", "Vitamin C deficiency", ""))
            if i == 65 and pi[0][65] == "1":
                self.list1.append((" Dryness, sandpaper feel, flakiness", "Increased or decreased Vitamin A", ""))
            if i == 66 and pi[0][66] == "1":
                self.list1.append(("Pellagra (thick, dry, scaly pigmented skin on sun-exposed areas", "Niacin, Tryptophan, Vitamin B6 deficiency", "Psoriasis; Sun or chemical burns"))
            if i == 67 and pi[0][67] == "1":
                self.list1.append(("Lack of fat under skin, cellophane appearance", "Protein-calorie deficiency, Vitamin C deficiency", ""))
            if i == 68 and pi[0][68] == "1":
                self.list1.append(("Bilateral edema", "Protein-calorie deficiency, Vitamin C deficiency", "Congestive heart failure; Kidney or liver disease"))
            if i == 69 and pi[0][69] == "1":
                self.list1.append(("Yellow Pigmentation", "Vitamin B12 deficiency", "Liver disease; Excessive hemolysis; Bile obstruction"))
            if i == 70 and pi[0][70] == "1":
                self.list1.append(("Yellow to Orange Pigmentation", "Excessive beta-carotene", ""))
            if i == 71 and pi[0][71] == "1":
                self.list1.append(("Cutaneous flushing – increased redness, desquamation", "Niacin excess (flushing) or deficiency (desquamation)", "High fever; Hyperthyroidism; Rosacea; Medications"))
            if i == 72 and pi[0][72] == "1":
                self.list1.append(("Body edema, round swollen face (moon face)", "Protein, Thiamin deficiency", "Medication, especially steroids"))
            if i == 73 and pi[0][73] == "1":
                self.list1.append(("Pallor, fatigue, depression", "Iron, Vitamin B12, Folate deficiency; Anemia", "Blood loss"))
            if i == 74 and pi[0][74] == "1":
                self.list1.append(("Poor skin turgor", "Dehydration", "May be normal finding in elderly"))

        nrv = LoginApp.get_running_app().root.get_screen('micronutrientsfinal').ids.patientlist2
        nrv.createview(self.list1)

    def ok(self):
        LogIn.updaterv(self, Connected.hospital)
        self.manager.transition = SwapTransition()
        self.manager.current = 'connected'

    def edit(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'micronutrients'

    def backp4(self):
        self.manager.transition = SlideTransition(direction="right")
        self.manager.current = 'nfpe2'


class LoginApp(MDApp):
    title = "Nutrition Focused Physical Exam"

    def build(self):
        Window.clearcolor = [1, 1, 1, 1]
        Window.softinput_mode = "resize"
        manager.add_widget(LogIn(name='login'))
        manager.add_widget(Connected(name='connected'))
        manager.add_widget(Signup(name="signup"))
        manager.add_widget(Patient(name="patient"))
        manager.add_widget(PFlag(name="pflag"))
        manager.add_widget(Nfpe3(name="nfpe3"))
        manager.add_widget(Updateprofile(name="updateprofile"))
        manager.add_widget(Patient2(name="patient2"))
        manager.add_widget(Patient3(name="patient3"))
        manager.add_widget(Nfpe(name="nfpe"))
        manager.add_widget(About(name="about"))
        manager.add_widget(Micronutrients(name="micronutrients"))
        manager.add_widget(Micronutrients2(name="micronutrients2"))
        manager.add_widget(Micronutrients3(name="micronutrients3"))
        manager.add_widget(Nfpe2(name="nfpe2"))
        manager.add_widget(Micronutrientsfinal(name="micronutrientsfinal"))

        return manager


LoginApp().run()

from kivy.app import App
from kivy.lang import Builder
from kivy.animation import Animation
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.image import Image
from kivy.uix. behaviors import ButtonBehavior
from datetime import datetime
import json, glob, random
from pathlib import Path
from hoverable import HoverBehavior


Builder.load_file('design.kv')

class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current="sign_up_screen"

    def login(self, uname, pword):
        with open("users.json") as myfile:
            users = json.load(myfile)
        if uname in users and users[uname]["password"] == pword:
            self.manager.current="login_screen_success"
        else:
            self.ids.login_wrong.text = "Wrong username or password"
    def forget(self):
        self.manager.current="forget_screen"

class RootWidget(ScreenManager):
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        with open("users.json") as myfile:
            users = json.load(myfile)

        if uname == "":
            self.ids.sign_info.text = "username can not be empty"
        elif pword == "":
            self.ids.sign_info.text = "password can not be empty"
        elif uname in users.keys():
            self.ids.sign_info.text = "username already exist"
        else:
            users[uname] = {'username':uname, 'password':pword,
                'created': datetime.now().strftime("%Y-%m-%d %H-%M-%S")}

            with open("users.json","w") as myfile:
                json.dump(users, myfile)

            self.manager.transition.direction = "right"
            self.manager.current = "sign_up_screen_success"

    def back_to_login(self):
        self.manager.current="login_screen"

class SignUpScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.current="login_screen"

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def get_quote(self, feel):
        feel= feel.lower()
        available_feelings = glob.glob("quotes/*txt")

        available_feelings = [Path(filename).stem for filename in available_feelings]

        if  feel in available_feelings:
            with open(f"quotes/{feel}.txt") as myfile:
                quotes = myfile.readlines()
                self.ids.quote.text = random.choice(quotes)
        else:
            self.ids.quote.text = "Try another feeling maybe?"

class ForgetScreen(Screen):
    def reset_pw(self, uname, pw1, pw2):
        with open("users.json") as myfile:
            users = json.load(myfile)

        if uname == "":
            self.ids.reset_info.text = "username can not be empty"
        elif pw1 == "" or pw2 =="":
            self.ids.reset_info.text = "password can not be empty"
        elif uname in users.keys():
            if pw1 != pw2:
                self.ids.reset_info.text = "password does not match"
            elif pw1 == users[uname]["password"]:
                self.ids.reset_info.text = "password is same with old password"
            else:
                users[uname]["password"] = pw1
                users[uname]["created"] = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                with open("users.json","w") as myfile:
                    json.dump(users, myfile)
                self.manager.current = "reset_screen_success"

        else:
            self.ids.reset_info.text = "username not exist, try another"

    def back_to_login(self):
        self.manager.current = "login_screen"

class ForgetScreenSuccess(Screen):
    def back_to_login(self):
        self.manager.current="login_screen"

class MainApp(App):
    def build(self):
        return RootWidget()

class ImageButton(ButtonBehavior, HoverBehavior,Image):
    pass


if __name__ == "__main__":
    MainApp().run()

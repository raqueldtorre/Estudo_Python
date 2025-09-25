from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from database import DataBase
import os

# ====================================================
# Caminho absoluto para o arquivo users.txt
# ====================================================
current_dir = os.path.dirname(os.path.abspath(__file__))
db_file = os.path.join(current_dir, "users.txt")
db = DataBase(db_file)

# ====================================================
# Tela de Criação de Conta
# ====================================================
class CreateAccountWindow(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        if (
            self.namee.text != ""
            and self.email.text != ""
            and self.email.text.count("@") == 1
            and self.email.text.count(".") > 0
        ):
            if self.password.text != "":
                db.add_user(self.email.text, self.password.text, self.namee.text)
                self.reset()
                sm.current = "login"
            else:
                invalidForm()
        else:
            invalidForm()

    def login(self):
        self.reset()
        sm.current = "login"

    def reset(self):
        self.email.text = ""
        self.password.text = ""
        self.namee.text = ""


# ====================================================
# Tela de Login
# ====================================================
class LoginWindow(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            MainWindow.current = self.email.text
            self.reset()
            sm.current = "main"
        else:
            invalidLogin()

    def createBtn(self):
        self.reset()
        sm.current = "create"

    def reset(self):
        self.email.text = ""
        self.password.text = ""


# ====================================================
# Tela Principal
# ====================================================
class MainWindow(Screen):
    n = ObjectProperty(None)
    email = ObjectProperty(None)
    created = ObjectProperty(None)
    current = ""

    def logOut(self):
        sm.current = "login"

    def on_enter(self, *args):
        password, name, created = db.get_user(self.current)
        self.n.text = f"Nome da conta: {name}"
        self.email.text = f"Email: {self.current}"
        self.created.text = f"Criado em {created}"


# ====================================================
# Gerenciador de telas
# ====================================================
class WindowManager(ScreenManager):
    pass


# ====================================================
# Popups
# ====================================================
def invalidLogin():
    pop = Popup(
        title="Login inválido",
        content=Label(text="Usuário e senha inválidos"),
        size_hint=(None, None),
        size=(400, 400),
    )
    pop.open()


def invalidForm():
    pop = Popup(
        title="Formulário inválido",
        content=Label(text="Preencha todas as informações antes do login"),
        size_hint=(None, None),
        size=(400, 400),
    )
    pop.open()


# ====================================================
# Carrega KV
# ====================================================
kv = Builder.load_file("mk.kv")

# ====================================================
# Inicializa gerenciador de telas
# ====================================================
sm = WindowManager()
screens = [
    LoginWindow(name="login"),
    CreateAccountWindow(name="create"),
    MainWindow(name="main"),
]

for screen in screens:
    sm.add_widget(screen)

sm.current = "login"


# ====================================================
# Classe principal
# ====================================================
class MyMainApp(App):
    def build(self):
        return sm


if __name__ == "__main__":
    MyMainApp().run()

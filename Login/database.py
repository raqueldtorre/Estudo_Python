import os
import datetime

class DataBase:
    def __init__(self, filename):
        # Caminho absoluto baseado no script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(current_dir, filename)

        # Cria o arquivo se não existir
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                pass  # cria arquivo vazio

        self.users = {}
        self.load()

    def load(self):
    #Carrega usuários do arquivo
        self.users = {}
        with open(self.filename, "r") as f:
            for line in f:
                parts = line.strip().split(";")
                if len(parts) != 4:
                    continue  # pula linhas inválidas
                email, password, name, created = parts
                self.users[email] = (password, name, created)


    def get_user(self, email):
        """Retorna dados do usuário (senha, nome, data) ou -1 se não existir"""
        return self.users.get(email, -1)

    def add_user(self, email, password, name):
        """Adiciona usuário se email não existir"""
        email = email.strip()
        if email not in self.users:
            self.users[email] = (password.strip(), name.strip(), DataBase.get_date())
            self.save()
            return 1
        else:
            print("Email já existe")
            return -1

    def validate(self, email, password):
        """Valida login com email e senha"""
        user = self.get_user(email)
        if user != -1:
            return user[0] == password
        return False

    def save(self):
        """Salva todos os usuários no arquivo"""
        with open(self.filename, "w") as f:
            for email, (password, name, created) in self.users.items():
                f.write(f"{email};{password};{name};{created}\n")

    @staticmethod
    def get_date():
        """Retorna a data atual no formato YYYY-MM-DD"""
        return str(datetime.datetime.now()).split(" ")[0]

# Importa classes básicas do Kivy para criar o app, botões e layouts
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

# Define a classe principal do App
class MainApp(App):
    def build(self):
        # Lista de operadores que vamos usar
        self.operador = ["/", "*", "+", "-"]
        # Flag para controlar se o último botão pressionado foi um operador
        self.ultimo_operador = False

        # Layout principal vertical
        main_layout = BoxLayout(orientation="vertical")

        # TextInput que vai mostrar o valor da calculadora
        # readonly=True para impedir digitação direta
        # halign='right' para alinhar o texto à direita
        self.solution = TextInput(
            multiline=False,
            readonly=True,
            halign='right',
            font_size=55
        )
        # Adiciona o TextInput ao layout principal
        main_layout.add_widget(self.solution)

        # Define os botões da calculadora em uma matriz (4x4)
        botoes = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"]
        ]

        # Cria cada linha de botões
        for linha in botoes:
            h_layout = BoxLayout()  # Layout horizontal para cada linha
            for label in linha:
                # Cria botão com texto
                button = Button(
                    text=label,
                    pos_hint={'center_x': 0.5, 'center_y': 0.5}
                )
                # Associa função que vai tratar o clique
                button.bind(on_press=self.on_button_press)
                # Adiciona botão à linha
                h_layout.add_widget(button)
            # Adiciona linha ao layout principal
            main_layout.add_widget(h_layout)

        # Botão "=" separado, adiciona no final
        equals_button = Button(
            text="=",
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        # Associa função para calcular o resultado
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    # Função chamada quando qualquer botão é pressionado
    def on_button_press(self, instance):
        button_text = instance.text  # texto do botão
        current = self.solution.text  # valor atual no display

        if button_text == "C":
            # Limpa o display
            self.solution.text = ""
            self.ultimo_operador = False
        elif button_text in self.operador:
            # Se o botão é um operador
            # Adiciona operador somente se o último botão não foi operador
            if current and not self.ultimo_operador:
                self.solution.text += button_text
                self.ultimo_operador = True
        else:
            # Se o botão é número ou ponto
            self.solution.text += button_text
            self.ultimo_operador = False

    # Função chamada quando "=" é pressionado
    def on_solution(self, instance):
        try:
            text = self.solution.text
            if text:
                # Calcula o resultado usando eval
                solution = str(eval(text))
                self.solution.text = solution
        except Exception:
            # Caso dê erro, mostra "Erro" no display
            self.solution.text = "Erro"


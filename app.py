#-*-coding: utf-8-*-

import wx
import sqlite3

con = sqlite3.connect('dados.db')
cur = con.cursor()


class WindowClass(wx.Frame):
    def __init__(self,*args, **kwargs):
        super(WindowClass, self).__init__(*args, **kwargs, size=(400,300))
        self.basic_gui()
        self.Centre()
        self.Show()

    def basic_gui(self):
        panel = wx.Panel(self)
       
        self.TextCtrlNome = wx.TextCtrl(panel, pos=(120,10), size=(450,25)) #cria um area de texto dentro do panel
        self.TextCtrlEndereco = wx.TextCtrl(panel, pos=(120,40), size=(450,25)) #cria um area de texto dentro do panel
        self.TextCtrlAltura = wx.TextCtrl(panel, pos=(120,70), size=(175,25)) #cria um area de texto dentro do panel
        self.TextCtrlPeso = wx.TextCtrl(panel, pos=(120,100), size=(175,25)) #cria um area de texto dentro do panel
        self.TextCtrlResultado = wx.TextCtrl(panel, pos=(300,70), size=(270,120), style=wx.TE_MULTILINE) #cria um area de texto dentro do panel

        text = wx.StaticText(panel, 4, 'Nome do Paciente: ', (5,15))
        text = wx.StaticText(panel, 5, 'Endereço Completo: ', (5,45))
        text = wx.StaticText(panel, 6, 'Altura: (cm): ', (5,75))
        text = wx.StaticText(panel, 7, 'Peso (Kg): ', (5,105))

        wx.Button(panel, id=3, label='Calcular', pos=(110,195)).SetSize((117,-1))
        wx.Button(panel, id=2, label='Reiniciar', pos=(230,195)).SetSize((117,-1))
        wx.Button(panel, id=1, label='Sair', pos=(455,195)).SetSize((117,-1))
        wx.Button(panel, id=4, label='Consultar', pos=(350,195)).SetSize((102,-1))

        self.Bind(wx.EVT_BUTTON, self.onQuit, id=1)
        self.Bind(wx.EVT_BUTTON, self.reset, id=2)
        self.Bind(wx.EVT_BUTTON, self.calcularImc, id=3)
        self.Bind(wx.EVT_BUTTON, self.consultarImc, id=4)           

        self.SetTitle('Cálculo do IMC - Índice de Massa Corporal')
        self.SetSize(600,260)

        self.Centre()
        self.Show(True)


    def onQuit(self, e):
        self.Close()

    def reset(self, e):
        # Limpa os TextCtrls
        self.TextCtrlNome.Clear()
        self.TextCtrlEndereco.Clear()
        self.TextCtrlAltura.Clear()
        self.TextCtrlPeso.Clear()
        self.TextCtrlResultado.Clear()

    def consultarImc(self, e):
        #consulta dados salbos
        cur.execute('SELECT * FROM dados')
        resultados = cur.fetchall()

        # Formata os resultados antes de definir o valor no TextCtrlResultado
        resultados_formatados = ""
        for row in resultados:
            resultados_formatados += f"Nome: {row[1]}, Endereço: {row[2]}, Altura: {row[3]}, Peso: {row[4]}, IMC: {row[5]}\n\n"

        # Define o valor no TextCtrlResultado
        self.TextCtrlResultado.SetValue(resultados_formatados)

    def calcularImc(self, e):
        nome = self.TextCtrlNome.GetValue()
        endereco = self.TextCtrlEndereco.GetValue()

        try:
            altura = int(self.TextCtrlAltura.GetValue())
            peso = int(self.TextCtrlPeso.GetValue())

            # Cálculo do IMC
            imc = peso / (altura / 100) ** 2
            resultado = f'Nome: {nome:} \nEndereço: {endereco:} \nSeu IMC é: {imc:.2f}'

            # Lógica para determinar a mensagem com base no IMC
            if imc < 17:
                mensagem = ' Muito abaixo do peso'
            elif 17 <= imc < 18.49:
                mensagem = ' Abaixo do peso'
            elif 18.49 <= imc < 24.99:
                mensagem = ' Peso Normal'
            elif 24.99 <= imc < 29.99:
                mensagem = 'Acima do peso'
            elif 29.99 <= imc < 34.99:
                mensagem = 'Obesidade I'
            elif 34.99 <= imc < 39.99:
                mensagem = 'Obesidade II (severa)'
            else:
                mensagem = 'Obesidade III (mórbida)'

            resultadocompleto = f'{resultado}\nClassificação: {mensagem}'

            array = [nome, endereco, altura, peso, imc]

            cur.execute('INSERT INTO dados (nome, endereco, altura, peso, imc ) values (?,?,?,?,?)', array)

            con.commit()


            # Definindo o valor no TextCtrlResultado
            self.TextCtrlResultado.SetValue(resultadocompleto)            
        except ValueError:
            wx.MessageBox('Por favor, insira valores numéricos para altura e peso.', 'Erro', wx.OK | wx.ICON_ERROR)

            


def main():
    app = wx.App()
    WindowClass(None)
    app.MainLoop()
    con.close()

main()

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime

class TurbidityApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Monitor de Turbidez")
        self.geometry("800x800") 

        ctk.set_appearance_mode("light")  

        self.__label_titulo = ctk.CTkLabel(self, text='Monitoramento do Fotobiorreator', font=('Open Sans', 20))
        self.__label_titulo.pack(pady=20)

        self.__load_button = ctk.CTkButton(self, text="Carregar Dados", command=self.carregar_dados)
        self.__load_button.pack(pady=10)

        self.__calc_co2_window_button = ctk.CTkButton(self, text="Abrir Calculadora de CO2", command=self.abrir_janela_calculo_co2)
        self.__calc_co2_window_button.pack(pady=10)

        self.__grafico_area = ctk.CTkFrame(self)
        self.__grafico_area.pack(pady=20, fill="both", expand=True)

    def carregar_dados(self) -> None:
        conn = sqlite3.connect('turbidity_data.db')
        cursor = conn.cursor()

        cursor.execute('SELECT date, turbidity FROM turbidity_data')
        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        if rows:
            datas, valores = zip(*rows)
            datas = [datetime.strptime(data, "%Y-%m-%d") for data in datas]

            self.plot_data(datas, valores)
        else:
            print("Nenhum dado encontrado no banco de dados.")

    def plot_data(self, datas, valores) -> None:
        for widget in self.__grafico_area.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots()

        ax.plot(datas, valores, marker='o', color='forestgreen', markersize=8, markerfacecolor='lightgreen', markeredgecolor='darkgreen')
        ax.set_title("Nível de Turbidez ao Longo do Tempo", fontsize=14, fontweight='bold', color='darkgreen')
        ax.set_xlabel("Tempo", fontsize=14, color='orange')
        ax.set_ylabel("Turbidez (NTU)", fontsize=14, color='orange')
        ax.grid(True)

        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.__grafico_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def abrir_janela_calculo_co2(self):
        self.__janela_calculo = ctk.CTkToplevel(self)
        self.__janela_calculo.title("Calculadora de CO₂")
        self.__janela_calculo.geometry("300x200")
        self.__janela_calculo.resizable(width=False, height=False)


        label_ntu = ctk.CTkLabel(self.__janela_calculo, text="Insira a turbidez (NTU):", font=('Open Sans', 14))
        label_ntu.pack(pady=10)

        self.__ntu_entry = ctk.CTkEntry(self.__janela_calculo, width=200)
        self.__ntu_entry.pack(pady=5)

        calc_button = ctk.CTkButton(self.__janela_calculo, text="Calcular CO2 Sequestrado", command=self.calcular_co2)
        calc_button.pack(pady=10)

        self.__co2_result_label = ctk.CTkLabel(self.__janela_calculo, text='', font=('Open Sans', 16))
        self.__co2_result_label.pack(pady=10)

    def calcular_co2(self) -> None:
        try:
            ntu = float(self.__ntu_entry.get())
        except ValueError:
            self.__co2_result_label.configure(text="Por favor, insira um valor numérico válido para NTU.")
            return

        co2_sequestrado = self.calcular_co2_sequestrado(ntu)

        self.__co2_result_label.configure(text=f"CO₂ sequestrado: {co2_sequestrado:.2f} g/L")

    def calcular_co2_sequestrado(self, ntu, k=0.01) -> float:
       
        biomassa = k * ntu  
        co2_sequestrado = (biomassa * 44) / 12  
        return co2_sequestrado

TurbidityApp().mainloop()

import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
from datetime import datetime
from db_config import DB_PATH, TABLE_NAME


class TurbidityApp(ctk.CTk):
    def __init__(self):
        super().__init__()  # Call parent class constructor
        
        self.title("Monitoramento de Turbidez")
        self.geometry("800x600")

        # Load button
        self.__load_button = ctk.CTkButton(
            self, 
            text="Carregar Dados", 
            command=self.carregar_dados  # Method binding is correct now
        )
        self.__load_button.pack(pady=10)

        # CO2 calculator button
        self.__calc_co2_window_button = ctk.CTkButton(
            self, 
            text="Abrir Calculadora de CO2", 
            command=self.abrir_janela_calculo_co2
        )
        self.__calc_co2_window_button.pack(pady=10)

        # Graph area
        self.__grafico_area = ctk.CTkFrame(self)
        self.__grafico_area.pack(pady=20, fill="both", expand=True)

    def carregar_dados(self):  # Changed to instance method
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute(f'SELECT date, turbidity FROM {TABLE_NAME}')
            rows = cursor.fetchall()

            if rows:
                datas, valores = zip(*rows)
                datas = [datetime.strptime(data, "%d/%m/%Y") for data in datas]
                self.plot_data(datas, valores)
            else:
                print("Nenhum dado encontrado no banco de dados.")

        except sqlite3.Error as e:
            print(f"Erro ao carregar dados: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    def plot_data(self, datas, valores):
        # Clear previous plot
        for widget in self.__grafico_area.winfo_children():
            widget.destroy()

        # Create new plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot the data
        ax.plot(datas, valores, marker='o', linestyle='-', color='b')

        # Configure x-axis with proper scaling
        ax.set_xlim([min(datas), max(datas)])
        ax.set_xticks(datas)  # Show each date as a tick
        ax.xaxis.set_major_formatter(plt.FixedFormatter([d.strftime("%d/%m/%Y") for d in datas]))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha="right")

        # Set labels and title
        ax.set_xlabel('Data')
        ax.set_ylabel('Turbidez (NTU)')
        ax.set_title('Histórico de Turbidez')

        # Add grid for better readability
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)

        # Add plot to Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=self.__grafico_area)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

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


if __name__ == "__main__":
    app = TurbidityApp()
    app.mainloop()
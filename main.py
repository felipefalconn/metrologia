import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
from statistics import mean, pstdev
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BlocoPadraoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bloco Padrão")
        self.background('#FFFFFF')
        self.data = {}
        
        self.label = tk.Label(root, text="Selecione um bloco padrão:")
        self.label.pack(pady=10)
        
        self.combo = ttk.Combobox(root, state="readonly")
        self.combo.pack(pady=10)
        self.combo.bind("<<ComboboxSelected>>", self.on_block_selected)
        
        self.text = tk.Text(root, height=10, width=50)
        self.text.pack(pady=10)
        
        self.figure = plt.Figure(figsize=(8, 6), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, root)
        self.canvas.get_tk_widget().pack()
        self.load_data()
    
    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if not file_path:
            return
        
        df = pd.read_excel(file_path)
        standard_blocks = list(df['Bloco Padrão'].unique())
        
        for c in standard_blocks:
            block_data = df[df['Bloco Padrão'] == c]['Medida'].tolist()
            block_mean = mean(block_data)
            block_trend = c - block_mean
            block_stdev = pstdev(block_data)
            
            self.data[c] = {
                'Média': f'{block_mean:.3f}',
                'Tendência': block_trend,
                'Desvio Padrão': block_stdev,
                'Repetibilidade': 2.365 * block_stdev,
                'Medidas': block_data
            }
        
        self.combo['values'] = standard_blocks
    
    def on_block_selected(self, event):
        selected_block = float(self.combo.get())
        if selected_block in self.data:
            block_info = self.data[selected_block]
            self.text.delete(1.0, tk.END)
            self.text.insert(tk.END, f"Média: {block_info['Média']}\n")
            self.text.insert(tk.END, f"Tendência: {block_info['Tendência']:.3f}\n")
            self.text.insert(tk.END, f"Desvio Padrão: {block_info['Desvio Padrão']:.3f}\n")
            self.text.insert(tk.END, f"Repetibilidade: {block_info['Repetibilidade']:.3f}\n")
            
            self.plot_data(block_info['Medidas'])
            
    def plot_data(self, measures):
        selected_block = float(self.combo.get())
        self.ax.clear()
        x_values = list(range(1, len(measures) + 1))  
        self.ax.plot(x_values, measures, marker='o')  
        self.ax.set_title(f"Medidas para {selected_block:.3f} mm")
        self.ax.set_xlabel("Índice")
        self.ax.set_ylabel("Medida")

        self.ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.3f'))

        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlocoPadraoApp(root)
    root.mainloop()
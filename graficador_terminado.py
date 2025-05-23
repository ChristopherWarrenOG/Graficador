import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GrafficadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('Graficador de Funciones')
        self.root.geometry('1000x600')

        #Iniciar Variables para evitar crasheos
        self.equation = tk.StringVar(value='x')
        self.title = tk.StringVar(value='Grafica')
        self.color = tk.StringVar(value='blue')
        self.v_min = tk.DoubleVar(value=-10)
        self.v_max = tk.DoubleVar(value=10)
        self.puntos = tk.IntVar(value=100)
        self.x_label = tk.StringVar(value='x')
        self.y_label = tk.StringVar(value='y')

        self.create_widgets()
    
    def create_widgets(self):
        #Frame principal
        main_frame = ttk.Frame(self.root, padding='10')
        main_frame.pack(fill=tk.BOTH, expand=True)

        #Frame de controles left
        control_frame = ttk.LabelFrame(main_frame, text='Parametros', padding='10')
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        #Frame de grafica right
        graph_frame = ttk.LabelFrame(main_frame, text='Grafica', padding='10')
        graph_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        #Controles de entrada
        ttk.Label(control_frame, text='Ecuacion en funcion de x: ').grid(row=0, column=0, sticky=tk.W, pady=2)
        equation_entry = ttk.Entry(control_frame, textvariable=self.equation, width=25)
        equation_entry.grid(row=0, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Titulo: ').grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.title).grid(row=1, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Color (Ex: red, blue, green, etc.): ').grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.color).grid(row=2, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Valor minimo de x: ').grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.v_min).grid(row=3, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Valor maximo de x: ').grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.v_max).grid(row=4, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Numero de puntos: ').grid(row=5, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.puntos).grid(row=5, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Etiqueta eje X: ').grid(row=6, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.x_label).grid(row=6, column=1, pady=2, padx=5)

        ttk.Label(control_frame, text='Etiqueta eje Y: ').grid(row=7, column=0, sticky=tk.W, pady=2)
        ttk.Entry(control_frame, textvariable=self.y_label).grid(row=7, column=1, pady=2, padx=5)

        #Boton para graficar
        ttk.Button(control_frame, text='Generar Gráfica', command=self.graficar).grid(row=8, column=0, columnspan=2, pady=15)

        #Area para la grafica
        self.figure = plt.Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=graph_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        #Ejemplos de ecuaciones
        examples_frame = ttk.LabelFrame(control_frame, text='Ejemplos', padding='10')
        examples_frame.grid(row=9, column=0, columnspan=2, pady=10, sticky=tk.W)

        examples = [
            'x**2',
            'np.sin(x)',
            'np.cos(x)',
            'np.exp(x)',
            'np.sqrt(x)',
            'x**3 - 2*x + 5',
        ]

        for i, example in enumerate(examples):
            ttk.Button(examples_frame, text=example, width=20, command=lambda e=example: self.equation.set(e)).grid(row=i, column=0, pady=2)

    def graficar(self):
        try:
            #Crear el dominio
            x = np.linspace(self.v_min.get(), self.v_max.get(), self.puntos.get())

            #Funciones permitidas
            allowed_funcs = {
                'sin' : np.sin, 'cos' : np.cos, 'tan' : np.tan, 'log' : np.log,
                'exp' : np.exp, 'sqrt' : np.sqrt, 'abs' : np.abs, 'pi' : np.pi, 
                'e' : np.e, 'np' : np #Poder usar np como prefijo
            }

            #Evaluar la funcion
            y = eval(self.equation.get(), {'__builtins__': {}}, {**allowed_funcs, 'x' : x})

            #Limpiar figura anterior
            self.figure.clear()

            #Crear nueva grafica
            ax = self.figure.add_subplot(111)
            ax.plot(x, y, color=self.color.get())
            ax.set_title(f'Grafica de: {self.title.get()}')
            ax.set_xlabel(self.x_label.get())
            ax.set_ylabel(self.y_label.get())
            ax.grid(True)
            ax.axhline(0, color='black', linewidth = 0.5)
            ax.axvline(0, color='black', linewidth=0.5)

            #Actualizar canvas
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror('Error', f'Error al graficar la ecuacion:\n{str(e)}')

if __name__ == '__main__':
    root = tk.Tk()
    app = GrafficadorApp(root)
    root.mainloop()
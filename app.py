from tkinter import *  
from tkinter import ttk  
import customtkinter as ctk  

from ventana_resumen import VentanaResumen  
from ventana_stock import VentanaStock 
from ventana_entradas import VentanaEntradas  
from ventana_salida import VentanaSalidas  
from con_database import *  

# NOMBRE EMPRESA: HAWK  
# RUBRO: INDUMENTARIA Y CALZADO  

# PARA EL FUNCIONAMIENTO CORRECTO DEL CODIGO ES NECESARIO INSTALAR LAS SIGUIENTES LIBRERIAS.
# pip install customtkinter barcode pillow python-barcode tkcalendar awesometkinter

class Application:  
    ''' 
    Constructor de la clase Application 
    Parámetros: 
    self: necesario para todos los métodos, hace referencia a la instancia de la clase
    '''  
    def __init__(self):  
        ''' 
        Método que inicializa la aplicación principal y configura los componentes de la interfaz gráfica
        '''  
        self.root = ctk.CTk()  # Crea la ventana principal utilizando customtkinter  
        
        self.layout_config()  # Configura el layout de la ventana  
        self.menu_bar()  # Método comentado que añade una barra de menú  (funcion para futuro, sirve para cambiar de blanco a negro y demas, pero hay que tener cuidado  porque si lo apretas muchas veces deja de funcionar, es una funcion admin)
        self.tabs_application()  # Inicializa las pestañas de la aplicación  

        self.root.mainloop()  # Inicia el bucle principal de la aplicación para mantener la ventana abierta  

    def layout_config(self):  
        ''' 
        Configuración del layout de la ventana principal 
        Se define el título, tamaño y si es redimensionable 
        '''  
        self.root.title("Administrador de Stock")  
        x = (self.root.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.root.winfo_screenheight() // 2) - (630 // 2)
        self.root.geometry(f"1000x630+{x}+{y}")
        self.root.resizable(False, False)  

    def menu_bar(self):  
        ''' 
        Método para crear una barra de menú 
        Añade opciones como "Editar" y "Configuración" 
        '''  
        menu_bar = Menu(self.root)  # Crea la barra de menú  
        self.root.configure(menu=menu_bar)  # Asigna la barra de menú a la ventana principal  
        edite = Menu(menu_bar)  # Crea un submenú para las opciones de edición  
        
        menu_bar.add_cascade(label="Editar", menu=edite)  # Añade el submenú "Editar"  
        edite.add_command(label="Configuración", command=WindowConfig)  # Añade la opción "Configuración" que abre una nueva ventana  

    def tabs_application(self):  
        ''' 
        Método que crea las pestañas principales de la aplicación 
        Se añaden las pestañas "Resumen", "Productos y Stock", "Entradas" y "Salidas" 
        '''  
        self.tabs_view = ctk.CTkTabview(self.root,  
                                        width=1000, height=600,  
                                        anchor="w",  
                                        text_color=('#000', '#FFF'))  # Crea un widget para gestionar las pestañas  
        self.tabs_view.pack()  # Empaqueta el widget de pestañas para que se muestre en la ventana  

        self.tabs_view.add("Resumen")  # Añade la pestaña "Resumen"  
        VentanaResumen(self.tabs_view.tab("Resumen"))  # Inicializa el contenido de la pestaña "Resumen"  

        self.tabs_view.add("Productos y Stock")  # Añade la pestaña "Productos y Stock"  
        VentanaStock(self.tabs_view.tab("Productos y Stock"))  # Inicializa el contenido de la pestaña "Productos y Stock"  

        self.tabs_view.add("Entradas")  # Añade la pestaña "Entradas"  
        VentanaEntradas(self.tabs_view.tab("Entradas"))  # Inicializa el contenido de la pestaña "Entradas"  
        
        self.tabs_view.add("Salidas")  # Añade la pestaña "Salidas"  
        VentanaSalidas(self.tabs_view.tab("Salidas"))  # Inicializa el contenido de la pestaña "Salidas"  

        self.tabs_view.set("Resumen")  # Establece "Resumen" como la pestaña seleccionada por defecto  

class WindowConfig(ctk.CTkToplevel):  
    ''' 
    Constructor de la clase WindowConfig 
    Crea una ventana independiente para la configuración de la aplicación 
    Parámetros: 
    self: necesario para todos los métodos, hace referencia a la instancia de la clase 
    '''  
    def __init__(self):  
        ''' 
        Método que inicializa la ventana de configuración 
        '''  
        super().__init__()  # Llama al constructor de la clase padre  
        
        self.layout_config()  # Configura el layout de la ventana  
        self.appearance_theme()  # Configura el tema de apariencia  
        self.confirm_config()  # Configura el botón de confirmación de cambios  

    def layout_config(self):  
        ''' 
        Método que configura el layout de la ventana de configuración 
        Define el tamaño mínimo y máximo de la ventana 
        '''  
        self.geometry("300x400")  # Tamaño de la ventana de configuración  
        self.minsize(300, 400)  # Tamaño mínimo de la ventana  
        self.maxsize(300, 400)  # Tamaño máximo de la ventana  
        self.focus()
        self.grab_set()
    
    def appearance_theme(self):
        ''' 
        Método para configurar el tema de apariencia de la aplicación 
        Permite seleccionar entre los temas "System", "Light" y "Dark"
        '''
        ctk.set_default_color_theme("dark-blue")  # Establece el tema de color por defecto
        ctk.set_appearance_mode("system")  # Establece el modo de apariencia basado en el sistema

        ctk.CTkLabel(self, text="Tema",  
                     font=("Cascadia Code", 15, "bold")
                     ).place(x=50, y=50)  # Crea una etiqueta para el selector de tema y la coloca en la ventana
        
        ctk.CTkOptionMenu(self, width=90, height=20,  
                          values=['System', 'Light', 'Dark'],  
                          font=("Cascadia Code", 15),  
                          command=ctk.set_appearance_mode  
                          ).place(x=50, y=100)  # Crea un menú desplegable para seleccionar el tema y lo coloca en la ventana
    
    def confirm_config(self):
        ''' 
        Método que configura los botones para aplicar o cancelar los cambios de configuración 
        '''
        ctk.CTkButton(self, text="APLICAR",  
                      width=75,  
                      font=("Cascadia Code", 15, "bold"),  
                      command=None  # Aquí se debería agregar la lógica para aplicar los cambios  
                      ).place(x=100, y=360)  # Botón para aplicar los cambios, colocado en la parte inferior de la ventana
        
        ctk.CTkButton(self, text="CANCELAR",  
                      width=75,  
                      font=("Cascadia Code", 15, "bold"),  
                      command=self.destroy  # Cierra la ventana de configuración  
                      ).place(x=185, y=360)  # Botón para cancelar y cerrar la ventana
    

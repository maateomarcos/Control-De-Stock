from tkinter import *
from tkinter import ttk
import customtkinter as ctk
from datetime import date
from datetime import datetime

from con_database import *
from functions_base import *


class FunctionsResumen(Database):

    def select_database(self, query_sql, view_target):
        view_target.delete(*view_target.get_children())

        data_return = Database().dql_database(query_sql)
        for dados in data_return:
            view_target.insert("", END, values=dados)

    def filter_todos(self, Resumen=False):
        query_select = """
            SELECT 
                id, producto, grupo, medida, lote, stock, 
                valor_stock, fecha_entrada, status, barcode
            FROM 
                stock
        """
        data_return = Database().dql_database(query_select)

        if Resumen:
            self.total_itens = len(data_return)
            for dados in data_return:
                self.valor_itens += dados[6]
        else:
            for dados in data_return:
                self.lista_todos.insert("", END, values=dados)
    
    def search_todos(self):
        self.lista_todos.delete(*self.lista_todos.get_children())
        
        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":
                
                sql = """
                    SELECT
                        id, producto, grupo, medida, lote, stock, 
                        valor_stock, fecha_entrada, status, barcode
                    FROM
                        stock
                """
        else:
            if self.busca.get():
                buscar = f"""
                    producto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%' 
                    OR barcode LIKE '%{self.busca.get()}%'
                """
            
            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"
            
            elif self.busca_status_listBox.get():
                buscar = f"status LIKE '%{self.busca_status_listBox.get()}%' ORDER BY stock DESC"
        
            sql = f"""
                SELECT
                    id, producto, grupo, medida, lote, stock, 
                    valor_stock, fecha_entrada, status, barcode
                FROM
                    stock
                WHERE
                    {buscar}
            """
            
        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                self.lista_todos.insert("", END, values=dados)
        
        self.clear_search()

    def filter_reponer(self, Resumen=False):
        query_select = """
            SELECT 
                id, status, producto, grupo, medida, lote, stock, 
                stock_mín, reponer, costo_unitario, costo_reponer, proveedor, barcode
            FROM 
                stock ORDER BY status DESC
        """
        data_return = Database().dql_database(query_select)

        for dados in data_return:
            if dados[6] <= dados[7]:
                if Resumen:
                    self.total_reponer += 1
                    self.valor_reponer += dados[9]
                else:
                    self.lista_reponer.insert("", END, values=dados)
    
    def search_reponer(self):
        self.lista_reponer.delete(*self.lista_reponer.get_children())

        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":

            sql = """
                    SELECT
                        id, status, producto, grupo, medida, lote, stock, 
                        stock_mín, reponer, costo_unitario, costo_reponer, proveedor, barcode
                    FROM
                        stock ORDER BY status DESC
                """
        else:
            if self.busca.get():
                buscar = f"""
                    producto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%'
                    OR barcode LIKE '%{self.busca.get()}%'
                """

            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"

            elif self.busca_status_listBox.get():
                buscar = f"status LIKE '%{self.busca_status_listBox.get()}%' ORDER BY stock DESC"

            sql = f"""
                SELECT
                    id, status, producto, grupo, medida, lote, stock,
                    stock_mín, reponer, costo_unitario, costo_reponer, proveedor, barcode
                FROM
                    stock
                WHERE
                    {buscar}
            """

        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                if dados[6] <= dados[7]:
                    self.lista_reponer.insert("", END, values=dados)
        
        self.clear_search()

    def filter_facturación(self, Resumen=False):
        query_select = """
            SELECT 
                id, fecha_salida, producto, grupo, medida, lote, 
                stock, salidas, valor_venta, facturación, status
            FROM 
                stock ORDER BY fecha_salida DESC
        """
        data_return = Database().dql_database(query_select)

        if Resumen:
            for dados in data_return:
                if dados[7] > 0:
                    self.total_movimentos += 1
                    self.valor_facturación += dados[9]
        else:
            for dados in data_return:
                if dados[7] > 0:
                    self.lista_facturación.insert("", END, values=dados)

    def search_facturación(self):
        self.lista_facturación.delete(*self.lista_facturación.get_children())

        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":

            sql = """
                    SELECT
                        id, fecha_salida, producto, grupo, medida, lote, 
                        stock, salidas, valor_venta, facturación, status
                    FROM
                        stock ORDER BY fecha_salida DESC
                """
        else:
            if self.busca.get():
                buscar = f"""
                    producto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%'
                    OR barcode LIKE '%{self.busca.get()}%'
                """

            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"

            sql = f"""
                SELECT
                    id, fecha_salida, producto, grupo, medida, lote, 
                    stock, salidas, valor_venta, facturación, status
                FROM
                    stock
                WHERE
                    {buscar}
            """

        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                if dados[7] > 0:
                    self.lista_facturación.insert("", END, values=dados)

        self.clear_search()
    
    def filter_nuevos(self, Resumen=False):
        query_select = """
                SELECT 
                    id, fecha_entrada, producto, medida, lote, entradas, 
                    costo_unitario, costo_total, stock, status, grupo, proveedor
                FROM 
                    stock ORDER BY fecha_entrada DESC
            """
        data_return = Database().dql_database(query_select)

        for dados in data_return:
            if dados[1] == None or dados[1] == "":
                continue
            try:
            # Parsea la cadena de texto en formato dd/mm/yyyy y obtiene los valores enteros
                Fecha = datetime.strptime(dados[1], "%d/%m/%Y")
                año, mes, dia = Fecha.year, Fecha.month, Fecha.day

            except ValueError:

                continue                
            # entradas realizadas en los últimos 30 días
            data_atual = date.today()
            fecha_entrada = date(año, mes, dia)
            data_diferenca = data_atual - fecha_entrada            

            if Fecha.days <= 30:
                if Resumen:
                    self.total_nuevos += 1
                    self.valor_nuevos += dados[7]
                else:
                    self.lista_nuevos.insert("", END, values=dados)
    
    def search_nuevos(self):
        self.lista_nuevos.delete(*self.lista_nuevos.get_children())

        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":

            sql = """
                    SELECT
                        id, fecha_entrada, producto, medida, lote, entradas, 
                        costo_unitario, costo_total, stock, status, grupo, proveedor
                    FROM
                        stock ORDER BY fecha_entrada DESC
                """
        else:
            if self.busca.get():
                buscar = f"""
                    producto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%'
                    OR barcode LIKE '%{self.busca.get()}%'
                """

            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"

            sql = f"""
                SELECT
                    id, fecha_entrada, producto, medida, lote, entradas,
                    costo_unitario, costo_total, stock, status, grupo, proveedor
                FROM
                    stock
                WHERE
                    {buscar}
            """

        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                if dados[1] == None or dados[1] == "":
                    continue
                try:
                    # Analiza la cadena de texto en formato dd/mm/aaaa y obtener los valores ingresados
                    Fecha = datetime.strptime(dados[1], "%d/%m/%Y")
                    año, mes, dia = Fecha.year, Fecha.month, Fecha.day

                    # Buscar entradas realizadas en los últimos 30 días
                    data_atual = date.today()
                    fecha_entrada = date(año, mes, dia)
                    data_diferenca = data_atual - fecha_entrada

                    if data_diferenca.days <= 30:
                        self.lista_nuevos.insert("", END, values=dados)

                except ValueError:
                    continue

        self.clear_search()

    def filter_parados(self, Resumen=False):
        sql = """
            SELECT 
                id, fecha_salida, producto, lote, medida, salidas, 
                stock, valor_stock, grupo, proveedor
            FROM 
                stock ORDER BY fecha_salida DESC
        """
        data_return = Database().dql_database(sql)

        for dados in data_return:
            if dados[1] == None or dados[1] == "":
                continue
            
            try:
                # Analiza la cadena de texto en formato dd/mm/aaaa hh:mm:ss y obtiene los valores ingresados
                Fecha = datetime.strptime(dados[1], "%d/%m/%Y %H:%M:%S")
                año, mes, dia = Fecha.year, Fecha.month, Fecha.day

                # Búsqueda de salidas realizadas hace más de 90 días
                data_atual = datetime.now()
                fecha_salida = datetime(año, mes, dia, hour=0, minute=0, second=0)
                data_diferenca = data_atual - fecha_salida

                if data_diferenca.days >= 90:
                    if Resumen:
                        self.total_parados += 1
                        self.valor_parados += dados[7]
                    else:
                        self.lista_parados.insert("", END, values=dados)
            except ValueError:
                continue
                    
    def search_parados(self):
        self.lista_parados.delete(*self.lista_parados.get_children())

        if self.busca.get() == "" \
            and self.busca_grupo_listBox.get() == "" \
                and self.busca_status_listBox.get() == "":

            sql = """
                    SELECT
                        id, fecha_salida, producto, lote, medida, salidas, 
                        stock, valor_stock, grupo, proveedor
                    FROM
                        stock ORDER BY fecha_salida DESC
                """
        else:
            if self.busca.get():
                buscar = f"""
                    producto LIKE '%{self.busca.get()}%'
                    OR lote LIKE '%{self.busca.get()}%'
                    OR barcode LIKE '%{self.busca.get()}%'
                """

            elif self.busca_grupo_listBox.get():
                buscar = f"grupo LIKE '%{self.busca_grupo_listBox.get()}%' ORDER BY id"

            sql = f"""
                SELECT
                    id, fecha_salida, producto, lote, medida, salidas, 
                    stock, valor_stock, grupo, proveedor
                FROM
                    stock
                WHERE
                    {buscar}
            """

        data_return = Database().dql_database(sql)
        if data_return is not None:
            for dados in data_return:
                if dados[1] == None or dados[1] == "":
                    continue
                
                try:
                    Fecha = datetime.strptime(dados[1], "%d/%m/%Y %H:%M:%S")
                    año, mes, dia = Fecha.year, Fecha.month, Fecha.day

                    data_atual = datetime.now()
                    fecha_salida = datetime(año, mes, dia, hour=0, minute=0, second=0)
                    data_diferenca = data_atual - fecha_salida

                    if data_diferenca.days >= 90:
                        self.lista_parados.insert("", END, values=dados)

                except ValueError:
                    continue

        self.clear_search()
    
    def clear_search(self):
        try:
            self.busca.delete(0, END)
            self.busca.configure(placeholder_text="Buscar Producto, Nº Lote, Código de Barras")
            self.busca_grupo_listBox.set("")
            self.busca_status_listBox.set("")
            self.busca_mes.delete(0, END)
            self.busca_mes.configure(placeholder_text="Mes")
            self.busca_año.delete(0, END)
            self.busca_año.configure(placeholder_text="Año")
            self.busca_facturación.set("")
        except:
            pass


class VentanaResumen(FunctionsResumen, FunctionsExtras):
    def __init__(self, root):
        self.root = root

        self.widgets_top()
        self.views_todos()

    def widgets_top(self):
        ctk.CTkLabel(self.root, text="Analisis de Stock",
                     font=("Constantia", 25), text_color=("#1C1C1C", "#D3D3D3")
                     ).place(x=20, y=10)

        self.frame_top = ctk.CTkFrame(self.root, width=985, height=75)
        self.frame_top.place(x=1, y=50)

        self.total_itens = 0
        self.valor_itens = 0
        self.filter_todos(Resumen=True)
        todos = f"TODOS \n{self.total_itens} productos\n$ {self.valor_itens:.2f}"

        self.total_reponer = 0
        self.valor_reponer = 0
        self.filter_reponer(Resumen=True)
        reponer = f"REPONER \n{self.total_reponer} productos\n$ {self.valor_reponer:.2f}"

        self.total_movimentos = 0
        self.valor_facturación = 0
        self.filter_facturación(Resumen=True)
        facturación = f"FACTURACIÓN \n{self.total_movimentos} productos\n$ {self.valor_facturación:.2f}"

        self.total_nuevos = 0
        self.valor_nuevos = 0
        self.filter_nuevos(Resumen=True)
        nuevos = f"NUEVOS \n{self.total_nuevos} productos\n$ {self.valor_nuevos:.2f}"

        self.total_parados = 0
        self.valor_parados = 0
        self.filter_parados(Resumen=True)
        parados = f"PARADOS \n{self.total_parados} productos\n$ {self.valor_parados:.2f}"

        ctk.CTkButton(self.frame_top, text=todos,
                      width=175, 
                      font=("Cascadia Code", 15),
                      fg_color="#000080",
                      command=self.views_todos).grid(column=0, row=0)
        ctk.CTkButton(self.frame_top, text=reponer, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#FF4500",
                      command=self.view_reponer).grid(column=1, row=0, padx=10)
        ctk.CTkButton(self.frame_top, text=facturación, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#FFD700",
                      command=self.view_facturación).grid(column=2, row=0)
        ctk.CTkButton(self.frame_top, text=nuevos, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#32CD32",
                      command=self.view_nuevos).grid(column=3, row=0, padx=10)
        ctk.CTkButton(self.frame_top, text=parados, 
                      width=175, 
                      font=("Cascadia Code", 15, "bold"), text_color="#4F4F4F",
                      fg_color="#D8BFD8",
                      command=self.view_parados).grid(column=4, row=0)

        ctk.CTkButton(self.frame_top, text="",
                      width=50,
                      image=self.image_button("actualizar.png", (34, 34)),  
                      compound=LEFT, anchor=NW, 
                      fg_color="transparent", 
                      hover_color=("#D3D3D3", "#363636"),
                      command=self.widgets_top).grid(column=5, row=0, padx=10)

    def views_todos(self):
        self.frame_todos = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_todos.place(x=0, y=125)

        ctk.CTkLabel(self.frame_todos, text="Seguimiento de productos registrados!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_todos, text="Producto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_todos,
                                  width=350,
                                  placeholder_text="Buscar Producto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM stock", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_todos, 
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Status",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        lista_status = ['OK', 'VACIO', 'CRÍTICO']
        self.busca_status_listBox = ctk.CTkComboBox(self.frame_todos, 
                                                    width=100,
                                                    values=lista_status,
                                                    font=("Cascadia Code", 13))
        self.busca_status_listBox.set("")
        self.busca_status_listBox.place(x=575, y=75)
        
        ctk.CTkLabel(self.frame_todos, text="Fecha",
                     font=("Cascadia Code", 13)).place(x=685, y=50)
        self.busca_mes = ctk.CTkEntry(self.frame_todos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mes",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=685, y=75)
        ctk.CTkLabel(self.frame_todos, text="/",
                     font=("Cascadia Code", 20, "bold"), text_color="#A9A9A9",
                     ).place(x=735, y=75)
        self.busca_año = ctk.CTkEntry(self.frame_todos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Año",
                                      font=("Cascadia Code", 13))
        self.busca_año.place(x=748, y=75)
        
        ctk.CTkButton(self.frame_todos, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_todos).place(x=820, y=75)

        ctk.CTkButton(self.frame_todos, text="LIMPIAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=890, y=75)
        # ---------------------------------------------------------------------------------------
        
        self.lista_todos = ttk.Treeview(self.frame_todos, height=3, column=(
            'id', 'producto', 'grupo', 'medida', 'lote', 
            'stock', 'valor', 'Fecha', 'status', 'barcode'
        ))
        
        self.lista_todos.heading("#0", text="")
        self.lista_todos.heading("id", text="Cód.")
        self.lista_todos.heading("producto", text="Producto")
        self.lista_todos.heading("grupo", text="Departamento")
        self.lista_todos.heading("medida", text="Medida")
        self.lista_todos.heading("lote", text="Nº Lote")
        self.lista_todos.heading("stock", text="stock")
        self.lista_todos.heading("valor", text="Valor stock")
        self.lista_todos.heading("Fecha", text="Últ.Registro")
        self.lista_todos.heading("status", text="Status")
        self.lista_todos.heading("barcode", text="Código de Barras")

        self.lista_todos.column("#0", width=0, stretch=False)
        self.lista_todos.column("id", width=30, anchor=CENTER)
        self.lista_todos.column("producto", width=270)
        self.lista_todos.column("grupo", width=125)
        self.lista_todos.column("medida", width=85, anchor=CENTER)
        self.lista_todos.column("lote", width=50, anchor=CENTER)
        self.lista_todos.column("stock", width=50, anchor=CENTER)
        self.lista_todos.column("valor", width=80, anchor=CENTER)
        self.lista_todos.column("Fecha", width=75, anchor=CENTER)
        self.lista_todos.column("status", width=70, anchor=CENTER)
        self.lista_todos.column("barcode", width=100, anchor=CENTER)

        self.lista_todos.place(y=110, width=970, height=315)

        scrollbar = ttk.Scrollbar(self.frame_todos, 
                                  orient="vertical", 
                                  command=self.lista_todos.yview)
        self.lista_todos.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=110, width=20, height=315)

        self.filter_todos()

    def view_reponer(self):
        self.frame_reponer = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_reponer.place(x=0, y=125)

        ctk.CTkLabel(self.frame_reponer, text="¡Recomendaciones de productos para reposición de stock!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_reponer, text="Producto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_reponer,
                                  width=350,
                                  placeholder_text="Buscar Producto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)
        
        ctk.CTkLabel(self.frame_reponer, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM stock", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_reponer, 
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_reponer, text="Status",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        lista_status = ['VACIO', 'CRÍTICO']
        self.busca_status_listBox = ctk.CTkComboBox(self.frame_reponer, 
                                                    width=100,
                                                    values=lista_status,
                                                    font=("Cascadia Code", 13))
        self.busca_status_listBox.set("")
        self.busca_status_listBox.place(x=575, y=75)
        
        ctk.CTkButton(self.frame_reponer, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_reponer).place(x=700, y=75)
        
        ctk.CTkButton(self.frame_reponer, text="LIMPIAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=770, y=75)
        # ---------------------------------------------------------------------------------------
        
        self.lista_reponer = ttk.Treeview(self.frame_reponer, height=3, column=(
            'id', 'status', 'producto', 'grupo', 'medida', 'lote', 'stock', 
            'mín', 'reponer', 'costo', 'total', 'proveedor', 'barcode'
        ))
        self.lista_reponer.heading("#0", text="")
        self.lista_reponer.heading("id", text="Cód.")
        self.lista_reponer.heading("status", text="Status")
        self.lista_reponer.heading("producto", text="Producto")
        self.lista_reponer.heading("grupo", text="Departamento")
        self.lista_reponer.heading("medida", text="Medida")
        self.lista_reponer.heading("lote", text="Nº Lote")
        self.lista_reponer.heading("stock", text="stock")
        self.lista_reponer.heading("mín", text="Est.Mín")
        self.lista_reponer.heading("reponer", text="reponer")
        self.lista_reponer.heading("costo", text="costo Unit.")
        self.lista_reponer.heading("total", text="costo Total")
        self.lista_reponer.heading("proveedor", text="proveedor")
        self.lista_reponer.heading("barcode", text="Código de Barras")

        self.lista_reponer.column("#0", width=0, stretch=False)
        self.lista_reponer.column("id", width=35, anchor=CENTER)
        self.lista_reponer.column("status", width=70, anchor=CENTER)
        self.lista_reponer.column("producto", width=270)
        self.lista_reponer.column("grupo", width=125)
        self.lista_reponer.column("medida", width=85, anchor=CENTER)
        self.lista_reponer.column("lote", width=50, anchor=CENTER)
        self.lista_reponer.column("stock", width=50, anchor=CENTER)
        self.lista_reponer.column("mín", width=50, anchor=CENTER)
        self.lista_reponer.column("reponer", width=50, anchor=CENTER)
        self.lista_reponer.column("costo", width=80, anchor=CENTER)
        self.lista_reponer.column("total", width=80, anchor=CENTER)
        self.lista_reponer.column("proveedor", width=150)
        self.lista_reponer.column("barcode", width=100, anchor=CENTER)

        self.lista_reponer.place(y=110, width=970, height=315)

        scrollbar_y = ttk.Scrollbar(self.frame_reponer,
                                    orient="vertical",
                                    command=self.lista_reponer.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_reponer,
                                    orient="horizontal",
                                    command=self.lista_reponer.xview)
        self.lista_reponer.configure(yscrollcommand=scrollbar_y.set, 
                                   xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=110, width=20, height=315)
        scrollbar_x.place(x=0, y=410, width=970, height=15)

        self.filter_reponer()

    def view_facturación(self):
        self.frame_facturación = ctk.CTkFrame(self.root,
                                             width=990, height=425,
                                             fg_color="#363636")
        self.frame_facturación.place(x=0, y=125)

        ctk.CTkLabel(self.frame_facturación, text="¡Registros de salidas realizadas en los últimos 30 días!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_facturación, text="Producto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_facturación,
                                  width=350,
                                  placeholder_text="Buscar Producto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)

        ctk.CTkLabel(self.frame_facturación, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM stock", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_facturación,
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_facturación, text="salidas",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        lista_facturación = ["Mayor Valor", "Menor Valor", "Mayor cnt", "Menor cnt"]
        self.busca_facturación = ctk.CTkComboBox(self.frame_facturación,
                                                 width=125,
                                                 values=lista_facturación,
                                                 font=("Cascadia Code", 13))
        self.busca_facturación.set("")
        self.busca_facturación.place(x=575, y=75)

        ctk.CTkLabel(self.frame_facturación, text="Fecha",
                     font=("Cascadia Code", 13)).place(x=705, y=50)
        self.busca_mes = ctk.CTkEntry(self.frame_facturación,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mes",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=710, y=75)
        ctk.CTkLabel(self.frame_facturación, text="/",
                     font=("Cascadia Code", 20, "bold"), text_color="#A9A9A9",
                     ).place(x=760, y=75)
        self.busca_año = ctk.CTkEntry(self.frame_facturación,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="año",
                                      font=("Cascadia Code", 13))
        self.busca_año.place(x=773, y=75)

        ctk.CTkButton(self.frame_facturación, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_facturación).place(x=837, y=75)

        ctk.CTkButton(self.frame_facturación, text="LIMPIAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=907, y=75)
        # ---------------------------------------------------------------------------------------
        
        self.lista_facturación = ttk.Treeview(self.frame_facturación, height=3, column=(
            'id', 'Fecha', 'producto', 'grupo', 'medida', 'lote', 'stock', 
            'salidas', 'reventa', 'facturación', 'status'
        ))
        self.lista_facturación.heading("#0", text="")
        self.lista_facturación.heading("id", text="Cód.")
        self.lista_facturación.heading("Fecha", text="Fecha Salida")
        self.lista_facturación.heading("producto", text="Producto")
        self.lista_facturación.heading("grupo", text="Departamento")
        self.lista_facturación.heading("medida", text="Medida")
        self.lista_facturación.heading("lote", text="Nº Lote")
        self.lista_facturación.heading("stock", text="stock")
        self.lista_facturación.heading("salidas", text="salidas")
        self.lista_facturación.heading("reventa", text="Valor Salida")
        self.lista_facturación.heading("facturación", text="facturación")
        self.lista_facturación.heading("status", text="Status")

        self.lista_facturación.column("#0", width=0, stretch=False)
        self.lista_facturación.column("id", width=30, anchor=CENTER)
        self.lista_facturación.column("Fecha", width=75, anchor=CENTER)
        self.lista_facturación.column("producto", width=270)
        self.lista_facturación.column("grupo", width=125)
        self.lista_facturación.column("medida", width=85, anchor=CENTER)
        self.lista_facturación.column("lote", width=50, anchor=CENTER)
        self.lista_facturación.column("stock", width=50, anchor=CENTER)
        self.lista_facturación.column("salidas", width=50, anchor=CENTER)
        self.lista_facturación.column("reventa", width=80, anchor=CENTER)
        self.lista_facturación.column("facturación", width=80, anchor=CENTER)
        self.lista_facturación.column("status", width=70, anchor=CENTER)

        self.lista_facturación.place(y=110, width=970, height=315)

        scrollbar = ttk.Scrollbar(self.frame_facturación,
                                  orient="vertical",
                                  command=self.lista_facturación.yview)
        self.lista_facturación.configure(yscrollcommand=scrollbar.set)
        scrollbar.place(x=970, y=110, width=20, height=315)

        self.filter_facturación()

    def view_nuevos(self):
        self.frame_nuevos = ctk.CTkFrame(self.root,
                                        width=990, height=425,
                                        fg_color="#363636")
        self.frame_nuevos.place(x=0, y=125)

        ctk.CTkLabel(self.frame_nuevos, text="¡Registros de entradas realizadas en los últimos 30 días!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_nuevos, text="Producto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_nuevos,
                                  width=350,
                                  placeholder_text="Buscar Producto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)

        ctk.CTkLabel(self.frame_nuevos, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM stock", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_nuevos,
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)
        
        ctk.CTkLabel(self.frame_nuevos, text="Fecha",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        self.busca_mes = ctk.CTkEntry(self.frame_nuevos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mes",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=575, y=75)
        ctk.CTkLabel(self.frame_nuevos, text="/",
                     font=("Cascadia Code", 20, "bold"), text_color="#A9A9A9",
                     ).place(x=625, y=75)
        self.busca_año = ctk.CTkEntry(self.frame_nuevos,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="año",
                                      font=("Cascadia Code", 13))
        self.busca_año.place(x=638, y=75)

        ctk.CTkButton(self.frame_nuevos, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_nuevos).place(x=710, y=75)

        ctk.CTkButton(self.frame_nuevos, text="LIMPIAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=780, y=75)
        # ---------------------------------------------------------------------------------------
        
        self.lista_nuevos = ttk.Treeview(self.frame_nuevos, height=3, column=(
            'id', 'Fecha', 'producto', 'medida', 'lote', 'entrada', 'costo',
            'total', 'stock', 'status', 'grupo', 'proveedor'
        ))
        self.lista_nuevos.heading("#0", text="")
        self.lista_nuevos.heading("id", text="Cód.")
        self.lista_nuevos.heading("Fecha", text="Fecha Registro")
        self.lista_nuevos.heading("producto", text="Producto")
        self.lista_nuevos.heading("medida", text="Medida")
        self.lista_nuevos.heading("lote", text="Nº Lote")
        self.lista_nuevos.heading("entrada", text="Entrada")
        self.lista_nuevos.heading("costo", text="costo Unit.")
        self.lista_nuevos.heading("total", text="costo Total")
        self.lista_nuevos.heading("stock", text="stock")
        self.lista_nuevos.heading("status", text="Status")
        self.lista_nuevos.heading("grupo", text="Departamento")
        self.lista_nuevos.heading("proveedor", text="proveedor")

        self.lista_nuevos.column("#0", width=0, stretch=False)
        self.lista_nuevos.column("id", width=35, anchor=CENTER)
        self.lista_nuevos.column("Fecha", width=80, anchor=CENTER)
        self.lista_nuevos.column("producto", width=270)
        self.lista_nuevos.column("medida", width=85, anchor=CENTER)
        self.lista_nuevos.column("lote", width=60, anchor=CENTER)
        self.lista_nuevos.column("entrada", width=50, anchor=CENTER)
        self.lista_nuevos.column("costo", width=80, anchor=CENTER)
        self.lista_nuevos.column("total", width=80, anchor=CENTER)
        self.lista_nuevos.column("stock", width=50, anchor=CENTER)
        self.lista_nuevos.column("status", width=70, anchor=CENTER)
        self.lista_nuevos.column("grupo", width=125)
        self.lista_nuevos.column("proveedor", width=150)

        self.lista_nuevos.place(y=110, width=970, height=315)

        scrollbar_y = ttk.Scrollbar(self.frame_nuevos,
                                    orient="vertical",
                                    command=self.lista_nuevos.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_nuevos,
                                    orient="horizontal",
                                    command=self.lista_nuevos.xview)
        self.lista_nuevos.configure(yscrollcommand=scrollbar_y.set, 
                                   xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=110, width=20, height=315)
        scrollbar_x.place(x=0, y=410, width=970, height=15)

        self.filter_nuevos()

    def view_parados(self):
        self.frame_parados = ctk.CTkFrame(self.root,
                                          width=990, height=425,
                                          fg_color="#363636")
        self.frame_parados.place(x=0, y=125)

        ctk.CTkLabel(self.frame_parados, text="¡Seguimiento de Lotes sin salida por más de 90 días!",
                     font=("Cascadia Code", 13), text_color="#D3D3D3"
                     ).place(x=5, y=5)

        # FILTROS -------------------------------------------------------------------------------
        ctk.CTkLabel(self.frame_parados, text="Producto",
                     font=("Cascadia Code", 13)).place(x=5, y=50)
        self.busca = ctk.CTkEntry(self.frame_parados,
                                  width=350,
                                  placeholder_text="Buscar Producto, Nº Lote, Código de Barras",
                                  font=("Cascadia Code", 13))
        self.busca.place(x=5, y=75)

        ctk.CTkLabel(self.frame_parados, text="Departamento",
                     font=("Cascadia Code", 13)).place(x=365, y=50)
        lista_grupo = self.dql_database("SELECT grupo FROM stock", column_names=True)
        self.busca_grupo_listBox = ctk.CTkComboBox(self.frame_parados,
                                                   width=200,
                                                   values=lista_grupo,
                                                   font=("Cascadia Code", 13))
        self.busca_grupo_listBox.set("")
        self.busca_grupo_listBox.place(x=365, y=75)

        ctk.CTkLabel(self.frame_parados, text="Fecha",
                     font=("Cascadia Code", 13)).place(x=575, y=50)
        self.busca_mes = ctk.CTkEntry(self.frame_parados,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="Mes",
                                      font=("Cascadia Code", 13))
        self.busca_mes.place(x=575, y=75)
        ctk.CTkLabel(self.frame_parados, text="/",
                     font=("Cascadia Code", 20, "bold"), text_color="#A9A9A9",
                     ).place(x=625, y=75)
        self.busca_año = ctk.CTkEntry(self.frame_parados,
                                      width=50,
                                      justify=CENTER,
                                      placeholder_text="año",
                                      font=("Cascadia Code", 13))
        self.busca_año.place(x=638, y=75)

        ctk.CTkButton(self.frame_parados, text="BUSCAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.search_parados).place(x=710, y=75)

        ctk.CTkButton(self.frame_parados, text="LIMPIAR",
                      width=60,
                      font=("Cascadia Code", 13, "bold"),
                      fg_color="#696969",
                      hover_color=("#D3D3D3", "#1C1C1C"),
                      command=self.clear_search).place(x=780, y=75)
        # ---------------------------------------------------------------------------------------
        
        self.lista_parados = ttk.Treeview(self.frame_parados, height=3, column=(
            'id', 'Fecha', 'producto', 'lote', 'medida', 'Salida',
            'stock', 'valor', 'grupo', 'proveedor'
        ))
        self.lista_parados.heading("#0", text="")
        self.lista_parados.heading("id", text="Cód.")
        self.lista_parados.heading("Fecha", text="Fecha Salida")
        self.lista_parados.heading("producto", text="Producto")
        self.lista_parados.heading("lote", text="Nº Lote")
        self.lista_parados.heading("medida", text="Medida")
        self.lista_parados.heading("Salida", text="Salida")
        self.lista_parados.heading("stock", text="stock")
        self.lista_parados.heading("valor", text="Valor stock")
        self.lista_parados.heading("grupo", text="Departamento")
        self.lista_parados.heading("proveedor", text="proveedor")

        self.lista_parados.column("#0", width=0, stretch=False)
        self.lista_parados.column("id", width=35, anchor=CENTER)
        self.lista_parados.column("Fecha", width=75, anchor=CENTER)
        self.lista_parados.column("producto", width=270)
        self.lista_parados.column("lote", width=60, anchor=CENTER)
        self.lista_parados.column("medida", width=85, anchor=CENTER)
        self.lista_parados.column("Salida", width=50, anchor=CENTER)
        self.lista_parados.column("stock", width=50, anchor=CENTER)
        self.lista_parados.column("valor", width=80, anchor=CENTER)
        self.lista_parados.column("grupo", width=125)
        self.lista_parados.column("proveedor", width=150)

        self.lista_parados.place(y=110, width=970, height=315)

        scrollbar_y = ttk.Scrollbar(self.frame_parados,
                                    orient="vertical",
                                    command=self.lista_parados.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_parados,
                                    orient="horizontal",
                                    command=self.lista_parados.xview)
        self.lista_parados.configure(yscrollcommand=scrollbar_y.set, 
                                     xscrollcommand=scrollbar_x.set)
        scrollbar_y.place(x=970, y=110, width=20, height=315)
        scrollbar_x.place(x=0, y=410, width=970, height=15)

        self.filter_parados()

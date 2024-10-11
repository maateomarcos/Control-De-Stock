import customtkinter as ctk
from tkinter import IntVar, messagebox
import sqlite3 

from con_database import * 
from app import Application 
import json

# admin 
# gerente
# empleado

ctk.set_appearance_mode("System")  
create_table()

class Registro(ctk.CTk):
    def __init__(self):
        super().__init__()

        x = (self.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.winfo_screenheight() // 2) - (600 // 2)
        self.geometry(f"900x600+{x}+{y}")

        self.geometry("900x600")
        self.title("Login y Registro")
        self.resizable(False, False)

        self.login_frame = ctk.CTkFrame(self, fg_color="grey", corner_radius=15, border_width=2)
        self.register_frame = ctk.CTkFrame(self, width=300, height=450, corner_radius=15,
                                            border_width=2, border_color="black")


        self.show_login()

        self.database_conexion = sqlite3.connect("StockDatabase.db")
        self.cursor = self.database_conexion.cursor()

        localidades = [
            ("San Miguel", "Dirección 1", "123456789"),
            ("Parque San Martín", "Dirección 2", "987654321"),
            ("La Roca", "Dirección 3", "456789123")
        ]

        insert_query = "INSERT INTO sucursales (nombre_sucursal, direccion_sucursal, telefono_sucursal) VALUES (?, ?, ?)"
        self.cursor.executemany(insert_query, localidades)
        self.database_conexion.commit()

    def show_login(self):
        self.clear_frame()
        self.check_var = IntVar(value=0)

        self.login_frame.configure(width=300, height=400, fg_color="#F0F0F0", border_color="black") 
        self.login_frame.place(x=300, y=100)

        title_label = ctk.CTkLabel(self.login_frame, text="Login", font=("Arial", 20), text_color="#000000")  
        title_label.place(x=120, y=30)

        user_label = ctk.CTkLabel(self.login_frame, text="Usuario:", text_color="#404040")  
        user_label.place(x=50, y=80)
        self.user_entry = ctk.CTkEntry(self.login_frame, corner_radius=5, width=200, 
                                       font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000")  
        self.user_entry.place(x=50, y=110)

        password_label = ctk.CTkLabel(self.login_frame, text="Contraseña:", text_color="#404040")
        password_label.place(x=50, y=155)
        self.password_entry = ctk.CTkEntry(self.login_frame, show="*", corner_radius=5, 
                                           width=200, font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000")  
        self.password_entry.place(x=50, y=185)

        checkbox = ctk.CTkCheckBox(self.login_frame, text="Mantener la sesión abierta", 
                                   variable=self.check_var, onvalue=1, offvalue=0,fg_color="black", text_color="#404040", hover=False)
        checkbox.place(x=50, y=245)

        login_button = ctk.CTkButton(self.login_frame, text="Iniciar sesión", command=self.login, fg_color="#000000", text_color="#FFFFFF", hover_color="#404040")
        login_button.place(x=75, y=290)

        register_button = ctk.CTkButton(self.login_frame, text="Registrarse", command=self.show_register, fg_color="transparent", hover=False, text_color="#000000")
        register_button.place(x=70, y=350)


    def show_register(self):
        self.clear_frame()
        self.combo_value = ""

        self.register_frame.configure(fg_color="#F0F0F0")
        self.register_frame.place(x=300, y=75)

        title_label = ctk.CTkLabel(self.register_frame, text="Registro", font=("Arial", 20), text_color="#000000")
        title_label.place(relx=0.5, y=40, anchor="center") 

        name_label = ctk.CTkLabel(self.register_frame, text="Nombre:", text_color="#404040")
        name_label.place(x=50, y=70)
        self.name_entry = ctk.CTkEntry(self.register_frame, corner_radius=5, width=200, font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000")
        self.name_entry.place(x=50, y=100)

        user_label = ctk.CTkLabel(self.register_frame, text="Usuario:", text_color="#404040")
        user_label.place(x=50, y=135)
        self.user_entry = ctk.CTkEntry(self.register_frame, corner_radius=5, width=200, font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000")
        self.user_entry.place(x=50, y=165)

        branch_label = ctk.CTkLabel(self.register_frame, text="Sucursal:", text_color="#404040")
        branch_label.place(x=50, y=200)
        self.branch_entry = ctk.CTkComboBox(self.register_frame, values=["San Miguel", "Parque San Martín", "La Roca"], 
                                            corner_radius=5, width=200, font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000",
                                            command=self.combobox_callback)
        self.branch_entry.place(x=50, y=230)

        password_label = ctk.CTkLabel(self.register_frame, text="Contraseña:", text_color="#404040")
        password_label.place(x=50, y=265)
        self.password_entry = ctk.CTkEntry(self.register_frame, show="*", corner_radius=5, width=200, font=("Arial", 15), fg_color="#FFFFFF", text_color="#000000")
        self.password_entry.place(x=50, y=295)

        register_button = ctk.CTkButton(self.register_frame, text="Registrar", command=self.register, fg_color="#000000", text_color="#FFFFFF", hover_color="#404040")
        register_button.place(x=150, y=360, anchor= "center")

        login_button = ctk.CTkButton(self.register_frame, text="Ya tengo una cuenta", command=self.show_login, fg_color="transparent", hover=False, text_color="#000000")
        login_button.place(x=150, y=410, anchor= "center")

    def combobox_callback(self, choice):
            self.combo_value = choice

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.place_forget()

    def login(self): 

        loguear_usuario =  "SELECT * FROM usuarios WHERE user=? AND password_usuario=?"

        self.cursor.execute(loguear_usuario, (self.user_entry.get(), self.password_entry.get()))
        result = self.cursor.fetchone()

        if result:
            self.destroy()
            aplicacion = Application()
            aplicacion.root.mainloop()
        else:
            messagebox.showinfo("Error", message="Usuario incorrecto");return


    def register(self):
        localidades = ["San Miguel", "Parque San Martín", "La Roca"]

        if len(self.name_entry.get()) < 4 : messagebox.showinfo("Error", message="El nombre debe contener al menos 4 digitos");return
        if len(self.user_entry.get()) < 4 :  messagebox.showinfo("Error", message="El usuario debe contener al menos 4 digitos");return
        if len(self.password_entry.get()) < 4 :  messagebox.showinfo("Error", message="La contraseña debe contener al menos 4 digitos");return
        if self.combo_value not in localidades: messagebox.showinfo("Error", message="Debe agregar un localidad valida");return

        sucursal = 0

        for i, x in enumerate(localidades):
            if self.combo_value == x:
                sucursal = i


        verificar_existencia_usuario = "SELECT user FROM usuarios WHERE user = ?"
        self.cursor.execute(verificar_existencia_usuario, (self.user_entry.get(), ))

        existencia = self.cursor.fetchone()
        if existencia:
            messagebox.showinfo("Error", message="El usuario ya existe")
            return

        registrar_usuario = "INSERT INTO usuarios (nombre_usuario, user, password_usuario, nivel_permiso, id_sucursal) VALUES (?, ?, ?, ?, ?)"
        self.cursor.execute(registrar_usuario, (self.name_entry.get(), self.user_entry.get(),
                                                self.password_entry.get(),"empleado", sucursal))
        
        self.database_conexion.commit()
        messagebox.showinfo("Exito", message="Usuario registrado exitosamente.")
        self.show_login()

if __name__ == "__main__":
    registro = Registro()
    registro.mainloop()

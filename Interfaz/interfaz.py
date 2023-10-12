import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from importlib import import_module
import json

class Testing:

    def __init__(self, driver, start):
        self.driver = driver
        self.start = start
    # Crear la ventana principal
        self.root = ctk.CTk()
        self.root.geometry("500x600")
        self.root.title("Test")

        # Etiqueta de título
        self.titulo_label = ctk.CTkLabel(self.root, text="Seleccionar módulo para testear", font=("Helvetica", 24))
        self.titulo_label.grid(row=0, columnspan=3, padx=0, pady=15)

        # Dropdown para seleccionar el módulo (Administración o Cotizaciones)
        self.modulos = ["Administración", "Cotizaciones"]
        self.modulo_var = tk.StringVar()
        self.modulo_dropdown = ctk.CTkOptionMenu(self.root, values=self.modulos)
        self.modulo_dropdown.grid(row=1, column=0, padx=0, pady=5, sticky="e")

        # Dropdown para seleccionar el submódulo (si se selecciona Administración)
        self.submodulos = ["Clientes", "Proveedores", "Usuarios", "Servicios", "Ciudades", "Transporte", "Condiciones"]
        self.submodulo_var = tk.StringVar()
        self.submodulo_dropdown = ctk.CTkOptionMenu(self.root, values=self.submodulos, command=self.update_data)
        self.submodulo_dropdown.grid(row=1, column=1, padx=0, pady=5)

        # Dropdown para seleccionar la acción
        self.acciones = ["Crear", "Editar", "Eliminar"]
        self.accion_var = tk.StringVar()
        self.accion_dropdown = ctk.CTkOptionMenu(self.root, values=self.acciones)
        self.accion_dropdown.grid(row=1, column=2, padx=0, pady=5, sticky="w")

        # Campo de texto para ingresar datos
        self.datos_label = ctk.CTkLabel(self.root, text="Datos:")
        self.datos_label.grid(row=2, column=1, padx=0, pady=1)
        self.datos_entry = ctk.CTkTextbox(self.root, width=350, height=100)
        self.update_data(self.submodulo_dropdown.get())
        self.datos_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

        # Botón "Probar"
        self.probar_button = ctk.CTkButton(self.root, text="Probar", command=self.probar)
        self.probar_button.grid(row=4, column=1, padx=0, pady=5)

        self.url_label = ctk.CTkLabel(self.root, text="URL:")
        self.url_label.grid(row=5, column=0, columnspan=3, padx=0, pady=1)

        self.method_label = ctk.CTkLabel(self.root, text="Method:")
        self.method_label.grid(row=6, column=1, padx=0, pady=1)

        self.status_label = ctk.CTkLabel(self.root, text="Status:")
        self.status_label.grid(row=7, column=1, padx=0, pady=1)

        self.respuesta_label = ctk.CTkLabel(self.root, text="Response:")
        self.respuesta_label.grid(row=8, column=1, padx=0, pady=1)
        # Campo de texto de solo lectura para mostrar la respuesta
        self.respuesta_text = ctk.CTkTextbox(self.root, height=190, width=490)
        self.respuesta_text.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

    def update_data(self, value):
        modulo = import_module(f".{value}", f"Administracion")
        clase = getattr(modulo, value)
        obj = clase()
        self.datos_entry.delete("0.0", "999.999")
        self.datos_entry.insert("0.0", obj.get_campos() if obj.get_campos() else value)

    # Función que se ejecutará al hacer clic en el botón "Probar"
    def probar(self):
        #Crear un objeto de la clase seleccionada
        modulo = import_module(f".{self.submodulo_dropdown.get()}", f"Administracion")
        clase = getattr(modulo, self.submodulo_dropdown.get())
        obj = clase()
        
        #Checkear si hay datos ingresados, si no hay, enviar los datos por defecto
        datos_modificados = json.loads(self.datos_entry.get("0.0", "999.999")) if self.datos_entry.get("0.0", "999.999") != obj.get_campos() else {}
        datos = {k:v for k,v in datos_modificados.items() if v}
        accion = getattr(obj, self.accion_dropdown.get().lower())
        #obtenemos la respuesta
        url, method, status, response = self.start(self.driver, accion, datos if datos else None)

        #escribir labels
        self.url_label.configure(text=f"URL: {url}")
        self.method_label.configure(text=f"Method: {method}")
        self.status_label.configure(text=f"Status: {status}", bg_color='red' if int(status) >= 400 else 'green' if int(status) < 300 and int(status) >= 200 else 'orange', text_color='white', width=150)
        self.respuesta_text.configure(state='normal')
        self.respuesta_text.delete("0.0", "999.999")
        self.respuesta_text.insert("0.0", response)
        self.respuesta_text.configure(state='disabled')
    
    def run(self):
        self.root.mainloop()
    
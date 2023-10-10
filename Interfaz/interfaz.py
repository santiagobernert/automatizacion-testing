import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

# Función que se ejecutará al hacer clic en el botón "Probar"
def probar():
    modulo = modulo_var.get()
    accion = accion_var.get()
    datos = datos_entry.get()
    
    try:
        modulo_clase = getattr(__import__(modulo), modulo)
        accion_func = getattr(modulo_clase, accion.lower())
        resultado = accion_func(datos)
        respuesta_text.configure(state=tk.NORMAL)
        respuesta_text.delete(1.0, tk.END)
        respuesta_text.insert(tk.END, resultado)
        respuesta_text.configure(state=tk.DISABLED)
    except Exception as e:
        respuesta_text.configure(state=tk.NORMAL)
        respuesta_text.delete(1.0, tk.END)
        respuesta_text.insert(tk.END, f"Error: {str(e)}")
        respuesta_text.configure(state=tk.DISABLED)


def update_data(value):
    print(submodulo_dropdown.get())
    datos_entry.delete("0.0", "999.999")
    datos_entry.insert("0.0", value)

# Crear la ventana principal
root = ctk.CTk()
root.geometry("500x600")
root.title("Test")

# Etiqueta de título
titulo_label = ctk.CTkLabel(root, text="Seleccionar módulo para testear", font=("Helvetica", 24))
titulo_label.grid(row=0, columnspan=3, padx=0, pady=15)

# Dropdown para seleccionar el módulo (Administración o Cotizaciones)
modulos = ["Administración", "Cotizaciones"]
modulo_var = tk.StringVar()
modulo_dropdown = ctk.CTkOptionMenu(root, values=modulos)
modulo_dropdown.grid(row=1, column=0, padx=0, pady=5, sticky="e")

# Dropdown para seleccionar el submódulo (si se selecciona Administración)
submodulos = ["Clientes", "Proveedores", "Usuarios", "Servicios Adicionales", "Ciudades", "Transporte", "Condiciones generales"]
submodulo_var = tk.StringVar()
submodulo_dropdown = ctk.CTkOptionMenu(root, values=submodulos, command=update_data)
submodulo_dropdown.grid(row=1, column=1, padx=0, pady=5)

# Dropdown para seleccionar la acción
acciones = ["Crear", "Editar", "Eliminar"]
accion_var = tk.StringVar()
accion_dropdown = ctk.CTkOptionMenu(root, values=acciones)
accion_dropdown.grid(row=1, column=2, padx=0, pady=5, sticky="w")

# Campo de texto para ingresar datos
datos_label = ctk.CTkLabel(root, text="Datos:")
datos_label.grid(row=2, column=1, padx=0, pady=1)
datos_entry = ctk.CTkTextbox(root, width=350, height=170)
datos_entry.insert("0.0", submodulo_dropdown.get())
datos_entry.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

# Botón "Probar"
probar_button = ctk.CTkButton(root, text="Probar", command=probar)
probar_button.grid(row=4, column=1, padx=0, pady=5)

respuesta_label = ctk.CTkLabel(root, text="Respuesta:")
respuesta_label.grid(row=5, column=1, padx=0, pady=1)
# Campo de texto de solo lectura para mostrar la respuesta
respuesta_text = ctk.CTkTextbox(root, height=200, width=490)
respuesta_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
respuesta_text.configure(state=tk.DISABLED)

# Función para actualizar el submódulo cuando se selecciona "Administración"
def actualizar_submodulo(event):
    if modulo_var.get() == "Administración":
        pass
    else:
        submodulo_var.set("")  # Reiniciar el submódulo si no es Administración
        submodulo_dropdown.configure(state="disabled")

modulo_var.trace("w", actualizar_submodulo)



# Ejecutar la ventana principal
root.mainloop()
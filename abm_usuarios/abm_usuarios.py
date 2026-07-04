import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE, "usuarios.txt")

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8"):
            pass

def limpiar_campos():
    for v in (dni, nombre, apellido, password):
        v.set("")
    rol.set("Operador")
    estado.set("ACTIVO")

def leer_usuarios():
    crear_archivo()
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 7]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return []

def guardar_usuarios(usuarios):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            for u in usuarios:
                f.write("|".join(u) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for u in leer_usuarios():
        tabla.insert("", "end", values=u)

def alta():
    if not all(v.get().strip() for v in (dni, nombre, apellido, password)):
        messagebox.showwarning("Atención", "Debe completar todos los campos.")
        return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser numérico.")
        return
    if not nombre.get().isalpha() or not apellido.get().isalpha():
        messagebox.showerror("Error", "Nombre y Apellido deben contener solo letras.")
        return
    if len(password.get().split()) < 8:
        messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
        return
    usuarios = leer_usuarios()
    if any(u[0] == dni.get() for u in usuarios):
        messagebox.showerror("Error", "El DNI ya existe.")
        return
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
    usuarios.append([dni.get(), nombre.get(), apellido.get(), password.get(), rol.get(), estado.get(), fecha])
    guardar_usuarios(usuarios)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Usuario registrado correctamente.")

def baja():
    if not dni.get():
        messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        return
    usuarios = leer_usuarios()
    for u in usuarios:
        if u[0] == dni.get():
            u[5] = "BAJA"
            u[6] = datetime.now().strftime("%d/%m/%Y %H:%M")
            guardar_usuarios(usuarios)
            cargar_tabla()
            messagebox.showinfo("Baja", "Usuario dado de baja correctamente.")
            return
    messagebox.showerror("Error", "Usuario no encontrado.")

def modificar():
    if not dni.get():
        messagebox.showwarning("Atención", "Seleccione un usuario de la tabla.")
        return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser numérico.")
        return
    if not password.get().strip():
        messagebox.showerror("Error", "La contraseña no puede estar vacía.")
        return
    usuarios = leer_usuarios()
    for u in usuarios:
        if u[0] == dni.get():
            u[1], u[2], u[3], u[4], u[5] = nombre.get(), apellido.get(), password.get(), rol.get(), estado.get()
            u[6] = datetime.now().strftime("%d/%m/%Y %H:%M")
            guardar_usuarios(usuarios)
            cargar_tabla()
            messagebox.showinfo("Modificación", "Usuario modificado correctamente.")
            return
    messagebox.showerror("Error", "Usuario no encontrado.")

def seleccionar(event):
    sel = tabla.focus()
    if sel:
        v = tabla.item(sel, "values")
        dni.set(v[0]); nombre.set(v[1]); apellido.set(v[2])
        password.set(v[3]); rol.set(v[4]); estado.set(v[5])

ventana = tk.Tk()
ventana.title("ABM Usuarios")
ventana.geometry("1200x580")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

dni = tk.StringVar(); nombre = tk.StringVar(); apellido = tk.StringVar()
password = tk.StringVar(); rol = tk.StringVar(value="Operador")
estado = tk.StringVar(value="ACTIVO")

tk.Label(ventana, text="ABM USUARIOS", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=70, width=400, height=430)

tk.Label(frame_form, text="Datos del usuario", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

for i, (txt, var) in enumerate([
    ("DNI:", dni), ("Nombre:", nombre), ("Apellido:", apellido),
    ("Contraseña:", password)
], start=1):
    tk.Label(frame_form, text=txt, bg="white").grid(row=i, column=0, sticky="w", pady=5)
    entry = tk.Entry(frame_form, textvariable=var, width=30)
    entry.grid(row=i, column=1, pady=5)
    if txt == "Contraseña:":
        entry.configure(show="*")

tk.Label(frame_form, text="Rol:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=rol, values=["Administrador", "Supervisor", "Operador", "Consulta"], state="readonly", width=27).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=alta).grid(row=8, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=modificar).grid(row=8, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=baja).grid(row=9, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos).grid(row=9, column=1, pady=5)

frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=450, y=70, width=600, height=370)

cols = ("dni", "nombre", "apellido", "password", "rol", "estado", "fecha")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for col, hdr, w in zip(cols, ["DNI", "Nombre", "Apellido", "Contraseña", "Rol", "Estado", "Últ. Modif."], [80, 80, 80, 70, 90, 55, 100]):
    tabla.heading(col, text=hdr)
    tabla.column(col, width=w)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar)

tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=720, y=470)

crear_archivo()
cargar_tabla()
ventana.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE, "clientes.txt")

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8"):
            pass

def limpiar_campos():
    for v in (codigo, nombre, apellido, dni, direccion):
        v.set("")
    estado.set("ACTIVO")

def leer_clientes():
    crear_archivo()
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 6]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return []

def guardar_clientes(clientes):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            for c in clientes:
                f.write("|".join(c) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for c in leer_clientes():
        tabla.insert("", "end", values=c)

def alta():
    if not all(v.get().strip() for v in (codigo, nombre, apellido, dni, direccion)):
        messagebox.showwarning("Atención", "Debe completar todos los campos.")
        return
    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser numérico.")
        return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser numérico.")
        return
    clientes = leer_clientes()
    if any(c[0] == codigo.get() for c in clientes):
        messagebox.showerror("Error", "El Identificador ya existe.")
        return
    clientes.append([codigo.get(), nombre.get(), apellido.get(), dni.get(), direccion.get(), estado.get()])
    guardar_clientes(clientes)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Cliente registrado correctamente.")

def baja():
    if not codigo.get():
        messagebox.showwarning("Atención", "Seleccione un cliente de la tabla.")
        return
    clientes = leer_clientes()
    for c in clientes:
        if c[0] == codigo.get():
            c[5] = "BAJA"
            guardar_clientes(clientes)
            cargar_tabla()
            messagebox.showinfo("Baja", "Cliente dado de baja correctamente.")
            return
    messagebox.showerror("Error", "Cliente no encontrado.")

def modificar():
    if not codigo.get():
        messagebox.showwarning("Atención", "Seleccione un cliente de la tabla.")
        return
    if not dni.get().isdigit():
        messagebox.showerror("Error", "El DNI debe ser numérico.")
        return
    if not direccion.get().strip():
        messagebox.showerror("Error", "La dirección no puede estar vacía.")
        return
    clientes = leer_clientes()
    for c in clientes:
        if c[0] == codigo.get():
            c[1], c[2], c[3], c[4], c[5] = nombre.get(), apellido.get(), dni.get(), direccion.get(), estado.get()
            guardar_clientes(clientes)
            cargar_tabla()
            messagebox.showinfo("Modificación", "Cliente modificado correctamente.")
            return
    messagebox.showerror("Error", "Cliente no encontrado.")

def seleccionar(event):
    sel = tabla.focus()
    if sel:
        v = tabla.item(sel, "values")
        codigo.set(v[0]); nombre.set(v[1]); apellido.set(v[2])
        dni.set(v[3]); direccion.set(v[4]); estado.set(v[5])

ventana = tk.Tk()
ventana.title("Gestión de Clientes — Industrias del Sur")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

codigo = tk.StringVar(); nombre = tk.StringVar(); apellido = tk.StringVar()
dni = tk.StringVar(); direccion = tk.StringVar(); estado = tk.StringVar(value="ACTIVO")

tk.Label(ventana, text="GESTIÓN DE CLIENTES", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=70, width=400, height=410)

tk.Label(frame_form, text="Datos del cliente", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

for i, (txt, var) in enumerate([
    ("Identificador:", codigo), ("Nombre:", nombre), ("Apellido:", apellido),
    ("DNI:", dni), ("Dirección:", direccion)
], start=1):
    tk.Label(frame_form, text=txt, bg="white").grid(row=i, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=var, width=30).grid(row=i, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=alta).grid(row=8, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=modificar).grid(row=8, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=baja).grid(row=9, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos).grid(row=9, column=1, pady=5)

frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=450, y=70, width=420, height=370)

cols = ("id", "nombre", "apellido", "dni", "direccion", "estado")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for col, hdr, w in zip(cols, ["ID", "Nombre", "Apellido", "DNI", "Dirección", "Estado"], [40, 80, 80, 70, 100, 55]):
    tabla.heading(col, text=hdr)
    tabla.column(col, width=w)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar)

tk.Button(ventana, text="Cerrar", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=720, y=490)

crear_archivo()
cargar_tabla()
ventana.mainloop()

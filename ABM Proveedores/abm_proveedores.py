import tkinter as tk
from tkinter import ttk, messagebox
import os

ARCHIVO = "proveedores.txt"

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8"):
            pass

def limpiar_campos():
    for v in (codigo, razon_social, cuit, telefono, direccion):
        v.set("")
    estado.set("ACTIVO")

def leer_proveedores():
    crear_archivo()
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return [datos for linea in archivo if len(datos := linea.strip().split("|")) == 6]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return []

def guardar_proveedores(proveedores):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            for p in proveedores:
                archivo.write("|".join(p) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for p in leer_proveedores():
        tabla.insert("", "end", values=p)

def alta_proveedor():
    if not all(v.get().strip() for v in (codigo, razon_social, cuit, telefono, direccion)):
        messagebox.showwarning("Atención", "Debe completar todos los campos.")
        return
    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser numérico.")
        return
    if not cuit.get().isdigit():
        messagebox.showerror("Error", "El CUIT debe ser numérico (sin guiones).")
        return

    proveedores = leer_proveedores()
    for p in proveedores:
        if p[0] == codigo.get():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    proveedores.append([codigo.get(), razon_social.get(), cuit.get(), telefono.get(), direccion.get(), estado.get()])
    guardar_proveedores(proveedores)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Proveedor dado de alta correctamente.")

def baja_proveedor():
    if not codigo.get():
        messagebox.showwarning("Atención", "Ingrese el Identificador del proveedor.")
        return
    proveedores = leer_proveedores()
    for p in proveedores:
        if p[0] == codigo.get():
            p[5] = "BAJA"
            guardar_proveedores(proveedores)
            cargar_tabla()
            messagebox.showinfo("Baja", "Proveedor dado de baja correctamente.")
            return
    messagebox.showerror("Error", "Proveedor no encontrado.")

def modificar_proveedor():
    if not codigo.get():
        messagebox.showwarning("Atención", "Ingrese el Identificador del proveedor.")
        return
    if not cuit.get().isdigit():
        messagebox.showerror("Error", "El CUIT debe ser numérico (sin guiones).")
        return
    if not direccion.get().strip():
        messagebox.showerror("Error", "La dirección no puede estar vacía.")
        return

    proveedores = leer_proveedores()
    for p in proveedores:
        if p[0] == codigo.get():
            p[1], p[2], p[3], p[4], p[5] = razon_social.get(), cuit.get(), telefono.get(), direccion.get(), estado.get()
            guardar_proveedores(proveedores)
            cargar_tabla()
            messagebox.showinfo("Modificación", "Proveedor modificado correctamente.")
            return
    messagebox.showerror("Error", "Proveedor no encontrado.")

def seleccionar_proveedor(event):
    seleccionado = tabla.focus()
    if seleccionado:
        v = tabla.item(seleccionado, "values")
        codigo.set(v[0])
        razon_social.set(v[1])
        cuit.set(v[2])
        telefono.set(v[3])
        direccion.set(v[4])
        estado.set(v[5])

ventana = tk.Tk()
ventana.title("Gestión de Proveedores")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

codigo = tk.StringVar()
razon_social = tk.StringVar()
cuit = tk.StringVar()
telefono = tk.StringVar()
direccion = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

tk.Label(ventana, text="GESTIÓN DE PROVEEDORES", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=80, width=400, height=400)

tk.Label(frame_form, text="Datos del proveedor", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

for i, (texto, var) in enumerate([
    ("Identificador:", codigo), ("Razón Social:", razon_social), ("CUIT:", cuit),
    ("Teléfono:", telefono), ("Dirección:", direccion)
], start=1):
    tk.Label(frame_form, text=texto, bg="white").grid(row=i, column=0, sticky="w", pady=5)
    tk.Entry(frame_form, textvariable=var, width=30).grid(row=i, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=alta_proveedor).grid(row=8, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=modificar_proveedor).grid(row=8, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=baja_proveedor).grid(row=9, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos).grid(row=9, column=1, pady=5)

frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=450, y=80, width=420, height=360)

columnas = ("codigo", "razon_social", "cuit", "telefono", "direccion", "estado")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
for col, txt in zip(columnas, ["ID", "Razón Social", "CUIT", "Teléfono", "Dirección", "Estado"]):
    tabla.heading(col, text=txt)
for col, w in zip(columnas, [40, 110, 80, 70, 90, 50]):
    tabla.column(col, width=w)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_proveedor)

tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=720, y=470)

crear_archivo()
cargar_tabla()
ventana.mainloop()

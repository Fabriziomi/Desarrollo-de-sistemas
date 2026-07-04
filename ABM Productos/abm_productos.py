import tkinter as tk
from tkinter import ttk, messagebox
import os

ARCHIVO = "productos.txt"
TALLES = ["XS", "S", "M", "L", "XL", "XXL"]
COLORES = ["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO"]

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8"):
            pass

def es_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def limpiar_campos():
    for v in (codigo, descripcion, talle, color, precio):
        v.set("")
    estado.set("ACTIVO")

def leer_productos():
    crear_archivo()
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as archivo:
            return [datos for linea in archivo if len(datos := linea.strip().split("|")) == 6]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return []

def guardar_productos(productos):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as archivo:
            for p in productos:
                archivo.write("|".join(p) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for p in leer_productos():
        tabla.insert("", "end", values=p)

def alta_producto():
    if not all(v.get().strip() for v in (codigo, descripcion, talle, color, precio)):
        messagebox.showwarning("Atención", "Debe completar todos los campos.")
        return
    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser numérico.")
        return
    if not es_numero(precio.get()):
        messagebox.showerror("Error", "El Precio debe ser numérico.")
        return

    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            messagebox.showerror("Error", "El Identificador ya existe.")
            return

    productos.append([codigo.get(), descripcion.get(), talle.get(), color.get(), precio.get(), estado.get()])
    guardar_productos(productos)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Producto dado de alta correctamente.")

def baja_producto():
    if not codigo.get():
        messagebox.showwarning("Atención", "Ingrese el Identificador del producto.")
        return
    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            p[5] = "BAJA"
            guardar_productos(productos)
            cargar_tabla()
            messagebox.showinfo("Baja", "Producto dado de baja correctamente.")
            return
    messagebox.showerror("Error", "Producto no encontrado.")

def modificar_producto():
    if not codigo.get():
        messagebox.showwarning("Atención", "Ingrese el Identificador del producto.")
        return
    if not es_numero(precio.get()):
        messagebox.showerror("Error", "El Precio debe ser numérico.")
        return
    if not descripcion.get().strip():
        messagebox.showerror("Error", "La descripción no puede estar vacía.")
        return

    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            p[1], p[2], p[3], p[4], p[5] = descripcion.get(), talle.get(), color.get(), precio.get(), estado.get()
            guardar_productos(productos)
            cargar_tabla()
            messagebox.showinfo("Modificación", "Producto modificado correctamente.")
            return
    messagebox.showerror("Error", "Producto no encontrado.")

def seleccionar_producto(event):
    seleccionado = tabla.focus()
    if seleccionado:
        v = tabla.item(seleccionado, "values")
        codigo.set(v[0])
        descripcion.set(v[1])
        talle.set(v[2])
        color.set(v[3])
        precio.set(v[4])
        estado.set(v[5])

ventana = tk.Tk()
ventana.title("Gestión de Productos")
ventana.geometry("900x550")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

codigo = tk.StringVar()
descripcion = tk.StringVar()
talle = tk.StringVar()
color = tk.StringVar()
precio = tk.StringVar()
estado = tk.StringVar(value="ACTIVO")

tk.Label(ventana, text="GESTIÓN DE PRODUCTOS", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=80, width=400, height=400)

tk.Label(frame_form, text="Datos del producto", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=5)

tk.Label(frame_form, text="Descripción:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=descripcion, width=30).grid(row=2, column=1, pady=5)

tk.Label(frame_form, text="Talle:", bg="white").grid(row=3, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=talle, values=TALLES, state="readonly", width=27).grid(row=3, column=1, pady=5)

tk.Label(frame_form, text="Color:", bg="white").grid(row=4, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=color, values=COLORES, state="readonly", width=27).grid(row=4, column=1, pady=5)

tk.Label(frame_form, text="Precio:", bg="white").grid(row=5, column=0, sticky="w", pady=5)
tk.Entry(frame_form, textvariable=precio, width=30).grid(row=5, column=1, pady=5)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=6, column=0, sticky="w", pady=5)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=6, column=1, pady=5)

tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=alta_producto).grid(row=8, column=0, pady=15)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=modificar_producto).grid(row=8, column=1, pady=15)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=baja_producto).grid(row=9, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos).grid(row=9, column=1, pady=5)

frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=450, y=80, width=420, height=360)

columnas = ("codigo", "descripcion", "talle", "color", "precio", "estado")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
for col, txt in zip(columnas, ["ID", "Descripción", "Talle", "Color", "Precio", "Estado"]):
    tabla.heading(col, text=txt)
for col, w in zip(columnas, [40, 110, 50, 70, 60, 50]):
    tabla.column(col, width=w)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar_producto)

tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=720, y=470)

crear_archivo()
cargar_tabla()
ventana.mainloop()

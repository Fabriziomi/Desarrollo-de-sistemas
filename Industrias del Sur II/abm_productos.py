import tkinter as tk
from tkinter import ttk, messagebox
import os

BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO = os.path.join(BASE, "productos.txt")

TALLES = ["XS", "S", "M", "L", "XL", "XXL"]
COLORES = ["BLANCO", "NEGRO", "AZUL", "ROJO", "AMARILLO", "VERDE", "GRIS"]

def crear_archivo():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, "w", encoding="utf-8"):
            pass

def es_numero(v):
    try:
        float(v)
        return True
    except ValueError:
        return False

def es_entero_positivo(v):
    try:
        return int(v) >= 0
    except ValueError:
        return False

def limpiar_campos():
    for v in (codigo, descripcion, precio_compra, precio_venta, stock):
        v.set("")
    talle.set("")
    color.set("")
    estado.set("ACTIVO")

def leer_productos():
    crear_archivo()
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 8]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
        return []

def guardar_productos(productos):
    try:
        with open(ARCHIVO, "w", encoding="utf-8") as f:
            for p in productos:
                f.write("|".join(p) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for p in leer_productos():
        tabla.insert("", "end", values=p)

def validar_campos():
    if not all(v.get().strip() for v in (codigo, descripcion, talle, color, precio_compra, precio_venta, stock)):
        messagebox.showwarning("Atención", "Debe completar todos los campos.")
        return False
    if not codigo.get().isdigit():
        messagebox.showerror("Error", "El Identificador debe ser numérico.")
        return False
    if not es_numero(precio_compra.get()):
        messagebox.showerror("Error", "El Precio de Compra debe ser numérico.")
        return False
    if not es_numero(precio_venta.get()):
        messagebox.showerror("Error", "El Precio de Venta debe ser numérico.")
        return False
    if not es_entero_positivo(stock.get()):
        messagebox.showerror("Error", "El Stock debe ser un número entero mayor o igual a 0.")
        return False
    return True

def alta():
    if not validar_campos():
        return
    productos = leer_productos()
    if any(p[0] == codigo.get() for p in productos):
        messagebox.showerror("Error", "El Identificador ya existe.")
        return
    productos.append([
        codigo.get(), descripcion.get(), talle.get(), color.get(),
        precio_compra.get(), precio_venta.get(), stock.get(), estado.get()
    ])
    guardar_productos(productos)
    cargar_tabla()
    limpiar_campos()
    messagebox.showinfo("Alta", "Producto registrado correctamente.")

def baja():
    if not codigo.get():
        messagebox.showwarning("Atención", "Seleccione un producto de la tabla.")
        return
    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            p[7] = "BAJA"
            guardar_productos(productos)
            cargar_tabla()
            messagebox.showinfo("Baja", "Producto dado de baja correctamente.")
            return
    messagebox.showerror("Error", "Producto no encontrado.")

def modificar():
    if not codigo.get():
        messagebox.showwarning("Atención", "Seleccione un producto de la tabla.")
        return
    if not es_numero(precio_compra.get()):
        messagebox.showerror("Error", "El Precio de Compra debe ser numérico.")
        return
    if not es_numero(precio_venta.get()):
        messagebox.showerror("Error", "El Precio de Venta debe ser numérico.")
        return
    if not es_entero_positivo(stock.get()):
        messagebox.showerror("Error", "El Stock debe ser un número entero mayor o igual a 0.")
        return
    productos = leer_productos()
    for p in productos:
        if p[0] == codigo.get():
            p[1], p[2], p[3], p[4], p[5], p[6], p[7] = (
                descripcion.get(), talle.get(), color.get(),
                precio_compra.get(), precio_venta.get(), stock.get(), estado.get()
            )
            guardar_productos(productos)
            cargar_tabla()
            messagebox.showinfo("Modificación", "Producto modificado correctamente.")
            return
    messagebox.showerror("Error", "Producto no encontrado.")

def seleccionar(event):
    sel = tabla.focus()
    if sel:
        v = tabla.item(sel, "values")
        codigo.set(v[0]); descripcion.set(v[1]); talle.set(v[2]); color.set(v[3])
        precio_compra.set(v[4]); precio_venta.set(v[5]); stock.set(v[6]); estado.set(v[7])

ventana = tk.Tk()
ventana.title("Gestión de Productos — Industrias del Sur")
ventana.geometry("1000x570")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

codigo = tk.StringVar(); descripcion = tk.StringVar(); talle = tk.StringVar()
color = tk.StringVar(); precio_compra = tk.StringVar(); precio_venta = tk.StringVar()
stock = tk.StringVar(); estado = tk.StringVar(value="ACTIVO")

tk.Label(ventana, text="GESTIÓN DE PRODUCTOS", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=15, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=70, width=420, height=460)

tk.Label(frame_form, text="Datos del producto", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=8)

tk.Label(frame_form, text="Identificador:", bg="white").grid(row=1, column=0, sticky="w", pady=4)
tk.Entry(frame_form, textvariable=codigo, width=30).grid(row=1, column=1, pady=4)

tk.Label(frame_form, text="Descripción:", bg="white").grid(row=2, column=0, sticky="w", pady=4)
tk.Entry(frame_form, textvariable=descripcion, width=30).grid(row=2, column=1, pady=4)

tk.Label(frame_form, text="Talle:", bg="white").grid(row=3, column=0, sticky="w", pady=4)
ttk.Combobox(frame_form, textvariable=talle, values=TALLES, state="readonly", width=27).grid(row=3, column=1, pady=4)

tk.Label(frame_form, text="Color:", bg="white").grid(row=4, column=0, sticky="w", pady=4)
ttk.Combobox(frame_form, textvariable=color, values=COLORES, state="readonly", width=27).grid(row=4, column=1, pady=4)

tk.Label(frame_form, text="Precio de Compra ($):", bg="white").grid(row=5, column=0, sticky="w", pady=4)
tk.Entry(frame_form, textvariable=precio_compra, width=30).grid(row=5, column=1, pady=4)

tk.Label(frame_form, text="Precio de Venta ($):", bg="white").grid(row=6, column=0, sticky="w", pady=4)
tk.Entry(frame_form, textvariable=precio_venta, width=30).grid(row=6, column=1, pady=4)

tk.Label(frame_form, text="Stock inicial:", bg="white").grid(row=7, column=0, sticky="w", pady=4)
tk.Entry(frame_form, textvariable=stock, width=30).grid(row=7, column=1, pady=4)

tk.Label(frame_form, text="Estado:", bg="white").grid(row=8, column=0, sticky="w", pady=4)
ttk.Combobox(frame_form, textvariable=estado, values=["ACTIVO", "BAJA"], state="readonly", width=27).grid(row=8, column=1, pady=4)

tk.Button(frame_form, text="Alta", width=12, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=alta).grid(row=10, column=0, pady=12)
tk.Button(frame_form, text="Modificar", width=12, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=modificar).grid(row=10, column=1, pady=12)
tk.Button(frame_form, text="Baja", width=12, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=baja).grid(row=11, column=0, pady=5)
tk.Button(frame_form, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 9, "bold"), command=limpiar_campos).grid(row=11, column=1, pady=5)

frame_tabla = tk.Frame(ventana, bg="white")
frame_tabla.place(x=470, y=70, width=510, height=440)

cols = ("id", "desc", "talle", "color", "p_compra", "p_venta", "stock", "estado")
hdrs = ["ID", "Descripción", "Talle", "Color", "P.Compra", "P.Venta", "Stock", "Estado"]
widths = [35, 115, 45, 65, 70, 70, 45, 55]
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for col, hdr, w in zip(cols, hdrs, widths):
    tabla.heading(col, text=hdr)
    tabla.column(col, width=w)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)
tabla.bind("<<TreeviewSelect>>", seleccionar)

tk.Button(ventana, text="Cerrar", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=860, y=520)

crear_archivo()
cargar_tabla()
ventana.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

BASE = os.path.dirname(__file__)
CLIENTES_TXT = os.path.join(BASE, "clientes.txt")
PRODUCTOS_TXT = os.path.join(BASE, "productos.txt")
FACTURAS_DIR = os.path.join(BASE, "facturas")

items_factura = []

def leer_clientes_activos():
    if not os.path.exists(CLIENTES_TXT):
        return []
    try:
        with open(CLIENTES_TXT, "r", encoding="utf-8") as archivo:
            return [datos for linea in archivo if len(datos := linea.strip().split("|")) == 6 and datos[5] == "ACTIVO"]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer clientes: {e}")
        return []

def leer_productos_activos():
    if not os.path.exists(PRODUCTOS_TXT):
        return []
    try:
        with open(PRODUCTOS_TXT, "r", encoding="utf-8") as archivo:
            return [datos for linea in archivo if len(datos := linea.strip().split("|")) == 6 and datos[5] == "ACTIVO"]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer productos: {e}")
        return []

def proximo_numero():
    if not os.path.exists(FACTURAS_DIR):
        return 1
    nums = []
    for nombre in os.listdir(FACTURAS_DIR):
        if nombre.startswith("factura_") and nombre.endswith(".txt"):
            try:
                nums.append(int(nombre[8:-4]))
            except ValueError:
                pass
    return max(nums) + 1 if nums else 1

def actualizar_total():
    total = sum(item[4] for item in items_factura)
    total_var.set(f"TOTAL:  ${total:,.2f}")
    return total

def agregar_producto():
    if not cliente_var.get():
        messagebox.showwarning("Atención", "Seleccione un cliente.")
        return

    label_prod = producto_var.get()
    if not label_prod or label_prod not in productos_dict:
        messagebox.showwarning("Atención", "Seleccione un producto.")
        return

    if not cantidad_var.get().strip().isdigit() or int(cantidad_var.get()) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0.")
        return

    datos = productos_dict[label_prod]
    codigo = datos[0]
    descripcion = datos[1]
    precio = float(datos[4])
    cantidad = int(cantidad_var.get())
    subtotal = precio * cantidad

    for item in items_factura:
        if item[0] == codigo:
            item[2] += cantidad
            item[4] = item[2] * item[3]
            break
    else:
        items_factura.append([codigo, descripcion, cantidad, precio, subtotal])

    refrescar_tabla()
    cantidad_var.set("")
    producto_var.set("")
    precio_var.set("")

def quitar_producto():
    seleccionado = tabla.focus()
    if not seleccionado:
        messagebox.showwarning("Atención", "Seleccione un producto de la factura para quitar.")
        return
    codigo = tabla.item(seleccionado, "values")[0]
    for item in list(items_factura):
        if item[0] == codigo:
            items_factura.remove(item)
            break
    refrescar_tabla()

def refrescar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for item in items_factura:
        tabla.insert("", "end", values=(item[0], item[1], item[2], f"${item[3]:,.2f}", f"${item[4]:,.2f}"))
    actualizar_total()

def mostrar_precio(event=None):
    label_prod = producto_var.get()
    if label_prod in productos_dict:
        precio_var.set(f"${float(productos_dict[label_prod][4]):,.2f}")
    else:
        precio_var.set("")

def limpiar_factura():
    items_factura.clear()
    cliente_var.set("")
    producto_var.set("")
    cantidad_var.set("")
    precio_var.set("")
    refrescar_tabla()

def generar_factura():
    if not cliente_var.get():
        messagebox.showwarning("Atención", "Seleccione un cliente.")
        return
    if not items_factura:
        messagebox.showwarning("Atención", "La factura no tiene productos cargados.")
        return

    numero = proximo_numero()
    cliente = clientes_dict[cliente_var.get()]
    total = actualizar_total()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    lineas = [
        "=" * 52,
        f"               FACTURA N° {numero:04d}",
        "=" * 52,
        f"Fecha:   {fecha}",
        f"Cliente: {cliente[0]} - {cliente[1]} {cliente[2]}",
        f"DNI:     {cliente[3]}",
        f"Dirección: {cliente[4]}",
        "-" * 52,
        f"{'Cód':<5}{'Descripción':<20}{'Cant':>5}{'P.Unit':>10}{'Subtot':>12}",
        "-" * 52,
    ]
    for item in items_factura:
        lineas.append(
            f"{item[0]:<5}{item[1][:19]:<20}{item[2]:>5}"
            f"{('$' + format(item[3], ',.2f')):>10}"
            f"{('$' + format(item[4], ',.2f')):>12}"
        )
    lineas.extend([
        "-" * 52,
        f"{'TOTAL:':>40}  ${total:,.2f}",
        "=" * 52,
    ])

    contenido = "\n".join(lineas)

    try:
        os.makedirs(FACTURAS_DIR, exist_ok=True)
        ruta = os.path.join(FACTURAS_DIR, f"factura_{numero:04d}.txt")
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar la factura: {e}")
        return

    messagebox.showinfo("Factura generada", f"Factura N° {numero:04d} generada correctamente.\n\nArchivo:\n{ruta}")
    limpiar_factura()
    actualizar_numero_titulo()

def actualizar_numero_titulo():
    numero_var.set(f"Factura N° {proximo_numero():04d}")

def recargar_datos():
    global clientes_dict, productos_dict
    clientes = leer_clientes_activos()
    productos = leer_productos_activos()

    clientes_dict = {f"{c[0]} - {c[1]} {c[2]}": c for c in clientes}
    productos_dict = {f"{p[0]} - {p[1]} (${float(p[4]):,.2f})": p for p in productos}

    combo_cliente["values"] = list(clientes_dict.keys())
    combo_producto["values"] = list(productos_dict.keys())
    actualizar_numero_titulo()

ventana = tk.Tk()
ventana.title("Generación de Facturas")
ventana.geometry("1000x600")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

cliente_var = tk.StringVar()
producto_var = tk.StringVar()
cantidad_var = tk.StringVar()
precio_var = tk.StringVar()
total_var = tk.StringVar(value="TOTAL:  $0.00")
numero_var = tk.StringVar(value="Factura N° 0001")

clientes_dict = {}
productos_dict = {}

tk.Label(ventana, text="GENERACIÓN DE FACTURAS", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=20, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=80, width=420, height=470)

tk.Label(frame_form, text="Datos de la factura", font=("Arial", 14, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(frame_form, textvariable=numero_var, font=("Arial", 11, "bold"), bg="white", fg="#EA580C").grid(row=1, column=0, columnspan=2, pady=(0, 10))

tk.Label(frame_form, text="Cliente:", bg="white").grid(row=2, column=0, sticky="w", pady=8)
combo_cliente = ttk.Combobox(frame_form, textvariable=cliente_var, state="readonly", width=27)
combo_cliente.grid(row=2, column=1, pady=8)

tk.Label(frame_form, text="Agregar producto", font=("Arial", 11, "bold"), bg="white").grid(row=3, column=0, columnspan=2, pady=(15, 5))

tk.Label(frame_form, text="Producto:", bg="white").grid(row=4, column=0, sticky="w", pady=8)
combo_producto = ttk.Combobox(frame_form, textvariable=producto_var, state="readonly", width=27)
combo_producto.grid(row=4, column=1, pady=8)
combo_producto.bind("<<ComboboxSelected>>", mostrar_precio)

tk.Label(frame_form, text="Precio unit.:", bg="white").grid(row=5, column=0, sticky="w", pady=8)
tk.Entry(frame_form, textvariable=precio_var, width=30, state="readonly").grid(row=5, column=1, pady=8)

tk.Label(frame_form, text="Cantidad:", bg="white").grid(row=6, column=0, sticky="w", pady=8)
tk.Entry(frame_form, textvariable=cantidad_var, width=30).grid(row=6, column=1, pady=8)

tk.Button(frame_form, text="Agregar producto", width=26, bg="#16A34A", fg="white", font=("Arial", 9, "bold"), command=agregar_producto).grid(row=7, column=0, columnspan=2, pady=(15, 5))
tk.Button(frame_form, text="Quitar producto", width=26, bg="#DC2626", fg="white", font=("Arial", 9, "bold"), command=quitar_producto).grid(row=8, column=0, columnspan=2, pady=5)

frame_factura = tk.Frame(ventana, bg="white", relief="ridge", borderwidth=1)
frame_factura.place(x=470, y=80, width=500, height=470)

tk.Label(frame_factura, text="DETALLE DE LA FACTURA", font=("Arial", 13, "bold"), bg="white", fg="#172033").pack(pady=10)

frame_tabla = tk.Frame(frame_factura, bg="white")
frame_tabla.pack(fill="both", expand=True, padx=10)

columnas = ("codigo", "descripcion", "cantidad", "precio", "subtotal")
tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
for col, txt in zip(columnas, ["Cód", "Descripción", "Cant", "P. Unit", "Subtotal"]):
    tabla.heading(col, text=txt)
tabla.column("codigo", width=40, anchor="center")
tabla.column("descripcion", width=160)
tabla.column("cantidad", width=50, anchor="center")
tabla.column("precio", width=90, anchor="e")
tabla.column("subtotal", width=100, anchor="e")

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)

tk.Label(frame_factura, textvariable=total_var, font=("Arial", 15, "bold"), bg="white", fg="#16A34A").pack(pady=10, anchor="e", padx=20)

tk.Button(frame_factura, text="Generar factura", width=18, bg="#EA580C", fg="white", font=("Arial", 10, "bold"), command=generar_factura).pack(side="left", padx=20, pady=10)
tk.Button(frame_factura, text="Limpiar", width=12, bg="#6B7280", fg="white", font=("Arial", 10, "bold"), command=limpiar_factura).pack(side="left", pady=10)

tk.Button(ventana, text="Recargar datos", width=15, bg="#2563EB", fg="white", font=("Arial", 9, "bold"), command=recargar_datos).place(x=30, y=560)
tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white", command=ventana.destroy).place(x=850, y=560)

recargar_datos()
ventana.mainloop()

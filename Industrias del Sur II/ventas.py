import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CLIENTES_TXT = os.path.join(BASE, "clientes.txt")
PRODUCTOS_TXT = os.path.join(BASE, "productos.txt")
FACTURAS_DIR = os.path.join(BASE, "facturas")

items_venta = []
clientes_dict = {}
productos_dict = {}

def leer_clientes_activos():
    if not os.path.exists(CLIENTES_TXT):
        return []
    try:
        with open(CLIENTES_TXT, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 6 and d[5] == "ACTIVO"]
    except:
        return []

def leer_productos_activos():
    if not os.path.exists(PRODUCTOS_TXT):
        return []
    try:
        with open(PRODUCTOS_TXT, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 8 and d[7] == "ACTIVO"]
    except:
        return []

def leer_todos_productos():
    if not os.path.exists(PRODUCTOS_TXT):
        return []
    try:
        with open(PRODUCTOS_TXT, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 8]
    except:
        return []

def guardar_productos(productos):
    try:
        with open(PRODUCTOS_TXT, "w", encoding="utf-8") as f:
            for p in productos:
                f.write("|".join(p) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el stock: {e}")

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
    total = sum(item[4] for item in items_venta)
    total_var.set(f"TOTAL:  ${total:,.2f}")
    return total

def mostrar_precio(event=None):
    label = producto_var.get()
    if label in productos_dict:
        p = productos_dict[label]
        precio_var.set(f"${float(p[5]):,.2f}   (Stock disponible: {p[6]})")
    else:
        precio_var.set("")

def agregar_producto():
    if not cliente_var.get():
        messagebox.showwarning("Atención", "Seleccione un cliente.")
        return
    label = producto_var.get()
    if not label or label not in productos_dict:
        messagebox.showwarning("Atención", "Seleccione un producto.")
        return
    if not cantidad_var.get().strip().isdigit() or int(cantidad_var.get()) <= 0:
        messagebox.showerror("Error", "La cantidad debe ser un número entero mayor a 0.")
        return

    datos = productos_dict[label]
    cod = datos[0]
    desc = datos[1]
    precio = float(datos[5])
    stock_disp = int(datos[6])
    cantidad = int(cantidad_var.get())

    ya_en_lista = next((item[2] for item in items_venta if item[0] == cod), 0)
    if ya_en_lista + cantidad > stock_disp:
        messagebox.showerror("Stock insuficiente",
            f"Stock disponible: {stock_disp} unidad(es).\n"
            f"Ya en factura: {ya_en_lista}.\n"
            f"No es posible agregar {cantidad} unidad(es) más.")
        return

    for item in items_venta:
        if item[0] == cod:
            item[2] += cantidad
            item[4] = item[2] * item[3]
            break
    else:
        items_venta.append([cod, desc, cantidad, precio, precio * cantidad])

    refrescar_tabla()
    cantidad_var.set("")
    producto_var.set("")
    precio_var.set("")

def quitar_producto():
    sel = tabla.focus()
    if not sel:
        messagebox.showwarning("Atención", "Seleccione un producto de la factura.")
        return
    cod = tabla.item(sel, "values")[0]
    for item in list(items_venta):
        if item[0] == cod:
            items_venta.remove(item)
            break
    refrescar_tabla()

def refrescar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)
    for item in items_venta:
        tabla.insert("", "end", values=(
            item[0], item[1], item[2],
            f"${item[3]:,.2f}", f"${item[4]:,.2f}"
        ))
    actualizar_total()

def limpiar():
    items_venta.clear()
    cliente_var.set("")
    producto_var.set("")
    cantidad_var.set("")
    precio_var.set("")
    refrescar_tabla()

def generar_factura():
    if not cliente_var.get():
        messagebox.showwarning("Atención", "Seleccione un cliente.")
        return
    if not items_venta:
        messagebox.showwarning("Atención", "La factura no tiene productos cargados.")
        return

    numero = proximo_numero()
    cliente = clientes_dict[cliente_var.get()]
    total = actualizar_total()
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

    productos = leer_todos_productos()
    for item in items_venta:
        for p in productos:
            if p[0] == item[0]:
                p[6] = str(int(p[6]) - item[2])
                break
    guardar_productos(productos)

    lineas = [
        "=" * 55,
        f"              FACTURA N° {numero:04d}",
        "=" * 55,
        f"Fecha:     {fecha}",
        f"Cliente:   {cliente[0]} - {cliente[1]} {cliente[2]}",
        f"DNI:       {cliente[3]}",
        f"Dirección: {cliente[4]}",
        "-" * 55,
        f"{'Cód':<5}{'Descripción':<22}{'Cant':>5}{'P.Unit':>10}{'Subtotal':>13}",
        "-" * 55,
    ]
    for item in items_venta:
        lineas.append(
            f"{item[0]:<5}{item[1][:21]:<22}{item[2]:>5}"
            f"{'$'+format(item[3],',.2f'):>10}{'$'+format(item[4],',.2f'):>13}"
        )
    lineas += [
        "-" * 55,
        f"{'TOTAL:':>42}  ${total:,.2f}",
        "=" * 55,
    ]

    try:
        os.makedirs(FACTURAS_DIR, exist_ok=True)
        ruta = os.path.join(FACTURAS_DIR, f"factura_{numero:04d}.txt")
        with open(ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(lineas) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar la factura: {e}")
        return

    messagebox.showinfo("Factura generada",
        f"Factura N° {numero:04d} generada correctamente.\n"
        f"Stock actualizado.\n\nArchivo: {ruta}")
    limpiar()
    numero_var.set(f"Factura N° {proximo_numero():04d}")

def recargar():
    global clientes_dict, productos_dict
    clientes = leer_clientes_activos()
    productos = leer_productos_activos()
    clientes_dict = {f"{c[0]} - {c[1]} {c[2]}": c for c in clientes}
    productos_dict = {f"{p[0]} - {p[1]} ({p[2]}/{p[3]})": p for p in productos}
    combo_cliente["values"] = list(clientes_dict.keys())
    combo_producto["values"] = list(productos_dict.keys())
    numero_var.set(f"Factura N° {proximo_numero():04d}")

ventana = tk.Tk()
ventana.title("Ventas / Facturación — Industrias del Sur")
ventana.geometry("1000x600")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

cliente_var = tk.StringVar()
producto_var = tk.StringVar()
cantidad_var = tk.StringVar()
precio_var = tk.StringVar()
total_var = tk.StringVar(value="TOTAL:  $0.00")
numero_var = tk.StringVar(value="Factura N° 0001")

tk.Label(ventana, text="VENTAS / FACTURACIÓN", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_form = tk.Frame(ventana, bg="white", padx=20, pady=15, relief="ridge", borderwidth=1)
frame_form.place(x=30, y=75, width=430, height=480)

tk.Label(frame_form, text="Datos de la venta", font=("Arial", 13, "bold"), bg="white").grid(row=0, column=0, columnspan=2, pady=8)
tk.Label(frame_form, textvariable=numero_var, font=("Arial", 11, "bold"), bg="white", fg="#EA580C").grid(row=1, column=0, columnspan=2, pady=(0, 8))

tk.Label(frame_form, text="Cliente:", bg="white").grid(row=2, column=0, sticky="w", pady=6)
combo_cliente = ttk.Combobox(frame_form, textvariable=cliente_var, state="readonly", width=27)
combo_cliente.grid(row=2, column=1, pady=6)

tk.Label(frame_form, text="Agregar producto", font=("Arial", 11, "bold"), bg="white").grid(row=3, column=0, columnspan=2, pady=(14, 4))

tk.Label(frame_form, text="Producto:", bg="white").grid(row=4, column=0, sticky="w", pady=6)
combo_producto = ttk.Combobox(frame_form, textvariable=producto_var, state="readonly", width=27)
combo_producto.grid(row=4, column=1, pady=6)
combo_producto.bind("<<ComboboxSelected>>", mostrar_precio)

tk.Label(frame_form, text="Precio / Stock:", bg="white").grid(row=5, column=0, sticky="w", pady=6)
tk.Entry(frame_form, textvariable=precio_var, width=30, state="readonly").grid(row=5, column=1, pady=6)

tk.Label(frame_form, text="Cantidad:", bg="white").grid(row=6, column=0, sticky="w", pady=6)
tk.Entry(frame_form, textvariable=cantidad_var, width=30).grid(row=6, column=1, pady=6)

tk.Button(frame_form, text="Agregar producto", width=26, bg="#16A34A", fg="white",
          font=("Arial", 9, "bold"), command=agregar_producto).grid(row=7, column=0, columnspan=2, pady=(14, 4))
tk.Button(frame_form, text="Quitar producto", width=26, bg="#DC2626", fg="white",
          font=("Arial", 9, "bold"), command=quitar_producto).grid(row=8, column=0, columnspan=2, pady=4)

frame_detalle = tk.Frame(ventana, bg="white", relief="ridge", borderwidth=1)
frame_detalle.place(x=475, y=75, width=500, height=480)

tk.Label(frame_detalle, text="DETALLE DE LA FACTURA", font=("Arial", 13, "bold"), bg="white", fg="#172033").pack(pady=10)

frame_tabla = tk.Frame(frame_detalle, bg="white")
frame_tabla.pack(fill="both", expand=True, padx=10)

cols = ("cod", "desc", "cant", "precio", "subtotal")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for col, txt, w, anchor in zip(
    cols,
    ["Cód", "Descripción", "Cant", "P.Unit", "Subtotal"],
    [40, 165, 50, 100, 105],
    ["center", "w", "center", "e", "e"]
):
    tabla.heading(col, text=txt)
    tabla.column(col, width=w, anchor=anchor)

scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll.set)
scroll.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)

tk.Label(frame_detalle, textvariable=total_var, font=("Arial", 14, "bold"), bg="white", fg="#16A34A").pack(pady=8, anchor="e", padx=20)

tk.Button(frame_detalle, text="Generar factura", width=18, bg="#EA580C", fg="white",
          font=("Arial", 10, "bold"), command=generar_factura).pack(side="left", padx=20, pady=8)
tk.Button(frame_detalle, text="Limpiar", width=12, bg="#6B7280", fg="white",
          font=("Arial", 10, "bold"), command=limpiar).pack(side="left", pady=8)

tk.Button(ventana, text="Recargar datos", width=15, bg="#2563EB", fg="white",
          font=("Arial", 9, "bold"), command=recargar).place(x=30, y=570)
tk.Button(ventana, text="Cerrar", width=15, bg="#111827", fg="white",
          command=ventana.destroy).place(x=850, y=570)

recargar()
ventana.mainloop()

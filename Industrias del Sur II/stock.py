import tkinter as tk
from tkinter import ttk, messagebox
import os

BASE = os.path.dirname(os.path.abspath(__file__))
PRODUCTOS_TXT = os.path.join(BASE, "productos.txt")

STOCK_BAJO = 5

def leer_productos():
    if not os.path.exists(PRODUCTOS_TXT):
        return []
    try:
        with open(PRODUCTOS_TXT, "r", encoding="utf-8") as f:
            return [d for linea in f if len(d := linea.strip().split("|")) == 8]
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo leer productos: {e}")
        return []

def cargar_tabla():
    for fila in tabla.get_children():
        tabla.delete(fila)

    filtro = filtro_var.get()
    productos = leer_productos()
    total_unidades = 0

    for p in productos:
        try:
            stk = int(p[6])
        except ValueError:
            stk = 0

        if filtro == "BAJOS" and stk > STOCK_BAJO:
            continue
        if filtro == "ACTIVOS" and p[7] != "ACTIVO":
            continue

        if stk == 0:
            tag = "sin_stock"
        elif stk <= STOCK_BAJO:
            tag = "stock_bajo"
        else:
            tag = ""

        tabla.insert("", "end", values=(p[0], p[1], p[2], p[3], p[5], stk, p[7]), tags=(tag,))
        total_unidades += stk

    lbl_total.config(text=f"Total de unidades en stock: {total_unidades}")

ventana = tk.Tk()
ventana.title("Consulta de Stock — Industrias del Sur")
ventana.geometry("820x530")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

filtro_var = tk.StringVar(value="TODOS")

tk.Label(ventana, text="CONSULTA DE STOCK", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=15)

frame_filtros = tk.Frame(ventana, bg="#f4f6fa")
frame_filtros.pack()

tk.Label(frame_filtros, text="Mostrar:", bg="#f4f6fa", font=("Arial", 10)).pack(side="left", padx=5)
for txt, val in [("Todos", "TODOS"), ("Solo activos", "ACTIVOS"), ("Stock bajo o sin stock", "BAJOS")]:
    tk.Radiobutton(frame_filtros, text=txt, variable=filtro_var, value=val,
                   bg="#f4f6fa", font=("Arial", 10), command=cargar_tabla).pack(side="left", padx=8)
tk.Button(frame_filtros, text="Actualizar", bg="#059669", fg="white",
          font=("Arial", 9, "bold"), command=cargar_tabla).pack(side="left", padx=15)

frame_tabla = tk.Frame(ventana, bg="white", relief="ridge", borderwidth=1)
frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

cols = ("id", "descripcion", "talle", "color", "p_venta", "stock", "estado")
hdrs = ["ID", "Descripción", "Talle", "Color", "P. Venta", "Stock", "Estado"]
widths = [40, 200, 55, 80, 80, 60, 65]
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings")
for col, hdr, w in zip(cols, hdrs, widths):
    tabla.heading(col, text=hdr)
    tabla.column(col, width=w, anchor="w" if col == "descripcion" else "center")

tabla.tag_configure("sin_stock", background="#FECACA")
tabla.tag_configure("stock_bajo", background="#FEF08A")

scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scroll_y.set)
scroll_y.pack(side="right", fill="y")
tabla.pack(fill="both", expand=True)

frame_footer = tk.Frame(ventana, bg="#f4f6fa")
frame_footer.pack(fill="x", padx=20, pady=(0, 5))

lbl_total = tk.Label(frame_footer, text="", font=("Arial", 10, "bold"), bg="#f4f6fa")
lbl_total.pack(side="left")

tk.Label(frame_footer, text="■ Rojo = sin stock   ■ Amarillo = stock bajo (≤ 5)",
         font=("Arial", 9), bg="#f4f6fa", fg="#555").pack(side="right")

tk.Button(ventana, text="Cerrar", width=15, bg="#111827", fg="white",
          command=ventana.destroy).pack(pady=5)

cargar_tabla()
ventana.mainloop()

import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

BASE = os.path.dirname(__file__)

PANTALLAS = {
    "Clientes":    os.path.join(BASE, "abm_clientes.py"),
    "Proveedores": os.path.join(BASE, "abm_proveedores.py"),
    "Productos":   os.path.join(BASE, "abm_productos.py"),
    "Facturación": os.path.join(BASE, "abm_factura.py"),
}

def abrir_pantalla(nombre):
    ruta = PANTALLAS[nombre]
    if not os.path.exists(ruta):
        messagebox.showinfo("Información", f"Sección {nombre} no programada.")
        return
    subprocess.Popen([sys.executable, ruta], cwd=BASE)

ventana = tk.Tk()
ventana.title("Menú Principal")
ventana.geometry("500x560")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

tk.Label(ventana, text="SISTEMA DE GESTIÓN", font=("Arial", 22, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=(30, 5))
tk.Label(ventana, text="Menú de Entidades", font=("Arial", 13), bg="#f4f6fa", fg="#475569").pack(pady=(0, 25))

frame_menu = tk.Frame(ventana, bg="white", padx=30, pady=30, relief="ridge", borderwidth=1)
frame_menu.place(x=60, y=130, width=380, height=350)

for i, (texto, color) in enumerate([
    ("Clientes", "#2563EB"),
    ("Proveedores", "#16A34A"),
    ("Productos", "#9333EA"),
    ("Facturación", "#EA580C"),
]):
    tk.Button(frame_menu, text=texto, width=22, height=2, bg=color, fg="white",
              font=("Arial", 12, "bold"), command=lambda t=texto: abrir_pantalla(t)).grid(row=i, column=0, pady=8)

tk.Button(ventana, text="Salir", width=15, bg="#111827", fg="white",
          font=("Arial", 10, "bold"), command=ventana.destroy).pack(side="bottom", pady=20)

ventana.mainloop()

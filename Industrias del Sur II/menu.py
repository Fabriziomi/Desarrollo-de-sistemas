import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def abrir(nombre):
    subprocess.Popen([sys.executable, os.path.join(BASE, nombre)])

ventana = tk.Tk()
ventana.title("Industrias del Sur")
ventana.geometry("400x510")
ventana.resizable(False, False)
ventana.configure(bg="#f4f6fa")

tk.Label(ventana, text="INDUSTRIAS DEL SUR", font=("Arial", 20, "bold"), bg="#f4f6fa", fg="#172033").pack(pady=20)
tk.Label(ventana, text="Sistema de Gestión Comercial", font=("Arial", 11), bg="#f4f6fa", fg="#555").pack()
tk.Label(ventana, text="Rubro Textil", font=("Arial", 10, "italic"), bg="#f4f6fa", fg="#888").pack(pady=(2, 20))

botones = [
    ("Gestión de Clientes",    "abm_clientes.py",    "#2563EB"),
    ("Gestión de Proveedores", "abm_proveedores.py",  "#2563EB"),
    ("Gestión de Productos",   "abm_productos.py",    "#2563EB"),
    ("Compras",                "compras.py",           "#7C3AED"),
    ("Ventas / Facturación",   "ventas.py",            "#EA580C"),
    ("Consulta de Stock",      "stock.py",             "#059669"),
]

for texto, archivo, color in botones:
    tk.Button(ventana, text=texto, width=28, height=2, bg=color, fg="white",
              font=("Arial", 10, "bold"),
              command=lambda a=archivo: abrir(a)).pack(pady=5)

def salir():
    if messagebox.askyesno("Salir", "¿Desea salir del sistema?"):
        ventana.destroy()

tk.Button(ventana, text="Salir", width=28, height=2, bg="#111827", fg="white",
          font=("Arial", 10, "bold"), command=salir).pack(pady=(12, 0))

ventana.mainloop()

import tkinter as tk
import mysql.connector
from tkinter import messagebox
from tkinter import ttk

conexion = None
cursor = None
tabla = None

def conectar_bd():
    global conexion, cursor, tabla
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2025000",
            database="base_ejemplo"
        )
        conexion.autocommit = True
        cursor = conexion.cursor()
        recargar_tabla(tabla)
        conexion.commit()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar con MySQL: {err}")

def start_transaction():
    global conexion
    if conexion:
        conexion.start_transaction()
        combobox.config(state="disabled")
        messagebox.showinfo("Transacción", "Transacción iniciada")

def insertar_usuario():
    global cursor, tabla
    nombre = entry_nombre.get()

    if not nombre:
        messagebox.showerror("Error", "El campo nombre es obligatorio")
        return

    try:
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        messagebox.showinfo("Insertado", f"'{nombre}' insertado dentro de la transaccion")
        recargar_tabla(tabla)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar: {err}")

    entry_nombre.delete(0, tk.END)

def commit_transaction():
    global conexion, cursor
    try:
        conexion.commit()
        combobox.config(state="normal")
        messagebox.showinfo("Commit", "Transacción confirmada")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer commit: {err}")

def rollback_transaction():
    global conexion, cursor, tabla
    try:
        conexion.rollback()
        messagebox.showinfo("Rollback", "Transacción cancelada")
        recargar_tabla(tabla)
        combobox.config(state="normal")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer rollback: {err}")

def combobox_aislamiento(event):
    global conexion, cursor
    nivelelegido = combobox.get()
    try:
        cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {nivelelegido}")
        messagebox.showinfo(nivelelegido, f"Nivel de aislamiento establecido a {nivelelegido}")
    
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al intentar establecer el nivel de aislamineto {err}")

def recargar_tabla(tabla_tk):
    global cursor
    try:
        cursor.execute("SELECT * FROM usuarios")
        result = cursor.fetchall()
        for row in result:
            tabla_tk.insert("", "end", values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al recargar tabla: {err}")

def actualizar_dato(id, nuevo_nombre):
    global cursor, tabla
    nombre = entry_nombre.get()

    if not nombre:
        messagebox.showerror("Error", "El campo nombre es obligatorio")
        return

    try:
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        messagebox.showinfo("Insertado", f"'{nombre}' insertado dentro de la transaccion")
        recargar_tabla(tabla)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar: {err}")

    entry_nombre.delete(0, tk.END)

root = tk.Tk()
root.title("Formulario de Usuarios")

tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Nuevo nombre:").grid(row=1, column=0, padx=10, pady=5)
entry_actualizar = tk.Entry(root)
entry_actualizar.grid(row=1, column=1, padx=10, pady=5)

opciones = ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
combobox = ttk.Combobox(root, values=opciones, state="readonly")
combobox.set("Selecciona una opción") 
combobox.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

combobox.bind("<<ComboboxSelected>>", combobox_aislamiento)

btn_update = tk.Button(root, text="Actualizar", command=lambda: actualizar_dato(2, entry_actualizar.get()))
btn_update.grid(row=1, column=2, columnspan=2, pady=5)

btn_start = tk.Button(root, text="Start", command=start_transaction)
btn_start.grid(row=1, column=0, columnspan=2, pady=5)

btn_insertar = tk.Button(root, text="Insertar", command=insertar_usuario)
btn_insertar.grid(row=2, column=0, columnspan=2, pady=5)

btn_commit = tk.Button(root, text="Commit", command=commit_transaction)
btn_commit.grid(row=3, column=0, columnspan=2, pady=5)

btn_rollback = tk.Button(root, text="Rollback", command=rollback_transaction)
btn_rollback.grid(row=4, column=0, columnspan=2, pady=5)

tabla = ttk.Treeview(root, columns=("ID", "Nombre"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

btn_recargar = tk.Button(root, text="Recargar tabla", command=lambda: recargar_tabla(tabla))
btn_recargar.grid(row=5, column=0, columnspan=2, pady=5)

conectar_bd()

root.mainloop()



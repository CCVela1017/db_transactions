import tkinter as tk
import mysql.connector
from tkinter import messagebox

conexion = None
cursor = None

def conectar_bd():
    global conexion, cursor
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="2025000",
            database="base_ejemplo"
        )
        cursor = conexion.cursor()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al conectar con MySQL: {err}")

def start_transaction():
    global conexion
    conectar_bd()
    if conexion:
        conexion.start_transaction()
        messagebox.showinfo("Transacción", "Transacción iniciada")

def insertar_usuario():
    global cursor
    nombre = entry_nombre.get()

    if not nombre:
        messagebox.showerror("Error", "El campo nombre es obligatorio")
        return

    try:
        cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
        messagebox.showinfo("Insertado", f"'{nombre}' insertado dentro de la transaccion")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al insertar: {err}")

    entry_nombre.delete(0, tk.END)

def commit_transaction():
    global conexion, cursor
    try:
        conexion.commit()
        messagebox.showinfo("Commit", "Transacción confirmada")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer commit: {err}")
    finally:
        cursor.close()
        conexion.close()

def rollback_transaction():
    global conexion, cursor
    try:
        conexion.rollback()
        messagebox.showinfo("Rollback", "Transacción cancelada")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer rollback: {err}")
    finally:
        cursor.close()
        conexion.close()

root = tk.Tk()
root.title("Formulario de Usuarios")

tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)

btn_start = tk.Button(root, text="Start", command=start_transaction)
btn_start.grid(row=1, column=0, columnspan=2, pady=5)

btn_insertar = tk.Button(root, text="Insertar", command=insertar_usuario)
btn_insertar.grid(row=2, column=0, columnspan=2, pady=5)

btn_commit = tk.Button(root, text="Commit", command=commit_transaction)
btn_commit.grid(row=3, column=0, columnspan=2, pady=5)

btn_rollback = tk.Button(root, text="Rollback", command=rollback_transaction)
btn_rollback.grid(row=4, column=0, columnspan=2, pady=5)

root.mainloop()

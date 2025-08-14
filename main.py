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
            password="Brandon12345678",
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
        try:
            cursor.execute(f"SET TRANSACTION ISOLATION LEVEL {combobox.get()}")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al establecer nivel de aislamiento: {err}")
            return
        conexion.start_transaction()
        combobox.config(state="disabled")
        btn_commit.config(state="normal")
        btn_rollback.config(state="normal")
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
        btn_commit.config(state="disabled")
        btn_rollback.config(state="disabled")
        recargar_tabla(tabla)
        messagebox.showinfo("Commit", "Transacción confirmada")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer commit: {err}")

def rollback_transaction():
    global conexion, cursor, tabla
    try:
        conexion.rollback()
        combobox.config(state="normal")
        btn_commit.config(state="disabled")
        btn_rollback.config(state="disabled")
        recargar_tabla(tabla)
        messagebox.showinfo("Rollback", "Transacción cancelada")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al hacer rollback: {err}")

def combobox_aislamiento(event):
    nivel = combobox.get()
    messagebox.showinfo("Nivel de aislamiento", f"Seleccionado: {nivel}")

def recargar_tabla(tabla_tk):
    global cursor
    try:
        tabla_tk.delete(*tabla_tk.get_children())
        cursor.execute("SELECT * FROM usuarios")
        result = cursor.fetchall()
        for row in result:
            tabla_tk.insert("", "end", values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al recargar tabla: {err}")

def actualizar_dato_seleccionado():
    selected = tabla.selection()
    if not selected:
        messagebox.showerror("Error", "Debes seleccionar un registro de la tabla")
        return
    item = tabla.item(selected[0])
    id_seleccionado = item["values"][0]
    nuevo_nombre = entry_actualizar.get()
    if not nuevo_nombre:
        messagebox.showerror("Error", "El campo nuevo nombre es obligatorio")
        return
    try:
        cursor.execute("UPDATE usuarios SET nombre = %s WHERE id = %s", (nuevo_nombre, id_seleccionado))
        recargar_tabla(tabla)
        messagebox.showinfo("Actualizado", f"ID {id_seleccionado} actualizado a '{nuevo_nombre}'")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al actualizar: {err}")
    entry_actualizar.delete(0, tk.END)


root = tk.Tk()
root.title("Formulario de Usuarios")

tk.Label(root, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1, padx=10, pady=5)
btn_insertar = tk.Button(root, text="Insertar", command=insertar_usuario)
btn_insertar.grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Nuevo nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_actualizar = tk.Entry(root)
entry_actualizar.grid(row=1, column=1, padx=10, pady=5)
btn_update = tk.Button(root, text="Actualizar", command=actualizar_dato_seleccionado)
btn_update.grid(row=1, column=2, padx=10, pady=5)

opciones = ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
tk.Label(root, text="Nivel de aislamiento:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
combobox = ttk.Combobox(root, values=opciones, state="readonly")
combobox.set("Selecciona una opción")
combobox.grid(row=2, column=1, padx=10, pady=5)
combobox.bind("<<ComboboxSelected>>", combobox_aislamiento)

btn_start = tk.Button(root, text="Start", command=start_transaction)
btn_start.grid(row=3, column=0, padx=10, pady=5)
btn_commit = tk.Button(root, text="Commit", command=commit_transaction, state="disabled")
btn_commit.grid(row=3, column=1, padx=10, pady=5)
btn_rollback = tk.Button(root, text="Rollback", command=rollback_transaction, state="disabled")
btn_rollback.grid(row=3, column=2, padx=10, pady=5)

btn_recargar = tk.Button(root, text="Recargar tabla", command=lambda: recargar_tabla(tabla))
btn_recargar.grid(row=4, column=0, columnspan=3, pady=5)


tabla = ttk.Treeview(root, columns=("ID", "Nombre"), show="headings")
tabla.heading("ID", text="ID")
tabla.heading("Nombre", text="Nombre")
tabla.grid(row=5, column=0, columnspan=3, padx=10, pady=10)


conectar_bd()

root.mainloop()



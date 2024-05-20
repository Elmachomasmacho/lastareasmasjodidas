import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime

# Conexión a la base de datos MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="presenteono"
    )

# Función para insertar un nuevo alumno
def add_student():
    name = entry_name.get()
    class_name = entry_class.get()

    if not name or not class_name:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        sql = "INSERT INTO estudiante (nombre,grado) VALUES (%s, %s)"
        cursor.execute(sql, (name, class_name))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Alumno agregado correctamente")
        entry_name.delete(0, tk.END)
        entry_class.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar alumno: {err}")

# Función para registrar asistencia
def add_attendance():
    student_id = entry_student_id.get()
    status = entry_status.get()
    date = datetime.now().date()

    if not student_id or not status:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        sql = "INSERT INTO asistencia (llego,fecha,hora) VALUES (%s, %s, %s)"
        cursor.execute(sql, (student_id, date, status))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Asistencia registrada correctamente")
        entry_student_id.delete(0, tk.END)
        entry_status.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al registrar asistencia: {err}")

# Función para consultar alumnos
def view_students():
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        for row in rows:
            tree.insert("", tk.END, values=row)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al consultar alumnos: {err}")

# Función para eliminar un alumno
def delete_student():
    student_id = entry_student_id.get()

    if not student_id:
        messagebox.showwarning("Advertencia", "El campo ID del alumno es obligatorio")
        return

    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        sql = "DELETE FROM students WHERE student_id = %s"
        cursor.execute(sql, (student_id,))
        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Éxito", "Alumno eliminado correctamente")
        entry_student_id.delete(0, tk.END)
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al eliminar alumno: {err}")

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.title("Sistema de Control de Asistencias")

# Sección para agregar alumnos
tk.Label(root, text="Nombre").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Clase").grid(row=1, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=10)
entry_class = tk.Entry(root)
entry_class.grid(row=1, column=1, padx=10, pady=10)
btn_add_student = tk.Button(root, text="Agregar Alumno", command=add_student)
btn_add_student.grid(row=2, columnspan=2, pady=10)

# Sección para registrar asistencia
tk.Label(root, text="ID del Alumno").grid(row=3, column=0, padx=10, pady=10)
tk.Label(root, text="Estado (Presente/Ausente)").grid(row=4, column=0, padx=10, pady=10)
entry_student_id = tk.Entry(root)
entry_student_id.grid(row=3, column=1, padx=10, pady=10)
entry_status = tk.Entry(root)
entry_status.grid(row=4, column=1, padx=10, pady=10)
btn_add_attendance = tk.Button(root, text="Registrar Asistencia", command=add_attendance)
btn_add_attendance.grid(row=5, columnspan=2, pady=10)

# Sección para consultar alumnos
btn_view_students = tk.Button(root, text="Consultar Alumnos", command=view_students)
btn_view_students.grid(row=6, columnspan=2, pady=10)

# Sección para eliminar alumnos
btn_delete_student = tk.Button(root, text="Eliminar Alumno", command=delete_student)
btn_delete_student.grid(row=7, columnspan=2, pady=10)

# Tabla para mostrar alumnos
columns = ("ID", "Nombre", "Clase")
tree = ttk.Treeview(root, columns=columns, show="headings")
tree.heading("ID", text="ID")
tree.heading("Nombre", text="Nombre")
tree.heading("Clase", text="Clase")
tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()

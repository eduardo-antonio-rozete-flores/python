import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Material:
    def __init__(self, titulo, estado="disponible"):
        self.titulo = titulo
        self.estado = estado

class Libro(Material):
    def __init__(self, titulo, autor, genero, estado="disponible"):
        super().__init__(titulo, estado)
        self.autor = autor
        self.genero = genero

class Revista(Material):
    def __init__(self, titulo, edicion, periodicidad, estado="disponible"):
        super().__init__(titulo, estado)
        self.edicion = edicion
        self.periodicidad = periodicidad

class MaterialDigital(Material):
    def __init__(self, titulo, tipo_archivo, enlace_descarga):
        super().__init__(titulo, "disponible")
        self.tipo_archivo = tipo_archivo
        self.enlace_descarga = enlace_descarga

class Persona:
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

class Usuario(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)
        self.materiales_prestados = []

class Bibliotecario(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)

class Sucursal:
    def __init__(self, nombre):
        self.nombre = nombre
        self.catalogo = []

class Prestamo:
    def __init__(self, usuario, material, fecha_prestamo, fecha_devolucion):
        self.usuario = usuario
        self.material = material
        self.fecha_prestamo = fecha_prestamo
        self.fecha_devolucion = fecha_devolucion
        self.devuelto = False

class Penalizacion:
    def __init__(self, usuario, monto, fecha):
        self.usuario = usuario
        self.monto = monto
        self.fecha = fecha

class Catalogo:
    def __init__(self):
        self.sucursales = []

class BibliotecaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Biblioteca")

        self.catalogo = [
            Libro("El rey Misterio", "Autor A", "terror"),
            Libro("El Futuro Es Ahora", "Autor B", "ciencia ficción"),
            Libro("Amor y Destino Final", "Autor C", "romance")
        ]
        self.prestamos = []

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Bienvenido al Sistema de Biblioteca", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Bibliotecario", command=self.mostrar_login_bibliotecario).pack(pady=5)
        ttk.Button(self.root, text="Usuario", command=self.mostrar_menu_usuario).pack(pady=5)

    def mostrar_login_bibliotecario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Ingrese la clave", font=("Arial", 12)).pack(pady=5)
        self.clave_entry = ttk.Entry(self.root, show="*")
        self.clave_entry.pack(pady=5)

        ttk.Button(self.root, text="Ingresar", command=self.validar_clave).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def validar_clave(self):
        if self.clave_entry.get() == "1234":
            self.mostrar_menu_bibliotecario()
        else:
            messagebox.showerror("Error", "Clave incorrecta")

    def mostrar_menu_bibliotecario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Bibliotecario", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Agregar Material", command=self.agregar_material).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def mostrar_menu_usuario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Usuario", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Consultar Catálogo", command=self.consultar_catalogo).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def agregar_material(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Material")

        ttk.Label(add_window, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        titulo_entry = ttk.Entry(add_window)
        titulo_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Autor:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        autor_entry = ttk.Entry(add_window)
        autor_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Género:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        genero_combo = ttk.Combobox(add_window, values=["terror", "ciencia ficción", "romance"], state="readonly")
        genero_combo.grid(row=2, column=1, padx=5, pady=5)

        def guardar_material():
            titulo = titulo_entry.get().strip()
            autor = autor_entry.get().strip()
            genero = genero_combo.get().strip()

            if not titulo or not autor or not genero:
                messagebox.showerror("Error", "Todos los campos son obligatorios", parent=add_window)
                return

            nuevo_libro = Libro(titulo, autor, genero)
            self.catalogo.append(nuevo_libro)
            messagebox.showinfo("Éxito", "Material agregado correctamente", parent=add_window)
            add_window.destroy()

        ttk.Button(add_window, text="Agregar", command=guardar_material).grid(row=3, column=0, columnspan=2, pady=10)

    def consultar_catalogo(self):
        consult_window = tk.Toplevel(self.root)
        consult_window.title("Consultar Catálogo")

        ttk.Label(consult_window, text="Nombre:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        nombre_entry = ttk.Entry(consult_window)
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(consult_window, text="Identificación:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        identificacion_entry = ttk.Entry(consult_window)
        identificacion_entry.grid(row=1, column=1, padx=5, pady=5)

        listbox = tk.Listbox(consult_window, width=60)
        listbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        for idx, libro in enumerate(self.catalogo):
            listbox.insert(tk.END, f"{idx+1}. {libro.titulo} - {libro.autor} - {libro.genero} ({libro.estado})")

        def pedir_prestamo():
            try:
                selected_index = listbox.curselection()[0]
            except IndexError:
                messagebox.showerror("Error", "Seleccione un libro", parent=consult_window)
                return

            nombre = nombre_entry.get().strip()
            identificacion = identificacion_entry.get().strip()
            if not nombre or not identificacion:
                messagebox.showerror("Error", "Ingrese nombre e identificación", parent=consult_window)
                return

            libro = self.catalogo[selected_index]
            if libro.estado != "disponible":
                messagebox.showerror("Error", "El libro no está disponible para préstamo", parent=consult_window)
                return

            libro.estado = "prestado"
            fecha_prestamo = datetime.date.today()
            fecha_devolucion = fecha_prestamo + datetime.timedelta(days=7)

            usuario = Usuario(nombre, identificacion)
            usuario.materiales_prestados.append(libro)

            prestamo = Prestamo(usuario, libro, fecha_prestamo, fecha_devolucion)
            self.prestamos.append(prestamo)

            messagebox.showinfo("Préstamo Exitoso", f"Libro prestado.\nFecha de devolución: {fecha_devolucion}", parent=consult_window)

            listbox.delete(selected_index)
            listbox.insert(selected_index, f"{selected_index+1}. {libro.titulo} - {libro.autor} - {libro.genero} ({libro.estado})")

        ttk.Button(consult_window, text="Pedir Préstamo", command=pedir_prestamo).grid(row=3, column=0, columnspan=2, pady=10)

# Crear ventana principal
root = tk.Tk()
app = BibliotecaGUI(root)
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class Persona:
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

class Usuario(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)
        self.reservas = []

class Empleado(Persona):
    def __init__(self, nombre, identificacion, rol):
        super().__init__(nombre, identificacion)
        self.rol = rol

class Espacio:
    def __init__(self, nombre):
        self.nombre = nombre

class Sala(Espacio):
    def __init__(self, nombre, tipo, capacidad):
        super().__init__(nombre)
        self.tipo = tipo
        self.capacidad = capacidad
        self.funciones = []

class ZonaComida(Espacio):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.productos = []

class Pelicula:
    def __init__(self, titulo, duracion, clasificacion, genero):
        self.titulo = titulo
        self.duracion = duracion
        self.clasificacion = clasificacion
        self.genero = genero

class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento

class Funcion:
    def __init__(self, pelicula, sala, horario):
        self.pelicula = pelicula
        self.sala = sala
        self.horario = horario
        self.asientos_ocupados = set()

class Reserva:
    def __init__(self, usuario, funcion, asientos, promocion=None):
        self.usuario = usuario
        self.funcion = funcion
        self.asientos = asientos
        self.promocion = promocion
        funcion.asientos_ocupados.update(asientos)
        usuario.reservas.append(self)

class CineGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Reservas de Cine")

        self.peliculas = [
            Pelicula("Acción Total", 120, "PG-13", "Acción"),
            Pelicula("Terror Nocturno", 100, "R", "Terror")
        ]

        self.salas = [
            Sala("Sala 1", "2D", 100),
            Sala("Sala 2", "3D", 80)
        ]

        self.funciones = []
        self.usuarios = [Usuario("Juan Pérez", "12345")]

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Bienvenido al Sistema de Reservas de Cine", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Empleado", command=self.mostrar_menu_empleado).pack(pady=5)
        ttk.Button(self.root, text="Usuario", command=self.mostrar_menu_usuario).pack(pady=5)

    def mostrar_menu_empleado(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Empleado", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Agregar Función", command=self.agregar_funcion).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def mostrar_menu_usuario(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Usuario", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Hacer Reserva", command=self.hacer_reserva).pack(pady=5)
        ttk.Button(self.root, text="Cancelar Reserva", command=self.cancelar_reserva).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def agregar_funcion(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Agregar Función")

        ttk.Label(add_window, text="Película:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        pelicula_combo = ttk.Combobox(add_window, values=[p.titulo for p in self.peliculas], state="readonly")
        pelicula_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Sala:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        sala_combo = ttk.Combobox(add_window, values=[s.nombre for s in self.salas], state="readonly")
        sala_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_window, text="Horario (HH:MM):").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        horario_entry = ttk.Entry(add_window)
        horario_entry.grid(row=2, column=1, padx=5, pady=5)

        def guardar_funcion():
            pelicula_titulo = pelicula_combo.get()
            sala_nombre = sala_combo.get()
            horario = horario_entry.get()

            if not pelicula_titulo or not sala_nombre or not horario:
                messagebox.showerror("Error", "Todos los campos son obligatorios", parent=add_window)
                return

            pelicula = next((p for p in self.peliculas if p.titulo == pelicula_titulo), None)
            sala = next((s for s in self.salas if s.nombre == sala_nombre), None)

            if not pelicula or not sala:
                messagebox.showerror("Error", "Película o Sala no válida", parent=add_window)
                return

            nueva_funcion = Funcion(pelicula, sala, horario)
            sala.funciones.append(nueva_funcion)
            self.funciones.append(nueva_funcion)
            messagebox.showinfo("Éxito", "Función agregada correctamente", parent=add_window)
            add_window.destroy()

        ttk.Button(add_window, text="Agregar", command=guardar_funcion).grid(row=3, column=0, columnspan=2, pady=10)

    def hacer_reserva(self):
        reserva_window = tk.Toplevel(self.root)
        reserva_window.title("Hacer Reserva")

        if not self.funciones:
            messagebox.showinfo("No hay funciones", "Actualmente no hay funciones disponibles")
            return

        ttk.Label(reserva_window, text="Selecciona una función:").pack(pady=5)
        funciones_combo = ttk.Combobox(reserva_window, values=[f"{f.pelicula.titulo} - {f.horario}" for f in self.funciones], state="readonly")
        funciones_combo.pack(pady=5)

        ttk.Label(reserva_window, text="Número de asientos:").pack(pady=5)
        asientos_entry = ttk.Entry(reserva_window)
        asientos_entry.pack(pady=5)

        def confirmar_reserva():
            funcion_index = funciones_combo.current()
            if funcion_index == -1:
                messagebox.showerror("Error", "Selecciona una función", parent=reserva_window)
                return

            try:
                num_asientos = int(asientos_entry.get())
                if num_asientos <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", "Número de asientos inválido", parent=reserva_window)
                return

            funcion = self.funciones[funcion_index]
            asientos_disponibles = set(range(funcion.sala.capacidad)) - funcion.asientos_ocupados

            if num_asientos > len(asientos_disponibles):
                messagebox.showerror("Error", "No hay suficientes asientos disponibles", parent=reserva_window)
                return

            asientos_reservados = set(list(asientos_disponibles)[:num_asientos])
            Reserva(self.usuarios[0], funcion, asientos_reservados)
            messagebox.showinfo("Éxito", "Reserva realizada correctamente", parent=reserva_window)
            reserva_window.destroy()

        ttk.Button(reserva_window, text="Confirmar Reserva", command=confirmar_reserva).pack(pady=10)

    def cancelar_reserva(self):
        usuario = self.usuarios[0]
        if not usuario.reservas:
            messagebox.showinfo("Cancelación", "No tienes reservas para cancelar")
            return

        reserva = usuario.reservas.pop()
        reserva.funcion.asientos_ocupados.difference_update(reserva.asientos)
        messagebox.showinfo("Cancelación", "Tu reserva ha sido cancelada correctamente")

if __name__ == "__main__":
    root = tk.Tk()
    app = CineGUI(root)
    root.mainloop()

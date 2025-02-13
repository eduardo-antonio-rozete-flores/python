import tkinter as tk
from tkinter import ttk, messagebox

# Clases
class Persona:
    def __init__(self, nombre, identificacion):
        self.nombre = nombre
        self.identificacion = identificacion

class Cliente(Persona):
    def __init__(self, nombre, identificacion):
        super().__init__(nombre, identificacion)
        self.historial_pedidos = []

    def realizar_pedido(self, pedido):
        self.historial_pedidos.append(pedido)

class Empleado(Persona):
    def __init__(self, nombre, identificacion, rol):
        super().__init__(nombre, identificacion)
        self.rol = rol

class ProductoBase:
    def __init__(self, nombre, precio, ingredientes):
        self.nombre = nombre
        self.precio = precio
        self.ingredientes = ingredientes

class Bebida(ProductoBase):
    def __init__(self, nombre, precio, ingredientes, tipo, tamano, personalizaciones=None):
        super().__init__(nombre, precio, ingredientes)
        self.tipo = tipo  # caliente o fría
        self.tamano = tamano
        self.personalizaciones = personalizaciones if personalizaciones else []

class Postre(ProductoBase):
    def __init__(self, nombre, precio, ingredientes, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio, ingredientes)
        self.vegano = vegano
        self.sin_gluten = sin_gluten

class Inventario:
    def __init__(self):
        self.ingredientes = {
            "leche": 10,
            "azucar": 10,
            "almendra": 10,
            "harina": 10,
            "cafe": 10
        }

    def verificar_stock(self, ingredientes):
        for ingrediente in ingredientes:
            if self.ingredientes.get(ingrediente, 0) <= 0:
                return False
        return True

    def actualizar_stock(self, ingredientes):
        for ingrediente in ingredientes:
            if self.ingredientes.get(ingrediente):
                self.ingredientes[ingrediente] -= 1

class Pedido:
    def __init__(self, cliente, productos):
        self.cliente = cliente
        self.productos = productos
        self.estado = "Pendiente"
        self.total = sum([producto.precio for producto in productos])

class Promocion:
    def __init__(self, descripcion, descuento):
        self.descripcion = descripcion
        self.descuento = descuento

    def aplicar_descuento(self, pedido):
        pedido.total -= pedido.total * (self.descuento / 100)

# Interfaz gráfica
class CafeteriaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Pedidos en Cafetería")

        self.inventario = Inventario()

        self.productos = [
            Bebida("Café", 5, ["cafe", "leche"], "caliente", "mediano"),
            Bebida("Café con Almendra", 6, ["cafe", "almendra"], "fría", "grande"),
            Postre("Pastel de Chocolate", 3, ["harina", "azucar"], vegano=True)
        ]

        self.clientes = [Cliente("Juan Pérez", "12345")]
        self.empleados = [Empleado("María López", "98765", "Barista")]

        self.mostrar_pantalla_inicio()

    def mostrar_pantalla_inicio(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Bienvenido al Sistema de Pedidos de Cafetería", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Cliente", command=self.mostrar_menu_cliente).pack(pady=5)
        ttk.Button(self.root, text="Empleado", command=self.mostrar_menu_empleado).pack(pady=5)

    def mostrar_menu_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Cliente", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Realizar Pedido", command=self.realizar_pedido_cliente).pack(pady=5)
        ttk.Button(self.root, text="Consultar Historial de Pedidos", command=self.consultar_historial).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def mostrar_menu_empleado(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        ttk.Label(self.root, text="Menú Empleado", font=("Arial", 14)).pack(pady=10)
        ttk.Button(self.root, text="Actualizar Inventario", command=self.actualizar_inventario).pack(pady=5)
        ttk.Button(self.root, text="Volver", command=self.mostrar_pantalla_inicio).pack(pady=5)

    def realizar_pedido_cliente(self):
        cliente = self.clientes[0]
        pedido_window = tk.Toplevel(self.root)
        pedido_window.title("Realizar Pedido")

        ttk.Label(pedido_window, text="Seleccione un producto:").grid(row=0, column=0, padx=5, pady=5)
        productos_combo = ttk.Combobox(pedido_window, values=[p.nombre for p in self.productos], state="readonly")
        productos_combo.grid(row=0, column=1, padx=5, pady=5)

        def confirmar_pedido():
            producto_index = productos_combo.current()
            if producto_index == -1:
                messagebox.showerror("Error", "Seleccione un producto", parent=pedido_window)
                return

            producto = self.productos[producto_index]
            if not self.inventario.verificar_stock(producto.ingredientes):
                messagebox.showerror("Error", "No hay suficiente stock para este pedido", parent=pedido_window)
                return

            self.inventario.actualizar_stock(producto.ingredientes)
            pedido = Pedido(cliente, [producto])
            cliente.realizar_pedido(pedido)

            messagebox.showinfo("Éxito", f"Pedido realizado. Total: ${pedido.total}", parent=pedido_window)
            pedido_window.destroy()

        ttk.Button(pedido_window, text="Confirmar Pedido", command=confirmar_pedido).grid(row=1, column=0, columnspan=2, pady=10)

    def consultar_historial(self):
        cliente = self.clientes[0]
        historial_window = tk.Toplevel(self.root)
        historial_window.title("Historial de Pedidos")

        if not cliente.historial_pedidos:
            messagebox.showinfo("Historial", "No tienes pedidos realizados aún.")
            return

        for idx, pedido in enumerate(cliente.historial_pedidos):
            ttk.Label(historial_window, text=f"Pedido {idx+1}: ${pedido.total} - {pedido.estado}").pack(pady=5)

    def actualizar_inventario(self):
        empleado = self.empleados[0]
        inventario_window = tk.Toplevel(self.root)
        inventario_window.title("Actualizar Inventario")

        ttk.Label(inventario_window, text="Ingrese ingrediente a actualizar:").grid(row=0, column=0, padx=5, pady=5)
        ingrediente_entry = ttk.Entry(inventario_window)
        ingrediente_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(inventario_window, text="Cantidad:").grid(row=1, column=0, padx=5, pady=5)
        cantidad_entry = ttk.Entry(inventario_window)
        cantidad_entry.grid(row=1, column=1, padx=5, pady=5)

        def actualizar():
            ingrediente = ingrediente_entry.get().strip()
            cantidad = cantidad_entry.get().strip()

            if not ingrediente or not cantidad.isdigit():
                messagebox.showerror("Error", "Por favor ingrese un ingrediente y una cantidad válida", parent=inventario_window)
                return

            cantidad = int(cantidad)
            if ingrediente in self.inventario.ingredientes:
                self.inventario.ingredientes[ingrediente] += cantidad
                messagebox.showinfo("Éxito", f"Inventario actualizado. {ingrediente}: {self.inventario.ingredientes[ingrediente]}", parent=inventario_window)
                inventario_window.destroy()

        ttk.Button(inventario_window, text="Actualizar Inventario", command=actualizar).grid(row=2, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeteriaGUI(root)
    root.mainloop()

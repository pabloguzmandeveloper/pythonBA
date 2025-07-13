import re

## Aplicación de Mercadito Casero Atlas
## Implementación orientada a objetos

class Producto:
    def __init__(self, nombre, precio, cantidad):
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad

class MercaditoAtlas:
    def __init__(self):
        self.productos = []
        self.running = True

    def mostrar_menu(self):
        menu = """
        Bienvenido al Mercadito Casero Atlas!!!

        Elige una opción para continuar:
        1. Agregar Producto
        2. Mostrar Productos
        3. Buscar Producto
        4. Eliminar Producto
        5. Salir
        >>>>>>>>>
        """
        print(menu)
        return input("Seleccione una opción: ")

    def agregar_producto(self):
        while True:
            print("\n=== Agregar Nuevo Producto ===")
            print("Ingrese 'm' para volver al menu principal")
            accion = input("\nDesea agregar producto presione Enter: ").upper()
            if accion == "M":
                return # salir del bucle con enter
            else:
                nombre = input("Ingrese el nombre del producto: ")
                precio = float(input("Ingrese el precio del producto: "))
                cantidad = int(input("Ingrese la cantidad disponible: "))
            
            nuevo_producto = Producto(nombre, precio, cantidad)
            self.productos.append(nuevo_producto)
            print("\n¡Producto agregado exitosamente!")
            input("\nPresione Enter para continuar...")

    def mostrar_productos(self):
        print("\n=== Lista de Productos ===")
        if not self.productos:
            print("No hay productos registrados.")
        else:
            for i, producto in enumerate(self.productos, 1):
                print(f"{i}. {producto.nombre} - Precio: ${producto.precio} - Cantidad: {producto.cantidad}")
        input("\nPresione Enter para continuar...")

    def buscar_producto(self):
        while True:
            print("\n=== Buscar Producto ===")
            accion = input("""\nIngrese 'm' para volver al menu principal,\no presione Enter para buscar productos: """).upper()
            if accion == "M":
                return # salir del bucle con enter
            else:
                nombre_buscar = input("""\nIngrese al menos 3 letras del producto a buscar: """)
                
                if len(nombre_buscar) < 3:
                    print("\nPor favor, ingrese al menos 3 letras para buscar.")
                    input("\nPresione Enter para continuar...")
                    return
                
                # Creamos un patrón que busca 3 o más letras consecutivas en cualquier parte del nombre
                patron = re.compile(nombre_buscar, re.IGNORECASE)
                
                # Buscamos coincidencias parciales
                encontrados = [
                    p for p in self.productos 
                    if patron.search(p.nombre)
                ]
                
                # También podemos buscar coincidencias similares
                if not encontrados:
                    # Si no hay coincidencias exactas, buscamos similitudes
                    encontrados = [
                        p for p in self.productos 
                        if any(
                            re.search(f"{parte}", p.nombre.lower()) 
                            for parte in nombre_buscar.lower().split()
                        )
                    ]
                
                if encontrados:
                    print("\nProductos encontrados:")
                    for producto in encontrados:
                        # Resaltamos la parte que coincide
                        nombre_resaltado = patron.sub(
                            lambda m: f"[{m.group()}]", 
                            producto.nombre
                        )
                        print(f"Nombre: {nombre_resaltado} - Precio: ${producto.precio} - Cantidad: {producto.cantidad}")
                else:
                    print("\nNo se encontraron productos con ese nombre.")
                    print("Sugerencia: Intente con una parte más corta del nombre")
                
                input("\nPresione Enter para continuar...")

    def eliminar_producto(self):
        print("\n=== Eliminar Producto ===")
        if not self.productos:
            print("No hay productos para eliminar.")
            input("\nPresione Enter para continuar...")
            return

        print("Productos disponibles:")
        for i, producto in enumerate(self.productos, 1):
            print(f"{i}. {producto.nombre}")
        
        try:
            indice = int(input("\nIngrese el número del producto a eliminar: ")) - 1
            if 0 <= indice < len(self.productos):
                producto_eliminado = self.productos.pop(indice)
                print(f"\nProducto '{producto_eliminado.nombre}' eliminado exitosamente.")
            else:
                print("\nNúmero de producto inválido.")
        except ValueError:
            print("\nPor favor, ingrese un número válido.")
        input("\nPresione Enter para continuar...")

    def ejecutar(self):
        while self.running:
            opcion = self.mostrar_menu()
            
            if opcion == "1":
                self.agregar_producto()
            elif opcion == "2":
                self.mostrar_productos()
            elif opcion == "3":
                self.buscar_producto()
            elif opcion == "4":
                self.eliminar_producto()
            elif opcion == "5":
                print("\n¡Gracias por usar Mercadito Casero Atlas!")
                self.running = False
            else:
                print("\nOpción inválida. Por favor, intente nuevamente.")
                input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    mercadito = MercaditoAtlas()
    mercadito.ejecutar()

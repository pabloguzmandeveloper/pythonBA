from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Input, Button, Label

class AddProductApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Agregar Nuevo Producto ==="),
            Input(placeholder="Nombre del producto", id="nombre"),
            Input(placeholder="Precio", id="precio"),
            Input(placeholder="Cantidad", id="cantidad"),
            Button("Guardar", id="guardar")
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "guardar":
            nombre = self.query_one("#nombre").value
            precio = self.query_one("#precio").value
            cantidad = self.query_one("#cantidad").value
            self.exit({"nombre": nombre, "precio": precio, "cantidad": cantidad})

if __name__ == "__main__":
    app = AddProductApp()
    resultado = app.run()
    print("\nProducto agregado:", resultado)


class ShowProductsApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Productos ==="),
            Button("Agregar Producto", id="agregar"),
        )
        

class SearchProductApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Buscar Producto ==="),
            Input(placeholder="Nombre del producto", id="nombre"),
            Button("Buscar", id="buscar"),
        )
        

class DeleteProductApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Eliminar Producto ==="),
            Input(placeholder="Nombre del producto", id="nombre"),
            Button("Eliminar", id="eliminar"),
        )

class UpdateProductApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Actualizar Producto ==="),
            Input(placeholder="Nombre del producto", id="nombre"),
            Input(placeholder="Precio", id="precio"),
            Input(placeholder="Cantidad", id="cantidad"),
            Button("Actualizar", id="actualizar"),
        )

class ExitApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("=== Salir ==="),
            Button("Salir", id="salir"),
        )
        

class MenuApp(App):
    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("<<<<< Menú >>>>>"),
            Button("Agregar Producto", id="agregar"),
            Button("Mostrar Productos", id="mostrar"),
            Button("Buscar Producto", id="buscar"),
            Button("Eliminar Producto", id="eliminar"),
            Button("Actualizar Producto", id="actualizar"),
            Button("Salir", id="salir"),
        )
        
 
        
        
        
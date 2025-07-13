from prompt_toolkit import PromptSession
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.validation import Validator, ValidationError

# Crear una sesión de prompt
session = PromptSession()

# Validador para números
class NumberValidator(Validator):
    def validate(self, document):
        text = document.text
        if text and not text.isdigit():
            raise ValidationError(message='Por favor ingrese solo números')

def agregar_producto():
    print("\n=== Agregar Nuevo Producto ===")
    
    # Input con estilo
    nombre = session.prompt(HTML("<ansired>Nombre del producto: </ansired>"))
    
    # Input con validación numérica
    precio = session.prompt(
        HTML("<ansigreen>Precio: </ansigreen>"),
        validator=NumberValidator()
    )
    
    cantidad = session.prompt(
        HTML("<ansiblue>Cantidad: </ansiblue>"),
        validator=NumberValidator()
    )
    
    return {
        "nombre": nombre,
        "precio": float(precio),
        "cantidad": int(cantidad)
    }

if __name__ == "__main__":
    producto = agregar_producto()
    print("\nProducto agregado:", producto)
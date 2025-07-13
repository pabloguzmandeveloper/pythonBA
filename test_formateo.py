# Archivo de prueba - mal formateado a proposito
def funcion_mal_formateada(  param1,param2   ):
    x=param1+param2
    y    =    param1*param2
    if x>y:
        print(   "x es mayor"   )
        resultado=x
    else:
           print("y es mayor")
           resultado=y
    return resultado

class MiClase:
    def __init__(self,nombre):
        self.nombre=nombre
        self.activo=True
    def obtener_nombre(self):
        return self.nombre 
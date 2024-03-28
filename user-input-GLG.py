def solicitar_datos():

    nombre = input("Ingresa tu nombre: ")
    apellido = input("Ingresa tu apellido: ")
    edad = input("Ingresa tu edad: ")
    sede = input("Ingresa tu sede: ")
    
    return nombre, apellido, edad, sede

def imprimir_datos(nombre, apellido, edad, sede):
    print("\nLos datos ingresados son:")
    print("Nombre:", nombre)
    print("Apellido:", apellido)
    print("Edad:", edad)
    print("Sede:", sede)

def main():
    nombre, apellido, edad, sede = solicitar_datos()
    
    imprimir_datos(nombre, apellido, edad, sede)

if __name__ == "__main__":
    main()


import os
class Producto:
    def __init__(self, id, nombre): #Se utiliza para definir una función o un método.
        self.id = id #self es una referencia al objeto actual de la instancia de la clase y se utiliza para acceder a las variables que pertenecen a la clase.
        self.nombre = nombre

class Palet:
    def __init__(self, id):
        self.id = id
        self.producto = None
        self.destino = None

    def cargar_producto(self, producto):
        self.producto = producto

    def definir_destino(self, destino):
        self.destino = destino

class Estanteria:
    def __init__(self): # Es el constructor, Se llama automáticamente cuando se crea una nueva instancia de la clase. Se utiliza para inicializar los atributos de un objeto.
        self.lugares = [[None for _ in range(4)] for _ in range(4)]  #El none nos sirve para llenar con vacio las estanterias de forma inicial

    def posiciones_adyacentes(self, fila, columna):
        adyacentes = [(fila-1, columna), (fila+1, columna), (fila, columna-1), (fila, columna+1)] #Esto crea una lista de tuplas con las coordenadas de las posiciones adyacentes
        return [(f, c) for f, c in adyacentes if 0 <= f < 4 and 0 <= c < 4] #filtra las posiciones adyacentes para asegurarse de que estén dentro de los límites de la estantería. Es decir, no queremos posiciones fuera de nuestra matriz 4x4.

    def puede_agregar_palet(self, fila, columna):
        if self.lugares[fila][columna]:
            return False  # Si la posición ya está ocupada, no se puede agregar un palet aquí
        return True

    def agregar_palet(self, palet):
        for fila in range(4):
            for columna in range(4):
                if not self.lugares[fila][columna] and self.puede_agregar_palet(fila, columna):
                    self.lugares[fila][columna] = palet
                    return (fila, columna)
        return None

    def mostrar_lugares_disponibles(self):
        for fila in range(4):
            for columna in range(4):
                if not self.lugares[fila][columna] and self.puede_agregar_palet(fila, columna):
                    print(f"Lugar disponible en fila {fila + 1}, columna {columna + 1}")

    def mostrar_lugares_no_disponibles(self):
        lugares = []
        for fila in range(4):
            for columna in range(4):
                if self.lugares[fila][columna]:
                    lugares.append(f"Fila {fila + 1}, Columna {columna + 1}")
        return lugares
    
    def obtener_palet_por_id(self, id):
        for fila in range(4):
            for columna in range(4):
                if self.lugares[fila][columna] and self.lugares[fila][columna].id == id:
                    return self.lugares[fila][columna]
        return None
    
    def remover_palet(self, id):
        for fila in range(4):
            for columna in range(4):
                if self.lugares[fila][columna] and self.lugares[fila][columna].id == id:
                    self.lugares[fila][columna] = None
                    return True
        return False


    

class Pasillo:
    def __init__(self, id):
        self.id = id
        self.estanterias = [Estanteria(), Estanteria()]

    def agregar_palet(self, palet):
        for estanteria in self.estanterias:
            posicion = estanteria.agregar_palet(palet)
            if posicion:
                return (self.id, self.estanterias.index(estanteria), posicion)
        return None

    def obtener_palet_por_id(self, id):
        for estanteria in self.estanterias:
            palet = estanteria.obtener_palet_por_id(id)
            if palet:
                return palet
        return None

    def remover_palet(self, id):
        for estanteria in self.estanterias:
            if estanteria.remover_palet(id):
                return True
        return False
    
    def mostrar_lugares_no_disponibles(self):
        for estanteria in self.estanterias:
            lugares = estanteria.mostrar_lugares_no_disponibles() #Esta función de la clase Estanteria devuelve una lista de lugares (en términos de fila y columna) que no están disponibles en esa estantería particular. Asignamos esta lista a la variable lugares.
            for lugar in lugares: #Ahora, para cada lugar en la lista de lugares que no están disponibles, vamos a hacer lo siguiente:
                print(f"Pasillo {self.id}, Estantería {self.estanterias.index(estanteria) + 1}, {lugar}")



class Deposito:
    def __init__(self):
        self.pasillos = [Pasillo(i) for i in range(1, 9)]

    def agregar_palet(self, palet):
        for pasillo in self.pasillos:
            posicion = pasillo.agregar_palet(palet)
            if posicion:
                return posicion
        return None
    
    def palet_existe(self, id):
        for pasillo in self.pasillos:
            palet = pasillo.obtener_palet_por_id(id)
            if palet:
                return True
        return False

    def obtener_palet_por_id(self, id):
        for pasillo in self.pasillos:
            palet = pasillo.obtener_palet_por_id(id)
            if palet:
                return palet
        return None

    def remover_palet(self, id):
        for pasillo in self.pasillos:
            if pasillo.remover_palet(id):
                return True
        return False

    def informe_producto(self, nombre_producto):
        for pasillo in self.pasillos:  # Recorre todos los pasillos del almacén.
            for estanteria in pasillo.estanterias:  # En cada pasillo, verifica cada estantería
                for fila in range(4):  # Dentro de cada estantería, examina cada espacio (fila y columna).
                    for columna in range(4):
                        palet = estanteria.lugares[fila][columna]
                        if palet and palet.id == id_palet:  # Se modifica la condición para comprobar el ID en lugar del nombre.
                            print(f"Producto {palet.producto.nombre} en Pasillo {pasillo.id}, Estantería {pasillo.estanterias.index(estanteria) + 1}, Ubicación {fila + 1, columna + 1}")

    def mostrar_lugares_no_disponibles_total(self):
        for pasillo in self.pasillos:
            pasillo.mostrar_lugares_no_disponibles()

if __name__ == "__main__": #Es una construcción especial en Python que verifica si el script se está ejecutando como el programa principal. Si es así, ejecuta el bloque de código que sigue.
    deposito = Deposito()

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("===== Menú de opciones =====")
        print("1. Agregar Palet")
        print("2. Egresar Palet")
        print("3. Ver informe de producto")
        print("4. Revisar lugares no disponibles")
        print("5. Salir")
        opcion = input("Ingrese una opción: ")

        if opcion == "1":
            id_palet = int(input("Ingrese ID de Palet: "))
    
            if deposito.palet_existe(id_palet):
                print("Ya existe un palet con ese ID. Intente nuevamente con un ID diferente.")
                continue

            nombre_producto = input("Ingrese nombre de producto: ")

            producto = Producto(id_palet, nombre_producto)
            palet = Palet(id_palet)
            palet.cargar_producto(producto)

            pasillo_elegido = int(input("Elige el número de pasillo (1-8): ")) - 1
            estanteria_elegida = int(input("Elige la estantería (1-2): ")) - 1
            fila_elegida = int(input("Elige la fila (1-4): ")) - 1
            columna_elegida = int(input("Elige la columna (1-4): ")) - 1

            if deposito.pasillos[pasillo_elegido].estanterias[estanteria_elegida].puede_agregar_palet(fila_elegida, columna_elegida): #verifica si es posible agregar un palet en la posición especificada en la estantería seleccionada dentro del pasillo seleccionado. Si es posible, agrega el palet y muestra un mensaje de éxito.
                deposito.pasillos[pasillo_elegido].estanterias[estanteria_elegida].lugares[fila_elegida][columna_elegida] = palet
                print("Palet añadido exitosamente!")
            else:
                print("El lugar elegido no está disponible o no cumple con las reglas de colocación.")

        elif opcion == "2":
            id_palet = int(input("Ingrese ID del Palet a egresar: "))
            palet = deposito.obtener_palet_por_id(id_palet)

            if palet:
                destino = input("Ingrese a dónde va el palet: ")
                transporte = input("Ingrese en qué transporte: ")
                palet.definir_destino(destino)

                for pasillo in deposito.pasillos:
                    for estanteria in pasillo.estanterias:
                        for fila in range(4):
                            for columna in range(4):
                                if estanteria.lugares[fila][columna] == palet:
                                    estanteria.lugares[fila][columna] = None
                                    print(f"Resumen de Egreso:")
                                    print(f"ID del Palet: {palet.id}")
                                    print(f"Producto: {palet.producto.nombre}")
                                    print(f"Ubicación original: Pasillo {pasillo.id}, Estantería {pasillo.estanterias.index(estanteria) + 1}, Fila {fila + 1}, Columna {columna + 1}")
                                    print(f"Destino: {palet.destino}")
                                    print(f"Transporte: {transporte}")
                                    break
            else:
                print("No se encontró el palet con el ID proporcionado.")


        elif opcion == "3":
            id_palet = int(input("Ingrese ID del palet para el informe: "))
            palet = deposito.obtener_palet_por_id(id_palet)
            if palet:
                deposito.informe_producto(id_palet)  # Modifica esto para pasar el ID en lugar del nombre.
            else:
                print("No se encontró el palet con el ID proporcionado.")
            input("Presione Enter para continuar...")

        elif opcion == "4":
            deposito.mostrar_lugares_no_disponibles_total()
            input("Presione Enter para continuar...")

        elif opcion == "5":
            break

        else:
            print("Opción no reconocida. Intente de nuevo.")
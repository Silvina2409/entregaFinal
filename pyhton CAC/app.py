'''
Hola chicas! Como estan? Les envio el codigo que estuve haciendo. Le hice algunas modificaciones a lo que hizo el profe, para que no quede exactamente igual. Aca les anoto lo que modifique. Cualquier cosa que quieran modificar, si quieren la pueden escribir aca asi nos entendemos entre las 3. 
 * class Producto => class Curso
 * en el init agregue duracion del curso y al metodo modificar tambien.
 * en el programa principal al objeto producto, lo modifique por curso
 * Utilice los nombres de los cursos que usamos en el ancla al instanciar los objetos
 * deje todos los comentarios que hizo el profe para orientarnos
 * en la class inventario, en el init porductos lo modifique por cursos

'''


class Curso:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self, codigo, descripcion, cantidad, precio, duracion):
        self.codigo = codigo           # Código 
        self.descripcion = descripcion # Descripción
        self.cantidad = cantidad       # Cantidad disponible (stock)
        self.precio = precio           # Precio 
        self.duracion= duracion        # Duración 

    # Este método permite modificar un producto.
    def modificar(self, nueva_descripcion, nueva_cantidad, nuevo_precio, duracion):
        self.descripcion = nueva_descripcion  # Modifica la descripción
        self.cantidad = nueva_cantidad        # Modifica la cantidad
        self.precio = nuevo_precio            # Modifica el precio
        self.duracion= duracion               # Modifica la duracion  

class Inventario:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.cursos = []  # Lista de productos en el inventario (variable de clase)


    # Este método permite crear objetos de la clase "Curso" y agregarlos al inventario.
    def agregar_curso(self, codigo, descripcion, cantidad, precio, duracion):
        nuevo_curso = Curso(codigo, descripcion, cantidad, precio, duracion)
        self.cursos.append(nuevo_curso)  # Agrega un nuevo curso a la lista
    # Este método permite consultar datos de productos que están en el inventario
    # Devuelve el producto correspondiente al código proporcionado o False si no existe.
    def consultar_curso(self, codigo):
        for curso in self.cursos:
            if curso.codigo == codigo:
                return curso # Retorna un objeto
        return False

    # Este método permite modificar datos de cursos que están en el inventario
     # Utiliza el método consultar_curso del inventario y modificar el curso.
    def modificar_curso(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_duracion):
        curso = self.consultar_curso(codigo)
        if curso:
            curso.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_duracion)
        else: print (f'El curso {codigo} no se pudo modificar')    


    # Este método elimina el curso indicado por codigo de la lista mantenida en el inventario.
    def eliminar_curso(self, codigo):
        eliminar = False
        for curso in self.cursos:
            if curso.codigo == codigo:
                eliminar = True
                curso_eliminar = curso       
        if eliminar == True:
            self.cursos.remove(curso_eliminar)
            print(f'El curso {codigo}  ha sido eliminado.')
        else:
            print(f'El curso {codigo} no ha sido no encontrado.')


    # Este método imprime en la terminal una lista con los datos de los cursos que figuran en el inventario.
    def listar_cursos(self):
        print("-"*50)
        print("Lista de cursos en el inventario:")
        print("Código\tDescripción\t\tCant\tPrecio\tDuración")
        for curso in self.cursos:
            print(f'{curso.codigo}\t{curso.descripcion}\t{curso.cantidad}\t{curso.precio}\t{curso.duracion}')
        print("-"*50)

class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia
    def __init__(self):
        self.items = []  # Lista de items en el carrito (variable de clase)


    # Este método permite agregar cursos del inventario al carrito.
    def agregar(self, codigo, cantidad, inventario):
        # Nos aseguramos que el producto esté en el inventario
        curso = inventario.consultar_curso(codigo)
        if curso is False: 
            print("El curso no existe.")
            return False


        # Verificamos que la cantidad en stock sea suficiente
        if curso.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False


        # Si existe y hay stock, vemos si ya existe en el carrito.
        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                # Actualizamos la cantidad en el inventario
                curso = inventario.consultar_curso(codigo)
                curso.modificar(curso.descripcion, curso.cantidad - cantidad, curso.precio, curso.duracion)
                return True


        # Si no existe en el carrito, lo agregamos como un nuevo item.
        nuevo_item = Curso(codigo, curso.descripcion, cantidad, curso.precio, curso.duracion)
        self.items.append(nuevo_item)
        # Actualizamos la cantidad en el inventario
        curso = inventario.consultar_curso(codigo)
        curso.modificar(curso.descripcion, curso.cantidad - cantidad, curso.precio, curso.duracion)
        return True

 # Este método quita unidades de un elemento del carrito, o lo elimina.
    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    print("Cantidad a quitar mayor a la cantidad en el carrito.")
                    return False
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                # Actualizamos la cantidad en el inventario
                curso = inventario.consultar_curso(codigo)
                curso.modificar(curso.descripcion, curso.cantidad + cantidad, curso.precio, curso.duracion)
                return True


        # Si el bucle finaliza sin novedad, es que ese producto NO ESTA en el carrito.
        print("El curso no se encuentra en el carrito.")
        return False


    def mostrar(self):
        print("-"*50)
        print("Lista de cursos en el carrito:")
        print("Código\tDescripción\t\tCant\tPrecio\tDuracion")
        for item in self.items:
            print(f'{item.codigo}\t{item.descripcion}\t{item.cantidad}\t{item.precio}\t{item.duracion}')
        print("-"*50)

                    

'''

# Programa principal
curso = Curso(1, 'Extraccionista de Laboratorio', 10, 5000, 4)
# Accedemos a los atributos del objeto
print(f'{curso.codigo} | {curso.descripcion} | {curso.cantidad} | {curso.precio} | {curso.duracion} ')
# Modificar los datos del curso
curso.modificar( 'Endocrinologia', 10, 6000, 8) 
print(f'{curso.codigo} | {curso.descripcion} | {curso.cantidad} | {curso.precio} | {curso.duracion}')


# Crear una instancia de la clase Inventario
mi_inventario = Inventario() 


# Agregar cursos 
mi_inventario.agregar_curso(1, 'Endocrinología General', 20, 6000, 8)
mi_inventario.agregar_curso(2, 'Procesam de muestras', 15 , 3000, 2)
mi_inventario.agregar_curso(3, 'Resonancia Magnetica', 20, 10000, 12)
mi_inventario.agregar_curso(4, 'Tomografía Computada', 30, 8000, 8)
mi_inventario.agregar_curso(5, 'Mamografia Nivel 1', 10, 8000, 8)


# Consultar un curso 
curso = mi_inventario.consultar_curso(30)
if curso != False:
    print(f'Curso encontrado:\nCódigo: {curso.codigo}\nDescripción: {curso.descripcion}\nCantidad: {curso.cantidad}\nPrecio: {curso.precio}\n Duracion: {curso.duracion}')  
else:
    print("Curso  no encontrado.")


# Modificar un curso
mi_inventario.modificar_curso(3, 'Resonancia Magnetica', 20, 15000, 12)


# Listar todos los cursos
mi_inventario.listar_cursos()


# Eliminar un curso 
mi_inventario.eliminar_curso(2)


# Confirmamos que haya sido eliminado
mi_inventario.listar_cursos()

# ---------------------------------------------------------------------
# Ejemplo de uso de las clases y objetos definidos antes:
# ---------------------------------------------------------------------


# Crear una instancia de la clase Inventario
mi_inventario = Inventario()


# Crear una instancia de la clase Carrito
mi_carrito = Carrito()


# Crear 3 cursos y agregarlos al inventario
mi_inventario.agregar_curso(1, 'Endocrinología General', 20, 6000, 8)
mi_inventario.agregar_curso(2, 'Procesam de muestras', 15 , 3000, 2)
mi_inventario.agregar_curso(3, 'Resonancia Magnetica', 20, 10000, 12)


# Listar todos los cursos del inventario
mi_inventario.listar_cursos()


# Agregar 2 cursos al carrito
mi_carrito.agregar(1, 2, mi_inventario) # Agregar 2 unidades del producto con código 1 al carrito
mi_carrito.agregar(3, 4, mi_inventario) # Agregar 1 unidad del producto con código 3 al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito

# Listar todos los cursos del carrito
mi_carrito.mostrar()
# Quitar 1 curso al carrito
mi_carrito.quitar (1, 1, mi_inventario) # Quitar 1 unidad del producto con código 1 al carrito
# Listar todos los cursos del carrito
mi_carrito.mostrar()
# Mostramos el inventario
mi_inventario.listar_cursos()
'''

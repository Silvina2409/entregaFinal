'''
Hola chicas! Como estan? Les envio el codigo que estuve haciendo. Le hice algunas modificaciones a lo que hizo el profe, para que no quede exactamente igual. Aca les anoto lo que modifique. Cualquier cosa que quieran modificar, si quieren la pueden escribir aca asi nos entendemos entre las 3. 
 * class Producto => class Curso
 * en el init agregue duracion del curso y al metodo modificar tambien.
 * en el programa principal al objeto producto, lo modifique por curso
 * Utilice los nombres de los cursos que usamos en el ancla al instanciar los objetos
 * deje todos los comentarios que hizo el profe para orientarnos
 * en la class inventario, en el init porductos lo modifique por cursos

 NOTE: Este archivo estaba presente en la branch MASTER

'''

import sqlite3
from flask import Flask, jsonify, request

# Configurar la conexión a la base de datos SQLite
DATABASE = 'inventario.db'

def get_db_connection():
    print("Obteniendo conexión...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla 'cursos' si no existe
def create_table():
    print("Creando tabla cursos...") # Para probar que se ejecuta la función
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cursos (
            codigo INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio REAL NOT NULL,
            duracion INTEGER NOT NULL
        ) ''')
    conn.commit()
    cursor.close()
    conn.close()


# Verificar si la base de datos existe, si no, crearla y crear la tabla
def create_database():
    print("Creando la BD...") # Para probar que se ejecuta la función
    conn = sqlite3.connect(DATABASE)
    conn.close()
    create_table()


# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()


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
        self.conexion = get_db_connection()
        self.cursor = self.conexion.cursor()
        
    def agregar_curso(self, codigo, descripcion, cantidad, precio, duracion):
        """Agrega un curso al sistema.
        Otras aclaraciones...
        """
        curso_existente = self.consultar_curso(codigo)
        if curso_existente:
            print("Ya existe un Curso con ese código.")
            return False
        nuevo_curso = Curso(codigo, descripcion, cantidad, precio, duracion)
        sql = f'INSERT INTO cursos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio}, {duracion});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

    def consultar_curso(self, codigo):
        sql = f'SELECT * FROM cursos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        row = self.cursor.fetchone()
        if row:
            codigo, descripcion, cantidad, precio, duracion = row
            return Curso(codigo, descripcion, cantidad, precio, duracion)
        return False

    def modificar_curso(self, codigo, nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_duracion):
        curso = self.consultar_curso(codigo)
        if curso:
            curso.modificar(nueva_descripcion, nueva_cantidad, nuevo_precio, nueva_duracion)
            sql = f'UPDATE cursos SET descripcion = "{nueva_descripcion}", cantidad = {nueva_cantidad}, precio = {nuevo_precio}, duracion ={nueva_duracion} WHERE codigo = {codigo};' 
            self.cursor.execute(sql)
            self.conexion.commit()



    # Este método elimina el curso indicado por codigo de la lista mantenida en el inventario.

    def eliminar_curso(self, codigo):
        sql = f'DELETE FROM cursos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Curso {codigo} eliminado.')
            self.conexion.commit()
        else:
            print(f'Curso {codigo} no encontrado.')

    # Este método imprime en la terminal una lista con los datos de los cursos que figuran en el inventario.
    def listar_cursos(self):
        print("-"*50)
        print("Lista de Cursos en el inventario:")
        print("Código\tDescripción\t\tCant\tPrecio\tDuración")
        self.cursor.execute("SELECT * FROM cursos ")
        rows = self.cursor.fetchall()
        for row in rows:
            codigo, descripcion, cantidad, precio, duracion = row
            print(f'{codigo}\t{descripcion}\t{cantidad}\t{precio}\t{duracion}')
        print("-"*50)



class Carrito:
    # Definimos el constructor e inicializamos los atributos de instancia


    def __init__(self):
        self.conexion = sqlite3.connect('inventario.db')  # Conexión a la BD
        self.cursor = self.conexion.cursor()
        self.items = []



    # Este método permite agregar cursos del inventario al carrito.

   
    def agregar(self, codigo, cantidad, inventario):
        curso = inventario.consultar_curso(codigo)
        if curso is False:
            print("El Curso no esta disponible.")
            return False
        if curso.cantidad < cantidad:
            print("Cantidad en stock insuficiente.")
            return False

        for item in self.items:
            if item.codigo == codigo:
                item.cantidad += cantidad
                sql = f'UPDATE cursos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True

        nuevo_item = Curso(codigo, curso.descripcion, cantidad, curso.precio, curso.duracion)
        self.items.append(nuevo_item)
        sql = f'UPDATE cursos SET cantidad = cantidad - {cantidad}  WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        self.conexion.commit()
        return True

    def quitar(self, codigo, cantidad, inventario):
        for item in self.items:
            if item.codigo == codigo:
                if cantidad > item.cantidad:
                    print("Cantidad a quitar mayor a la cantidad en el carrito.")
                    return False
                item.cantidad -= cantidad
                if item.cantidad == 0:
                    self.items.remove(item)
                sql = f'UPDATE cursos SET cantidad = cantidad + {cantidad} WHERE codigo = {codigo};'
                self.cursor.execute(sql)
                self.conexion.commit()
                return True



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

# Programa principal
# Crear la base de datos y la tabla si no existen
create_database()


# Crear una instancia de la clase Inventario
mi_inventario = Inventario()


# Agregar cursos al inventario
mi_inventario.agregar_curso(1, 'Endocrinología General', 20, 6000, 8)
mi_inventario.agregar_curso(2, 'Procesam de muestras', 15 , 3000, 2)
mi_inventario.agregar_curso(3, 'Resonancia Magnetica', 20, 10000, 12)


# Consultar algún curso del inventario
print(mi_inventario.consultar_curso(3)) #Existe, se muestra la dirección de memoria
print(mi_inventario.consultar_curso(6)) #No existe, se muestra False


# Listar los cursos del inventario
mi_inventario.listar_cursos()
# Modificar un curso del inventario
mi_inventario.modificar_curso(2, "Procesam de Muestras", 10, 5000, 4)


# Listar nuevamente los cursos del inventario para ver la modificación
mi_inventario.listar_cursos()


# Eliminar un curso
mi_inventario.eliminar_curso(3)


# Listar nuevamente los cursos del inventario para ver la eliminación
mi_inventario.listar_cursos()


# Crear una instancia de la clase Carrito
mi_carrito = Carrito()
# Agregar 2 unidades del curso con código 1 al carrito
mi_carrito.agregar(1, 2, mi_inventario)  
# Agregar 1 unidad del curso con código 2 al carrito
mi_carrito.agregar(2, 1, mi_inventario)  


# Mostrar el contenido del carrito y del inventario
mi_carrito.mostrar()
mi_inventario.listar_cursos()

# Quitar 1 unidad del curso con código 1 al carrito y 1 unidad del producto con código 2 al carrito
mi_carrito.quitar(1, 1, mi_inventario)
mi_carrito.quitar(2, 1, mi_inventario)


# Mostrar el contenido del carrito y del inventario
mi_carrito.mostrar()
mi_inventario.listar_cursos()

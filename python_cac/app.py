'''
Hola chicas! Como estan? Les envio el codigo que estuve haciendo. Le hice algunas modificaciones a lo que hizo el profe, para que no quede exactamente igual. Aca les anoto lo que modifique. Cualquier cosa que quieran modificar, si quieren la pueden escribir aca asi nos entendemos entre las 3. 
 * class Curso => class Curso
 * en el init agregue duracion del curso y al metodo modificar tambien.
 * en el programa principal al objeto Curso, lo modifique por curso
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

    # Este método permite modificar un Curso.
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
            return jsonify({'message': 'Ya existe un curso con ese código.'}), 400
        nuevo_curso = Curso(codigo, descripcion, cantidad, precio, duracion)
        sql = f'INSERT INTO cursos VALUES ({codigo}, "{descripcion}", {cantidad}, {precio}, {duracion});'
        self.cursor.execute(sql)
        self.conexion.commit()
        return jsonify({'message': 'Curso agregado correctamente.'}), 200

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
            return jsonify({'message': 'Curso modificado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404



    # Este método elimina el curso indicado por codigo de la lista mantenida en el inventario.

    def eliminar_curso(self, codigo):
        sql = f'DELETE FROM cursos WHERE codigo = {codigo};'
        self.cursor.execute(sql)
        if self.cursor.rowcount > 0:
            print(f'Curso {codigo} eliminado.')
            self.conexion.commit()
            return jsonify({'message': 'Curso eliminado correctamente.'}), 200
        return jsonify({'message': 'Curso no encontrado.'}), 404

    # Este método imprime en la terminal una lista con los datos de los cursos que figuran en el inventario.
    def listar_cursos(self):
        self.cursor.execute("SELECT * FROM cursos ")
        rows = self.cursor.fetchall()
        cursos = []
        for row in rows:
            codigo, descripcion, cantidad, precio, duracion = row
            curso = {'codigo': codigo, 'descripcion': descripcion, 'cantidad': cantidad, 'precio': precio, 'duracion': duracion}
            cursos.append(curso)
        return jsonify(cursos), 200



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


# Inicialización de Flask
app = Flask(__name__)

carrito = Carrito() # Instanciamos un carrito
inventario = Inventario() # Instanciamos un inventario

# Ruta para obtener el index
@app.route('/')
def index():
    return 'API de Inventario'

# Ruta para obtener los datos de un Curso según su código
@app.route('/Cursos/<int:codigo>', methods=['GET'])
def obtener_Curso(codigo):
    Curso = inventario.consultar_Curso(codigo)
    if Curso:
        return jsonify({
        'codigo': Curso.codigo,
        'descripcion': Curso.descripcion,
        'cantidad': Curso.cantidad,
        'precio': Curso.precio
        }), 200
    return jsonify({'message': 'Curso no encontrado.'}), 404

# Ruta para obtener la lista de Cursos del inventario
@app.route('/Cursos', methods=['GET'])
def obtener_Cursos():
    return inventario.listar_Cursos()

# Ruta para agregar un Curso al inventario
@app.route('/Cursos', methods=['POST'])
def agregar_Curso():
    codigo = request.json.get('codigo')
    descripcion = request.json.get('descripcion')
    cantidad = request.json.get('cantidad')
    precio = request.json.get('precio')
    return inventario.agregar_Curso(codigo, descripcion, cantidad, precio)

# Ruta para modificar un Curso del inventario
@app.route('/Cursos/<int:codigo>', methods=['PUT'])
def modificar_Curso(codigo):
    nueva_descripcion = request.json.get('descripcion')
    nueva_cantidad = request.json.get('cantidad')
    nuevo_precio = request.json.get('precio')
    return inventario.modificar_Curso(codigo, nueva_descripcion, nueva_cantidad, nuevo_precio)

# Ruta para eliminar un Curso del inventario
@app.route('/Cursos/<int:codigo>', methods=['DELETE'])
def eliminar_Curso(codigo):
    return inventario.eliminar_Curso(codigo)

# Ruta para agregar un Curso al carrito
@app.route('/carrito', methods=['POST'])
def agregar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.agregar(codigo, cantidad, inventario)

# Ruta para quitar un Curso del carrito
@app.route('/carrito', methods=['DELETE'])
def quitar_carrito():
    codigo = request.json.get('codigo')
    cantidad = request.json.get('cantidad')
    inventario = Inventario()
    return carrito.quitar(codigo, cantidad, inventario)

# Ruta para obtener el contenido del carrito
@app.route('/carrito', methods=['GET'])
def obtener_carrito():
    return carrito.mostrar()
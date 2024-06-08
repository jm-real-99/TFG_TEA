import mysql.connector
import configparser
from Paciente import Paciente
from Terapeuta import Terapeuta


class DataBase:
    def __init__(self):
        # Configura los detalles de conexión
        config = configparser.ConfigParser()
        config.read('config.properties')

        user = config.get('db', 'user')
        password = config.get('db', 'password')
        host = config.get('db', 'host')
        port = config.get('db', 'port')
        database = config.get('db','database')

        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

        print("USER: "+user)
        print("PASS: " + password)
        print("HOST: " + host)
        print("PORT: " + port)
        print()
        print(config)

        try:
            # Crea una conexión
            self.connection = mysql.connector.connect(**config)

            # Crea un cursor para ejecutar consultas
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            print(f"Error al conectar a la base de datos: {err}")

    """
        Obtenemos una lista de todos los pacientes
    """

    def obtener_all_pacientes(self):
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Pacientes")
            pacientes_data = self.cursor.fetchall()  # Obtiene todos los registros

            # Crea instancias de Paciente y almacénalas en una lista
            pacientes = []
            for paciente_data in pacientes_data:
                paciente = Paciente(*paciente_data)
                pacientes.append(paciente)

            return pacientes
        except mysql.connector.Error as err:
            print(f"Error al obtener datos de la tabla Paciente: {err}")
            return None

    """
        Obtenemos una lista de todos los terapeutas
    """

    def obtener_all_terapeutas(self):
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Terapeutas")
            terapeutas_data = self.cursor.fetchall()  # Obtiene todos los registros

            # Crea instancias de Paciente y almacénalas en una lista
            terapeutas = []
            for terapeuta_data in terapeutas_data:
                terapeuta = Paciente(*terapeuta_data)
                terapeutas.append(terapeuta)

            return terapeutas
        except mysql.connector.Error as err:
            print(f"Error al obtener datos de la tabla Paciente: {err}")
            return None

    """
        Obtenemos un terapeuta según su usuario y contraseña
    """

    def obtener_rerapeuta_by_usuario_y_contrasena(self, usuario, contrasena):
        #if usuario is not str or contrasena is not str:
        #    print("Error al obtener datos de la tabla Paciente: Los tipos de datos deben ser str")
        #    return None
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Terapeutas WHERE usuario = %s AND contrasena = %s", (usuario, contrasena))
            terapeutas_data = self.cursor.fetchall()  # Obtiene todos los registros

            print(terapeutas_data)
            print(terapeutas_data[0])

            if terapeutas_data:
                return Terapeuta(*terapeutas_data[0])
            else:
                return None

        except mysql.connector.Error as err:
            print(f"Error al obtener datos de la tabla Paciente: {err}")
            return None

    """
        Cerramos la conexión
    """

    def cerrar_conexion(self):
        # Cierra la conexión
        self.cursor.close()
        self.connection.close()

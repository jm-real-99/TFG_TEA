import mysql.connector
import configparser

from Estadistica import Estadistica
from Paciente import Paciente
from Terapeuta import Terapeuta


class DataBase:
    """
    En esta clase gestionamos la conexión con la Base de Datos.
    """
    def __init__(self):
        """
        Establecemos las propiedades de la conexión con la BD y la iniciamos
        """
        # Configura los detalles de conexión
        config = configparser.ConfigParser()
        config.read('config.properties')

        user = config.get('db', 'user')
        password = config.get('db', 'password')
        host = config.get('db', 'host')
        port = config.get('db', 'port')
        database = config.get('db', 'database')

        config = {
            'user': user,
            'password': password,
            'host': host,
            'database': database
        }

        print("USER: " + user)
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
            print(f"[DB] Error al conectar a la base de datos: {err}")

    """ **************************************************************************************
        *********************** MÉTODOS RELACIONADOS CON LOS PACIENTES ***********************
        ************************************************************************************** """
    def obtener_all_pacientes(self):
        """
        Obtenemos una lista de todos los pacientes
        @return: Lista de los pacientes
        """
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
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None

    def crear_paciente(self, nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones, telf_contacto):
        """
        Creamos un nuevo paciente por sus atributos
        @param nombre: Nombre del paciente
        @param apellido: Apellidos del paciente
        @param edad: Edad del paciente
        @param num_expediente: Número del paciente
        @param terapeuta_asignado: Terapeuta asignado al paciente
        @param observaciones: Observaciones del paciente
        @param telf_contacto: Teléfono de contacto del paciente
        @return: Booleano
            True si se ha creado con éxito
            False si ha ocurrido algún error
        """
        if ((nombre is None) or (apellido is None) or (num_expediente is None) or
                (terapeuta_asignado is None)):
            print("[DB] Error al introducir paciente en la base de datos, uno de los datos es None")
            return False
        try:
            print("Edad: " + edad)
            if edad is not "":
                edad = int(edad)
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("INSERT INTO Pacientes (nombre, apellido, edad, num_expediente, "
                                "terapeuta_asignado, observaciones, telf_contacto) values (%s, %s, %s, %s, %s, %s, %s);"
                                , (nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones,
                                   telf_contacto))
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return False
        except ValueError:
            print("[DB] Error, el formato de la edad no es el correcto")
            return False

        return True

    """
            Añadimos un nuevo paciente a la base de datos a partir de la clase paciente
    """

    def crear_paciente_clase(self, paciente):
        """
        Creamos un paciente a partir de la entidad del paciente. La descomponemos llamando a crear_paciente
        @param paciente: Entidad del paciente
        @return: Booleano
            True si se ha creado con éxito
            False si ha ocurrido algún error
        """
        return self.crear_paciente(paciente.get_nombre(), paciente.get_apellido(), paciente.get_edad(),
                                   paciente.get_num_expediente(), paciente.get_terapeuta_asignado(),
                                   paciente.get_observaciones(), paciente.get_telf_contacto())

    def obtener_paciente_by_num_expediente(self, num_expediente):
        """
        Obtenemos un paciente según su número de expediente
        @param num_expediente: Número expediente del paciente a buscar
        @return: Paciente
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Pacientes WHERE num_expediente  = %s",
                                [num_expediente])
            pacientes_data = self.cursor.fetchall()  # Obtiene todos los registros

            if pacientes_data:
                print("[DB] Paciente obtenido con éxito")
                return Paciente(*pacientes_data[0])
            else:
                print("[DB] Error en la consulta del paciente")
                return None

        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None
        except IndexError as err:
            print(f"[DB] Index error: {err}")
            return None

    def obtener_paciente_by_id(self, identificador):
        """
        Obtenemos un paciente según su id
        @param identificador: Identificador del paciente a buscar
        @return: Paciente
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Pacientes WHERE id  = %s",
                                [identificador])
            pacientes_data = self.cursor.fetchall()  # Obtiene todos los registros

            if pacientes_data:
                print("[DB] Paciente obtenido con éxito")
                return Paciente(*pacientes_data[0])
            else:
                print("[DB] Error en la consulta del paciente")
                return None

        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None
        except IndexError as err:
            print(f"[DB] Index error: {err}")
            return None

    """ **************************************************************************************
        *********************** MÉTODOS RELACIONADOS CON LOS TERAPEUTAS ***********************
        ************************************************************************************** """

    def obtener_all_terapeutas(self):
        """
        Obtenemos una lista de todos los terapeutas
        @return:
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Terapeutas")
            terapeutas_data = self.cursor.fetchall()  # Obtiene todos los registros

            # Crea instancias de Paciente y almacénalas en una lista
            terapeutas = []
            for terapeuta_data in terapeutas_data:
                terapeuta = Terapeuta(*terapeuta_data)
                terapeutas.append(terapeuta)

            return terapeutas
        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None

    def obtener_terapeuta_by_usuario_y_contrasena(self, usuario, contrasena):
        """
        Obtenemos un terapeuta según su usuario y contraseña
        @param usuario: usuario terapeuta
        @param contrasena: contraseña del terapeuta
        @return: Terapeuta
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Terapeutas WHERE usuario = %s AND contrasena = %s",
                                (usuario, contrasena))
            terapeutas_data = self.cursor.fetchall()  # Obtiene todos los registros

            print(terapeutas_data)
            print(terapeutas_data[0])

            if terapeutas_data:
                return Terapeuta(*terapeutas_data[0])
            else:
                return None

        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None
        except IndexError:
            return None


    def obtener_terapeuta_by_nombre_y_apellido(self, nombre, apellido):
        """
        Obtenemos un terapeuta según su nombre y apellido
        @param nombre: Nombre del terapeuta a buscar
        @param apellido: Apellido del terapeuta a buscar
        @return:
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM Terapeutas WHERE nombre = %s AND apellido = %s",
                                (nombre, apellido))
            terapeutas_data = self.cursor.fetchall()  # Obtiene todos los registros

            print(terapeutas_data)
            print(terapeutas_data[0])

            if terapeutas_data:
                return Terapeuta(*terapeutas_data[0])
            else:
                return None

        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None

    """ **************************************************************************************
        ********************* MÉTODOS RELACIONADOS CON LAS ESTADÍSTICAS **********************
        ************************************************************************************** """

    def incluir_estadistica_terapia(self, estadistica):
        """
        Creamos una estadística nueva
        @param estadistica: Estadística a crear
        @return: Booleano
            True si se ha creado con éxito
            False si ha ocurrido algún error
        """
        if ((estadistica.get_paciente_id() is None) or (estadistica.get_terapeuta_id() is None) or
                (estadistica.get_horacomienzo() is None) or (estadistica.get_fecha() is None) or
                (estadistica.get_horafin() is None) or (estadistica.get_tiempototal() is None)):
            print("[DB] Error al introducir la estadística en la base de datos, uno de los datos Not Null es None")
            return False
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("INSERT INTO EstadisticasTerapias (paciente_id, terapeuta_id, enfadado, "
                                "enfadadototal, disgustado, disgustadototal, miedoso, miedosototal, contento, "
                                "contentototal, triste, tristetotal, sorprendido, sorprendidototal, neutro, "
                                "neturototal, atencion, atenciontotal, fecha, fechahoracomienzo, fechahorafin, tiempototal, "
                                "observaciones) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,"
                                " %s, %s, %s,  %s, %s, %s, %s);"
                                , (estadistica.get_paciente_id(), estadistica.get_terapeuta_id(),
                                   estadistica.get_enfadado(), estadistica.get_enfadado_total(),
                                   estadistica.get_disgustado(), estadistica.get_disgustadototal(),
                                   estadistica.get_miedoso(), estadistica.get_miedosototal(),
                                   estadistica.get_contento(),
                                   estadistica.get_contentototal(), estadistica.get_triste(),
                                   estadistica.get_tristetotal(), estadistica.get_sorprendido(),
                                   estadistica.get_sorprendidototal(), estadistica.get_neutro(),
                                   estadistica.get_neutrototal(), estadistica.get_atencion(),
                                   estadistica.get_atenciontotal(), estadistica.get_fecha(),
                                   estadistica.get_horacomienzo(), estadistica.get_horafin(),
                                   estadistica.get_tiempototal(), estadistica.get_observaciones()))
            print("[DB] Creada la consulta")
            self.connection.commit()
        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla EstadisticasTerapias: {err}")
            return False
        print("[DB] Estadístia añadida con éxito")
        return True

    def obtener_estadisticas_by_paciente(self, idpaciente):
        """
        Obtenemos las estadísticas asociadas a un paciente
        @param idpaciente: Identificador del paciente con las estadísticas a buscar
        @return: Array de estadisticas
        """
        try:
            # Ejecuta la consulta para obtener datos de la tabla Paciente
            self.cursor.execute("SELECT * FROM EstadisticasTerapias WHERE paciente_id  = %s",
                                [idpaciente])
            estadisticas_data = self.cursor.fetchall()  # Obtiene todos los registros

            # Crea instancias de Paciente y almacénalas en una lista
            estadisticas = []
            for estadistica_data in estadisticas_data:
                estadistica = Estadistica(*estadistica_data)
                estadisticas.append(estadistica)

            return estadisticas

        except mysql.connector.Error as err:
            print(f"[DB] Error al obtener datos de la tabla Paciente: {err}")
            return None
        except IndexError as err:
            print(f"[DB] Index error: {err}")
            return None

    def cerrar_conexion(self):
        """
        Cerramos la conexión
        @return: None
        """
        # Cierra la conexión
        self.cursor.close()
        self.connection.close()

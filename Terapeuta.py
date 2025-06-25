class Terapeuta:
    """
    Clase de la entidad Terapeuta
    """
    def __init__(self, terapeuta_id, usuario, contrasena, nombre, apellido, correo, admin):
        self._terapeuta_id = terapeuta_id
        self._usuario = usuario
        self._contrasena = contrasena
        self._nombre = nombre
        self._apellido = apellido
        self._correo = correo
        self._admin = admin

    """ **************************************************************************************
        ************************************** GETTERS ***************************************
        ************************************************************************************** """
    def get_terapeuta_id(self):
        return self._terapeuta_id

    def get_usuario(self):
        return self._usuario

    def get_contrasena(self):
        return self._contrasena

    def get_nombre(self):
        return self._nombre

    def get_apellido(self):
        return self._apellido

    def get_correo(self):
        return self._correo

    def get_admin(self):
        return self._admin

    """ **************************************************************************************
        ************************************** SETTERS ***************************************
        ************************************************************************************** """

    def set_terapeuta_id(self, terapeuta_id):
        self._terapeuta_id = terapeuta_id

    def set_usuario(self, usuario):
        self._usuario = usuario

    def set_contrasena(self, contrasena):
        self._contrasena = contrasena

    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_apellido(self, apellido):
        self._apellido = apellido

    def set_correo(self, correo):
        self._correo = correo

    def set_admin(self, admin):
        self._admin = admin

    def __str__(self):
        """
        To String
        @return: Valor a imprimir asociado a la clase
        """
        return self._nombre+" "+self._apellido


class Terapeuta:
    def __init__(self, terapeuta_id, usuario, contrasena, correo):
        self._terapeuta_id = terapeuta_id
        self._usuario = usuario
        self._contrasena = contrasena
        self._correo = correo

    # Métodos getter
    def get_terapeuta_id(self):
        return self._terapeuta_id

    def get_usuario(self):
        return self._usuario

    def get_contrasena(self):
        return self._contrasena

    def get_correo(self):
        return self._correo

    # Métodos setter
    def set_terapeuta_id(self, terapeuta_id):
        self._terapeuta_id = terapeuta_id

    def set_usuario(self, usuario):
        self._usuario = usuario

    def set_contrasena(self, contrasena):
        self._contrasena = contrasena

    def set_correo(self, correo):
        self._correo = correo


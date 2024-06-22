class Paciente:
    def __init__(self, paciente_id, nombre, apellido, edad, num_expediente, terapeuta_asignado, observaciones, telf_contacto):
        self._paciente_id = paciente_id
        self._nombre = nombre
        self._apellido = apellido
        self._edad = edad
        self._num_expediente = num_expediente
        self._terapeuta_asignado = terapeuta_asignado
        self._observaciones = observaciones
        self._telf_contacto = telf_contacto

    # Métodos getter
    def get_paciente_id(self):
        return self._paciente_id

    def get_nombre(self):
        return self._nombre

    def get_apellido(self):
        return self._apellido

    def get_edad(self):
        return self._edad

    def get_num_expediente(self):
        return self._num_expediente

    def get_terapeuta_asignado(self):
        return self._terapeuta_asignado

    def get_observaciones(self):
        return self._observaciones

    def get_telf_contacto(self):
        return self._telf_contacto

    # Métodos setter
    def set_paciente_id(self, paciente_id):
        self._paciente_id = paciente_id

    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_apellido(self, apellido):
        self._apellido = apellido

    def set_edad(self, edad):
        self._edad = edad

    def set_num_expediente(self, num_expediente):
        self._num_expediente = num_expediente

    def set_terapeuta_asignado(self, terapeuta_asignado):
        self._terapeuta_asignado = terapeuta_asignado

    def set_observaciones(self, observaciones):
        self._observaciones = observaciones

    def set_telf_contacto(self, telf_contacto):
        self._telf_contacto = telf_contacto

    def __str__(self):
        return self._nombre+" "+self._apellido

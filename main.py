from Camara import Camara
import cv2
import tkinter as tk
from datetime import datetime
from Paciente import Paciente
from Terapeuta import Terapeuta
from Database import DataBase
from Estadistica import Estadistica


class VentanaInicioSesion:
    # Variables globales
    VENTANA = (400, 300)
    VENTANA_NOTI = (100, 50)
    BOTON = (4, 2)
    CAMPO_INPUT = (14, 40)

    def __init__(self):
        self.database = DataBase()
        self.root = tk.Tk()
        self.terapeuta = None

    """
        Método mediante el que establecemos que la ventana va a estar abierta en todo momento.
        Comenzamos iniciando la sesión del terapeuta
    """

    def comenzar_programa(self):
        self.root.minsize(width=self.VENTANA[0], height=self.VENTANA[1])
        self.iniciar_sesion()
        self.root.mainloop()

    """
        Iniciamos sesión con el terapeuta
    """

    def iniciar_sesion(self):
        self.root.title("Inicio de Sesión")
        # Variables de instancia para usuario y contraseña
        usuario = tk.StringVar()
        contrasena = tk.StringVar()
        # Cuadros de texto para usuario y contraseña
        tk.Label(self.root, text="Usuario:").pack(pady=2)
        (tk.Entry(self.root, font=("Arial", self.CAMPO_INPUT[0]), textvariable=usuario, width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Contraseña:").pack(pady=2)
        tk.Entry(self.root, show="*", font=("Arial", self.CAMPO_INPUT[0]), textvariable=contrasena,
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Button(self.root, text="Iniciar Sesión",
                  command=lambda: self.comprobar_inicio_sesion(usuario, contrasena)).pack()

    """
        Vamos a evaluar si los datos introducidos en el inicio de sesión son correctos
    """

    def comprobar_inicio_sesion(self, usuario, contrasena):
        if usuario.get() != "" or contrasena.get() != "":
            self.terapeuta = self.database.obtener_terapeuta_by_usuario_y_contrasena(usuario.get(), contrasena.get())

            if self.terapeuta is not None:
                notificacion = self.mostrar_mensaje_exito("¡Inicio de sesión correcto!")
                self.mostrar_main(notificacion)
            else:
                notificacion = self.mostrar_mensaje_exito("¡Error! Creenciales incorrectas")
                self.reset_page(notificacion)
                self.iniciar_sesion()

    """
        Mostramos las opciones disponibles una vez que hayamos inciado sesión correctamente. En este caso serán:
            -Crear paciente
            -Iniciar terapia
    """

    def mostrar_main(self, notificacion):

        self.reset_page(notificacion)

        tk.Button(self.root, text="Dar de alta paciente", command=lambda: self.formulario_crear_paciente(None)).pack(
            pady=10)
        # TODO:
        # tk.Button(self.root, text="Iniciar terapia", command=self.seleccionar_paciente_terapia).pack(pady=10)
        tk.Button(self.root, text="Iniciar terapia", command=self.comenzar_terapia).pack(pady=10)

        # Actualiza la ventana principal
        self.root.update_idletasks()

    """
        Gestionamos la ventana donde daremos de alta los pacientes
    """

    def formulario_crear_paciente(self, notificacion):

        self.reset_page(notificacion)

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        nombre_var = tk.StringVar()
        apellido_var = tk.StringVar()
        edad_var = tk.StringVar()
        num_expediente_var = tk.StringVar()
        terapeuta_asignado_var = tk.StringVar()
        observaciones_var = tk.StringVar()
        telf_contacto_var = tk.StringVar()

        tk.Label(self.root, text="Nombre*:").pack(pady=2)
        (tk.Entry(self.root, textvariable=nombre_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Apellido*:").pack(pady=2)
        (tk.Entry(self.root, textvariable=apellido_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Edad:").pack(pady=2)
        (tk.Entry(self.root, textvariable=edad_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Telefono contacto:").pack(pady=2)
        tk.Entry(self.root, textvariable=telf_contacto_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        tk.Label(self.root, text="Numero Expediente*:").pack(pady=2)
        tk.Entry(self.root, textvariable=num_expediente_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        # Cargamos todos los terapeutas activos
        tk.Label(self.root, text="Terapeuta Asignado*:").pack(pady=2)
        tk.OptionMenu(self.root, terapeuta_asignado_var, *self.database.obtener_all_terapeutas()).pack(pady=10)
        print(terapeuta_asignado_var.get())
        tk.Label(self.root, text="Observaciones:").pack(pady=2)
        tk.Entry(self.root, textvariable=observaciones_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="Terapeuta Asignado*:", font=("Arial",4)).pack(pady=2)
        # Botón para crear el objeto Paciente
        tk.Button(self.root, text="Crear Paciente",
                  command=lambda: self.crear_paciente(nombre_var.get(), apellido_var.get(), edad_var.get(),
                                                      num_expediente_var.get(), terapeuta_asignado_var.get(),
                                                      observaciones_var.get(), telf_contacto_var.get())).pack()
        # Actualiza la ventana principal
        self.root.update_idletasks()

    """
        Gestionamos que el formulario se ha rellenado correctamente y si es así damos de alta el paciente en la base de 
        datos.
    """

    def crear_paciente(self, nombre_var, apellido_var, edad_var, num_expediente_var, terapeuta_asignado_var
                       , observaciones_var, telf_contacto_var):

        terpeuta_id = self.__obtener_id_terpeuta(terapeuta_asignado_var)
        if self.database.crear_paciente(nombre_var, apellido_var, edad_var, num_expediente_var, terpeuta_id
                ,observaciones_var, telf_contacto_var):
            notificacion = self.mostrar_mensaje_exito("Paciente " + nombre_var + " creado con éxito")
            self.mostrar_main(notificacion)
        else:
            notificacion = self.mostrar_mensaje_exito("ERROR: Por favor, introduzca todos los datos correctamente")
            self.formulario_crear_paciente(notificacion)

    """
        Enumera las cámaras disponibles y muestra información sobre cada una.
    """

    def listar_camaras(self):
        num_camara = 0
        while True:
            cap = cv2.VideoCapture(num_camara)
            if not cap.isOpened():
                break
            _, frame = cap.read()
            h, w = frame.shape[:2]
            print(f"Cámara {num_camara}: {w}x{h}")
            cap.release()
            num_camara += 1
        return int(input("Introduce camara: "))

    def seleccionar_paciente_terapia(self):
        # TODO: Implementar ventana para seleccionar y llamar a comenzar_terapia con ese usuario
        return None
    """
        Comenzamos la terapia y activamos la cámara.
    """
    def comenzar_terapia(self, paciente):
        #TODO: Obtener paciente al que vamos a hacer terapia
        # estadisticas = Estadistica.init_minimo(paciente, self.terapeuta.get_terapeuta_id(), datetime.now())
        # camara = Camara(2, estadisticas)
        camara = Camara(2)

        while True:
            end = camara.read_frame()
            if not end:
                break

        # TODO: Revisar que los datos de la variable estadísticas se están recogiendo bien

    """
        Método auxiliar mediante el que vamos a eliminar todo el contenido que haya en la vista. Esto nos permite 
        refrescar el contenido correctamente
    """

    def reset_page(self, no_eliminar):
        for componente in self.root.winfo_children():
            if componente != no_eliminar:
                componente.destroy()

    def mostrar_mensaje_exito(self, notificacion):
        # Crear una nueva ventana emergente (Toplevel)
        ventana_exito = tk.Toplevel(self.root)
        ventana_exito.minsize(width=self.VENTANA_NOTI[0], height=self.VENTANA_NOTI[1])
        ventana_exito.title("Notificación")
        tk.Label(ventana_exito, text=notificacion).pack()

        # Agregar un botón "Cerrar" para cerrar la ventana emergente
        tk.Button(ventana_exito, text="Cerrar", command=ventana_exito.destroy).pack()

        # Actualizar la ventana principal antes de mostrar la ventana emergente
        self.root.update()
        return ventana_exito

    """
     Como para crear el paciente necesitamos el id y no su nombre y apellido, además de que tampoco podemos buscar 
     por nombre y apellido ya juntado, vamos a emplear este método para obtener el id del terpeuta asignado.
    """

    def __obtener_id_terpeuta(self, nombre_y_apellidos):
        # Primero vamos a ahorrarnos la búsqueda en la bd si este terpaueta somos nosotros
        if (self.terapeuta.get_nombre() + " " + self.terapeuta.get_apellido()) == nombre_y_apellidos:
            return self.terapeuta.get_terapeuta_id()
        # Si no lo somos entonces realizamos una búsqueda en BD
        terapeutas = self.database.obtener_all_terapeutas()
        for terpeuta in terapeutas:
            if (terpeuta.get_nombre() + " " + terpeuta.get_apellido()) == nombre_y_apellidos:
                return terpeuta.get_terapeuta_id()


if __name__ == "__main__":
    interfaz = VentanaInicioSesion()
    interfaz.comenzar_programa()

"""
TODO:

- Añadir ventana previa a iniciar terapia para seleccionar el paciente al que le vamos a realizar la terapia:
    - (mostrar_main) # TODO: 
    - (seleccionar_paciente_terapia) # TODO: Implementar ventana para seleccionar y llamar a comenzar_terapia con ese 
    usuario
    - (comenzar_terapia) #TODO: Obtener paciente al que vamos a hacer terapia
- Comprobar que los datos se guardan bien en la variable estadísticas
    -(comenzar_terapia) # TODO: Revisar que los datos de la variable estadísticas se están recogiendo bien
- Crear método en DataBase para guardar las estadísticas
    - (incluir_estadistica_terapia) # TODO: Realizar consulta
    
- Ver como mostrar en la interfaz gráfica los resultados de las estadísticas de los pacientes: 
    - Añadir botón para ir a de vista estadísticas
    - Añadir vista de lista de todos los pacientes
    - Añadir vista concreta de cada  paciente donde veremos las estadísticas a lo largo del tiempo y por terapia
     
Menos importantes:
- Hacer menú de terapeuta admin para que puedas crear desde la aplicación otros usuarios de terpeutas
"""

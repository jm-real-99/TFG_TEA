from Camara import Camara
import cv2
import tkinter as tk

from Paciente import Paciente
from Terapeuta import Terapeuta
from Database import DataBase


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

        # Botón para iniciar sesión
        boton_iniciar_sesion = tk.Button(self.root, text="Iniciar Sesión",
                                         command=lambda: self.comprobar_inicio_sesion(usuario, contrasena))

        boton_iniciar_sesion.pack()

    """
        Vamos a evaluar si los datos introducidos en el inicio de sesión son correctos
    """

    def comprobar_inicio_sesion(self, usuario, contrasena):
        self.terapeuta = self.database.obtener_rerapeuta_by_usuario_y_contrasena(usuario.get(), contrasena.get())
        self.reset_page()

        if self.terapeuta is None:
            self.mostrar_mensaje_exito("¡Error! Creenciales incorrectas")
            self.iniciar_sesion()
        else:
            self.mostrar_mensaje_exito("¡Inicio de sesión correcto!")
            self.mostrar_main()

    """
        Mostramos las opciones disponibles una vez que hayamos inciado sesión correctamente. En este caso serán:
            -Crear paciente
            -Iniciar terapia
    """

    def mostrar_main(self):

        tk.Button(self.root, text="Dar de alta paciente", command=self.formulario_crear_paciente).pack(pady=10)
        tk.Button(self.root, text="Iniciar terapia", command=self.comenzar_terapia).pack(pady=10)

        # Actualiza la ventana principal
        self.root.update_idletasks()

    """
        Gestionamos la ventana donde daremos de alta los pacientes
    """

    def formulario_crear_paciente(self):
        self.reset_page()

        nombre_var = tk.StringVar()
        apellido_var = tk.StringVar()
        edad_var = tk.StringVar()
        num_expediente_var = tk.StringVar()
        terapeuta_asignado_var = tk.StringVar()
        observaciones_var = tk.StringVar()
        telf_contacto_var = tk.StringVar()

        tk.Label(self.root, text="Nombre:").pack(pady=2)
        (tk.Entry(self.root, textvariable=nombre_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Apellido:").pack(pady=2)
        (tk.Entry(self.root, textvariable=apellido_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Edad:").pack(pady=2)
        (tk.Entry(self.root, textvariable=edad_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Telefono contacto:").pack(pady=2)
        tk.Entry(self.root, textvariable=telf_contacto_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        tk.Label(self.root, text="Numero Expediente:").pack(pady=2)
        tk.Entry(self.root, textvariable=num_expediente_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        # TODO: Hacer que el terapeuta se obtenga desde una lista de terapeutas
        tk.Label(self.root, text="Terapeuta Asignado:").pack(pady=2)
        tk.Entry(self.root, textvariable=terapeuta_asignado_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        tk.Label(self.root, text="Observaciones:").pack(pady=2)
        tk.Entry(self.root, textvariable=observaciones_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        # Botón para crear el objeto Paciente
        # tk.Button(self.root, text="Crear Paciente", command=self.crear_paciente).pack()
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
        self.reset_page()

        # TODO: Realizar comprobaciones de que todo está correcto

        paciente = Paciente(0, nombre_var, apellido_var, edad_var, num_expediente_var, terapeuta_asignado_var
                            , observaciones_var, telf_contacto_var)

        # TODO: Dar de alta al paciente en la base de datos.

        self.mostrar_mensaje_exito("Paciente " + paciente.get_nombre() + " creado con éxito")
        self.mostrar_main()

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

    """
        Comenzamos la terapia y activamos la cámara.
    """

    def comenzar_terapia(self):
        camara = Camara(2)

        while True:
            end = camara.read_frame()
            if not end:
                break

    """
        Método auxiliar mediante el que vamos a eliminar todo el contenido que haya en la vista. Esto nos permite 
        refrescar el contenido correctamente
    """

    def reset_page(self):
        for componente in self.root.winfo_children():
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


if __name__ == "__main__":
    interfaz = VentanaInicioSesion()
    interfaz.comenzar_programa()

"""
TODO:
- Realizar TODOs:

    # formulario_crear_paciente : TODO: Hacer que el terapeuta se obtenga desde una lista de terapeutas
    # crear_paciente: TODO: Realizar comprobaciones de que todo está correcto
    # crear_paciente: TODO: Dar de alta al paciente en la base de datos.
    
- Crear Tabla y lógica para guardar los datos de las estadísticas de las terapias
- Ver como mostrar en la interfaz gráfica los resultados de las estadísticas de los pacientes: 
    - Añadir botón para ir a de vista estadísticas
    - Añadir vista de lista de todos los pacientes
    - Añadir vista concreta de cada  paciente donde veremos las estadísticas a lo largo del tiempo y por terapia
     
Menos importantes:
- Hacer menú de terapeuta admin para que puedas crear desde la aplicación otros usuarios de terpeutas
"""

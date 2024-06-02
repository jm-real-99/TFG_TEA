from Camara import Camara
import cv2
import tkinter as tk

from Paciente import Paciente


class VentanaInicioSesion:

    def __init__(self):
        self.root = tk.Tk()

        # Variables de instancia para usuario y contraseña
        self.usuario = tk.StringVar()
        self.contrasena = tk.StringVar()

    """
        Método mediante el que establecemos que la ventana va a estar abierta en todo momento.
        Comenzamos iniciando la sesión del terapeuta
    """
    def comenzar_programa(self):
        self.iniciar_sesion()
        self.root.mainloop()

    """
        Iniciamos sesión con el terapeuta
    """
    def iniciar_sesion(self):
        self.root.title("Inicio de Sesión")
        # Cuadros de texto para usuario y contraseña
        tk.Label(self.root, text="Usuario:").pack(pady=10)
        entry_usuario = tk.Entry(self.root, font=("Arial", 14), textvariable=self.usuario)
        tk.Label(self.root, text="Contraseña:").pack(pady=10)
        entry_contrasena = tk.Entry(self.root, show="*", font=("Arial", 14), textvariable=self.contrasena)

        # Botón para iniciar sesión
        boton_iniciar_sesion = tk.Button(self.root, text="Iniciar Sesión", command=self.mostrar_inicio_correcto)

        # Posicionamiento de widgets
        entry_usuario.pack(pady=10)
        entry_contrasena.pack(pady=10)
        boton_iniciar_sesion.pack()

    """
        Vamos a evaluar si los datos introducidos en el inicio de sesión son correctos
    """
    def comprobar_inicio_sesion(self):
        # TODO: CONSULTAR CONTRA BASES DE DATOS SI EL INICIO ES CORRECTO
        return None

    """
        Mostramos las opciones disponibles una vez que hayamos inciado sesión correctamente. En este caso serán:
            -Crear paciente
            -Iniciar terapia
    """
    def mostrar_inicio_correcto(self):

        # Obtener los valores de los cuadros de texto
        usuario = self.usuario.get()
        contrasena = self.contrasena.get()

        print("Usuario ", end=" ")
        print(usuario)
        print("Contraseña ", end=" ")
        print(contrasena)

        self.reset_page()

        # Crea un Label en la ventana principal para mostrar el mensaje
        tk.Label(self.root, text="¡Inicio de sesión correcto!").pack()

        tk.Button(self.root, text="Dar de alta paciente", command=self.formulario_crear_paciente).pack()
        tk.Button(self.root, text="Iniciar terapia", command=self.comenzar_terapia).pack()

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

        tk.Label(self.root, text="Nombre:").pack(pady=10)
        tk.Entry(self.root, textvariable=nombre_var, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Apellido:").pack(pady=10)
        tk.Entry(self.root, textvariable=apellido_var, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Edad:").pack(pady=10)
        tk.Entry(self.root, textvariable=edad_var, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Telefono contacto:").pack(pady=10)
        tk.Entry(self.root, textvariable=telf_contacto_var, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Numero Expediente:").pack(pady=10)
        tk.Entry(self.root, textvariable=num_expediente_var, font=("Arial", 14)).pack(pady=10)
        # TODO: Hacer que el terapeuta se obtenga desde una lista de terapeutas
        tk.Label(self.root, text="Terapeuta Asignado:").pack(pady=10)
        tk.Entry(self.root, textvariable=terapeuta_asignado_var, font=("Arial", 14)).pack(pady=10)
        tk.Label(self.root, text="Observaciones:").pack(pady=10)
        tk.Entry(self.root, textvariable=observaciones_var, font=("Arial", 14)).pack(pady=10)

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

        # Crea un Label en la ventana principal para mostrar el mensaje
        tk.Label(self.root, text="Paciente " + paciente.get_nombre() + " creado con éxito").pack()

        #TODO: Dar de alta al paciente en la base de datos.

        # Actualiza la ventana principal
        self.root.update_idletasks()

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
            print("elmininado ", end=" ")
            print(componente)


if __name__ == "__main__":
    interfaz = VentanaInicioSesion()
    interfaz.comenzar_programa()


"""
TODO:
- Arreglar flujo de alta pacientes, actualmente cuando das de alta uno, nos quedamos ahí. Para solventar esto tendremos 
que llamar a la función de mostrar_inicio_correcto y en cada vista permitir un mensaje superior con información.
- Poder seleccionar un paciente para el inicio de terapia
- Incluir base de datos.
"""

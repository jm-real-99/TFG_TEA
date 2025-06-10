import time
from Emociones import Emociones
from Calculo_estadisticas import Calculo_estadisticas
from Camara import Camara
import cv2
from PIL import Image, ImageTk

import tkinter as tk
from datetime import datetime
from Paciente import Paciente
from Terapeuta import Terapeuta
from Database import DataBase
from Estadistica import Estadistica

from pygrabber.dshow_graph import FilterGraph

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


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
        self.paciente_mapa = self.__obtener_mapa_pacientes()
        self.terapeuta_mapa = self.__obtener_mapa_terapeuta()
        self.estadisticas = None

        # Vista del video de la terapia
        self.label_video = tk.Label(self.root)
        self.frame_grafica = tk.Frame(self.root)
        self.window_resized = False
        self.end = False

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
        tk.Button(self.root, text="Consultar estadísticas", command=self.consultar_estadisticas).pack(
            pady=10)
        tk.Button(self.root, text="Iniciar terapia", command=self.seleccionar_paciente_terapia).pack(pady=10)
        # tk.Button(self.root, text="Iniciar terapia", command=self.comenzar_terapia).pack(pady=10)

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

        tk.Label(self.root, text="Nombre *:").pack(pady=2)
        (tk.Entry(self.root, textvariable=nombre_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Apellido *:").pack(pady=2)
        (tk.Entry(self.root, textvariable=apellido_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Edad:").pack(pady=2)
        (tk.Entry(self.root, textvariable=edad_var, font=("Arial", self.CAMPO_INPUT[0]), width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(self.root, text="Telefono contacto:").pack(pady=2)
        tk.Entry(self.root, textvariable=telf_contacto_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        tk.Label(self.root, text="Numero Expediente *:").pack(pady=2)
        tk.Entry(self.root, textvariable=num_expediente_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)
        # Cargamos todos los terapeutas activos
        tk.Label(self.root, text="Terapeuta Asignado *:").pack(pady=2)
        tk.OptionMenu(self.root, terapeuta_asignado_var, *list(self.terapeuta_mapa.values())).pack(pady=10)
        print(terapeuta_asignado_var.get())
        tk.Label(self.root, text="Observaciones:").pack(pady=2)
        tk.Entry(self.root, textvariable=observaciones_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="* Campos obligatorios", font=("Arial", 8)).pack(pady=2)
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

        print("Terapeuta asignado: " + terapeuta_asignado_var)
        print(" Num_Exp: "+num_expediente_var)
        terpeuta_id = self.terapeuta_mapa[terapeuta_asignado_var].get_terapeuta_id()

        if self.database.crear_paciente(nombre_var, apellido_var, edad_var, num_expediente_var, terpeuta_id
                , observaciones_var, telf_contacto_var):

            # No hay que olvidarnos de mantener la sincronía del mapa de pacientes con la base de datos
            paciente = self.database.obtener_paciente_by_num_expediente(num_expediente_var)
            self.paciente_mapa[f"{paciente.get_nombre()} {paciente.get_apellido()}"] = paciente

            notificacion = self.mostrar_mensaje_exito("Paciente " + nombre_var + " creado con éxito")
            self.mostrar_main(notificacion)
        else:
            notificacion = self.mostrar_mensaje_exito("ERROR: Por favor, introduzca todos los datos correctamente")
            self.formulario_crear_paciente(notificacion)

    def seleccionar_paciente_terapia(self):
        # Cargamos todos los terapeutas activos
        paciente_var = tk.StringVar()
        tk.Label(self.root, text="Seleccione paciente para terapia:").pack(pady=2)
        tk.OptionMenu(self.root, paciente_var, *list(self.paciente_mapa.values())).pack(pady=10)
        # Botón para crear el objeto Paciente
        tk.Button(self.root, text="Seleccionar cámara",
                  command=lambda: self.comenzar_terapia(paciente_var.get())).pack()
        # Actualiza la ventana principal
        self.root.update_idletasks()
        return None

    """
        Comenzamos la terapia y activamos la cámara.
    """
    def comenzar_terapia(self, paciente):
        # Nos aseguramos que la variable con la que vamos a terminar la terapia este a false
        self.end = False

        # Lineas de depuración
        print("\n" * 2)
        print("*" * 20)
        print("Comenzamos terapia")
        print("*" * 20)
        print("[OK] Seleccionado paciente: "+paciente)

        paciente = self.paciente_mapa[paciente]
        pacienteid = paciente.get_paciente_id()
        self.estadisticas = Estadistica.init_minimo(pacienteid,
                                               self.terapeuta.get_terapeuta_id(), datetime.now())
        print("[OK] Estadísticas iniciales: ")

        self.listar_camaras()

    """
            Enumera las cámaras disponibles y muestra información sobre cada una.
    """

    def listar_camaras(self):
        graph = FilterGraph()
        camaras = graph.get_input_devices()

        # Crear un botón por cada cámara
        for i, nombre in enumerate(camaras):
            boton = tk.Button(self.root, text=nombre, command=lambda idx=i: self.camara_terapia(idx))
            boton.pack(padx=10, pady=5, fill="x")

    def camara_terapia(self, camara):
        print(" Iniciamos la cámara con id "+str(camara))
        camara = Camara(camara, self.estadisticas)
        print("[OK] Creada camara")

        self.reset_page(None)

        self.end = False  # Nos aseguramos de tener esta bandera en tu clase
        # Actualizamos las etiquetas porque se habrán eliminado
        self.label_video = tk.Label(self.root)
        self.label_video.pack(side=tk.LEFT)

        btn_parar = tk.Button(self.root, text="Parar Terapia", command= lambda: self.parar_terapia(camara))
        btn_parar.pack(pady=10)

        # Frame para la gráfica
        self.frame_grafica = tk.Frame(self.root)
        self.frame_grafica.pack(side=tk.RIGHT, padx=30)

        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(5, 4))
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.get_tk_widget().pack()

        self.mostrar_frame(camara,ax,canvas)  # Inicia el refresco del video

    def mostrar_frame(self,camara,ax,canvas):
        print("**********  Frame  ***********")
        end, frame, emociones = camara.read_frame()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.label_video.imgtk = imgtk
        self.label_video.configure(image=imgtk)
        self.label_video.pack()

        if emociones:
            self.actualizar_grafica(emociones,ax,canvas)

        if not hasattr(self, 'window_resized'):
            self.root.update()
            self.window_resized = True

        if self.end:
            self.cerrar_terapia(camara)
            return
        else:
            self.root.after(30,lambda: self.mostrar_frame(camara,ax,canvas))  # 30ms ≈ 33fps

    def actualizar_grafica(self, emociones_dict,ax,canvas):
        ax.clear()
        emociones = list(emociones_dict.keys())
        valores = list(emociones_dict.values())

        max_index = valores.index(max(valores))
        colores = ['skyblue' if i == max_index else 'lightgray' for i in range(len(emociones))]

        ax.bar(emociones, valores, color=colores)
        ax.set_ylim(0, 100)
        ax.set_ylabel('%')
        ax.set_title('Probabilidades de Emociones')
        ax.tick_params(axis='x', rotation=45)
        # Pintamos la gráfica actualizada
        fig = ax.figure
        fig.tight_layout()
        canvas.draw()

    def parar_terapia(self,camara):
        print("Terapia detenida por el usuario.")
        self.end = True

    def cerrar_terapia(self, camara):
        camara.cerrar_camara()
        self.pintar_datos()
        self.database.incluir_estadistica_terapia(self.estadisticas)

        notificacion = self.mostrar_mensaje_exito("Terapia finalizada")
        self.mostrar_main(notificacion)

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

    """
        Creamos un mapa clave-valor de los pacientes donde la clave va a ser la concatenación del nombre y apellidos.
    """

    def __obtener_mapa_pacientes(self):
        paciente_mapa = {}
        pacientes = self.database.obtener_all_pacientes()
        # Si queremos aumentar la seguridad no cargaremos las contraseñas
        for paciente in pacientes:
            paciente_mapa[f"{paciente.get_nombre()} {paciente.get_apellido()}"] = paciente
        return paciente_mapa

    """
            Creamos un mapa clave-valor de los pacientes donde la clave va a ser la concatenación del nombre y apellidos.
        """

    def __obtener_mapa_terapeuta(self):
        terapeuta_mapa = {}
        terapeutas = self.database.obtener_all_terapeutas()
        for terapeuta in terapeutas:
            terapeuta_mapa[f"{terapeuta.get_nombre()} {terapeuta.get_apellido()}"] = terapeuta
        return terapeuta_mapa

    def terminarTerapia(self):
        self.end = True


    def pintar_datos(self):
        self.cabecera_end()
        print("Paciente ID:", self.estadisticas.get_paciente_id())
        print("Terapeuta ID:", self.estadisticas.get_terapeuta_id())
        print("Enfadado:", self.estadisticas.get_enfadado())
        print("Enfadado Total:", self.estadisticas.get_enfadado_total())
        print("Disgustado:", self.estadisticas.get_disgustado())
        print("Disgustado Total:", self.estadisticas.get_disgustadototal())
        print("Miedoso:", self.estadisticas.get_miedoso())
        print("Miedoso Total:", self.estadisticas.get_miedosototal())
        print("Contento:", self.estadisticas.get_contento())
        print("Contento Total:", self.estadisticas.get_contentototal())
        print("Triste:", self.estadisticas.get_triste())
        print("Triste Total:", self.estadisticas.get_tristetotal())
        print("Sorprendido:", self.estadisticas.get_sorprendido())
        print("Sorprendido Total:", self.estadisticas.get_sorprendidototal())
        print("Neutro:", self.estadisticas.get_neutro())
        print("Neutro Total:", self.estadisticas.get_neutrototal())
        print("Atención:", self.estadisticas.get_atencion())
        print("Atención Total:", self.estadisticas.get_atenciontotal())
        print("Fecha y Hora Comienzo:", self.estadisticas.get_fechahoracomienzo())
        print("Fecha y Hora Fin:", self.estadisticas.get_fechahorafin())
        print("Tiempo Total:", self.estadisticas.get_tiempototal())
        print("Observaciones:", self.estadisticas.get_observaciones())

    def cabecera_end(self):
        end = [
            "****** ***      ** *****",
            "**     ** **    ** **   **",
            "****** **   **  ** **    **",
            "**     **    ** ** **   **",
            "****** **     **** *****"
        ]

        print("\n" * 5)

        for linea in end:
            print(linea)

        print("\n" * 2)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~RESULTADOS 2~~~~~~~~~~~~~~~~~~~~")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    """ *******************************************
           MÉTODOS RELACIONADOS CON LAS ESTADÍSTICAS
           ******************************************* """

    def consultar_estadisticas(self):
        # Cargamos todos los terapeutas activos
        paciente_var = tk.StringVar()
        tk.Label(self.root, text="Seleccione paciente para ver las estadísticas:").pack(pady=2)
        tk.OptionMenu(self.root, paciente_var, *list(self.paciente_mapa.values())).pack(pady=10)
        # Botón para crear el objeto Paciente
        tk.Button(self.root, text="Comenzar",
                  command=lambda: self.consultas_estadisticas_paciente(paciente_var.get())).pack()
        # Actualiza la ventana principal
        self.root.update_idletasks()
        return None

    def consultas_estadisticas_paciente(self, paciente):
        self.reset_page(None)

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        paciente = self.paciente_mapa[paciente]
        estadisticas = self.database.obtener_estadisticas_by_paciente(paciente.get_paciente_id())
        calculo_estadisticas = Calculo_estadisticas(estadisticas)
        calculo_estadisticas.inicializarDatos()

        valores = [calculo_estadisticas.porcentaje_enfadado, calculo_estadisticas.porcentaje_disgustado,
                    calculo_estadisticas.porcentaje_miedoso, calculo_estadisticas.porcentaje_contento,
                    calculo_estadisticas.porcentaje_triste, calculo_estadisticas.porcentaje_sorprendido,
                    calculo_estadisticas.porcentaje_neutro]
        etiquetas = [Emociones.ENFADO.name, Emociones.DISGUSTADO.name, Emociones.MIEDOSO.name, Emociones.CONTENTO.name,
                     Emociones.TRISTE.name, Emociones.SORPRENDIDO.name, Emociones.NEUTRO.name]

        # Crear una figura y un conjunto de subtramas
        figura = Figure(figsize=(10, 9), dpi=80)
        ax1 = figura.add_subplot(121)  # Gráfico de tarta
        ax2 = figura.add_subplot(122)  # Gráfico de barras
        if (all(x == 0.0 for x in valores)):
            # Crear gráfico de tarta
            ax1.pie([100], labels=[Emociones.NONE.name], autopct='%1.1f%%')
        else:
            ax1.pie(valores, labels=etiquetas, autopct='%1.1f%%')


        ax1.set_title('Gráfico de tarta')

        # Crear gráfico de barras
        y_pos = np.arange(len(etiquetas))
        ax2.bar(y_pos, valores, align='center', alpha=0.5)
        ax2.set_xticks(y_pos)
        ax2.set_xticklabels(etiquetas)
        ax2.set_title('Gráfico de barras')

        # Crear el lienzo de Tkinter con la figura
        canvas = FigureCanvasTkAgg(figura, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)



if __name__ == "__main__":
    interfaz = VentanaInicioSesion()
    interfaz.comenzar_programa()

"""
TODO:
- ¡¡¡ ARREGLAR Y VER POR QUÉ AHORA NO DEJA INICIALIZAR LA CÁMARA Y DA ERROR AL INICIAR TERAPIAS !!!
    Seguro sea un error con las librerías y haya que reinstalar todo.
- Implementar boton para terminar la terapia (Actualmente no refresca bien la ventana) 
    
- Ver como mostrar en la interfaz gráfica los resultados de las estadísticas de los pacientes: 
    - Ajustar los componentes de gráficas para que se vea mejor y no se pisen los textos
    - Añadir en texto información como los minutos totales, nº de terapias, apariciones totales, etc
    - Incluir vista para ver información por terapia
    - Mostrar los datos para solo esa terapia.

     
Menos importantes:
- Hacer menú de terapeuta admin para que puedas crear desde la aplicación otros usuarios de terpeutas
"""

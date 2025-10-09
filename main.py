import json
import time
from Emociones import Emociones
from Camara import Camara
import cv2
from PIL import Image, ImageTk


from LoggerManager import LoggerManager

import tkinter as tk
import ttkbootstrap as tb

from datetime import datetime, date
from Paciente import Paciente
from Terapeuta import Terapeuta
from Database import DataBase
from Estadistica import Estadistica

from Calculo_estadisticas import Calculo_estadisticas
from pygrabber.dshow_graph import FilterGraph
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as pdf_canvas
from reportlab.lib.utils import ImageReader
import tempfile
import os
import sys
from reportlab.lib.units import cm
import configparser
import re


class AplicacionTEA:
    # Variables globales
    VENTANA = (400, 300)
    VENTANA_NOTI = (100, 50)
    BOTON = (20, 10)
    CAMPO_INPUT = (40, 60)
    TEXT_SIZE = 12

    def __init__(self):
        """
        Inicializamos la clase main.
        """

        # Inicializamos los logs:
        self._logger = LoggerManager.get_logger()

        # Obtenemos la ruta donde se esté ejecutando la aplicación
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        self.database = DataBase(base_dir)

        self._logger.info("Creamos la ventana")

        #Estilos con bootstrap
        self.root = tb.Window(themename="flatly")

        # Pantalla completa
        self.root.attributes("-fullscreen", True)
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
        self._logger.info("Ventana creada")

        # Estilo global para botones
        self.root.option_add("*Button.font", ("Arial", self.TEXT_SIZE))
        self.root.option_add("*Button.padX", self.BOTON[0])
        self.root.option_add("*Button.padY", self.BOTON[1])
        # Estilo global para labels
        self.root.option_add("*Label.font", ("Arial", self.TEXT_SIZE))
        # Estilo global para optionMenu
        self.root.option_add("*Menubutton.font", ("Arial", self.TEXT_SIZE))
        self.root.option_add("*Menu.font", ("Arial", self.TEXT_SIZE))

        self.terapeuta = None
        self.paciente_mapa = self.__obtener_mapa_pacientes()
        self.terapeuta_mapa = self.__obtener_mapa_terapeuta()
        self.estadisticas = None

        # Vista del video de la terapia
        self.label_video = tk.Label(self.root)
        self.frame_grafica = tk.Frame(self.root)
        self.window_resized = False
        self.end = False

        # Exportación estadísticas
        config = configparser.ConfigParser()
        config.read('config.properties')
        self.route = config.get('export', 'route')

    def comenzar_programa(self):
        """
        Métododonde que establecemos que la ventana va a estar abierta en todo momento.
        Comenzamos iniciando la sesión del terapeuta
        """
        self._logger.info("Comenzamos mostrando la ventana")
        # self.root.minsize(width=self.VENTANA[0], height=self.VENTANA[1])
        self.formulario_inicio_sesion()
        self.root.mainloop()

    def formulario_inicio_sesion(self):
        """
        Creamos el formulario de inicio de sesión
        """
        self._logger.info("Formulario inicio de sesión")
        self.root.title("Inicio de Sesión")
        # Creamos un frame central con padding
        frame = tk.Frame(self.root, padx=20, pady=20)
        frame.pack(expand=True, fill="both")

        # Variables de instancia para usuario y contraseña
        usuario = tk.StringVar()
        contrasena = tk.StringVar()

        # Cuadros de texto para usuario y contraseña
        tk.Label(frame, text="Usuario:").pack(pady=2)
        (tk.Entry(frame, font=("Arial", self.CAMPO_INPUT[0]), textvariable=usuario, width=self.CAMPO_INPUT[1])
         .pack(pady=10))
        tk.Label(frame, text="Contraseña:").pack(pady=2)
        tk.Entry(frame, show="*", font=("Arial", self.CAMPO_INPUT[0]), textvariable=contrasena,
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Button(frame, text="Iniciar Sesión",
                  command=lambda: self.comprobar_inicio_sesion(usuario, contrasena)).pack()

    def comprobar_inicio_sesion(self, usuario, contrasena):
        """
        Vamos a evaluar si los datos introducidos en el inicio de sesión son correcto
        @param usuario: Nombre usuario introducido
        @param contrasena: Contraseña introducida
        """
        if usuario.get() != "" or contrasena.get() != "":
            self.terapeuta = self.database.obtener_terapeuta_by_usuario_y_contrasena(usuario.get(), contrasena.get())

            if self.terapeuta is not None:
                notificacion = self.__mostrar_mensaje_exito("¡Inicio de sesión correcto!")
                self.mostrar_main(notificacion)
            else:
                notificacion = self.__mostrar_mensaje_exito("¡Error! Creenciales incorrectas")
                self.__reset_page(notificacion)
                self.formulario_inicio_sesion()

    def mostrar_main(self, notificacion):
        """
        Mostramos las opciones disponibles una vez que hayamos inciado sesión correctamente. En este caso serán:
            - Crear paciente
            - Consultar estadísticas
            - Iniciar terapia
        @param notificacion: Notificación de inicio de sesión exitoso
        """
        self.__reset_page(notificacion)
        self.root.title("Menú principal")
        tk.Button(self.root, text="Dar de alta paciente", command=lambda: self.formulario_crear_paciente(None)).pack(
            pady=10)
        if self.terapeuta.get_admin():
            tk.Button(self.root, text="Dar de alta terapeuta",
                      command=lambda: self.formulario_crear_terapeuta(None)).pack(
                pady=10)
        tk.Button(self.root, text="Consultar estadísticas", command=self.consultar_estadisticas).pack(
            pady=10)
        tk.Button(self.root, text="Iniciar terapia", command=lambda:self.seleccionar_paciente_terapia(None)).pack(pady=10)

        # Actualiza la ventana principal
        self.root.update_idletasks()

    """ **************************************************************************************
    ****************** MÉTODOS RELACIONADOS CON LA CREACIÓN DE PACIENTES *******************
    ************************************************************************************** """

    def formulario_crear_paciente(self, notificacion):
        """
        Gestionamos la ventana donde tendremos el formulario de alta los pacientes
        @param notificacion: Notificación a mostrar en caso de que queramos hacerlo
        """
        self.__reset_page(notificacion)

        self.root.title("Crear paciente")
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
        tk.Label(self.root, text="Edad *:").pack(pady=2)
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
        self._logger.info(terapeuta_asignado_var.get())
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
        """
        Gestionamos que el formulario se ha rellenado correctamente y si es así, creamos el paciente con los datos
        que ha introducido el usuario en el formulario
        @param nombre_var: Nombre del paciente
        @param apellido_var: Apellido del paciente
        @param edad_var: Edad del paciente
        @param num_expediente_var: Número de expediente del paciente
        @param terapeuta_asignado_var: Terapeuta asignado al paciente
        @param observaciones_var: Observaciones del paciente
        @param telf_contacto_var: Teléfono de contato del paciente
        """

        self._logger.info("Terapeuta asignado: " + terapeuta_asignado_var)
        self._logger.info(" Num_Exp: "+num_expediente_var)
        try:
            if terapeuta_asignado_var is None:
                notificacion = self.__mostrar_mensaje_exito(
                    "ERROR: Por favor, introduzca todos los datos correctamente")
                self.formulario_crear_paciente(notificacion)

            if self.database.crear_paciente(nombre_var, apellido_var, edad_var, num_expediente_var, self.terapeuta_mapa[terapeuta_asignado_var].get_terapeuta_id()
                    , observaciones_var, telf_contacto_var):

                # No hay que olvidarnos de mantener la sincronía del mapa de pacientes con la base de datos
                paciente = self.database.obtener_paciente_by_num_expediente(num_expediente_var)
                self.paciente_mapa[f"{paciente.get_nombre()} {paciente.get_apellido()}"] = paciente

                notificacion = self.__mostrar_mensaje_exito("Paciente " + nombre_var + " creado con éxito")
                self.mostrar_main(notificacion)
            else:
                notificacion = self.__mostrar_mensaje_exito(
                    "ERROR: Por favor, introduzca todos los datos correctamente")
                self.formulario_crear_paciente(notificacion)
        except Exception:
            notificacion = self.__mostrar_mensaje_exito(
                "ERROR: Ha ocurrido algún error gestionando la petición")
            self._logger.error("Ha ocurrido algún error gestionando la petición")
            self.formulario_crear_paciente(notificacion)


    """ **************************************************************************************
    ****************** MÉTODOS RELACIONADOS CON LA CREACIÓN DE TERAPEUTAS *******************
    ************************************************************************************** """

    def formulario_crear_terapeuta(self, notificacion):
        """
        Gestionamos la ventana donde tendremos el formulario de alta de los terapeutas
        @param notificacion: Notificación a mostrar en caso de que queramos hacerlo
        """
        self.__reset_page(notificacion)

        self.root.title("Crear terapeuta")
        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        # Variables del formulario
        usuario_var = tk.StringVar()
        contrasena_var = tk.StringVar()
        nombre_var = tk.StringVar()
        apellido_var = tk.StringVar()
        correo_var = tk.StringVar()
        admin_var = tk.StringVar(value="No")

        # Campos del formulario
        tk.Label(self.root, text="Usuario *:").pack(pady=2)
        tk.Entry(self.root, textvariable=usuario_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="Contraseña *:").pack(pady=2)
        tk.Entry(self.root, show="*", textvariable=contrasena_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="Nombre *:").pack(pady=2)
        tk.Entry(self.root, textvariable=nombre_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="Apellido *:").pack(pady=2)
        tk.Entry(self.root, textvariable=apellido_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        tk.Label(self.root, text="Correo *:").pack(pady=2)
        tk.Entry(self.root, textvariable=correo_var, font=("Arial", self.CAMPO_INPUT[0]),
                 width=self.CAMPO_INPUT[1]).pack(pady=10)

        # Selector de rol administrador
        tk.Label(self.root, text="¿Administrador?:").pack(pady=2)
        tk.OptionMenu(self.root, admin_var, "Sí", "No").pack(pady=10)

        tk.Label(self.root, text="* Campos obligatorios", font=("Arial", 8)).pack(pady=2)

        # Botón para crear terapeuta
        tk.Button(
            self.root,
            text="Crear Terapeuta",
            command=lambda: self.crear_terapeuta(
                usuario_var.get(),
                contrasena_var.get(),
                nombre_var.get(),
                apellido_var.get(),
                correo_var.get(),
                admin_var.get()
            )
        ).pack(pady=10)

        self.root.update_idletasks()

    def crear_terapeuta(self, usuario, contrasena, nombre, apellido, correo, admin):
        """
        Gestionamos la validación y creación del terapeuta en la base de datos
        @param usuario: Usuario del terapeuta
        @param contrasena: Contraseña del terapeuta
        @param nombre: Nombre del terapeuta
        @param apellido: Apellido del terapeuta
        @param correo: Correo electrónico del terapeuta
        @param admin: Rol de administrador ("Sí" o "No")
        """
        try:
            self._logger.info(f"Creando terapeuta: {usuario}")

            # Validación básica
            if not usuario or not contrasena or not nombre or not apellido or not correo:
                notificacion = self.__mostrar_mensaje_exito("ERROR: Por favor, rellene todos los campos obligatorios.")
                self.formulario_crear_terapeuta(notificacion)
                return

            es_admin = True if admin == "Sí" else False

            # Llamada a la base de datos
            if self.database.crear_terapeuta(usuario, contrasena, nombre, apellido, correo, es_admin):
                # Actualizamos el mapa de terapeutas para mantener sincronía
                terapeuta = self.database.obtener_terapeuta_by_usuario_y_contrasena(usuario,contrasena)
                self.terapeuta_mapa[f"{terapeuta.get_nombre()} {terapeuta.get_apellido()}"] = terapeuta

                notificacion = self.__mostrar_mensaje_exito(f"Terapeuta '{nombre} {apellido}' creado con éxito.")
                self.mostrar_main(notificacion)
            else:
                notificacion = self.__mostrar_mensaje_exito("ERROR: No se ha podido crear el terapeuta.")
                self.formulario_crear_terapeuta(notificacion)

        except Exception as e:
            self._logger.error(f"Error al crear terapeuta: {e}")
            notificacion = self.__mostrar_mensaje_exito("ERROR: Ha ocurrido un error gestionando la petición.")
            self.formulario_crear_terapeuta(notificacion)

    """ **************************************************************************************
        ****************** MÉTODOS RELACIONADOS CON LA EJECUCIÓN DE LA TERAPIA *******************
        ************************************************************************************** """
    def seleccionar_paciente_terapia(self, notificacion):
        """
        Mostramos los pacientes y las camaras disponibles para hacer la terapia.
        @return: None
        """
        self.__reset_page(notificacion)

        self.root.title("Iniciar terapia")

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)
        # Cargamos todos los pacientes activos
        paciente_var = tk.StringVar()
        tk.Label(self.root, text="Seleccione paciente para terapia:").pack(pady=2)
        tk.OptionMenu(self.root, paciente_var, *list(self.paciente_mapa.values())).pack(pady=10)

        self._logger.info("Listamos cámaras")
        graph = FilterGraph()
        camaras = graph.get_input_devices()

        # Variable para almacenar la cámara seleccionada
        camara_var = tk.StringVar()

        tk.Label(self.root, text="Seleccione cámara para la terapia:").pack(pady=2)
        # Menú desplegable de cámaras
        tk.OptionMenu(self.root, camara_var, *camaras).pack(pady=10)

        # Botón para iniciar la terapia con la cámara seleccionada
        tk.Button(self.root, text="Iniciar Terapia",
                  command=lambda: self.comenzar_terapia(paciente_var.get(),camara_var.get(),camaras)).pack(pady=10)

        # Actualiza la ventana principal
        self.root.update_idletasks()
        return None

    def comenzar_terapia(self, paciente, camara, camaras):
        """
        Con el paciente seleccionado inicializamos las estadísticas.
        @param paciente: Paciente seleccionado para la terapia
        """
        if not paciente or not camara:
            notificacion = self.__mostrar_mensaje_exito(
                "ERROR: Por favor, seleccione toda la información")
            self.seleccionar_paciente_terapia(notificacion)


        self._logger.info("Comenzamos terapia")
        # Nos aseguramos que la variable con la que vamos a terminar la terapia este a false
        self.end = False

        paciente = self.paciente_mapa[paciente]
        pacienteid = paciente.get_paciente_id()
        self.estadisticas = Estadistica.init_minimo(pacienteid,
                                               self.terapeuta.get_terapeuta_id(), date.today() ,datetime.now())

        self._logger.info(" Iniciamos la terapia con usuario "+ str(paciente))

        self.camara_terapia(camaras.index(camara))

    def camara_terapia(self, camara):
        """
        Creamos y configuramos la ventana de la terapia. Mostraremos la cámara, con sus estadísticas
        y un botón para detenerla.
        @param camara: Cámara seleccionada
        """
        self._logger.info(" Iniciamos la cámara con id "+str(camara))
        camara = Camara(camara, self.estadisticas)
        self._logger.info("[OK] Creada camara")

        self.__reset_page(None)
        self.root.title("Terapia en curso")
        self.end = False  # Nos aseguramos de tener esta bandera en tu clase


        btn_parar = tk.Button(self.root, text="Parar Terapia", command= lambda: self.parar_terapia(camara))
        btn_parar.pack(pady=10)

        # Actualizamos las etiquetas porque se habrán eliminado
        self.label_video = tk.Label(self.root)
        self.label_video.pack(side=tk.LEFT)

        # Frame para la gráfica
        self.frame_grafica = tk.Frame(self.root)
        self.frame_grafica.pack(side=tk.RIGHT, padx=30)

        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(5, 4))
        canvas = FigureCanvasTkAgg(fig, master=self.frame_grafica)
        canvas.get_tk_widget().pack()

        self.mostrar_frame(camara,ax,canvas)  # Inicia el refresco del video

    def mostrar_frame(self,camara,ax,canvas):
        """
        Mostramos el frame que ha recogido la cámara y lo mostramos. Función recursiva
        @param camara: Referencia a la cámara seleccionada
        @param ax: Figura de las estadísticas
        @param canvas: Marco de la figura
        """
        end, frame, emociones = camara.read_frame()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Mostramos el frame en el campo creado para ello
        self.label_video.imgtk = imgtk
        self.label_video.configure(image=imgtk)
        self.label_video.pack()

        if emociones:
            self.actualizar_grafica(emociones,ax,canvas)

        if not hasattr(self, 'window_resized'):
            self.root.update()
            self.window_resized = True

        # Si se ha pulsado el botón de terminar la terpia, lo hacemos
        if self.end:
            self.cerrar_terapia(camara)
            return
        else:
        # Llamamos a esta función cada 30ms
            self.root.after(30,lambda: self.mostrar_frame(camara,ax,canvas))

    def actualizar_grafica(self, emociones_dict,ax,canvas):
        """
        Actualizamos la gráfica de las emociones detectadas durante la terpia
        @param emociones_dict: Diccionario de las emociones
        @param ax: Figura de las estadísticas
        @param canvas: Marco de la figura
        """
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
        """
        Si se ha pulsado el botón de parar la terapia, indicamos al bucle que deberá pararla
        @param camara: Referencia a la cámara seleccionada para la terapia
        """
        self._logger.info("Terapia detenida por el usuario.")
        self.end = True

    def cerrar_terapia(self, camara):
        """
        Hacemos las gestiones necesarias para finalizar la terapia y luego iremos a la ventana de
        añadir las observaciones
        @param camara: Referencia a la cámara
        @return:
        """
        camara.cerrar_camara()
        self.add_observaciones()

    def add_observaciones(self):
        """
        Formulario para añadir observaciones de la terapia una vez que haya finalizado
        """
        self.__reset_page(None)
        self.root.title("Terapia finalizada. Añadir observaciones")
        tk.Label(self.root, text="Introduce tus observaciones:", font=("Arial", 12)).pack(pady=10)

        # Campo de texto grande
        self.text_area = tk.Text(self.root, height=10, width=60, wrap=tk.WORD)
        self.text_area.pack(padx=10, pady=10)

        # Botones
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Añadir observaciones", command=self.enviar_terapia_finalizada).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Saltar", command=self.enviar_terapia_finalizada).pack(side=tk.LEFT, padx=10)

    def enviar_terapia_finalizada(self):
        """
        Una vez terminada toda la gestión de finalización de la terpia, la guardamos en BD
        y mostramos una notificación de éxito
        """
        texto = self.text_area.get("1.0", tk.END).strip()
        if texto:
            self.estadisticas.set_observaciones(texto)

        self.database.incluir_estadistica_terapia(self.estadisticas)

        notificacion = self.__mostrar_mensaje_exito("Terapia finalizada")
        self.mostrar_main(notificacion)



    """ **************************************************************************************
    *********************** MÉTODOS RELACIONADOS CON LAS ESTADÍSTICAS ************************
    ************************************************************************************** """

    def consultar_estadisticas(self):
        """
        Damos a elegir al usuario el paciente del que vamos a mostrar las estdísticas
        @return: None
        """
        self.__reset_page(None)

        self.root.title("Seleccionar paciente estadísticas")
        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        # Cargamos todos los terapeutas activos
        paciente_var = tk.StringVar()
        tk.Label(self.root, text="Seleccione paciente para ver las estadísticas:").pack(pady=2)
        tk.OptionMenu(self.root, paciente_var, *list(self.paciente_mapa.values())).pack(pady=10)
        # Botón para crear el objeto Paciente
        tk.Button(self.root, text="Ver estadísticas",
                  command=lambda: self.consultas_estadisticas_paciente(paciente_var.get())).pack()
        # Actualiza la ventana principal
        self.root.update_idletasks()
        return None

    def consultas_estadisticas_paciente(self, paciente_selected):
        """
        Mostramos las estadísticas generales del paciente pasado por parámetro
        @param paciente_selected: Clave del paciente seleccionado
        """
        self.__reset_page(None)

        self.root.title(f"Estadísticas generales paciente {paciente_selected}")
        tk.Label(self.root, text=paciente_selected).pack(pady=2)

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        paciente = self.paciente_mapa[paciente_selected]
        estadisticas = self.database.obtener_estadisticas_by_paciente(paciente.get_paciente_id())
        calculo_estadisticas = Calculo_estadisticas(estadisticas)
        calculo_estadisticas.inicializarDatos()

        # Canvas con Scrollbar
        tk_canvas  = tk.Canvas(self.root)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=tk_canvas .yview)
        scroll_frame = tk.Frame(tk_canvas)

        scroll_window  = tk_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        # Ajustamos el canvas para que se adapte horizontalmente
        tk_canvas.bind("<Configure>", lambda event: tk_canvas.itemconfig(
            scroll_window, width=event.width)
            )

        # Añadimos el scroll vertical
        scroll_frame.bind(
            "<Configure>",
            lambda e: tk_canvas.configure(
                scrollregion=tk_canvas.bbox("all")
            )
        )

        tk_canvas.configure(yscrollcommand=scrollbar.set)

        tk_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # == Añadimos los campos ==

        # Frame principal
        content_frame = tk.Frame(scroll_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Frame para los gráficos
        frame_graficos = tk.Frame(content_frame)
        frame_graficos.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame para los botones y etiquetas
        frame_info = tk.Frame(content_frame)
        frame_info.pack(side=tk.TOP, fill=tk.X, pady=10, expand=True)


        # Creamos un frame para contener los botones de terapias individuales
        botones_frame = tk.Frame(content_frame)
        botones_frame.pack(side=tk.TOP, fill=tk.X, pady=10, expand=True)

        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_tarta_emociones_general(calculo_estadisticas,figura, gs)
        self.mostrar_grafico_barra_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_tarta_atencion_general(calculo_estadisticas,figura, gs)
        self.mostrar_grafico_progreso_atencion(estadisticas,figura,gs)
        # Crear el lienzo de Tkinter con la figura
        figura_canvas = FigureCanvasTkAgg(figura, master=frame_graficos)
        figura_canvas.draw()
        figura_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Ajustar layout automáticamente para evitar superposición
        figura.tight_layout()

        # Estadísticas de texto
        tk.Label(frame_info, text=f"Mejora desde el inicio en la expresión de emociones: {calculo_estadisticas.mejora_inicio_expresion_emociones:.2f}").pack(pady=2)
        tk.Label(frame_info,
                 text=f"Tendencia en la mejora de expresión de emociones: {calculo_estadisticas.mejora_tendencia_expresion_emociones:.2f}").pack(
            pady=2)
        tk.Label(frame_info,
                 text=f"Mejora desde el inicio en la atención: {calculo_estadisticas.mejora_inicio_atencion:.2f}").pack(
            pady=2)
        tk.Label(frame_info,
                 text=f"Tendencia en la mejora de atención: {calculo_estadisticas.mejora_tendencia_atencion:.2f}").pack(
            pady=2)
        tk.Label(frame_info,
                 text=f"Expresión más expresada: {calculo_estadisticas.emocion_mas_expresada.name}").pack(
            pady=2)

        tk.Button(frame_info, text="Exportar a PDF",
                  command=lambda: self.exportar_estadisticas_generales_pdf(estadisticas, calculo_estadisticas, paciente_selected)).pack(
            pady=10)

        # Botones por cada terapia individual
        max_botones_por_fila = 8
        for i, estadistica in enumerate(estadisticas):
            fila = i // max_botones_por_fila
            columna = i % max_botones_por_fila

            btn = tk.Button(
                botones_frame,
                text=f"Terapia {estadistica.get_fecha()}",
                command=lambda est=estadistica: self.mostrar_estadisticas_terapia(est, paciente_selected)
            )
            btn.grid(row=fila, column=columna, padx=5, pady=5, sticky="ew")



    def mostrar_grafico_tarta_emociones_general(self,calculo_estadisticas, figura, gs):
        """
        Creamos el gráfico de tarta de las emociones expresadas en todas las estadísticas.
        @param calculo_estadisticas: Estadísticas calculadas
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        """
        valores_emociones_porcentaje = [calculo_estadisticas.porcentaje_enfadado,
                                        calculo_estadisticas.porcentaje_disgustado,
                                        calculo_estadisticas.porcentaje_miedoso,
                                        calculo_estadisticas.porcentaje_contento,
                                        calculo_estadisticas.porcentaje_triste,
                                        calculo_estadisticas.porcentaje_sorprendido,
                                        calculo_estadisticas.porcentaje_neutro]
        emociones_etiquetas = [Emociones.ENFADO.name, Emociones.DISGUSTADO.name, Emociones.MIEDOSO.name,
                               Emociones.CONTENTO.name,
                               Emociones.TRISTE.name, Emociones.SORPRENDIDO.name, Emociones.NEUTRO.name]

        # Creamos un gráfico de tarta
        ax1 = figura.add_subplot(gs[0, 0])  # Gráfico de tarta
        # Filtramos los valores y etiquetas para omitir los ceros
        valores_filtrados = [v for v in valores_emociones_porcentaje if v > 0]
        etiquetas_filtradas = [e for v, e in zip(valores_emociones_porcentaje, emociones_etiquetas) if v > 0]

        # Crear gráfico de tarta
        if not valores_filtrados:
            ax1.pie([100], labels=[Emociones.NONE.name], autopct='%1.1f%%')
        else:
            ax1.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%')
        ax1.set_title('% expresión global de emociones')

    def mostrar_grafico_barra_emociones_general(self, calculo_estadisticas, figura, gs):
        """
        Creamos el gráfico de barras de las apariciones de cada emoción en todas las terpias.
        @param calculo_estadisticas: Estadísticas calculadas
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        """
        valores_emociones_apariciones = [calculo_estadisticas.totalenfadado, calculo_estadisticas.totaldisgustado,
                                         calculo_estadisticas.totalmiedoso, calculo_estadisticas.totalcontento,
                                         calculo_estadisticas.totaltriste, calculo_estadisticas.totalsorprendido,
                                         calculo_estadisticas.totalneutro]
        emociones_etiquetas = [Emociones.ENFADO.name, Emociones.DISGUSTADO.name, Emociones.MIEDOSO.name,
                               Emociones.CONTENTO.name,
                               Emociones.TRISTE.name, Emociones.SORPRENDIDO.name, Emociones.NEUTRO.name]
        # Crear gráfico de barras
        ax2 = figura.add_subplot(gs[0, 1]) # Gráfico de barras
        y_pos = np.arange(len(emociones_etiquetas))
        ax2.bar(y_pos, valores_emociones_apariciones, align='center', alpha=0.5)
        ax2.set_xticks(y_pos)
        ax2.set_xticklabels(emociones_etiquetas, rotation=45, ha='right')  # Rotar y alinear etiquetas
        ax2.set_title('Tiempo total de cada emoción')

    def mostrar_grafico_tarta_atencion_general(self, calculo_estadisticas, figura, gs):
        """
        Creamos el gráfico de tarta del porcentaje de la atención en todas las terapias.
        @param calculo_estadisticas: Estadísticas calculadas
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        """
        valores_atencion_porcentaje = [calculo_estadisticas.porcentaje_atencion,
                                       100 - calculo_estadisticas.porcentaje_atencion]
        atención_etiquetas = ["Atención", "No atención"]

        # Creamos un gráfico de tarta de la atención
        ax3 = figura.add_subplot(gs[1, 0])  # Gráfico de tarta atención
        if all(x == 0.0 for x in valores_atencion_porcentaje):
            # Crear gráfico de tarta
            ax3.pie([100], labels=[atención_etiquetas[1]], autopct='%1.1f%%')
        else:
            ax3.pie(valores_atencion_porcentaje, labels=atención_etiquetas, autopct='%1.1f%%')
        ax3.set_title('% atención global')

    def mostrar_grafico_progreso_atencion(self, estadisticas, figura, gs):
        """
        Creamos el gráfico de puntos donde mostramos el progreso de la atención a lo largo de todas las terpias.
        @param estadisticas: Estadísticas de todas las terapias
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        """
        ax = figura.add_subplot(gs[1, 1])
        ax.set_title("Progreso de atención por terapia")
        ax.set_xlabel("Sesión")
        ax.set_ylabel("Atención (%)")

        sesiones = []
        porcentajes = []

        for idx, estadistica in enumerate(estadisticas):
            if estadistica.get_tiempototal() > 0:
                porcentaje = (estadistica.get_atenciontotal() / estadistica.get_tiempototal()) * 100
            else:
                porcentaje = 0.0

            sesiones.append(idx + 1)
            porcentajes.append(porcentaje)

        ax.plot(sesiones, porcentajes, marker='o', linestyle='-', color='green')
        ax.set_xticks(sesiones)
        ax.set_ylim(0, 100)
        ax.grid(True)

    def exportar_estadisticas_generales_pdf(self,estadisticas, calculo_estadisticas, paciente_key ):
        """
        Creamos el documento .pdf donde vamos a exportar las estadísticas generales del paciente seleccionado.
        @param estadisticas: Estadísticas de todas las terapias
        @param calculo_estadisticas: Estadísticas calculadas
        @param paciente_key: Clave del paciente seleccionado.
        """
        paciente = self.paciente_mapa[paciente_key]

        # Crear figuras
        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_tarta_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_barra_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_tarta_atencion_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_progreso_atencion(estadisticas, figura, gs)

        figura.tight_layout()

        # Guardar figura en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figura.savefig(tmpfile.name)
            imagen_path = tmpfile.name

        # Crear PDF
        pdf_name = f"resumen_terapias_{paciente_key}_{paciente.get_num_expediente()}.pdf"
        pdf_path = os.path.join(self.route, pdf_name)
        c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        margin = 50
        y_cursor = height - margin

        def draw_line(text, font="Helvetica", size=12, spacing=15):
            nonlocal y_cursor
            if y_cursor < 100:
                c.showPage()
                y_cursor = height - margin
            c.setFont(font, size)
            c.drawString(margin, y_cursor, text)
            y_cursor -= spacing

        # --- Página 1: Estadísticas generales ---
        # Información paciente
        draw_line("Paciente:", "Helvetica-Bold", 16, 20)
        draw_line(f"Paciente ID: {paciente.get_paciente_id()}")
        draw_line(f"    Nombre: {paciente.get_nombre()} {paciente.get_apellido()}")
        draw_line(f"    Expediente: {paciente.get_num_expediente()}", spacing=25)

        # Información terapeuta
        draw_line("Terapeuta:", "Helvetica-Bold", 16, 20)
        draw_line(f"    Terapeuta ID: {self.terapeuta.get_terapeuta_id()}")
        draw_line(f"    Nombre: {self.terapeuta.get_nombre()} {self.terapeuta.get_apellido()}", spacing=25)

        # Información terapias
        draw_line("Estadísticas terapia:", "Helvetica-Bold", 16, 20)
        draw_line(f"    Mejora desde el inicio en la expresión de emociones: {calculo_estadisticas.mejora_inicio_expresion_emociones:.2f}")
        draw_line(f"    Tendencia en la mejora de expresión de emociones: {calculo_estadisticas.mejora_tendencia_expresion_emociones:.2f}")
        draw_line(f"    Mejora desde el inicio en la atención: {calculo_estadisticas.mejora_inicio_atencion:.2f}")
        draw_line(f"    Tendencia en la mejora de atención: {calculo_estadisticas.mejora_tendencia_atencion:.2f}")
        draw_line(f"    Expresión más expresada: {calculo_estadisticas.emocion_mas_expresada.name}")

        # Si no hay espacio suficiente para imagen, se pasa a una nueva página
        if y_cursor < 300:
            c.showPage()
            y_cursor = height - margin

        # Insertar imagen
        img_width = 16 * cm
        img_height = 13 * cm
        c.drawImage(ImageReader(imagen_path), margin, y_cursor - img_height, width=img_width, height=img_height)

        c.showPage()
        c.save()

        os.remove(imagen_path)  # Eliminar imagen temporal

        self.__mostrar_mensaje_exito(f"PDF creado con éxito en la ruta {pdf_path}")
        self._logger.info(f"[INFO] PDF guardado en: {pdf_path}")

    def mostrar_estadisticas_terapia(self, estadistica, paciente):
        """
        Mostramos las estadísticas de una terapia en específico.
        @param estadistica: estadísticas de la terapia
        @param paciente: Paciente seleccionado.
        """
        self._logger.info(f"Mostrando estadísticas para la terapia con ID: {estadistica.get_id_terapia()}")
        self.__reset_page(None)
        self.root.title(f"Estadísticas terapia {estadistica.get_id_terapia()}")
        tk.Button(self.root, text="Volver", command=lambda: self.consultas_estadisticas_paciente(paciente)).pack(pady=10)
        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_emociones_tiempo(estadistica, figura,gs)
        self.mostrar_grafico_atencion_tiempo(estadistica,figura,gs)
        self.mostrar_grafica_emociones_tarta(estadistica,figura,gs)

        tk.Label(self.root,
                 text=f"Fecha terapia: {estadistica.get_fecha()}").pack(pady=2)
        tk.Label(self.root,
                 text=f"Hora comienzo: {estadistica.get_horacomienzo()}").pack(pady=2)
        tk.Label(self.root,
                 text=f"Tiempo total terapia:  {estadistica.get_tiempototal()/60} min").pack(pady=2)
        tk.Label(self.root,
                 text=f"Emoción más expresada:  {estadistica.get_emocion_mas_expresada().name}").pack(pady=2)
        tk.Label(self.root,
                 text=f"Observaciones:  {estadistica.get_observaciones()}").pack(pady=2)

        tk.Button(self.root, text="Exportar a PDF", command=lambda: self.exportar_estadistica_pdf(estadistica,paciente)).pack(
            pady=10)

        # Ajustar layout automáticamente para evitar superposición
        figura.tight_layout()

        # Crear el lienzo de Tkinter con la figura
        canvas = FigureCanvasTkAgg(figura, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def mostrar_grafico_emociones_tiempo(self, estadistica, figura, gs):
        """
        Creamos el gráfico de las emociones expresadas a lo largo del tiempo de la terapia.
        @param estadistica: Estadística de la terpia
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        @return:
        """
        ax = figura.add_subplot(gs[0, 0])
        ax.set_title("Emociones a lo largo de la terapia")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Emoción")

        # Guardamos en variables locales ya transformadas
        enfadado = self.__parse_intervalos(estadistica.get_enfadado())
        disgustado = self.__parse_intervalos(estadistica.get_disgustado())
        miedoso = self.__parse_intervalos(estadistica.get_miedoso())
        contento = self.__parse_intervalos(estadistica.get_contento())
        triste = self.__parse_intervalos(estadistica.get_triste())
        sorprendido = self.__parse_intervalos(estadistica.get_sorprendido())
        neutro = self.__parse_intervalos(estadistica.get_neutro())

        # Mapeo de emociones a Y ejes y colores
        emociones_info = {
            "Enfadado": (enfadado, 0, 'red'),
            "Disgustado": (disgustado, 1, 'orange'),
            "Miedoso": (miedoso, 2, 'purple'),
            "Contento": (contento, 3, 'green'),
            "Triste": (triste, 4, 'blue'),
            "Sorprendido": (sorprendido, 5, 'pink'),
            "Neutro": (neutro, 6, 'gray'),
        }

        yticks = []
        ylabels = []

        for emocion, (intervalos, y, color) in emociones_info.items():
            if intervalos:
                bars = [(item["inicio"], item["fin"] - item["inicio"]) for item in intervalos]
                ax.broken_barh(bars, (y - 0.4, 0.8), facecolors=color)
                yticks.append(y)
                ylabels.append(emocion)

        ax.set_ylim(-1, len(emociones_info))
        ax.set_yticks(yticks)
        ax.set_yticklabels(ylabels)

        ax.set_xlim(0, estadistica.get_tiempototal())
        ax.grid(True)

    def mostrar_grafico_atencion_tiempo(self, estadistica, figura, gs):
        """
        Creamos el gráfico de la atención expresada a lo largo del tiempo de la terapia.
        @param estadistica: Estadística de la terpia
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        @return:
        """
        ax = figura.add_subplot(gs[0, 1])
        ax.set_title("Atención a lo largo de la terapia")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Atención")

        # Convertir datos JSON a lista de intervalos
        intervalos = self.__parse_intervalos(estadistica.get_atencion())

        if intervalos:
            bars = [(item["inicio"], item["fin"] - item["inicio"]) for item in intervalos]
            ax.broken_barh(bars, (0.3, 0.4), facecolors='green')  # Altura 0.4 en y=0.3
            ax.set_yticks([0.5])
            ax.set_yticklabels(["Atento"])
        else:
            ax.text(0.5, 0.5, "Sin datos de atención", ha="center", va="center", transform=ax.transAxes)

        ax.set_xlim(0, estadistica.get_tiempototal())
        ax.set_ylim(0, 1)
        ax.grid(True)

    def mostrar_grafica_emociones_tarta(self, estadistica, figura, gs):
        """
        Creamos el gráfico de barras de las apariciones de cada emoción a lo largo de la terpia.
        @param estadistica: Estadísticas calculadas
        @param figura: Figura donde vamos a mostrar esta gráfica
        @param gs: Referenecia de la posición en la figura.
        """
        # Creamos un gráfico de tarta
        emociones_etiquetas = [Emociones.ENFADO.name, Emociones.DISGUSTADO.name, Emociones.MIEDOSO.name,
                               Emociones.CONTENTO.name,
                               Emociones.TRISTE.name, Emociones.SORPRENDIDO.name, Emociones.NEUTRO.name]
        emociones_porcentajes = estadistica.get_emociones_porcentajes()
        ax1 = figura.add_subplot(gs[1, :])  # Gráfico de tarta
        # Filtramos los valores y etiquetas para omitir los ceros
        valores_filtrados = [v for v in emociones_porcentajes if v > 0]
        etiquetas_filtradas = [e for v, e in zip(emociones_porcentajes, emociones_etiquetas) if v > 0]

        # Crear gráfico de tarta
        if not valores_filtrados:
            ax1.pie([100], labels=[Emociones.NONE.name], autopct='%1.1f%%')
        else:
            ax1.pie(valores_filtrados, labels=etiquetas_filtradas, autopct='%1.1f%%')

        ax1.set_title('% expresión global de emociones')

    def exportar_estadistica_pdf(self, estadistica, paciente_name):
        """
        Creamos el documento .pdf donde vamos a exportar las estadísticas generales de la terpia seleccionada
        @param estadistica: Estadísticas de la terpia
        @param paciente_name: Clave del paciente seleccionado.
        """
        # Crear figuras
        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_emociones_tiempo(estadistica, figura, gs)
        self.mostrar_grafico_atencion_tiempo(estadistica, figura, gs)
        self.mostrar_grafica_emociones_tarta(estadistica,figura,gs)

        figura.tight_layout()

        # Guardar figura en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figura.savefig(tmpfile.name)
            imagen_path = tmpfile.name

        # Crear el PDF
        nombre_pdf = f"estadisticas_terapia_{estadistica.get_id_terapia()}_f{estadistica.get_fecha()}.pdf"
        pdf_path = os.path.join(self.route, nombre_pdf)
        c = pdf_canvas.Canvas(pdf_path, pagesize=A4)
        width, height = A4
        margin = 50
        y_cursor = height - margin

        paciente = self.paciente_mapa[paciente_name]

        def draw_line(text, font="Helvetica", size=12, spacing=15):
            nonlocal y_cursor
            if y_cursor < 100:
                c.showPage()
                y_cursor = height - margin
            c.setFont(font, size)
            c.drawString(margin, y_cursor, text)
            y_cursor -= spacing

        # Información paciente
        draw_line("Paciente:", "Helvetica-Bold", 16, 20)
        draw_line(f"Paciente ID: {paciente.get_paciente_id()}")
        draw_line(f"Nombre: {paciente.get_nombre()} {paciente.get_apellido()}")
        draw_line(f"Expediente: {paciente.get_num_expediente()}", spacing=25)

        # Información terapeuta
        draw_line("Terapeuta:", "Helvetica-Bold", 16, 20)
        draw_line(f"Terapeuta ID: {self.terapeuta.get_terapeuta_id()}")
        draw_line(f"Nombre: {self.terapeuta.get_nombre()} {self.terapeuta.get_apellido()}", spacing=25)

        # Información terapia
        draw_line(f"Estadísticas de la Terapia ID {estadistica.get_id_terapia()}", "Helvetica-Bold", 16, 20)
        draw_line(f"Fecha: {estadistica.get_fecha()}")
        draw_line(f"Hora de inicio: {estadistica.get_horacomienzo()}")
        draw_line(f"Duración total: {estadistica.get_tiempototal() / 60:.2f} min")
        draw_line(f"Emoción más expresada: {estadistica.get_emocion_mas_expresada()}", spacing=25)

        # Observaciones
        draw_line("Observaciones:", "Helvetica-Bold", 12, 18)
        c.setFont("Helvetica", 12)
        text_obj = c.beginText(margin, y_cursor)
        for line in estadistica.get_observaciones().splitlines():
            if y_cursor < 100:
                c.drawText(text_obj)
                c.showPage()
                y_cursor = height - margin
                text_obj = c.beginText(margin, y_cursor)
            text_obj.textLine(line)
            y_cursor -= 14
        c.drawText(text_obj)
        y_cursor -= 20

        # Si no hay espacio suficiente para imagen, se pasa a una nueva página
        if y_cursor < 300:
            c.showPage()
            y_cursor = height - margin

        # Insertar imagen
        img_width = 16 * cm
        img_height = 13 * cm
        c.drawImage(ImageReader(imagen_path), margin, y_cursor - img_height, width=img_width, height=img_height)

        c.showPage()
        c.save()

        os.remove(imagen_path)  # Eliminar imagen temporal

        self.__mostrar_mensaje_exito(f"PDF creado con éxito en la ruta {pdf_path}")
        self._logger.info(f"[INFO] PDF guardado en: {pdf_path}")

    """ **************************************************************************************
        ****************************** MÉTODOS AUXILIARES ************************************
        ************************************************************************************** """

    def __reset_page(self, no_eliminar):
        """
        Eliminamos todo el contenido que haya en la vista.
        Esto nos permite refrescar el contenido correctamente
        @param no_eliminar: Pasamos los componente que no queremos eliminar
        """
        for componente in self.root.winfo_children():
            if componente != no_eliminar:
                componente.destroy()

    def __mostrar_mensaje_exito(self, notificacion):
        """
        Mostramos una notificacion en una ventana nueva mostrando el mensaje que se pasa por la variable "notificación"
        @param notificacion: Mensaje a mostrar
        @return: Ventana emergente
        """
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

    def __obtener_id_terpeuta(self, nombre_y_apellidos):
        """
        Como para crear el paciente necesitamos el id y no su nombre y apellido, además de que tampoco podemos buscar
        por nombre y apellido ya juntado, vamos a emplear este método para obtener el id del terpeuta asignado.
        @param nombre_y_apellidos: Nombre y apellidos del paciente
        @return: Id del terapeuta
        """
        # Primero vamos a ahorrarnos la búsqueda en la bd si este terpaueta somos nosotros
        if (self.terapeuta.get_nombre() + " " + self.terapeuta.get_apellido()) == nombre_y_apellidos:
            return self.terapeuta.get_terapeuta_id()
        # Si no lo somos entonces realizamos una búsqueda en BD
        terapeutas = self.database.obtener_all_terapeutas()
        for terpeuta in terapeutas:
            if (terpeuta.get_nombre() + " " + terpeuta.get_apellido()) == nombre_y_apellidos:
                return terpeuta.get_terapeuta_id()

    """
        
    """

    def __obtener_mapa_pacientes(self):
        """
        Para acceder rápidamente a los paciente y no consultar repetidamente a la BD,
        creamos un mapa clave-valor de los pacientes donde la clave va a ser la concatenación del nombre y apellidos.
        @return: Mapa de pacientes
        """
        paciente_mapa = {}
        pacientes = self.database.obtener_all_pacientes()
        # Si queremos aumentar la seguridad no cargaremos las contraseñas
        for paciente in pacientes:
            paciente_mapa[f"{paciente.get_nombre()} {paciente.get_apellido()}"] = paciente
        return paciente_mapa

    def __obtener_mapa_terapeuta(self):
        """
        Para acceder rápidamente a los paciente y no consultar repetidamente a la BD,
        creamos un mapa clave-valor de los pacientes donde la clave va a ser la concatenación del nombre y apellidos.
        @return:
        """
        terapeuta_mapa = {}
        terapeutas = self.database.obtener_all_terapeutas()
        for terapeuta in terapeutas:
            terapeuta_mapa[f"{terapeuta.get_nombre()} {terapeuta.get_apellido()}"] = terapeuta
        return terapeuta_mapa

    def __parse_intervalos(self, data):
        """
        Como desde BD los intervalos nos vienen en texto plano, lo transformamos a un diccionario para hacer uso de él
        @param data: Datos a transformar.
        @return: Los datos transformados o una lista vacía si no se ha podido hacer el parseo.
        """
        if isinstance(data, str):
            try:
                # Añadir coma entre "número fin" si falta (entre comillas o no)
                data = re.sub(r'("inicio"\s*:\s*\d+)\s+("fin"\s*:\s*\d+)', r'\1, \2', data)
                parsed = data
                return json.loads(parsed)
            except json.JSONDecodeError as e:
                self._logger.error(f"[ERROR] Al parsear a json los intervalos: {e}")
                return []
        return data or []

if __name__ == "__main__":
    interfaz = AplicacionTEA()
    interfaz.comenzar_programa()


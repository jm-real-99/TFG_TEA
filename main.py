import json
import time
from Emociones import Emociones
from Calculo_estadisticas import Calculo_estadisticas
from Camara import Camara
import cv2
from PIL import Image, ImageTk

import tkinter as tk
from datetime import datetime, date
from Paciente import Paciente
from Terapeuta import Terapeuta
from Database import DataBase
from Estadistica import Estadistica

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
from reportlab.lib.units import cm

import re


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
                                               self.terapeuta.get_terapeuta_id(), date.today() ,datetime.now())
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

    """
        Inicializamos la configuración necesaria para la Cámara y la vista de esta
    """
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

    """
        Mostramos el frame que ha recogido la cámara y lo mostramos. Función recursiva
    """
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

    """
        Actualizamos la gráfica con las emociones detectadas durante la terapia
    """
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

    """
        Indicamos al bucle que deberá parar la terapia
    """
    def parar_terapia(self,camara):
        print("Terapia detenida por el usuario.")
        self.end = True

    """
        Hacemos las gestiones necesarias para finalizar la terapia.
    """
    def cerrar_terapia(self, camara):
        camara.cerrar_camara()
        self.add_observaciones()

    def add_observaciones(self):
        self.reset_page(None)
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
        texto = self.text_area.get("1.0", tk.END).strip()
        if texto:
            self.estadisticas.set_observaciones(texto)

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

    """
        Mostramos una notificacion en una ventana nueva mostrando el mensaje que se pasa por la variable "notificación"
    """
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
        print("Fecha y Hora Comienzo:", self.estadisticas.get_horacomienzo())
        print("Fecha y Hora Fin:", self.estadisticas.get_horafin())
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
    *********************************************** """

    """
        Damos a elegir al usuario el paciente del que vamos a mostrar las estdísticas
    """
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

    """
        Mostramos las estadísticas del paciente pasado por parámetro
    """
    def consultas_estadisticas_paciente(self, paciente_selected):
        self.reset_page(None)

        tk.Label(self.root, text=paciente_selected).pack(pady=2)

        tk.Button(self.root, text="Volver", command=lambda: self.mostrar_main(None)).pack(pady=10)

        paciente = self.paciente_mapa[paciente_selected]
        estadisticas = self.database.obtener_estadisticas_by_paciente(paciente.get_paciente_id())
        calculo_estadisticas = Calculo_estadisticas(estadisticas)
        calculo_estadisticas.inicializarDatos()

        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_tarta_emociones_general(calculo_estadisticas,figura, gs)
        self.mostrar_grafico_barra_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_tarta_atencion_general(calculo_estadisticas,figura, gs)

        tk.Label(self.root, text=f"Mejora desde el inicio en la expresión de emociones: {calculo_estadisticas.mejora_inicio_expresion_emociones:.2f}").pack(pady=2)
        tk.Label(self.root,
                 text=f"Tendencia en la mejora de expresión de emociones: {calculo_estadisticas.mejora_tendencia_expresion_emociones:.2f}").pack(
            pady=2)
        tk.Label(self.root,
                 text=f"Mejora desde el inicio en la atención: {calculo_estadisticas.mejora_inicio_atencion:.2f}").pack(
            pady=2)
        tk.Label(self.root,
                 text=f"Tendencia en la mejora de atención: {calculo_estadisticas.mejora_tendencia_atencion:.2f}").pack(
            pady=2)
        tk.Label(self.root,
                 text=f"Expresión más expresada: {calculo_estadisticas.emocion_mas_expresada.name}").pack(
            pady=2)

        tk.Button(self.root, text="Exportar a PDF",
                  command=lambda: self.exportar_estadisticas_generales_pdf(calculo_estadisticas, paciente_selected)).pack(
            pady=10)

        # Crear el lienzo de Tkinter con la figura
        canvas = FigureCanvasTkAgg(figura, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Botones por cada terapia individual

        # Creamos un frame para contener los botones
        botones_frame = tk.Frame(self.root)
        botones_frame.pack(pady=(10, 30))
        for estadistica in estadisticas:

            btn = tk.Button(
                self.root,
                text=f"Terapia {estadistica.get_fecha()}",
                command=lambda est=estadistica: self.mostrar_estadisticas_terapia(est, paciente_selected)
            )
            btn.pack(side=tk.LEFT, padx=5)

        # Ajustar layout automáticamente para evitar superposición
        figura.tight_layout()


    def mostrar_grafico_tarta_emociones_general(self,calculo_estadisticas, figura, gs):
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
        if (all(x == 0.0 for x in valores_emociones_porcentaje)):
            # Crear gráfico de tarta
            ax1.pie([100], labels=[Emociones.NONE.name], autopct='%1.1f%%')
        else:
            ax1.pie(valores_emociones_porcentaje, labels=emociones_etiquetas, autopct='%1.1f%%')
        ax1.set_title('% expresión global de emociones')

    def mostrar_grafico_barra_emociones_general(self, calculo_estadisticas, figura, gs):
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
        valores_atencion_porcentaje = [calculo_estadisticas.porcentaje_atencion,
                                       100 - calculo_estadisticas.porcentaje_atencion]
        atención_etiquetas = ["Atención", "No atención"]

        # Creamos un gráfico de tarta de la atención
        ax3 = figura.add_subplot(gs[1, :])  # Gráfico de tarta atención
        if (all(x == 0.0 for x in valores_atencion_porcentaje)):
            # Crear gráfico de tarta
            ax3.pie([100], labels=[atención_etiquetas[1]], autopct='%1.1f%%')
        else:
            ax3.pie(valores_atencion_porcentaje, labels=atención_etiquetas, autopct='%1.1f%%')
        ax3.set_title('% atención global')

    def exportar_estadisticas_generales_pdf(self,calculo_estadisticas, paciente_key ):
        paciente = self.paciente_mapa[paciente_key]

        # Crear figuras
        figura = Figure(figsize=(10, 8), dpi=100)
        gs = figura.add_gridspec(2, 2)
        self.mostrar_grafico_tarta_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_barra_emociones_general(calculo_estadisticas, figura, gs)
        self.mostrar_grafico_tarta_atencion_general(calculo_estadisticas, figura, gs)

        figura.tight_layout()

        # Guardar figura en un archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            figura.savefig(tmpfile.name)
            imagen_path = tmpfile.name

        # Crear PDF
        pdf_path = f"resumen_terapias_{paciente_key}_{paciente.get_num_expediente()}.pdf"
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

        print(f"[INFO] PDF guardado en: {pdf_path}")

    def mostrar_estadisticas_terapia(self, estadistica, paciente):
        print(f"Mostrando estadísticas para la terapia con ID: {estadistica.get_id_terapia()}")
        self.reset_page(None)

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
                 text=f"Emoción más expresada:  {estadistica.get_emocion_mas_expresada()}").pack(pady=2)
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
        ax = figura.add_subplot(gs[0, 0])
        ax.set_title("Emociones a lo largo de la terapia")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Emoción")

        # Guardamos en variables locales ya transformadas
        enfadado = self.parse_intervalos(estadistica.get_enfadado())
        disgustado = self.parse_intervalos(estadistica.get_disgustado())
        miedoso = self.parse_intervalos(estadistica.get_miedoso())
        contento = self.parse_intervalos(estadistica.get_contento())
        triste = self.parse_intervalos(estadistica.get_triste())
        sorprendido = self.parse_intervalos(estadistica.get_sorprendido())
        neutro = self.parse_intervalos(estadistica.get_neutro())

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

        ax.set_xlim(0, estadistica._tiempototal)
        ax.grid(True)

    def mostrar_grafico_atencion_tiempo(self, estadistica, figura, gs):
        ax = figura.add_subplot(gs[0, 1])
        ax.set_title("Atención a lo largo de la terapia")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Atención")

        # Convertir datos JSON a lista de intervalos
        intervalos = self.parse_intervalos(estadistica.get_atencion())

        if intervalos:
            bars = [(item["inicio"], item["fin"] - item["inicio"]) for item in intervalos]
            ax.broken_barh(bars, (0.3, 0.4), facecolors='green')  # Altura 0.4 en y=0.3
            ax.set_yticks([0.5])
            ax.set_yticklabels(["Atento"])
        else:
            ax.text(0.5, 0.5, "Sin datos de atención", ha="center", va="center", transform=ax.transAxes)

        ax.set_xlim(0, estadistica._tiempototal)
        ax.set_ylim(0, 1)
        ax.grid(True)

    def mostrar_grafica_emociones_tarta(self, estadistica, figura, gs):
        # Creamos un gráfico de tarta
        emociones_etiquetas = [Emociones.ENFADO.name, Emociones.DISGUSTADO.name, Emociones.MIEDOSO.name,
                               Emociones.CONTENTO.name,
                               Emociones.TRISTE.name, Emociones.SORPRENDIDO.name, Emociones.NEUTRO.name]
        emociones_porcentajes = estadistica.get_emociones_porcentajes()
        ax1 = figura.add_subplot(gs[1, :])  # Gráfico de tarta
        if (all(x == 0.0 for x in emociones_porcentajes)):
            # Crear gráfico de tarta
            ax1.pie([100], labels=[Emociones.NONE.name], autopct='%1.1f%%')
        else:
            ax1.pie(emociones_porcentajes, labels=emociones_etiquetas, autopct='%1.1f%%')

        ax1.set_title('% expresión global de emociones')

    def exportar_estadistica_pdf(self, estadistica, paciente_name):
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
        pdf_path = f"estadisticas_terapia_{estadistica.get_id_terapia()}_f{estadistica.get_fecha()}.pdf"
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

        print(f"[INFO] PDF guardado en: {pdf_path}")

    def parse_intervalos(self, data):
        if isinstance(data, str):
            try:
                # Añadir coma entre "número fin" si falta (entre comillas o no)
                data = re.sub(r'("inicio"\s*:\s*\d+)\s+("fin"\s*:\s*\d+)', r'\1, \2', data)
                parsed = data
                return json.loads(parsed)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Al parsear a json los intervalos: {e}")
                return []
        return data or []

if __name__ == "__main__":
    interfaz = VentanaInicioSesion()
    interfaz.comenzar_programa()

"""
TODO:
    
- Ver como mostrar en la interfaz gráfica los resultados de las estadísticas de los pacientes: 
    - Añadir en texto información como los minutos totales, nº de terapias, apariciones totales, etc
    - Incluir vista para ver información por terapia
    - Mostrar los datos para solo esa terapia.
    - Exportar terapias a PDF

     
Menos importantes:
- Hacer menú de terapeuta admin para que puedas crear desde la aplicación otros usuarios de terpeutas
"""

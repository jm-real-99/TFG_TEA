# TFG_TEA
### Juan Manuel Real Domínguez

### OBJETIVO
El objetivo principal de este trabajo de fin de grado es aplicar los conocimientos, competencias y habilidades adquiridas a lo largo del grado cursado con el fin de desarrollar un proyecto que cumpla con los requisitos y especificaciones que mencionamos a continuación:
1.	Diseñar y desarrollar un robot capaz de interactuar con pacientes TEA de manera efectiva y segura.
2.	Evaluar el impacto del robot en el bienestar y la calidad de vida de los pacientes TEA y sus cuidadores.
3.	Analizar la efectividad del robot en el apoyo a la adquisición y mejora de habilidades sociales y emocionales en pacientes TEA.
4.	Investigar la percepción de los pacientes TEA y sus cuidadores sobre la usabilidad y utilidad del robot.
5.	Establecer las limitaciones y posibilidades del robot para su uso en terapias para pacientes TEA.

### ORGANIZACIÓN 
En este repositorio podremos encontrar el código relacionado con mi trabajo de fin de grado.
Como se puede ver está dividido en distintos ficheros que corresponden a clases: 
- **Main.py**: Script donde contenemos la clase de la interfaz gráfica.
- **Camara.py**: Script con la clase correspondiente a la terapia, obtiene la imagen de la webcam y la distribuye a los gestores correspondientes.
- **GestorEmociones.py**: Script con la clase que gestiona el análisis de las emociones dado un frame.
- **GestorAtencion.py**: Script con la clase que gestiona el análisis de la atención dado un frame, se apoya en GazeTraking.
- **CalculoEstadisticas.py**: Script que contiene la clase correspondiente al calculo de las estadísticas dados los datos recabados por la terapia
- **Database.py**: Script con la clase interfaz de la base de datos.
- **Emociones.py**: Enum con las emociones que vamos a obtener.
- **Estadistica.py**: Script que contiene la clase correspondiente a las estadísticas que almacenamos en BD
- **LoggerManager.py**: Script con el gestor de Logs.
- **Paciente.py**: Entidad paciente.
- **Terapeuta.py**: Entidad terapeuta.
- 
Para información más detallada, consultar la memoria del trabajo.

La organización de este proyecto se está llevando mediante la herramienta de figma. Se puede consultar en el siguiente enlace: [Board Figma](https://www.figma.com/file/zuwWNhBL8BXATAkKylHJ8S/TFG-ROBOTICA?type=whiteboard&t=pxDveDdwZCL8EPoZ-1). 

## INSTALACION
Hay que instalar python 3.9 y las siguientes librerías:
- opencv-python mediante el comando: pip install opencv-python
- cmake mediante el comando: pip install cmake
- dlib mediante el comando: pip install dlib

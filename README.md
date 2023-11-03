# TFG_TEA
### Juan Manuel Real Domínguez

### OBJETIVO
El objetivo principal de este trabajo de fin de grado es aplicar los conocimientos, competencias y habilidades adquiridas a lo largo del grado cursado con el fin de desarrollar un proyecto que cumpla con los requisitos y especificaciones que mencionamos a continuación:
1.	Diseñar y desarrollar un robot capaz de interactuar con pacientes TEA de manera efectiva y segura.
2.	Evaluar  el impacto del robot en el bienestar y la calidad de vida de los pacientes TEA y sus cuidadores.
3.	Analizar la efectividad del robot en el apoyo a la adquisición y mejora de habilidades sociales y emocionales en pacientes TEA.
4.	Investigar la percepción de los pacientes TEA y sus cuidadores sobre la usabilidad y utilidad del robot.
5.	Establecer las limitaciones y posibilidades del robot para su uso en terapias para pacientes TEA.

### ORGANIZACIÓN 
En este repositorio podremos encontrar el código relacionado con mi trabajo de fin de grado.
Como se puede ver está dividido en distintos módulos: 
- **camera-core**: Este será el servicio que se encargará de analizar los comportamientos del niño con el fin de complementar las analíticas y ver si hay un progreso también en la atención o imitación de gestos.
- **interactive-app**: Módulo donde Este será el servicio con el que jugará el niño. Mediante los juegos propuestos podremos ir tomando las métricas que se irán guardando en la base de datos.
- **monitoring-app**: Este será el servicio donde podremos ir siguiendo el seguimiento del paciente. Esto se hará mediante la consulta en BD y obteniendo los datos, que los modelizará para que el asistente pueda ver el progreso.
- **persistence-api**: Gracias a esta API podremos realizar la conexión con la base de datos mysql de una manera homogénea en los distintos proyectos.

Para información más detallada, consultar los README.md de cada proyecto. 

La organización de este proyecto se está llevando mediante la herramienta de figma. Se puede consultar en el siguiente enlace: [Board Figma](h[ttps://pages.github.com/](https://www.figma.com/file/zuwWNhBL8BXATAkKylHJ8S/TFG-ROBOTICA?type=whiteboard&node-id=0-1&t=jODJ2miafOtQoKqD-0)https://www.figma.com/file/zuwWNhBL8BXATAkKylHJ8S/TFG-ROBOTICA?type=whiteboard&node-id=0-1&t=jODJ2miafOtQoKqD-0). 

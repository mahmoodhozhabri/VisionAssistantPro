# Documentación de Vision Assistant Pro

<!-- DOWNLOAD_COUNT_START --> Descargas totales: 75.451 <!-- DOWNLOAD_COUNT_END -->

**Vision Assistant Pro** es un asistente de IA avanzado y multimodal para NVDA. Utiliza motores de IA de primer nivel para proporcionar lectura de pantalla inteligente, traducción, dictado por voz y análisis de documentos.

_Este complemento fue lanzado a la comunidad en honor al Día Internacional de las Personas con Discapacidad._

## 1. Configuración

Ve a **Menú de NVDA > Preferencias > Configuración > Vision Assistant Pro**. El diálogo de configuración está organizado en 9 pestañas accesibles: **Conexión**, **Asistente en vivo**, **Comportamiento de IA**, **Idiomas de traducción**, **Lector de documentos**, **Vídeo**, **CAPTCHA**, **Indicaciones** y **Avanzado**.

### 1.1 Pestaña Conexión

- **Proveedor:** Selecciona tu servicio de IA preferido. Los proveedores compatibles incluyen **Google Gemini**, **OpenAI**, **Mistral**, **Groq**, **MiniMax** y **Personalizado** (servidores compatibles con OpenAI como Ollama, LM Studio, Jan.ai o KoboldCPP).
- **Clave API:** Introduce una o varias claves API (separadas por comas o saltos de línea) para rotación automática.
- **Obtener modelos:** Presiona este botón después de introducir tu clave API para descargar la lista de modelos disponibles más reciente del proveedor.
- **Modelo de IA:** Selecciona el modelo principal utilizado para el chat general y análisis.
- **Enrutamiento avanzado de modelos (específico por tarea):** Selecciona opcionalmente modelos dedicados desde desplegables para tareas de OCR, STT, TTS, Operador de IA, Vídeo y Asistente en vivo. Para Gemini, los modelos se categorizan dinámicamente por capacidad sin saturar la lista.
- **Configuración del proveedor personalizado:** Configura puntos de acceso locales o personalizados. Incluye **Configurar IA local** (configuración en un clic para Ollama, LM Studio, Jan.ai o KoboldCPP) y **Configuración avanzada de punto de acceso**.
- **Configuración de proxy:** Soporte completo para tunelización y redirección de puntos de acceso en todo el complemento (incluyendo el Asistente en vivo, el Observador ambiental y el TTS). Introduce tu **URL de proxy** y selecciona tu **Modo de proxy**:
  - **Detección automática:** Detecta automáticamente si la URL es un proxy de reenvío o un proxy inverso.
  - **Proxy SOCKS5:** Fuerza la tunelización de reenvío mediante SOCKS5 con autenticación de usuario y contraseña según RFC 1929 y resolución de nombres de dominio.
  - **Proxy HTTP:** Fuerza la tunelización de reenvío mediante un proxy HTTP con autenticación básica.
  - **Proxy inverso:** Reemplazo directo de punto de acceso para puertas de enlace de IA personalizadas y réplicas autoalojadas (las credenciales están desactivadas en este modo).
- **Probar conexión del proxy:** Un botón no bloqueante que prueba la conectividad y mide la latencia del servidor en milisegundos (anunciada por NVDA).
- **Opciones de conexión y salida:** Configura URL del proxy, comprobaciones de actualización al inicio, limpiar Markdown en el chat, copiar respuestas de IA al portapapeles y salida directa (sin ventana de chat).
- **Guardar chats en el historial:** Mantén tus conversaciones de chat en la lista de Historial.

### 1.2 Pestaña Asistente en vivo

- **Asistente en vivo: Salida directa (sin ventana):** Inicia el Asistente en vivo sin su ventana de conversación; ábrela después con la tecla Recuperar último resultado (`Espacio`).
- **Pulsar para hablar:** Activa el modo de pulsar para hablar. Cuando está activado, el micrófono solo envía audio mientras mantienes presionada la tecla asignada.
- **Tecla de pulsar para hablar:** Presiona las teclas para registrar el atajo (por ejemplo, `F12` o `Ctrl+F12`) — incluso puedes asignar un modificador solo como `Ctrl izquierdo`. Mantén la tecla para hablar y suéltala al terminar; un pitido corto confirma cada pulsación y suelta.

Nota: Esta pestaña aparece solo cuando **Google Gemini** (o un proveedor personalizado compatible con Gemini) es tu proveedor activo.

### 1.3 Pestaña Comportamiento de IA

- **Creatividad (Temperatura):** Controla la aleatoriedad y creatividad de la IA (de 0,0 a 2,0). Los valores más bajos producen resultados de traducción/OCR más deterministas y precisos.

### 1.4 Pestaña Idiomas de traducción

- **Idioma de origen:** Selecciona tu idioma de entrada predeterminado.
- **Idioma de destino:** Selecciona tu idioma de traducción de destino principal.
- **Idioma de respuesta de la IA:** Selecciona el idioma para las respuestas generales de la IA.
- **Intercambio inteligente:** Intercambia automáticamente los idiomas de origen y destino según el idioma detectado.

### 1.5 Pestaña Lector de documentos

- **Motor OCR:** Elige entre **Chrome (Rápido)** para resultados rápidos o **IA (Avanzado)** para una mejor conservación del diseño.
- **Tamaño del lote OCR:** Especifica páginas por solicitud (configura en 0 para procesamiento en una sola solicitud).
- **Describir imágenes en línea:** Activa o desactiva las descripciones de imágenes en línea durante la extracción de texto de documentos.
- **Incluir números de página al exportar:** Activa o desactiva los números de página y separadores en las salidas de documentos de varias páginas.
- **Voz TTS:** Selecciona el estilo de voz predeterminado para la generación de audio.
- **Guardar documentos en el historial:** Mantén los documentos abiertos en la lista de Historial; el texto OCR en caché y los datos de reanudación se siguen guardando igualmente.

### 1.6 Pestaña Vídeo

- **Tamaño de fragmento de vídeo:** Duración del segmento en minutos para la generación de audiodescripción (configura en 0 para procesar el archivo completo).
- **Añadir lista de personajes:** Opción para añadir el diccionario de personajes como primera entrada de subtítulo.
- **Añadir aviso de IA:** Opción para insertar un aviso de IA al principio de los subtítulos SRT del vídeo.
- **Diccionario de personajes y gestión de series:** Añade, edita, importa o administra nombres de personajes, descripciones físicas y roles por serie — la IA vincula automáticamente los personajes detectados con tu diccionario y fusiona los nuevos a medida que analizas más episodios. Tus notas manuales siempre se conservan con prioridad sobre las actualizaciones de la IA, mientras que las descripciones físicas se mantienen al día en todos los episodios.

### 1.7 Pestaña CAPTCHA

- **Habilitar solucionador visual de CAPTCHA:** Activa o desactiva la resolución automática de desafíos visuales (hCaptcha, reCAPTCHA).
- **Método de CAPTCHA de texto:** Elige entre capturar el **Objeto del navegador** o la **Pantalla completa**.

### 1.8 Pestaña Indicaciones

- **Administrar indicaciones:** Abre un diálogo dedicado para personalizar las indicaciones predeterminadas del sistema o crear, editar, reordenar y previsualizar indicaciones personalizadas con variables dinámicas (por ejemplo, `[selection]`, `[screen_fg_obj]`).
- **Atajos para indicaciones personalizadas:** Asigna una tecla de atajo dedicada a cualquier indicación personalizada directamente en el Administrador de indicaciones. Presiona las teclas para registrarlas — las teclas simples funcionan dentro de la Capa de comandos (y globalmente como `NVDA + Shift + tecla`), mientras que las combinaciones como `Control + Shift + 1` funcionan globalmente por sí solas.
- **Comportamiento de retroalimentación por indicación:** Elige cómo cada indicación entrega su resultado individualmente (Configuración global, Copiar al portapapeles, Salida directa / mensaje de NVDA, Copiar al portapapeles + salida directa, o Ventana de chat).

### 1.9 Pestaña Avanzado y registro global

Navega a la pestaña **Avanzado** para configurar el registro global del complemento:

- **Habilitar archivo de registro dedicado:** Activa el registro de todos los eventos operativos, tráfico de API y errores en todos los módulos del complemento en un archivo separado (`vision_assistant.log`).
- **Nivel de registro:** Selecciona la verbosidad entre **Depuración (todos los detalles)**, **Información (información general)**, **Advertencia (solo advertencias)** y **Error (solo errores)**.
- **Conservar registros durante:** Configura períodos de retención automática para limpiar entradas de registro antiguas (desde 1 hora hasta 90 días).
- **Controles de gestión de registros:** Usa **Abrir archivo de registro**, **Abrir carpeta de registro** o **Limpiar archivo de registro** para inspeccionar o borrar datos de registro directamente sin reiniciar NVDA.
- **Directorio de datos unificado:** Todos los archivos de datos del complemento (historial, series, etiquetas, progreso de OCR, cachés y registros) se almacenan en una única carpeta `VisionAssistant` dentro de tu directorio de configuración de NVDA — manteniendo todo organizado y facilitando las copias de seguridad manuales.

### 1.10 Copia de seguridad y restauración de configuración

La pestaña **Avanzado** también incluye una sección de **Copia de seguridad y restauración**:

- **Copia de seguridad:** Guarda tu configuración en un único archivo JSON. Al hacer clic, eliges qué incluir: **Todo** (configuración, etiquetas personalizadas, progreso de OCR e historial) o **Solo configuración**.
- **Restaurar:** Carga una copia de seguridad guardada previamente para restaurar tu configuración y datos en cualquier momento, en cualquier equipo o después de reinstalar NVDA. Se te pedirá confirmación primero, ya que la restauración reemplaza toda la configuración y datos actuales.

## 2. Administrador de claves de la API de Gemini

Crear una clave API de Gemini en **aistudio.google.com** solía ser el paso más difícil del complemento. Con un lector de pantalla las páginas eran confusas, y algunas personas simplemente no podían crear una clave. El **Administrador de claves API de Gemini** resuelve ese problema. Presiona **G** en la Capa de comandos, o abre **Menú de NVDA > Preferencias > Configuración > Vision Assistant > Conexión** y presiona **Obtener una clave API de Gemini...**.

- **Iniciar sesión:** Al abrir el administrador, tu navegador predeterminado se abre directamente con la página segura de inicio de sesión de Google. Inicia sesión con tu cuenta de Google — no se requieren herramientas externas, SDKs ni configuraciones de línea de comandos. La cuenta con la que iniciaste sesión siempre se muestra en el botón **Cerrar sesión**.
- **Crear una clave:** Después de iniciar sesión, puedes crear una clave de inmediato con **Nuevo proyecto y clave** sin ninguna configuración previa. Si ya tienes proyectos existentes, aparecen en una lista sencilla donde puedes seleccionar uno y presionar **Crear clave para el proyecto seleccionado**.
- **Qué sucede después:** La nueva clave se copia al portapapeles de inmediato, se guarda dentro del complemento para más tarde, y se te pregunta una vez si deseas añadirla a la lista de claves del complemento. Eso es todo lo que necesitas — sin tener que buscar entre páginas web.
- **Trabajar con tus claves:** **Copiar clave del proyecto seleccionado** copia la clave del proyecto que tienes seleccionado, **Copiar última clave creada** copia la clave que creaste hace un momento, y **Exportar claves guardadas a CSV...** guarda todo lo que has creado en un archivo.
- **Eliminar una clave:** **Eliminar una clave...** muestra las claves que existen en el proyecto seleccionado, te pregunta cuál quieres quitar, y confirma antes de eliminarla. Eliminar una clave también la quita de la lista de claves del complemento, de modo que nunca queda una clave rota en la rotación. Las claves creadas fuera del complemento también se pueden eliminar, siempre que tu cuenta tenga permiso sobre ese proyecto.
- **Cerrar sesión:** **Cerrar sesión** elimina la información de inicio de sesión almacenada en tu equipo, para que puedas cambiar a otra cuenta cuando quieras.

## 3. Capa de comandos y atajos

Para evitar conflictos de teclado, este complemento usa una **Capa de comandos**.

1. Presiona **NVDA + Shift + V** (tecla maestra) para activar la capa (escucharás un pitido).
2. Suelta las teclas, luego presiona una de las siguientes teclas individuales:

| Tecla                   | Función                                         | Descripción                                                                                                                                                                                                                                                            |
| ----------------------- | ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Shift + A**           | **Operador de IA**                              | **Operación autónoma:** Indica a la IA que realice una tarea en tu pantalla. Presionarlo de nuevo cancela las operaciones activas al instante.                                                                         |
| **E**                   | **Explorador de interfaz**                      | **Clic interactivo:** Identifica y hace clic en elementos de la interfaz en cualquier aplicación.                                                                                                                                      |
| **T**                   | Traductor inteligente                           | Traduce el texto bajo el cursor del navegador o la selección.                                                                                                                                                                                          |
| **Shift + T**           | Traductor del portapapeles                      | Traduce el contenido que hay actualmente en el portapapeles.                                                                                                                                                                                           |
| **R**                   | Refinador de texto                              | Resume, corrige gramática, explica o ejecuta **Indicaciones personalizadas**.                                                                                                                                                                          |
| **V**                   | Visión de objeto                                | Describe el objeto del navegador actual.                                                                                                                                                                                                               |
| **O**                   | Visión de pantalla completa                     | Analiza el diseño y contenido completo de la pantalla.                                                                                                                                                                                                 |
| **Shift + V**           | Análisis de vídeo                               | Analiza archivos de vídeo locales o vídeos en línea de **YouTube**, **Instagram**, **TikTok** o **Twitter (X)**.                                                                                                                    |
| **Control + V**         | Grabación de vídeo local                        | Graba un vídeo silencioso de tu pantalla y analiza las acciones y el diseño.                                                                                                                                                                           |
| **D**                   | Lector de documentos                            | Lector avanzado de PDF, imágenes y archivos de texto/HTML con selección de rango de páginas.                                                                                                                                                           |
| **F**                   | **Acción inteligente de archivo**               | Reconocimiento contextual desde imagen, PDF o archivos TIFF seleccionados.                                                                                                                                                                             |
| **M**                   | Transcripción y doblaje de medios               | Transcribe o dobla archivos de audio/vídeo (MP3, WAV, MP4, etc.) a tu idioma de destino.                                                                                                                            |
| **C**                   | Solucionador de CAPTCHA                         | Captura y resuelve CAPTCHAs.                                                                                                                                                                                                                           |
| **Shift + C**           | Chat directo                                    | Abre una interfaz de chat de texto directo con la IA.                                                                                                                                                                                                  |
| **S**                   | Dictado inteligente                             | Convierte voz a texto. Presiona para iniciar la grabación, vuelve a presionar para detener/escribir.                                                                                                                                   |
| **Control+T**           | Traducción de voz                               | Transcribe, traduce y escribe el resultado según la configuración de idioma.                                                                                                                                                                           |
| **Control+L**           | **Asistente en vivo**                           | **Copiloto en tiempo real (solo Gemini):** Inicia o finaliza una conversación de voz y pantalla en vivo con el asistente de IA.                                                                                     |
| **Control+A**           | **Operador en directo**                         | **Control autónomo del ordenador (solo Gemini):** Inicia o finaliza una sesión de operador en directo para delegar la pantalla y las acciones en la IA.                                                             |
| **G**                   | **Administrador de claves de la API de Gemini** | **Cree su clave API sin la web (solo Gemini):** Abre el administrador que configura lo que su ordenador necesita, abre el navegador para iniciar sesión y crea, copia o elimina una clave para el proyecto elegido. |
| **I**                   | Informe de estado                               | Anuncia el progreso actual (p. ej., "Escaneando...", "Inactivo").                                                                                   |
| **L**                   | **Etiquetar objeto**                            | **Etiquetado semántico con IA:** Etiqueta permanentemente el objeto o icono actual del navegador.                                                                                                                                      |
| **Shift + L**           | **Administrar/Escanear etiquetas**              | Abre el administrador de etiquetas (si existen) o busca elementos sin etiquetar en la aplicación.                                                                                                                                   |
| **U**                   | Buscar actualizaciones                          | Busca manualmente en GitHub la versión más reciente del complemento.                                                                                                                                                                                   |
| **Espacio**             | Recuperar el último resultado                   | Muestra la última respuesta de la IA en un cuadro de diálogo de chat para revisarla o continuar.                                                                                                                                                       |
| **H**                   | Ayuda de comandos                               | Muestra una lista de todos los atajos disponibles.                                                                                                                                                                                                     |
| **Control + H**         | **Historial**                                   | Abre el cuadro de diálogo Historial que enumera sus chats y documentos anteriores con filtros de tipo y opciones de eliminar/borrar.                                                                                                                   |
| **Alt + S**             | Opciones                                        | Abre el diálogo de configuración de Vision Assistant Pro.                                                                                                                                                                                              |
| **Alt + Q**             | Informe de claves con cuota agotada             | Informa del número de claves de API de Gemini que han superado su cuota diaria, los modelos afectados y su hora de restablecimiento.                                                                                                                   |
| **Alt + M**             | Auditoría de enrutamiento                       | Informa de los modelos de IA seleccionados actualmente en el enrutamiento avanzado para tareas especializadas (omitiendo los predeterminados).                                                                                      |
| **Arriba / Abajo**      | Navegación de configuración rápida              | Navega entre las categorías de configuración rápida (Proveedor, Modelo, Salida)... en la capa.                                                                                      |
| **Izquierda / Derecha** | Cambiar configuración rápida                    | Cambia el valor de la configuración rápida actualmente seleccionada.                                                                                                                                                                                   |

## 4. Chat e Historial

Las ventanas de chat y el diálogo de historial funcionan en todas las funciones, para que puedas revisar conversaciones y continuar exactamente donde lo dejaste.

### 3.1 Atajos de la ventana de chat

Cuando hay una ventana de chat abierta (Chat directo, chat de documento, refinar y similares), puedes revisar la conversación con:

- **Alt + Abajo:** Leer el siguiente mensaje.
- **Alt + Arriba:** Leer el mensaje anterior.
- **Alt + C:** Copiar el mensaje actual.

### 3.2 Historial (Control + H)

Presiona **Control + H** en la Capa de comandos para abrir el diálogo de **Historial** con tus chats y documentos anteriores, filtrables por tipo (Todo / Chats / Documentos). Abre un chat para continuar la conversación — incluyendo sus archivos adjuntos, que se vuelven a adjuntar automáticamente — o abre un documento y sigue leyendo. Presiona **Eliminar** en cualquier elemento para quitarlo, o **Borrar todo** para vaciar la lista. Para documentos, Eliminar pregunta si quieres quitar solo la entrada del historial o también borrar el texto OCR en caché de ese documento para que la próxima apertura lo vuelva a escanear desde cero — con una opción **No preguntar de nuevo** para recordar tu elección.

También puedes elegir qué recuerda la lista. **Guardar chats en el historial** (pestaña Conexión) y **Guardar documentos en el historial** (pestaña Lector de documentos) están activados de forma predeterminada, y ambos se pueden alternar desde la configuración rápida. La opción de documentos afecta solo a la entrada del Historial — el texto OCR en caché y los datos de reanudación siempre se conservan.

## 5. Operador de IA - Control autónomo del ordenador

El **Operador de IA** convierte Vision Assistant Pro de un lector pasivo en un asistente activo capaz de interactuar con tu equipo en tu nombre. Puedes pedirle que describa la pantalla, responda preguntas sobre lo que ve, o tome el control: hacer clic en botones, arrastrar elementos, escribir texto y navegar por aplicaciones mediante comandos en lenguaje natural.

¿La mayor ventaja? La mayor ventaja es que funciona perfectamente en software completamente inaccesible. Si estás atascado en una aplicación personalizada, un escritorio remoto o un sitio web donde tu lector de pantalla permanece en silencio, al Operador no le importa. Como "ve" la pantalla visualmente, puede encontrar, leer e interactuar con elementos que no tienen ninguna etiqueta de accesibilidad.

### 4.1 Cómo funciona

1. Presiona **NVDA + Shift + V**, luego presiona **Shift + A** para abrir el diálogo del Operador de IA.
2. Escribe lo que quieres hacer en lenguaje natural (por ejemplo, "Haz clic en el botón Guardar", "¿Qué dice el mensaje de error?" o "Cambia el nombre del archivo a final.pdf").
3. La IA analizará tu pantalla, identificará los elementos relevantes y realizará la acción o proporcionará la respuesta. Si una tarea requiere varios pasos, el Operador continuará trabajando hasta completarla.
4. Presiona **Shift + A** de nuevo en cualquier momento para cancelar una operación en curso al instante.

### 4.2 Acciones admitidas

El Operador entiende una amplia variedad de comandos:

- **Describir y responder**: "Describe el diseño de la pantalla" o "¿Qué dice el mensaje de error?"
- **Clic**: "Haz clic en el botón Guardar"
- **Clic derecho**: "Haz clic derecho en el archivo"
- **Doble clic**: "Haz doble clic en el documento"
- **Arrastrar y soltar**: "Arrastra el documento a la carpeta Archivo"
- **Escribir**: "Escribe 'Hola Mundo' en el cuadro de búsqueda"
- **Desplazar**: "Desplázate hacia abajo tres veces"
- **Tecla**: "Presiona Enter", "Presiona Tab", "Presiona Escape"
- **Tareas de varios pasos**: "Abre el Explorador de archivos, encuentra el informe y cámbiale el nombre a final.pdf"

### 4.3 Notas importantes

- **⚠️ Advertencia de uso de API:** El Operador envía una captura de pantalla de alta resolución con cada paso. El uso frecuente consumirá tu cuota de API mucho más rápido que las funciones estándar.
- **Aplicaciones de administrador:** Si NVDA no se ejecuta con privilegios de administrador, es posible que el Operador no pueda interactuar con ventanas que requieren permisos elevados. Esta es una limitación de seguridad de Windows, no un error del complemento.
- **Mejores prácticas:** Da comandos claros y específicos. "Haz clic en el botón azul Enviar en la parte inferior del formulario" funcionará mejor que simplemente "Haz clic en el botón".

### 4.4 Operador en directo (Control+A)

El Operador en vivo permite que el Asistente en vivo lleve a cabo lo que le pidas en tu equipo mientras hablas con él, incluidas aplicaciones que tu lector de pantalla no puede leer.
_(Nota: Esta función es exclusiva de Google Gemini y los proveedores personalizados compatibles con Gemini)._

- **Activación:** Presiona **Control+A** en la Capa de comandos para iniciar una sesión de operador en vivo; vuelve a presionarlo para finalizarla.
- **Cómo funciona:** Pide en lenguaje natural, por ejemplo "abre Chrome y busca un sitio web" o "cambia el nombre de este archivo a final". El operador observa la pantalla, lleva a cabo los pasos uno por uno, y sigue trabajando en solicitudes de varios pasos hasta que la tarea está hecha.
- **Anuncios:** Cada paso se dice con la propia voz del Asistente en vivo, y te avisa cuando la tarea termina, o por qué no se pudo completar.
- **CAPTCHA:** Si aparece un CAPTCHA, el operador primero intenta usar tu **solucionador de CAPTCHA** integrado; si no puede resolverlo, te pide que completes tú mismo el desafío accesible.
- **Detener:** Presiona **Detener acción del operador** en la ventana del Asistente en vivo para cancelar la tarea actual.
- **Configuración:** La propia instrucción del operador se puede editar en el Administrador de indicaciones (sección **En vivo**, **Instrucción del Operador en vivo**). El interruptor **Salida directa en vivo (sin ventana)** también está disponible en la configuración rápida.

## 6. Análisis de vídeo y audiodescripción

> **Nota:** Las funciones de análisis de vídeo y audiodescripción funcionan exclusivamente con el proveedor **Google Gemini**. Asegúrate de que tu proveedor activo sea Google Gemini.

Vision Assistant Pro incluye potentes funciones de procesamiento de vídeo diseñadas específicamente para usuarios ciegos. Puede analizar tanto vídeos en línea como grabaciones locales de pantalla para ofrecer descripciones visuales muy detalladas y generar guiones profesionales de audiodescripción (SRT).

### 5.1 Grabación de pantalla local (Control + V)

Si te encuentras con un vídeo silencioso, una animación o un tutorial en tu pantalla, puedes capturarlo directamente:

1. Presiona **NVDA + Shift + V** para entrar en la Capa de comandos, luego presiona **Control + V**.
2. El complemento grabará silenciosamente tu pantalla en segundo plano.
3. Presiona **Control + V** de nuevo para detener la grabación.
4. La IA analizará el segmento de vídeo grabado y proporcionará una descripción muy detallada.

### 5.2 Análisis de vídeo (Shift + V)

Puedes analizar tanto archivos de vídeo locales como vídeos en línea. Selecciona un archivo de vídeo local en el Explorador de Windows, o copia un enlace en línea al portapapeles. También puedes presionar **Shift + V** en cualquier lugar para abrir un diálogo donde examinar un archivo o pegar una URL.

- **Plataformas en línea compatibles:** YouTube, Instagram, TikTok y Twitter (X).
- La IA detectará automáticamente el archivo local o la URL, procesará el vídeo y proporcionará una descripción visual completa y un resumen de audio.
- **Caché de archivos de vídeo por 48 horas:** ¡Los vídeos cargados a Gemini se almacenan en caché durante 48 horas! Puedes regenerar salidas SRT o MP3 para el mismo vídeo sin volver a cargarlo — incluso después de reiniciar NVDA. La caché reconoce la clave API y se invalida automáticamente cuando esta cambia.

### 5.3 Generación de audiodescripción (SRT)

Para una experiencia más estructurada, el complemento puede generar guiones profesionales de audiodescripción en formato estándar SubRip (SRT).

- **Temporización inteligente de pausas:** La IA ancla las descripciones a los silencios naturales del audio para minimizar la superposición con el diálogo.
- **Seguimiento de personajes:** El motor realiza una pre-pasada para extraer personajes distintos según rasgos faciales inmutables. Construye un diccionario global para rastrear y etiquetar con precisión a los personajes en distintas escenas sin confusiones. También rastrea la **primera aparición** de cada personaje, describiendo su aspecto físico solo una vez — en el momento en que aparece por primera vez — y usando después solo los nombres ya establecidos para mantener la narrativa fresca y natural.
- **OCR textual literal:** Cualquier texto en pantalla (carteles, teléfonos, créditos) se cita literalmente.
- **Cómo usar:** Coloca el archivo `.srt` en la misma carpeta que tu vídeo con el mismo nombre. Configura tu reproductor multimedia (VLC, PotPlayer) para enrutar los subtítulos a tu lector de pantalla durante la reproducción.
- **Experiencia de guardado mejorada:** Al guardar archivos SRT o MP3, el cuadro de diálogo de archivo ahora se abre de forma predeterminada en la carpeta del vídeo de origen, ya sea que hayas abierto el vídeo desde el cuadro de diálogo de archivo o con Shift+V desde el Explorador.

### 5.4 Narración de audio sincronizada (exportación a MP3)

Más allá de crear archivos SRT basados en texto, el complemento funciona como una herramienta completa de producción de audiodescripción al sintetizar las descripciones en voz y mezclarlas con el vídeo. Ahora puedes elegir **TTS de Gemini en vivo** como motor de voz, que utiliza la API de Gemini en vivo para generar una narración de voz altamente realista y sin límites. Modos de mezcla disponibles para vídeos locales:

- **AD estándar (mezclar voz):** La narración se superpone sobre el audio del vídeo. Puedes aplicar **Atenuación de audio** para bajar el volumen de fondo.
- **AD extendida (pausar audio):** El motor pausa el audio original durante las descripciones. La detección de silencios ahora usa el modelo neuronal **Silero VAD** (descargado automáticamente en el primer uso, igual que ffmpeg y eSpeak) para una temporización precisa de los huecos — distinguiendo las pausas naturales del diálogo de la música y el ruido de fondo.
- **Vídeos de YouTube:** El MP3 contendrá solo la pista de voz de la IA sincronizada, sin el audio de fondo.

## 7. Transcripción y doblaje de medios (M)

El transcriptor de audio ha sido completamente reconstruido para admitir archivos de audio y vídeo (MP3, WAV, MP4, MKV, etc.). Presiona **M** en la Capa de comandos para seleccionar un archivo multimedia y elegir uno de los 3 modos de operación:

1. **Transcribir (idioma original)**: Transcribe con precisión el habla en su idioma original.
2. **Transcribir y traducir (idioma de destino)**: Transcribe el habla y la traduce al idioma de destino configurado.
3. **Doblar y traducir (idioma de destino)** _(solo Gemini)_: Transcribe el habla, la traduce al idioma de destino y sintetiza un doblaje de audio hablado usando el motor TTS del complemento.

## 8) Lector avanzado de documentos e imágenes

El **Lector de documentos** convierte tus documentos en texto legible y limpio. Maneja PDFs de varias páginas, imágenes complejas, formatos HEIC de iPhone y archivos de texto sin formato (`.txt`) y HTML (`.html`, `.htm`), que se abren instantáneamente sin OCR ni IA. Selecciona varios archivos a la vez y se fusionan en un único documento continuo. Hay tres motores OCR disponibles — **Chrome (Rápido)**, **IA (Avanzado)** y **Ninguno (Extraer capa de texto)** para PDFs con capacidad de búsqueda — seleccionables en Configuración → Lector de documentos.

### Cómo funciona

1. Presiona **NVDA + Shift + V**, luego **D** para abrir el Lector de documentos — o resalta primero un archivo en el Explorador de archivos y presiona **D** / **F** para omitir el diálogo de archivo.
2. Elige uno o más PDFs o imágenes. El complemento los escanea y anuncia el número total de páginas.
3. En el diálogo **Opciones**, elige el rango de páginas. También puedes marcar **Traducir salida** y elegir el idioma de destino, activar **Describir imágenes en línea durante el OCR**, o activar **Comprimir páginas PDF antes de procesar** para reducir y recomprimir las páginas escaneadas de gran tamaño antes de cargarlas.
4. La extracción de texto comienza en segundo plano por lotes. Puedes cerrar la ventana en cualquier momento y continuar después.
5. Una vez que las páginas estén listas, léelas en el visor: muévete entre páginas, salta a cualquier página, hazle preguntas a la IA, guarda el texto o genera una narración de audio.

### 7.1 Procesamiento por lotes y reanudación

No necesitas leer un documento enorme de una sola vez. Elige un rango de páginas (por ejemplo, `1-20`) y la IA extrae todas las páginas en segundo plano. Si NVDA se bloquea o interrumpes el escaneo, el complemento recuerda tu progreso y ofrece **Reanudar** exactamente donde lo dejaste. Los documentos completados también se guardan en caché, por lo que volver a abrirlos carga el texto instantáneamente sin volver a ejecutar el OCR.

### 7.2 Acción inteligente sobre archivos

No siempre necesitas abrir primero el documento. En el Explorador de archivos de Windows, resalta un PDF, imagen o archivo de texto/HTML y presiona **D** (Lector de documentos) o **F** (Acción inteligente de archivo) dentro de la Capa de comandos. El complemento omite instantáneamente el diálogo de archivo y comienza a procesar el archivo resaltado. Seleccionar varios archivos a la vez los procesa juntos como un único documento.

### 7.3 Controles y atajos del visor de documentos

Cuando la ventana del Lector de documentos está abierta, puedes usar lo siguiente:

#### Atajos de teclado

- **Ctrl + AvPág / Ctrl + RePág:** Ir a la página siguiente / anterior.
- **Flecha Abajo / Arriba:** Al llegar al final de una página, presiona **Abajo** para saltar a la siguiente; presiona **Arriba** al principio de una página para volver a la anterior.
- **Alt + A:** Abrir un diálogo de chat para hacer preguntas sobre el documento.
- **Alt + R:** Forzar un **Nuevo escaneo con IA** usando tu proveedor activo.
- **Alt + G:** Generar y guardar un archivo de audio de alta calidad (WAV/MP3). _Oculto si el proveedor no admite TTS._
- **Alt + S / Ctrl + S:** Guardar el texto extraído como archivo TXT o HTML.

#### Botones y controles

- **Ir a:** Elige cualquier página desde el selector de páginas.
- **Ver formateado:** Ver el documento completo combinado como texto formateado.
- **Reintentar páginas fallidas:** Reintenta solo los lotes que fallaron por un error temporal del servidor. Este botón aparece automáticamente cuando es necesario.
- **Voz TTS / Motor TTS:** Elige la voz y, en Gemini, selecciona entre **TTS estándar** y **Gemini en vivo** (streaming).
- **Anterior / Siguiente:** Muévete entre páginas.

### 7.4 Documentos recientes (D)

Presionar **D** en la Capa de comandos lista primero tus documentos leídos recientemente. Elige uno para continuar desde la página donde lo dejaste, o presiona **Abrir archivo...** (`Ctrl + O`) para explorar un archivo como siempre.

## 9. Etiquetado semántico con IA y explorador de interfaz

¿Atascado en una aplicación con "botones sin etiquetar" por todas partes? El motor de Etiquetado semántico con IA resuelve esto de forma permanente.

### 8.1 Etiquetado permanente de objetos (L)

Enfoca tu lector de pantalla en un gráfico o botón sin etiquetar y presiona **L** en la Capa de comandos. La IA observará el botón visualmente, determinará su función y aplicará una etiqueta permanente.
_A diferencia de las herramientas de etiquetado de lectores de pantalla más antiguas, este complemento usa un sistema híbrido avanzado de "firma de objeto" (AutomationId/ControlID). ¡Tus etiquetas personalizadas sobrevivirán al redimensionamiento de ventanas, el cambio de monitor y las actualizaciones de la aplicación!_

### 8.2 Escaneo completo de la aplicación (Shift + L)

Presiona **Shift + L** para escanear toda la ventana activa de una vez. La IA encontrará todos los elementos sin etiquetar y los nombrará inteligentemente. Luego puedes administrar, renombrar o eliminar en lote estas etiquetas desde el Administrador de etiquetas incorporado.

### 8.3 Explorador de interfaz (E)

¿Necesitas interactuar con un elemento sin navegar hasta él manualmente? Presiona **E** para activar el Explorador de interfaz. La IA escaneará la pantalla y generará una lista accesible de cada elemento en el que se puede hacer clic (ignorando el ruido del sistema como las barras de tareas). Elige un elemento de la lista y el complemento hará clic en él instantáneamente.

## 10. Asistente de voz en directo

El Asistente en vivo convierte a Vision Assistant Pro en un copiloto interactivo en tiempo real.
_(Nota: Esta función es exclusiva de Google Gemini y los proveedores personalizados compatibles con Gemini)._

- **Activación:** Presiona **Control + L** en la Capa de comandos.
- **Interacción en tiempo real:** Habla naturalmente a través de tu micrófono. La IA escuchará tu voz y mirará simultáneamente tu pantalla activa. Puedes hacer preguntas como "¿Qué estoy viendo?" o "Léeme el tercer párrafo".
- **Pulsar para hablar:** Activa **Pulsar para hablar** en la pestaña de configuración del Asistente en vivo (o actívalo dentro de la ventana del Asistente en vivo), luego mantén la tecla asignada para hablar y suéltala al terminar. Mantiene el micrófono silenciado hasta que presionas la tecla.
- **Entrada por webcam:** Marca **Usar &webcam** en la ventana del Asistente en vivo para enviar la imagen de tu cámara a la IA en lugar de tu pantalla — pregunta sobre objetos físicos, documentos impresos o tu entorno. Si ffmpeg aún no está instalado, marcar la casilla lo descarga una vez con tu permiso; la opción se desactiva cuando no se detecta ninguna cámara o cuando la configuración de privacidad de Windows bloquea el acceso a la cámara.
- **Personalización:** Dentro del diálogo, puedes cambiar el estilo de voz de la IA y ajustar su "Profundidad de razonamiento".

## 11. Observador ambiental (asistente en segundo plano)

El Observador ambiental convierte a Vision Assistant Pro en tus ojos en segundo plano, sin ninguna conversación: sigue escuchando y observando mientras trabajas, informa de lo que cambia, y permanece en silencio cuando no pasa nada.
_(Nota: Esta función es exclusiva de Google Gemini y los proveedores personalizados compatibles con Gemini)._

- **Activación:** Presiona **Shift+O** en la Capa de comandos para abrir el diálogo del Observador ambiental; vuelve a presionarlo para detener el observador.
- **Modos:** **Solo traducción de audio** traduce lo que escucha, **Solo observador de pantalla** informa de los cambios en la pantalla, y **Solo observador de webcam** abre la ventana del Asistente en vivo con tu cámara y Pulsar para hablar, para que puedas hacer preguntas sobre lo que ve la cámara.
- **Fuente de audio:** En el modo de audio, elige si traducir tu **Micrófono** o el **Audio del sistema (bucle de retorno)**. La pequeña biblioteca de bucle de retorno se descarga una vez en el primer uso, con tu permiso.
- **Contexto:** Para los modos de pantalla y webcam, elige una opción opcional **Sobre lo que estoy haciendo** (por ejemplo viendo una película, siguiendo una reunión o llamada, leyendo una etiqueta, o revisando tu aspecto) para enfocar los informes; también puedes escribir tu propio contexto.
- **Informes:** El complemento compara cada nuevo fotograma con el anterior y solo lo envía a la IA cuando la imagen realmente cambió, de modo que una pantalla estática nunca te cuesta solicitudes. La IA entonces informa solo de lo nuevo y nunca se repite.
- **Mensaje de bienvenida:** Excepto en el modo de traducción, el observador te saluda brevemente al iniciar, para que sepas que está escuchando.
- **Configuración:** En **Configuración > Asistente en vivo**, define el **Modo del observador**, el **Intervalo de fotogramas** (de 1 a 10 segundos) y el **Estilo de informe** (breve o detallado). La instrucción del observador y cada texto de contexto se pueden editar en el Administrador de indicaciones (sección **Ambiental**).

## 12. Indicaciones personalizadas y variables

Puedes administrar las indicaciones en **Configuración > Indicaciones > Administrar indicaciones...**.

- **Filtro:** La pestaña **Indicaciones predeterminadas** tiene una lista de **Filtro** encima de la lista de indicaciones que muestra **Todo** o solo una sección a la vez (por ejemplo **Ambiental**), para que las listas largas sigan siendo fáciles de recorrer.

### Atajos para indicaciones personalizadas

Asigna a cualquier indicación personalizada su propia tecla de atajo directamente en el Administrador de indicaciones, y ejecútala al instante con tu selección o contexto actual:

- **Tecla simple** (por ejemplo, `1`, `p` o `F3`): Funciona dentro de la Capa de comandos, y también globalmente como `NVDA + Shift + tecla`.
- **Combinación de teclas** (por ejemplo, `Control + Shift + 1`, `Alt + P` o `Insert + 1`): Funciona globalmente por sí sola.

### Comportamiento de retroalimentación por indicación

Cada indicación personalizada puede definir individualmente su comportamiento de entrega de resultados:

- **Configuración global:** Sigue la configuración general de salida de Conexión (Salida directa o Ventana de chat).
- **Copiar al portapapeles:** Copia la respuesta de la IA directamente al portapapeles sin abrir una ventana.
- **Salida directa (mensaje de NVDA):** Dice/braillea la respuesta de la IA directamente mediante la voz de NVDA.
- **Copiar al portapapeles y salida directa:** Copia la respuesta al portapapeles y la dice directamente.
- **Ventana de chat:** Siempre abre el resultado en una ventana de conversación interactiva.

### Variables compatibles

- `[selection]`: Texto seleccionado actualmente.
- `[text]`: Contenido de texto completo del campo de edición actualmente enfocado (ignora automáticamente los cuadros de contraseña protegidos).
- `[currentURL]`: URL de la página web o documento desde navegadores compatibles (Chrome, Edge, Firefox).
- `[clipboard]`: Contenido del portapapeles.
- `[clipboard_image]`: Imagen actualmente en el portapapeles.
- `[screen_obj]`: Captura de pantalla del objeto del navegador.
- `[screen_fg_obj]`: Captura de pantalla de la ventana activa en primer plano.
- `[screen_full]`: Captura de pantalla completa.
- `[file_ocr]`: Seleccionar imagen/PDF para extracción de texto.
- `[file_read]`: Seleccionar documento para leer (TXT, Código, PDF).
- `[file_audio]`: Seleccionar archivo de audio para análisis (MP3, WAV, OGG).
- `[ambient_screen]`: Inicia una sesión continua en segundo plano del Observador de pantalla.
- `[ambient_webcam]`: Inicia una sesión continua en segundo plano del Observador de webcam (usa la configuración de Pulsar para hablar).
- `[ambient_audio]`: Inicia una sesión de traducción en vivo del Observador de audio.
- `[loopback]`: Usa la reproducción de audio del sistema como fuente de sonido (para `[ambient_audio]`).
- `[mic]`: Usa el micrófono como fuente de sonido (para `[ambient_audio]` y `[ambient_webcam]`).
- `[brief]`: Establece el estilo de informe del observador en breve (una sola oración).
- `[detailed]`: Establece el estilo de informe del observador en detallado (2-3 oraciones).
- `[lang:code]`: Especifica el código de idioma de destino para la traducción de audio (por ejemplo, `[lang:fa]`, `[lang:en]`).
- `{target_lang}`: Idioma de destino actual.
- `{source_lang}`: Idioma de origen actual.
- `{response_lang}`: Idioma actual de respuesta de la IA.
- `{swap_target}`: Idioma alternativo para traducción con intercambio inteligente.
- `{swap_instruction}`: Bloque de instrucción de traducción con intercambio inteligente.

_Nota sobre las indicaciones ambientales:_ Las indicaciones que contienen variables ambientales funcionan como un interruptor — presionar el atajo mientras está activa detiene la sesión de inmediato. Las combinaciones incompatibles (como combinar variables de captura estática como `[screen_full]` con los modos del observador ambiental, combinar varios modos ambientales, o añadir instrucciones de indicación a `[ambient_audio]`) se validan estrictamente y se impiden al guardar.

## 13. Casos de uso en el mundo real (¿Qué función debería usar?)

Vision Assistant Pro está repleto de herramientas avanzadas. Aquí tienes algunos escenarios comunes para ayudarte a elegir la adecuada:

- **Quieres entender el diseño completo de una ventana complicada o inaccesible.**
  _Presiona **O** (Visión de pantalla completa)._ La IA analizará toda la pantalla y describirá exactamente dónde están ubicados los elementos, textos y botones.

- **Encontraste una imagen en una página web o un gráfico sin etiquetar en un documento.**
  _Mueve tu objeto del navegador al gráfico y presiona **V** (Visión de objeto)._ La IA describirá específicamente qué contiene esa imagen.

- **Quieres ver una película o un videoclip con audiodescripción.**
  _Presiona **Shift + V** en tu vídeo, elige **"Generar audiodescripción (archivo SRT)"**. Cuando termine, haz clic en **"Generar narración sincronizada (MP3)"** y selecciona **"AD extendida"**._ El complemento creará una pista de audio que pausa inteligentemente el diálogo de la película para describir las escenas visuales.

- **Encontraste una aplicación llena de "botones sin etiqueta".**
  _Presiona **L** para etiquetar permanentemente el botón específico. O presiona **Shift + L** para escanear toda la ventana. Si solo quieres hacer clic en algo rápidamente, presiona **E** (Explorador de interfaz)._

- **Soporte de CAPTCHA visual**: Se añadió soporte robusto para la resolución de CAPTCHA visual. Intenta resolver automáticamente desafíos de imagen complejos como hCaptcha y reCAPTCHA.

- **Quieres leer un documento PDF largo de 50 páginas.**
  _Presiona **D** (Lector de documentos), configura el proveedor como Google Gemini e introduce el rango de páginas `1-50`._ El complemento extraerá el texto con precisión en segundo plano.

- **Estás viendo un tutorial de vídeo silencioso o una animación en tu pantalla.**
  _Presiona **Control + V** para comenzar a grabar la pantalla. Deja que el tutorial se reproduzca, luego presiona **Control + V** de nuevo._ La IA explicará exactamente lo que se demostró.

- **Encuentras un error inesperado, fallo de conexión a la API o quieres diagnosticar problemas con servidores locales personalizados.**
  _Ve a **Configuración > Avanzado**, marca **"Habilitar archivo de registro dedicado"** y configura el **Nivel de registro** en **"Depuración"**. Realiza la acción de nuevo, luego haz clic en **"Abrir archivo de registro"** para inspeccionar los detalles técnicos o adjunta `vision_assistant.log` a un ticket de soporte._

***

**Nota:** Se requiere una conexión a Internet activa para todas las funciones de IA. Los documentos de varias páginas se procesan automáticamente.

## 14. Soporte y comunidad

Mantente al día con las últimas noticias, funciones y lanzamientos:

- **Canal de Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **GitHub Issues:** Para informes de errores y solicitudes de funciones.

### Informar errores y registros

Al abrir un issue en GitHub o pedir soporte, incluye detalles sobre tu proveedor de IA activo, modelo y versión de NVDA. Si experimentas problemas de conexión o fallos inesperados, habilita el archivo de registro dedicado en **Configuración > Avanzado**, reproduce el problema y adjunta tu archivo `vision_assistant.log`.

## 15. Colaboradores del proyecto

Un agradecimiento de corazón a los miembros de nuestra comunidad que apoyan el desarrollo continuo y el mantenimiento de este proyecto con sus generosas contribuciones económicas:

- **@Alyabani94**
- **Ali Alamri**
- **Ilya**
- **leonardo0216**
- **Sergei Fleytin**
- **Arne Siebert**
- **Schalkefan**
- **Rainer Brell**
- **[avalai.org](https://avalai.org)**

_Si deseas apoyar el proyecto económicamente y ver tu nombre aquí, puedes encontrar la opción **Donar** en el menú Herramientas de NVDA (submenú Vision Assistant) o durante el proceso de configuración después de la instalación._

---

## Cambios para 2026.10.15

- **La corrección más solicitada — Crear una clave API de Gemini por fin es fácil**: Obtener una clave API en **aistudio.google.com** solía ser el paso más difícil de todos. Con un lector de pantalla las páginas eran confusas, y algunas personas simplemente no podían crear una clave. Ese problema ahora se resuelve directamente dentro del complemento. Presiona **G** en la Capa de comandos (o usa **Obtener una clave API de Gemini...** en Configuración), inicia sesión a través de tu navegador predeterminado sin ninguna configuración externa, y tu clave se crea y configura con una sola confirmación — incluso si nunca tuviste un proyecto antes.
- **Observador ambiental**: El asistente en segundo plano ya está aquí. Presiona **Shift+O** en la Capa de comandos para iniciarlo, y vuelve a presionarlo para detenerlo. Puede traducir lo que escucha (tu micrófono o el sonido del sistema), observar la pantalla y contarte qué cambió, o abrir el Asistente en vivo con tu webcam y Pulsar para hablar para que puedas preguntar sobre lo que ve la cámara. Solo envía una imagen cuando algo cambió de verdad, así que una pantalla quieta no te cuesta nada, y permanece en silencio cuando no pasa nada. También puedes iniciar y alternar el observador directamente mediante Indicaciones personalizadas y teclas de atajo dedicadas usando `[ambient_screen]`, `[ambient_webcam]` o `[ambient_audio]` junto con modificadores (`[loopback]`, `[mic]`, `[brief]`, `[detailed]`, `[lang:code]`), con validación automática contra combinaciones de variables conflictivas.
- **Operador en vivo**: El Asistente en vivo ahora puede llevar a cabo lo que le pidas en tu equipo mientras hablas con él. Presiona **Control+A** en la Capa de comandos para iniciar una sesión de operador en vivo, y simplemente pide en lenguaje natural. Funciona con solicitudes de varios pasos, dice cada paso con la propia voz del Asistente en vivo, se encarga de las combinaciones de teclas que necesita, y decide por sí mismo cuándo terminó la tarea. **Salida directa en vivo (sin ventana)** también está en la configuración rápida.
- **Diccionario de personajes y gestión de series**: El diálogo de Análisis de vídeo ahora incluye un potente sistema de **Diccionario de personajes**. Añade, edita, importa o administra nombres de personajes, descripciones físicas y roles por serie — la IA vincula automáticamente los personajes detectados con tu diccionario y fusiona los nuevos a medida que analizas más episodios. Tus notas manuales siempre se conservan con prioridad sobre las actualizaciones de la IA, mientras que las descripciones físicas se mantienen al día en todos los episodios. El diccionario se guarda por serie y se reutiliza en cada vídeo de esa serie. En la lista de personajes, presiona **F2** para editar el personaje seleccionado y **Eliminar** para quitarlo.
- **Soporte de proxy SOCKS5, HTTP y proxy inverso con prueba de latencia**: Evita sin problemas las restricciones de red con soporte de proxy completo en todo el complemento — incluyendo el Asistente en vivo, el Observador ambiental y la generación de TTS. Elige entre 4 modos de funcionamiento en la configuración general: **Detección automática**, **Proxy SOCKS5**, **Proxy HTTP** o **Proxy inverso**. SOCKS5 admite autenticación de usuario y contraseña según RFC 1929 y tunelización de dominios; el proxy HTTP admite autenticación básica. Un nuevo botón **Probar conexión del proxy** se ejecuta en segundo plano y anuncia la latencia de tu conexión en milisegundos.
- **Caché de archivos de vídeo por 48 horas**: Los vídeos cargados a Gemini ahora se almacenan en caché durante 48 horas. Puedes regenerar salidas SRT o MP3 para el mismo vídeo sin volver a cargarlo — incluso después de reiniciar NVDA. La caché reconoce la clave API y se invalida automáticamente cuando esta cambia.
- **Detección de silencios con IA (Silero VAD)**: La audiodescripción extendida ahora usa el modelo neuronal Silero VAD para una detección precisa de silencios — distinguiendo las pausas naturales del diálogo de la música y el ruido de fondo. El modelo se descarga automáticamente en el primer uso (con tu permiso), igual que ffmpeg y eSpeak.
- **Vídeo por webcam para el Asistente en vivo**: La ventana del Asistente en vivo ahora tiene una casilla **Usar &webcam** para enviar la imagen de tu cámara web a la IA en lugar de tu pantalla — perfecta para hacer preguntas sobre objetos físicos, documentos o tu entorno. Si ffmpeg aún no está instalado, marcar la casilla lo descarga (una sola vez, con tu permiso). La opción se desactiva cuando no se detecta ninguna cámara o cuando la configuración de privacidad de Windows bloquea el acceso a la cámara, con un botón para abrir esa configuración de privacidad. Si la cámara está habilitada pero no produce fotogramas, el problema se registra en el log de NVDA para diagnóstico en lugar de volver silenciosamente a la pantalla.
- **Selección de dispositivo de salida de audio**: Ahora puedes seleccionar un dispositivo de salida de audio dedicado para el Asistente en vivo y el Observador ambiental. Elige entre la salida predeterminada de NVDA, el Asignador de sonido de Windows, o cualquier tarjeta de sonido física conectada (como auriculares USB o altavoces externos) en la pestaña de configuración en vivo, directamente dentro del diálogo del Asistente en vivo, o al vuelo mediante la configuración rápida (NVDA+Shift+V y luego Arriba/Abajo/Izquierda/Derecha).
- **Administrador de indicaciones**: La pestaña de indicaciones predeterminadas ahora tiene una lista de **Filtro**, para que puedas mostrar todas las indicaciones o solo una sección (por ejemplo **Ambiental**). También puedes editar ahí los textos de contexto del observador y la nueva **Instrucción del Operador en vivo**.
- **Filtrado inteligente de modelos en el enrutamiento avanzado**: Los desplegables de Enrutamiento avanzado de modelos ahora clasifican dinámicamente los modelos de Gemini por capacidad sin saturar la lista. El Asistente en vivo solo muestra modelos genuinos bidireccionales en vivo y de audio nativo, TTS solo muestra modelos dedicados de síntesis de voz, STT prioriza los modelos de transcripción y multimodales, y Análisis de vídeo, OCR y Operador de IA filtran de forma limpia los modelos de utilidad de un solo propósito (como generación de imágenes, generación de vídeo y modelos de incrustación). Los modelos futuros se detectan automáticamente según su capacidad, sin necesitar actualizaciones de versión.
- **Seguimiento de la primera aparición de personajes**: La IA ahora describe el aspecto físico de cada personaje solo una vez — en su primera aparición en el vídeo. Las apariciones posteriores usan solo el nombre, eliminando descripciones repetitivas entre segmentos y manteniendo la narrativa fresca y natural.
- **Directorio de datos unificado**: Todos los archivos de datos del complemento (historial, series, etiquetas, progreso de OCR, cachés y registros) se han migrado a una única carpeta `VisionAssistant` dentro de tu directorio de configuración de NVDA — manteniendo todo organizado y facilitando las copias de seguridad manuales.
- **Experiencia mejorada al guardar vídeos**: Al guardar archivos SRT o MP3, el cuadro de diálogo de archivo ahora se abre de forma predeterminada en la carpeta del vídeo de origen, ya sea que abras el vídeo desde el cuadro de diálogo de archivo o con Shift+V desde el Explorador.
- **Eliminar documentos con o sin su texto en caché**: El diálogo de Historial (`Control + H`) ahora ofrece dos formas de eliminar un documento — presiona Eliminar y elige **Eliminar solo del historial** o **Eliminar del historial y el texto en caché**. La segunda opción borra el texto OCR en caché de ese documento, por lo que la próxima apertura lo vuelve a escanear desde cero — ideal tras un escaneo deficiente. Una casilla **No preguntar de nuevo** recuerda tu elección para futuras eliminaciones. Los datos de reanudación de operaciones interrumpidas nunca se ven afectados.
- **Caché de OCR por motor y con fusión en el Lector de documentos**: El texto OCR en caché ahora se almacena por motor de OCR, de modo que cambiar de motor siempre vuelve a escanear con el nuevo motor en lugar de repetir el resultado anterior. Al reabrir un documento se muestra de nuevo el diálogo de rango de páginas (ya rellenado con tu última elección), reutilizando al instante las páginas ya escaneadas y escaneando solo las que faltan — la caché se fusiona página por página en lugar de reemplazarse, de modo que cada rango que lees se conserva para después.
- **Compresión de PDF en el Lector de documentos**: Se añadió una opción **Comprimir páginas PDF antes de procesar** en el diálogo de rango de páginas del Lector de documentos. Al cargar documentos PDF escaneados grandes o de alta resolución a Gemini o Mistral, las páginas se reducen y recomprimen automáticamente para disminuir drásticamente el tamaño de la carga, acelerar el procesamiento y evitar tiempos de espera agotados en la red. La opción está desactivada de forma predeterminada y se oculta automáticamente al usar el motor Chrome o proveedores de imágenes basados en base64.
- **Personalización del comportamiento de retroalimentación por indicación**: ¡Personaliza cómo entrega su resultado cada indicación personalizada individualmente! En el editor de indicaciones personalizadas, elige entre **Configuración global**, **Copiar al portapapeles**, **Salida directa (mensaje de NVDA)**, **Copiar al portapapeles y salida directa**, o **Ventana de chat**. Esto permite que indicaciones específicas hablen directamente sin abrir una ventana mientras otras abren un chat completo.
- **Nuevas variables dinámicas de indicación (`[currentURL]` y `[text]`)**: Las Indicaciones personalizadas ahora admiten `[currentURL]` para capturar la URL del documento activo en Google Chrome, Mozilla Firefox y Microsoft Edge, y `[text]` para insertar dinámicamente el contenido de texto completo del campo de edición actualmente enfocado (ignorando los cuadros de contraseña protegidos).
- **Renovación del descargador de vídeos de Twitter/X**: Se restauró la descarga y el análisis de vídeos de Twitter/X tras fallos del scraper original. La extracción de vídeo ahora utiliza la robusta API de FixTweet para obtener directamente transmisiones MP4 de la más alta calidad desde la CDN de Twitter, con alternativa automática a TwitSave y soporte de proxy.
- **Corrección del descargador de vídeos de Instagram**: Se restauró la descarga y el análisis de Reels y URLs de vídeo de Instagram tras cambios en el formulario del servicio de descarga original.
- **Correcciones y rendimiento**: Pulsar para hablar responde en el momento en que presionas la tecla, el Asistente en vivo ya no empieza una respuesta a mitad de una oración, el observador ya no informa de la imagen anterior, y la lista de Profundidad de razonamiento solo ofrece lo que tu modelo realmente admite. El Operador de IA también puede desplazarse a la izquierda y a la derecha. Se corrigió un `AttributeError` al analizar vídeos en línea, y se evitó que las indicaciones personalizadas sin selección de texto inyectaran accidentalmente títulos de ventanas en segundo plano en las solicitudes a la IA.

## Cambios para 2026.09.01

- **Historial (Control + H)**: La Capa de comandos ahora incluye un diálogo de **Historial** (`Control + H`) que lista tus chats y documentos anteriores con filtros para Todo, Chats y Documentos. Reabre cualquier chat con toda la conversación — los archivos adjuntos se vuelven a adjuntar automáticamente — o reabre un documento y sigue leyendo. Presiona **Eliminar** en cualquier elemento para quitarlo, o borra todo de una vez.
- **Documentos recientes en el Lector**: Presionar **D** en la Capa de comandos ahora muestra primero tus documentos leídos recientemente. Elige uno para continuar desde la página donde lo dejaste, o presiona **Abrir archivo...** (`Ctrl + O`) para explorar como siempre.
- **Pulsar para hablar en el Asistente en vivo**: ¡Toma el control total de tus conversaciones en vivo! **Pulsar para hablar en el Asistente en vivo**: Activa **Pulsar para hablar** en la nueva pestaña de configuración del Asistente en vivo y asigna cualquier tecla — incluso un modificador solo como `Ctrl izquierdo` — para hablar. Mantén la tecla para hablar y suéltala al terminar, con un pitido corto en cada pulsación y suelta. Un interruptor equivalente también aparece directamente en la ventana del Asistente en vivo, para que puedas cambiar entre el modo pulsar para hablar y el micrófono abierto sin salir de la conversación.
- **Audio nativo de Gemini 2.5 Flash**: El Asistente en vivo ahora admite el modelo de audio nativo de Gemini 2.5 Flash (`gemini-2.5-flash-native-audio-preview-12-2025`) para conversaciones de voz naturales y con baja latencia. Puedes cambiar a él desde **Configuración → Enrutamiento avanzado de modelos → Modelo del Asistente en vivo (solo Gemini)**, o mantener "Automático" para usar el modelo recomendado.
- **Copia de seguridad y restauración de configuración**: Se añadió un potente sistema de copia de seguridad y restauración en la pestaña **Avanzado**. Guarda toda la configuración del complemento — incluidas claves API, modelos, indicaciones personalizadas y preferencias — en un único archivo JSON y restáurala en cualquier momento, en cualquier equipo o después de reinstalar NVDA. Al hacer la copia de seguridad, eliges qué incluir: **Todo** (configuración, etiquetas personalizadas, progreso de OCR e historial) o **Solo configuración**.
- **Lectura directa de texto y HTML**: El Lector de documentos ahora puede abrir archivos de texto sin formato (`.txt`) y HTML (`.html`, `.htm`) directamente, sin OCR ni IA. Detecta automáticamente la codificación del archivo, elimina scripts y elementos de formato innecesarios, y divide inteligentemente el contenido en páginas legibles — incluso reimportando sus propios archivos exportados conservando la estructura de páginas — para que puedas leerlos al instante sin OCR ni procesamiento de IA.
- **TTS de Gemini en vivo para el Lector de documentos**: El botón "Generar audio" ahora admite Gemini en vivo — un motor TTS de streaming de alta calidad y ritmo natural. Cuando Gemini es tu proveedor activo, puedes elegir entre TTS estándar y Gemini en vivo directamente en el lector.
- **Atajos para indicaciones personalizadas**: Ahora puedes asignar una tecla de atajo a cualquiera de tus indicaciones personalizadas desde el Administrador de indicaciones. Dale a cada indicación su propia tecla o combinación de teclas para ejecutarla al instante, capturando automáticamente tu selección o contexto actual sin pasos adicionales.
- **Navegación por mensajes del chat**: ¡Revisa cualquier conversación sin usar las manos! **Navegación por mensajes del chat**: Dentro de cualquier ventana de chat, presiona `Alt + Abajo` para escuchar el siguiente mensaje y `Alt + Arriba` para el anterior — con prefijos claros "Tú" / "IA" y límites "Primer mensaje" / "Último mensaje" anunciados.
- **Copiar mensaje del chat (Alt + C)**: Mientras revisas una conversación, presiona `Alt + C` para copiar el mensaje actual al portapapeles.
- **Indicación del sistema del Chat directo**: El Chat directo (`Shift+C`) ahora tiene su propia indicación del sistema editable — "Instrucción de chat directo" — que establece la personalidad del asistente y el idioma de respuesta para cada conversación. Puedes personalizarla desde la pestaña de indicaciones predeterminadas del Administrador de indicaciones.
- **Navegación por cursor entre páginas en el Lector de documentos**: ¡Leer documentos de varias páginas ahora es más fluido! **Navegación por cursor en el Lector de documentos**: Al llegar al final de una página y presionar `Abajo`, el lector salta automáticamente a la siguiente página. Presionar `Arriba` al principio de una página te lleva de vuelta sin problemas a la anterior — ¡se acabó el cambio manual de página mientras lees!
- **Nuevos activadores de configuración rápida**: Copiar respuestas de IA al portapapeles, salida directa (sin ventana de chat), limpiar Markdown en el chat e intercambio inteligente ya se pueden activar y desactivar al instante desde la configuración rápida de la capa de comandos.
- **Pestaña de configuración del Asistente en vivo**: El Asistente en vivo ahora tiene su propia pestaña de configuración dedicada. La opción "Asistente en vivo: Salida directa (sin ventana)" se movió aquí desde la pestaña Conexión, y la pestaña aparece solo cuando Google Gemini (o un proveedor personalizado compatible con Gemini) es tu proveedor activo.

## Cambios para 2026.08.06

- **Etiquetado en el Explorador de interfaz**: Ahora puedes añadir etiquetas directamente a los elementos encontrados dentro del Explorador de interfaz. Se ha añadido un nuevo botón "Añadir etiqueta", y la interfaz permanece abierta y conserva el foco para que puedas etiquetar rápidamente varios objetos sin interrupciones.
- **Mejora de la capa de configuración rápida**: La capa de Vision Assistant (`Insert+Shift+V`) es ahora persistente y muy interactiva. Puedes usar las flechas `Arriba/Abajo` para navegar entre configuraciones rápidas (Proveedor, Modelo, Idioma de respuesta de la IA, Modelo TTS) y las flechas `Izquierda/Derecha` para cambiar sus valores al instante con retroalimentación de voz concisa. Tus selecciones tienen efecto inmediato y la capa permanece activa mientras configuras.
- **Chat directo (`Shift+C`)**: Se añadió un nuevo comando a la capa. Presiona `Shift+C` para abrir instantáneamente una ventana de "Chat directo". Proporciona una interfaz conversacional limpia y basada en texto con la IA de inmediato, sin necesitar una imagen o documento como punto de partida.
- **Recuperación de historial de chat sin fallos**: Se corrigió un error importante donde presionar `Espacio` para recuperar el último resultado perdía el historial de chat subsiguiente. Ahora, el complemento realiza un seguimiento global de tu conversación. Si chateas, cierras el diálogo y presionas `Espacio` para recuperarlo, todo tu historial de ida y vuelta se restaura perfectamente. Funciona para Chat directo, Análisis de visión, Chat de documento y Traducción.
- **Descripciones de imágenes en línea en el OCR**: Se añadió una función opcional para describir imágenes en línea durante el OCR de documentos. Puedes activar esta configuración en las opciones del complemento, dentro de las opciones del Lector de documentos antes de la extracción, y rápidamente sobre la marcha mediante la capa de configuración rápida.
- **Traducción de voz (`Control+T`)**: Se añadió una nueva y poderosa función. Dicta habla e instantáneamente tradúcela y escríbela usando IA según los idiomas de origen y destino configurados.
- **Mejoras en el descargador de actualizaciones**: El diálogo de descarga de actualizaciones ahora muestra correctamente el progreso de descarga en porcentajes, y se corrigió un error donde aparecía un mensaje fantasma "Descargando actualización" al cancelar la instalación.
- **Mejoras en el descargador de eSpeak-NG**: Se añadió seguimiento de progreso en porcentaje para las descargas de eSpeak-NG.
- **Resistencia del OCR en lotes**: Se corrigió un problema en el OCR de PDF en lotes donde el proceso se detenía si la clave API activa alcanzaba su cuota a mitad del proceso; ahora cambia automáticamente a la siguiente clave disponible y reanuda el proceso.
- **Soporte de CAPTCHA visual**: Se añadió soporte robusto para la resolución de CAPTCHA visual. Intenta resolver automáticamente desafíos de imagen complejos como hCaptcha y reCAPTCHA.
- **Revisión completa del transcriptor de audio**: El módulo transcriptor de audio se ha reconstruido completamente y ahora admite archivos de audio y vídeo. Presenta 3 modos de operación distintos: "Transcribir (idioma original)", "Transcribir y traducir (idioma de destino)" y el nuevo y poderoso "Doblar y traducir (idioma de destino)" (exclusivo de Gemini).
- **Números de página opcionales en el Lector de documentos**: Se añadió una nueva configuración para activar o desactivar la inclusión de números de página y separadores en las salidas de documentos de varias páginas. Puedes gestionar fácilmente esta opción desde la configuración principal o activarla sobre la marcha mediante la capa de configuración rápida. Esta función se aplica tanto a las exportaciones de archivos de texto/HTML como a la ventana integrada "Ver formateado", permitiéndote leer documentos combinados sin problemas.
- **TTS de Gemini en vivo ilimitado para descripciones de vídeo**: Ahora puedes seleccionar "TTS de Gemini en vivo" como motor de voz al generar Narración de audio sincronizada (MP3) para vídeos. Esto utiliza la API de Gemini en vivo para sintetizar audiodescripciones de alta calidad sin límites de caracteres ni restricciones de longitud.
- **Modularización del código**: Se refactorizó la estructura del complemento de un único archivo a una arquitectura modular de múltiples archivos.
- **Rediseño de la interfaz de configuración**: Se rediseñó completamente el diálogo de configuración para usar una interfaz moderna basada en pestañas.
- **Registro global en archivo dedicado**: Se añadió un sistema opcional de registro global en archivo bajo la nueva pestaña "Avanzado". Captura automáticamente eventos operativos, tráfico de API y errores en todos los módulos del complemento en un archivo dedicado (`vision_assistant.log`). Compatible con niveles de verbosidad configurables (Depuración, Información, Advertencia, Error) y períodos de retención automatizados (1 hora a 90 días).
- **Seguimiento del progreso de carga en Gemini**: Se añadieron anuncios de progreso en porcentaje en tiempo real al cargar archivos grandes (vídeo, audio, documentos) a la API de Google Gemini.

## Cambios para 2026.07.15

- **Filtrado inteligente de modelos de API**: Revisión completa del sistema de filtrado de modelos. Se añadieron palabras clave de filtrado más potentes para mantener el desplegable principal limpio y preparado para el futuro, mientras que todos los modelos especializados siguen siendo accesibles en el Enrutamiento avanzado.
- **Búsqueda en enrutamiento avanzado**: Todos los desplegables de Enrutamiento avanzado de modelos (OCR, STT, TTS, Operador, Vídeo, En vivo) y el selector de variante de eSpeak son ahora completamente buscables. Puedes escribir rápidamente para filtrar y encontrar el modelo o variante que deseas.
- **Nuevos atajos de la Capa de comandos**:
  - **Análisis directo de archivos**: Procesamiento inmediato desde el Explorador de archivos sin diálogo.
  - **Gestión inteligente de cuotas de API**: Cuarentena por modelo para errores 429 de límite diario.
  - **Auditoría de enrutamiento (`Alt + M`)**: Audita y anuncia tu configuración actual de Enrutamiento avanzado, leyendo qué modelos están seleccionados activamente para tareas especializadas (omitiendo la configuración predeterminada).
- **Revisión completa del Analizador de vídeo**: ¡El Analizador de vídeo se ha transformado por completo! Anteriormente, solo ofrecía una descripción básica de los vídeos en línea. Ahora es una suite completa de procesamiento de vídeo diseñada para usuarios ciegos:
  - **Grabación de pantalla local (`Control+V`)**: Ahora puedes grabar vídeos silenciosos directamente desde tu pantalla. La IA analizará el segmento grabado y proporcionará una descripción muy detallada de la escena, el diseño y las acciones.
  - **Revisión completa del Analizador de vídeo**: Transformado en una suite completa de procesamiento de vídeo con grabación de pantalla local, generación de audiodescripción SRT, narración sincronizada MP3, seguimiento avanzado de personajes y enrutamiento de modelos de vídeo especializados.
  - **Narración de audio sincronizada (exportación a MP3)**: Más allá de los subtítulos basados en texto, el complemento puede sintetizar la audiodescripción en voz, mezclarla automáticamente con la pista de audio original del vídeo, aplicar atenuación de audio (bajar el volumen de fondo durante las descripciones) y exportar el resultado sincronizado final como un archivo MP3.
  - **Acción inteligente sobre archivos de vídeo**: Si enfocas un archivo de vídeo local y presionas el atajo de vídeo, el complemento lo detectará automáticamente y procesará el archivo directamente.
  - **Seguimiento avanzado de personajes**: La IA ahora realiza una pre-pasada de extracción de personajes. Construye un diccionario global de personajes y los rastrea con precisión segmento por segmento sin confundir identidades.
  - **Configuración del Análisis de vídeo**: Se añadieron nuevas opciones para controlar el tamaño de los fragmentos SRT, los subtítulos de personajes y los avisos.
  - **Enrutamiento de modelos ampliado**: Ahora puedes seleccionar explícitamente modelos de vídeo especializados (`gemini_video_model`, `custom_video_model`) en la configuración de Enrutamiento avanzado de modelos.
- **Gestión inteligente de cuotas de API**: Manejo mejorado de errores 429 (límite diario) rastreando las cuotas por modelo. Si una clave alcanza su límite diario en un modelo, se pone en cuarentena de forma inteligente solo para ese modelo específico, dejando la clave disponible para usarse con otros modelos.

## Cambios para 7.0.0

- **Reanudar escaneos sin terminar**: Se añadió una función de reanudación tanto para el Lector de documentos como para la Acción inteligente de archivo. Si un escaneo se interrumpe, ahora puedes continuar desde donde se detuvo en lugar de empezar desde cero.
- **Nueva variable `[screen_fg_obj]`**: Captura solo la ventana activa en primer plano.
- **Reintentos inteligentes y rotación de claves**: El complemento ahora reintenta silenciosamente hasta 5 veces con la misma clave al encontrar sobrecargas temporales del servidor (como "alta demanda" o respuestas mal formadas). Si los reintentos fallan, cambia automáticamente a la siguiente clave API de tu lista.
- **Detección de cortina de pantalla**: Evita capturas cuando la Cortina de pantalla está activa. Te advertirá y detendrá la acción, evitando que envíes imágenes negras y desperdicies tokens de API.
- **Ajustes del Lector de documentos**: Pre-selección de idioma de destino y manejo de hilos mejorado. También se mejoró el manejo de hilos para asegurar que las tareas en segundo plano se detengan correctamente al cerrar el lector.
- **Integración OCR nativa de Mistral**: Procesamiento en lotes usando el punto de acceso `/v1/ocr`. Los documentos de varias páginas se fusionan, cargan y procesan automáticamente en lotes usando el punto de acceso especializado `/v1/ocr` de Mistral, mientras que las imágenes de una sola página se procesan directamente sin conversiones de PDF innecesarias [1].
- **Controladores de URL personalizados dinámicos**: Borrado instantáneo de caché de modelos al cambiar URL. Esto garantiza compatibilidad total con puntos de acceso personalizados (como Cloudflare AI Gateway) que no admiten el punto de acceso estándar de listado `/v1/models`.
- **Motor de entrada del Operador de IA renovado**: Se reescribió por completo el sistema subyacente de simulación de mouse y teclado del Operador de IA. Se reemplazó la antigua API `mouse_event` por la moderna API `SendInput` de Windows, logrando una compatibilidad significativamente mayor con aplicaciones modernas, ventanas protegidas por UAC y pantallas de alta densidad (DPI).
- **Arrastrar y soltar corregido**: Operaciones de arrastrar y soltar completamente estables. El nuevo motor usa curvas naturales de "suavizado", posicionamiento preciso del cursor, temporización optimizada y una técnica inteligente de "empuje" para asegurar que Windows y las aplicaciones reconozcan y ejecuten correctamente los gestos de arrastrar y soltar sin fallar a mitad de camino.
- **Soporte multimonitor**: Funciona correctamente en configuraciones de varios monitores. Los movimientos y clics del mouse funcionan correctamente en todos los monitores usando el indicador `MOUSEEVENTF_VIRTUALDESK`, asegurando un posicionamiento preciso sin importar en qué monitor esté la aplicación objetivo.
- **Simulación de teclado mejorada**: Soporte completo para teclas extendidas. Esto garantiza que los comandos de navegación y atajos enviados por el Operador de IA funcionen perfectamente en todas las aplicaciones.
- **Soporte de imágenes HEIC/HEIF**: Compatibilidad nativa con formatos de foto de iPhone. Ahora puedes seleccionar directamente archivos `.heic` y `.heif` para descripción de IA, OCR o lectura de documentos sin conversión previa.

## Cambios para 6.5.0

- **Asistente en vivo**: Asistente de voz y pantalla en tiempo real, exclusivo de Google Gemini. Incluye personalización interactiva de la voz y la profundidad de razonamiento directamente dentro del diálogo, con reconexión automática al cambiar la configuración.
- **Proveedor de IA MiniMax**: Integrado como proveedor par con soporte multimodal completo. respuesta\`) de las salidas.
- **Traducción del visor de documentos**: Corrección de error de traducción silencioso para usuarios que no usan inglés.
- **Reintento de escaneo en lotes de PDF**: Lógica de reintento optimizada y silenciosa.
- **Estado del visor de documentos**: Corrección del estado bloqueado en "Procesamiento por lotes iniciado".
- **Fallo de hilo resuelto**: Corrección del fallo `IsMain() failed in wxTimerImpl`.

## Cambios para 6.1.2

- **Verificación previa de etiquetas duplicadas**: Se corrigió un problema en el etiquetado individual donde la comprobación de duplicados usaba claves de coordenadas antiguas, provocando que NVDA hiciera solicitudes de IA duplicadas para objetos ya etiquetados en lugar de anunciar la etiqueta existente.
- **Chat de documentos para proveedores que no son Gemini**: Corregida verificación estricta de clave API.
- **Traducción rápida de OCR de Chrome**: Restaurada la API de traducción gratuita. Traducir el texto extraído ahora evita a Gemini, ahorrando cuota de API y acelerando el proceso de traducción.
- **Filtro alfanumérico de CAPTCHA**: Corregida la lógica de filtrado.
- **Actualización de ayuda de la capa de comandos**: Corrección del atajo de anuncio de estado de `L` a `I`.

## Cambios para 6.1.1

- **Corrección de salida de Gemma 4 Thinking**: Extracción correcta del texto de respuesta final. El complemento ahora aísla y extrae correctamente solo la respuesta final en texto limpio.
- **OCR en lotes desde el Explorador de archivos**: Ahora puedes seleccionar varias fotos o PDFs directamente en el Explorador de archivos de Windows y extraer texto o analizarlos en lote. El complemento filtrará y procesará automáticamente solo los formatos de archivo compatibles.

## Cambios para 6.1.0

- **Integración universal de IA local**: Botón "Configurar IA local" para Ollama, LM Studio, Jan.ai y KoboldCPP. Los usuarios ahora pueden configurar automáticamente motores de IA locales, incluyendo **Ollama**, **LM Studio**, **Jan.ai** y **KoboldCPP** al instante.
- **Omisión inteligente de proxy local**: Omisión completa de proxies del sistema para conexiones locales. El complemento ahora es lo bastante inteligente como para omitir por completo los proxies del sistema de Windows en conexiones locales de bucle de retorno, garantizando conexiones estables con la IA local incluso cuando tu VPN/modo TUN está activo.
- **Etiquetado de IA ultraestable (v2)**: Sistema híbrido de firma de objeto basado en AutomationId/ControlID. Las etiquetas ahora dependen de identificadores programáticos (**AutomationId** de UIA o **ControlID** de Win32) y coordenadas relativas a la ventana, haciendo que tus etiquetas personalizadas sean completamente resistentes al redimensionamiento de ventanas, el movimiento, el cambio de monitor o el escalado.
- **Migración automática de etiquetas**: Migración transparente al nuevo formato de huella digital. El complemento migrará automáticamente tus etiquetas antiguas basadas en coordenadas al nuevo formato de huella digital estable en segundo plano, al primer enfoque, sin pérdida de datos.

## Cambios para 6.0

- **Presentamos el Etiquetado semántico con IA**: Los usuarios ahora pueden etiquetar permanentemente botones e iconos sin nombre usando IA. **Etiquetado semántico con IA**: Tecla **L** para etiquetar el objeto actual, **Shift+L** para escanear toda la aplicación.
- **Gestión inteligente de etiquetas**: Nuevo administrador de etiquetas completamente accesible.
- **Análisis directo de archivos (omitiendo el diálogo de archivo)**: El complemento ahora es lo bastante inteligente como para detectar si estás enfocando actualmente un archivo PDF o de imagen en el Explorador de archivos de Windows. Presionar **F (Acción inteligente de archivo)** o **D (Lector de documentos)** en un archivo resaltado lo procesará de inmediato, omitiendo por completo el diálogo estándar de "Abrir".

## Cambios para 5.6

- **Motor "Ninguno (Extraer capa de texto)"**: Extracción directa de PDFs con capacidad de búsqueda sin créditos de IA.
- **Precisión mejorada del Explorador de interfaz**: Mejor identificación de tipos de elementos y estados.
- **Recordatorio de configuración de instalación**: Notificación post-instalación para configurar claves API.

## Cambios para 5.5.2

- **Error de escritura del Operador de IA corregido:** Se resolvió un error por el que se escribía la letra 'v' en lugar de pegar el texto en ciertos sistemas. Esta corrección soluciona conflictos de temporización que ocurrían durante cargas altas del sistema.
- **Estabilidad mejorada:** Se añadió manejo robusto de errores para operaciones del portapapeles, evitando bloqueos del complemento cuando el portapapeles del sistema está temporalmente bloqueado por otras aplicaciones.
- **Optimización de temporización**: Ajuste de retrasos internos para eventos de teclado.

## Cambios para 5.5 (La actualización de automatización)

- **Operador de IA (Control autónomo - Shift+A):** Esta es la joya de la corona de la v5.5. Vision Assistant Pro ha pasado de ser un asistente pasivo a convertirse en tu **Operador de IA** personal. No solo describe la pantalla: toma el mando.
  - _Cómo funciona:_ Ahora puedes dar instrucciones verbales para operar tu PC. Por ejemplo, en una aplicación completamente inaccesible donde tu lector de pantalla permanece en silencio, puedes presionar **Shift+A** y escribir: _"Haz clic en el botón Configuración"_ o _"Encuentra el campo de búsqueda, escribe 'Últimas noticias' y presiona enter."_ La IA identifica visualmente los elementos, mueve el mouse y ejecuta la tarea por ti.
  - _Nota de rendimiento:_ Esta función está optimizada para **Gemini 3.0 Flash (Preview)**, ofreciendo respuestas increíblemente rápidas e inteligentes que pueden manejar incluso los diseños de interfaz más complejos.
  - **⚠️ Advertencia de uso de API:** Dado que el Operador de IA necesita "ver" exactamente lo que ocurre para ser preciso, envía una captura de pantalla de alta resolución con cada paso. Ten en cuenta que el uso frecuente consumirá tu cuota de API mucho más rápido que las tareas estándar basadas en texto.
- **Explorador visual de interfaz (E):** ¿Cansado de navegar entre "botones sin etiquetar"? Presiona **E** para activar el Explorador de interfaz. La IA escaneará toda la ventana y generará una lista de cada elemento en el que se puede hacer clic que detecte — incluyendo iconos, gráficos y menús. Simplemente elige un elemento de la lista, y el Operador de IA hará clic en él por ti. Es como tener una "capa accesible" encima de cualquier aplicación.
- **Acción inteligente de archivo según contexto (F):** La tecla "F" se ha renovado por completo. Ya no asume que solo quieres OCR. Cuando seleccionas una sola imagen, ahora te pregunta inteligentemente tu intención: puedes elegir una **Descripción visual detallada** para entender la escena o una **Extracción de texto estructurada (OCR)** para leerla. El menú se adapta dinámicamente según el tipo de archivo y tu motor de IA activo.
- **Optimización del núcleo**: Limpieza profunda de la lógica interna del complemento. Esto resulta en una experiencia más ligera, rápida y confiable para todos los usuarios.

## Cambios para 5.0

- Soporte para OpenAI, Groq y Mistral junto a Google Gemini. Los usuarios ahora pueden elegir su motor de IA preferido.
- **Enrutamiento avanzado de modelos**: Los usuarios de proveedores nativos (Gemini, OpenAI, etc.) ahora pueden seleccionar modelos específicos desde una lista desplegable para diferentes tareas (OCR, STT, TTS).
- **Configuración avanzada de punto de acceso**: Los usuarios de proveedores personalizados pueden introducir manualmente URLs y nombres de modelo específicos para un control granular sobre servidores locales o de terceros.
- **Visibilidad inteligente de funciones**: El menú de configuración y la interfaz del Lector de documentos ahora ocultan automáticamente las funciones no compatibles (como TTS) según el proveedor seleccionado.
- Obtención dinámica de modelos directamente desde la API del proveedor.
- **OCR y traducción híbridos**: Se optimizó la lógica para usar Google Translate por velocidad al usar OCR de Chrome, y traducción con IA al usar los motores Gemini/Groq/OpenAI.
- **"Nuevo escaneo con IA" universal**: La función de nuevo escaneo del Lector de documentos ya no se limita a Gemini. Ahora utiliza cualquier proveedor de IA que esté activo para volver a procesar las páginas.

## Cambios para 4.6

- **Recuperación interactiva de resultados:** Se añadió la tecla **Espacio** a la capa de comandos, permitiendo a los usuarios reabrir al instante la última respuesta de la IA en una ventana de chat para preguntas de seguimiento, incluso cuando el modo "Salida directa" está activo.
- Enlace al canal oficial de Telegram en el menú Herramientas de NVDA.
- **Estabilidad de respuesta mejorada:** Se optimizó la lógica central de las funciones de Traducción, OCR y Visión para garantizar un rendimiento más fiable y una experiencia más fluida al usar la salida de voz directa.
- **Orientación de interfaz mejorada:** Se actualizaron las descripciones de configuración y la documentación para explicar mejor el nuevo sistema de recuperación y cómo funciona junto con la configuración de salida directa.

## Cambios para 4.5

- **Administrador de indicaciones avanzado:** Se introdujo un diálogo de gestión dedicado en la configuración para personalizar las indicaciones predeterminadas del sistema y administrar indicaciones definidas por el usuario, con soporte completo para añadir, editar, reordenar y previsualizar.
- **Soporte completo de proxy:** Se resolvieron problemas de conectividad de red asegurando que la configuración de proxy del usuario se aplique estrictamente a todas las solicitudes de API, incluyendo traducción, OCR y generación de voz.
- **Migración automatizada de datos:** Se integró un sistema de migración inteligente para actualizar automáticamente las configuraciones de indicaciones antiguas a un formato JSON v2 robusto en la primera ejecución, sin pérdida de datos.
- **Compatibilidad actualizada (2025.1):** Se estableció la versión mínima requerida de NVDA en 2025.1 debido a dependencias de bibliotecas en funciones avanzadas como el Lector de documentos, para garantizar un rendimiento estable.
- **Interfaz de configuración optimizada:** Se simplificó la interfaz de configuración reorganizando la gestión de indicaciones en un diálogo separado, ofreciendo una experiencia de usuario más limpia y accesible.
- **Guía de variables de indicación:** Se añadió una guía integrada dentro de los diálogos de indicaciones para ayudar a los usuarios a identificar y usar fácilmente variables dinámicas como [selection], [clipboard] y [screen_obj].

## Cambios para 4.0.3

- **Resistencia de red mejorada:** Se añadió un mecanismo de reintento automático para manejar mejor las conexiones a internet inestables y los errores temporales del servidor, garantizando respuestas de IA más fiables.
- **Diálogo visual de traducción:** Se introdujo una ventana dedicada para los resultados de traducción. Los usuarios ahora pueden navegar y leer fácilmente traducciones largas línea por línea, de forma similar a los resultados de OCR.
- **Vista formateada agregada:** La función "Ver formateado" en el Lector de documentos ahora muestra todas las páginas procesadas en una única ventana organizada con encabezados de página claros.
- **Flujo de OCR optimizado:** Se omite automáticamente la selección de rango de páginas para documentos de una sola página, haciendo el proceso de reconocimiento más rápido y fluido.
- **Estabilidad de API mejorada:** Se cambió a un método de autenticación más robusto basado en encabezados, resolviendo posibles errores de "Todas las claves API fallaron" causados por conflictos de rotación de claves.
- **Correcciones de errores:** Se resolvieron varios bloqueos potenciales, incluyendo un problema durante el cierre del complemento y un error de enfoque en el diálogo de chat.

## Cambios para 4.0.1

- **Lector avanzado de documentos:** Un potente visor nuevo para PDF e imágenes con selección de rango de páginas, procesamiento en segundo plano y navegación fluida con `Ctrl+AvPág/RePág`.
- **Nuevo submenú de Herramientas:** Se añadió un submenú dedicado "Vision Assistant" bajo el menú Herramientas de NVDA para un acceso más rápido a las funciones principales, la configuración y la documentación.
- **Personalización flexible:** Ahora puedes elegir tu motor OCR y voz TTS preferidos directamente desde el panel de configuración.
- **Soporte de múltiples claves API:** Se añadió soporte para varias claves API de Gemini. Puedes introducir una clave por línea o separarlas con comas en la configuración.
- **Motor OCR alternativo:** Se introdujo un nuevo motor OCR para garantizar un reconocimiento de texto fiable incluso al alcanzar los límites de cuota de la API de Gemini.
- **Rotación inteligente de claves API:** Cambia automáticamente a la clave API más rápida que funcione y la recuerda para evitar los límites de cuota.
- Generación de audio MP3/WAV directamente dentro del lector.
- **Soporte de Historias de Instagram:** Se añadió la capacidad de describir y analizar Historias de Instagram mediante sus URL.
- **Soporte de TikTok:** Se introdujo soporte para vídeos de TikTok, permitiendo la descripción visual completa y transcripción de audio de los clips.
- **Diálogo de actualización rediseñado:** Cuenta con una nueva interfaz accesible con un cuadro de texto desplazable para leer claramente los cambios de versión antes de instalar.
- **Estado y experiencia unificados:** Se estandarizaron los diálogos de archivo en todo el complemento y se mejoró el comando 'L' para informar del progreso en tiempo real.

## Cambios para 3.6.0

- **Sistema de ayuda:** Se añadió un comando de ayuda (`H`) dentro de la Capa de comandos para ofrecer una lista de fácil acceso de todos los atajos y sus funciones.
- Soporte para vídeos de Twitter (X). También se mejoró la detección de URL y la estabilidad para una experiencia más fiable.
- **Contribución al proyecto:** Se añadió un diálogo de donación opcional para los usuarios que deseen apoyar las futuras actualizaciones y el crecimiento continuo del proyecto.

## Cambios para 3.5.0

\*   Sistema de capa de comandos (`NVDA+Shift+V`). Por ejemplo, en lugar de presionar `NVDA+Control+Shift+T` para traducir, ahora presionas `NVDA+Shift+V` seguido de `T`.
\*   Análisis de vídeos de YouTube e Instagram por URL.

## Cambios para 3.1.0

- **Modo de salida directa:** Se añadió una opción para omitir el diálogo de chat y escuchar las respuestas de la IA directamente mediante voz, para una experiencia más rápida y fluida.
- **Integración con el portapapeles:** Se añadió una nueva opción para copiar automáticamente las respuestas de la IA al portapapeles.

## Cambios para 3.0

- **Nuevos idiomas:** Se añadieron las traducciones al **persa** y al **vietnamita**.
- **Modelos de IA ampliados:** Se reorganizó la lista de selección de modelos con prefijos claros (`[Gratis]`, `[Pro]`, `[Auto]`) para ayudar a distinguir entre modelos gratuitos y de pago con límite de velocidad. Se añadió soporte para **Gemini 3.0 Pro** y **Gemini 2.0 Flash Lite**.
- Mejoras de estabilidad en el Dictado inteligente. Se añadió una comprobación de seguridad para ignorar clips de audio de menos de 1 segundo, evitando alucinaciones de la IA y errores vacíos.
- **Manejo de archivos:** Se corrigió un problema por el que fallaba la carga de archivos con nombres no ingleses.
- **Optimización de indicaciones:** Se mejoró la lógica de traducción y la estructuración de los resultados de Visión.

## Cambios para 2.9

- **Se añadieron traducciones al francés y turco.**
- **Vista formateada:** Se añadió un botón "Ver formateado" en los diálogos de chat para ver la conversación con el estilo correcto (encabezados, negrita, código) en una ventana estándar navegable.
- **Opción de Markdown:** Se añadió una nueva opción "Limpiar Markdown en el chat" en Configuración. Al desmarcarla, los usuarios pueden ver la sintaxis Markdown sin procesar (por ejemplo, `**`, `#`) en la ventana de chat.
- **Gestión de diálogos:** Se corrigió un problema por el que las ventanas de "Refinar texto" o chat se abrían varias veces o no obtenían el foco correctamente.
- **Mejoras de experiencia:** Se estandarizaron los títulos de los diálogos de archivo a "Abrir" y se eliminaron anuncios de voz redundantes (por ejemplo, "Abriendo menú...") para una experiencia más fluida.

## Cambios para 2.8

- Traducción al italiano.
- **Informe de estado:** Se añadió un nuevo comando (NVDA+Control+Shift+I) para anunciar el estado actual del complemento (por ejemplo, "Cargando...", "Analizando...").
- Exportación HTML desde el botón "Guardar contenido".
- **Interfaz de configuración:** Se mejoró el diseño del panel de Configuración con agrupación accesible.
- **Nuevos modelos:** Se añadió soporte para gemini-flash-latest y gemini-flash-lite-latest.
- **Idiomas:** Se añadió el nepalí a los idiomas compatibles.
- **Lógica del menú Refinar:** Se corrigió un error crítico por el que los comandos de "Refinar texto" fallaban si el idioma de la interfaz de NVDA no era el inglés.
- **Dictado:** Se mejoró la detección de silencios para evitar una salida de texto incorrecta cuando no hay entrada de voz.
- **Configuración de actualizaciones:** "Buscar actualizaciones al inicio" ahora está desactivado de forma predeterminada para cumplir con las políticas de la tienda de complementos.
- Limpieza de código.

## Cambios para 2.7

- Migración a la plantilla oficial de complementos de NV Access.
- Reintento automático para errores HTTP 429.
- Se optimizaron las indicaciones de traducción para mayor precisión y mejor manejo de la lógica de "Intercambio inteligente".
- Actualización de la traducción al ruso.

## Cambios para 2.6

- Traducción al ruso (gracias a nvda-ru).
- Se actualizaron los mensajes de error para ofrecer información más descriptiva sobre la conectividad.
- Idioma de destino predeterminado cambiado al inglés.

## Cambios para 2.5

- Comando de OCR de archivos nativo (NVDA+Control+Shift+F).
- Se añadió el botón "Guardar chat" a los diálogos de resultados.
- Soporte completo de localización (i18n).
- Se migró la retroalimentación de audio al módulo de tonos nativo de NVDA.
- API de archivos de Gemini para mejor manejo de PDF y audio.
- Se corrigió un bloqueo al traducir texto que contenía llaves.

## Cambios para 2.1.1

- Corrección de la variable [file_ocr] en indicaciones personalizadas.

## Cambios para 2.1

- Todos los atajos estandarizados con NVDA+Control+Shift.

## Cambios para 2.0

- Sistema de actualización automática.
- Se añadió una Caché de traducción inteligente para la recuperación instantánea de texto previamente traducido.
- Memoria de conversación en diálogos de chat.
- Comando de traducción del portapapeles (NVDA+Control+Shift+Y).
- Se optimizaron las indicaciones de IA para forzar estrictamente la salida en el idioma de destino.
- Se corrigió un bloqueo causado por caracteres especiales en el texto de entrada.

## Cambios para 1.5

- Soporte para más de 20 nuevos idiomas.
- Diálogo interactivo de refinado para preguntas de seguimiento.
- Función de Dictado inteligente nativo.
- Nuevo submenú "Vision Assistant" en el menú Herramientas de NVDA.
- Se corrigieron bloqueos por COMError en aplicaciones específicas como Firefox y Word.
- Se añadió un mecanismo de reintento automático para errores del servidor.

## Cambios para 1.0

- Lanzamiento inicial.

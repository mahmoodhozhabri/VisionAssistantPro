# Documentación de Vision Assistant Pro

**Vision Assistant Pro** es un asistente de IA avanzado y multimodal para NVDA. Utiliza motores de IA de primer nivel para proporcionar lectura de pantalla inteligente, traducción, dictado por voz y análisis de documentos.

_Este complemento fue lanzado a la comunidad en honor al Día Internacional de las Personas con Discapacidad._

## 1. Configuración

Ve a **Menú NVDA > Preferencias > Configuración > Vision Assistant Pro**.

### 1.1 Configuración de conexión
- **Proveedor:** Selecciona tu servicio de IA preferido. Los proveedores compatibles incluyen **Google Gemini**, **OpenAI**, **Mistral**, **Groq** y **Personalizado** (servidores compatibles con OpenAI como Ollama/LM Studio).
- **Nota importante:** Recomendamos encarecidamente usar **Google Gemini** para obtener el mejor rendimiento y precisión (especialmente para análisis de imágenes y archivos).
- **Clave API:** Obligatoria. Puedes ingresar múltiples claves (separadas por comas o saltos de línea) para rotación automática.
- **Obtener modelos:** Después de ingresar tu clave API, presiona este botón para descargar la lista más reciente de modelos disponibles del proveedor.
- **Modelo de IA:** Selecciona el modelo principal usado para chat general y análisis.

### 1.2 Enrutamiento avanzado de modelos
*Disponible para todos los proveedores, incluyendo Gemini, OpenAI, Groq, Mistral y Personalizado.*

> **⚠️ Advertencia:** Esta configuración está destinada **únicamente a usuarios avanzados**. Si no estás seguro de lo que hace un modelo específico, déjalo **desmarcado**. Seleccionar un modelo incompatible para una tarea (por ejemplo, un modelo solo de texto para Visión) causará errores y dejará de funcionar el complemento.

Marca **"Enrutamiento avanzado de modelos (por tarea)"** para desbloquear el control detallado. Esto te permite seleccionar modelos específicos de la lista desplegable para diferentes tareas:
- **Modelo OCR / Visión:** Elige un modelo especializado para analizar imágenes.
- **Voz a texto (STT):** Elige un modelo específico para dictado.
- **Texto a voz (TTS):** Elige un modelo para generar audio.
- **Modelo del Operador IA:** Selecciona un modelo específico para tareas autónomas de operación del equipo.
*Nota: Las funciones no compatibles (por ejemplo, TTS para Groq) se ocultarán automáticamente.*

### 1.3 Configuración avanzada de endpoints (Proveedor personalizado)
*Disponible solo cuando se selecciona "Personalizado".*

> **⚠️ Advertencia:** Esta sección permite la configuración manual de la API y está diseñada para **usuarios avanzados** que ejecutan servidores locales o proxies. Las URLs o nombres de modelos incorrectos romperán la conectividad. Si no sabes exactamente qué son estos endpoints, mantenlo **desmarcado**.

Marca **"Configuración avanzada de endpoints"** para ingresar manualmente los detalles del servidor. A diferencia de los proveedores nativos, aquí debes **escribir** las URLs y nombres de modelos específicos:
- **URL de lista de modelos:** El endpoint para obtener los modelos disponibles.
- **URL de endpoint OCR/STT/TTS:** URLs completas para servicios específicos (por ejemplo, `http://localhost:11434/v1/audio/speech`).
- **Modelos personalizados:** Escribe manualmente el nombre del modelo (por ejemplo, `llama3:8b`) para cada tarea.

### 1.4 Preferencias generales
- **Motor OCR:** Elige entre **Chrome (Rápido)** para resultados rápidos o **IA (Avanzado)** para una mejor preservación del formato.
    - *Nota:* Si seleccionas "IA (Avanzado)" pero tu proveedor está configurado como OpenAI/Groq, el complemento enrutará inteligentemente la imagen al modelo de visión de tu proveedor activo.
- **Voz TTS:** Selecciona tu estilo de voz preferido. Esta lista se actualiza dinámicamente según tu proveedor activo.
- **Creatividad (Temperatura):** Controla la aleatoriedad de la IA. Los valores más bajos son mejores para traducción/OCR precisos.
- **URL de proxy:** Configúralo si los servicios de IA están restringidos en tu región (admite proxies locales como `127.0.0.1` o URLs puente).

## 2. Capa de comandos y atajos

Para evitar conflictos de teclado, este complemento usa una **Capa de comandos**.
1. Presiona **NVDA + Mayús + V** (tecla maestra) para activar la capa (escucharás un pitido).
2. Suelta las teclas, luego presiona una de las siguientes teclas individuales:

| Tecla         | Función                       | Descripción                                                                                  |
|---------------|-------------------------------|----------------------------------------------------------------------------------------------|
| **Mayús + A** | **Operador IA**               | **Operación autónoma:** Dile a la IA que realice una tarea en tu pantalla.                   |
| **E**         | **Explorador de UI**          | **Clic interactivo:** Identifica y hace clic en elementos de UI en cualquier app.            |
| **T**         | Traductor inteligente         | Traduce el texto bajo el cursor del navegador o la selección.                                |
| **Mayús + T** | Traductor de portapapeles     | Traduce el contenido actualmente en el portapapeles.                                         |
| **R**         | Refinador de texto            | Resumir, corregir gramática, explicar o ejecutar **prompts personalizados**.                 |
| **V**         | Visión del objeto             | Describe el objeto navegador actual.                                                         |
| **O**         | Visión de pantalla completa   | Analiza el diseño y contenido de toda la pantalla.                                           |
| **Mayús + V** | Análisis de vídeo en línea    | Analiza vídeos de **YouTube**, **Instagram**, **TikTok** o **Twitter (X)**.                  |
| **D**         | Lector de documentos          | Lector avanzado de PDF e imágenes con selección de rango de páginas.                        |
| **F**         | **Acción inteligente de archivo** | Reconocimiento contextual de imágenes, PDF o archivos TIFF seleccionados.               |
| **A**         | Transcripción de audio        | Transcribe archivos MP3, WAV u OGG a texto.                                                  |
| **C**         | Solucionador de CAPTCHA       | Captura y resuelve CAPTCHAs (compatible con portales gubernamentales).                       |
| **S**         | Dictado inteligente           | Convierte voz a texto. Presiona para iniciar la grabación, otra vez para detener y escribir. |
| **I**         | Informe de estado             | Anuncia el progreso actual (por ejemplo, "Escaneando...", "Inactivo").                       |
| **L**         | **Etiquetar objeto**          | **Etiquetado semántico con IA:** Etiqueta de forma permanente el elemento o icono enfocado.  |
| **Mayús + L** | **Gestionar/escanear etiquetas** | Abre el Gestor de etiquetas (si existen) o escanea la app en busca de elementos sin nombre. |
| **U**         | Buscar actualización          | Busca manualmente en GitHub la última versión del complemento.                               |
| **Espacio**   | Recuperar último resultado    | Muestra la última respuesta de la IA en un diálogo de chat para revisión o seguimiento.     |
| **H**         | Ayuda de comandos             | Muestra una lista de todos los atajos disponibles.                                           |

### 2.1 Atajos del Lector de documentos (dentro del visor)
- **Ctrl + Av Pág:** Ir a la página siguiente.
- **Ctrl + Re Pág:** Ir a la página anterior.
- **Alt + A:** Abrir un diálogo de chat para hacer preguntas sobre el documento.
- **Alt + R:** Forzar un **reescaneo con IA** usando tu proveedor activo.
- **Alt + G:** Generar y guardar un archivo de audio de alta calidad (WAV/MP3). *Oculto si el proveedor no admite TTS.*
- **Alt + S / Ctrl + S:** Guardar el texto extraído como archivo TXT o HTML.

## 3. Prompts personalizados y variables

Puedes gestionar los prompts en **Configuración > Prompts > Administrar prompts...**.

### Variables compatibles
- `[selection]`: Texto seleccionado actualmente.
- `[clipboard]`: Contenido del portapapeles.
- `[screen_obj]`: Captura de pantalla del objeto navegador.
- `[screen_full]`: Captura de pantalla completa.
- `[file_ocr]`: Selecciona imagen/PDF para extracción de texto.
- `[file_read]`: Selecciona documento para lectura (TXT, código, PDF).
- `[file_audio]`: Selecciona archivo de audio para análisis (MP3, WAV, OGG).

***
**Nota:** Se requiere conexión a Internet activa para todas las funciones de IA. Los documentos de varias páginas se procesan automáticamente.

## 4. Soporte y comunidad

Mantente al día con las últimas noticias, funciones y versiones:
- **Canal de Telegram:** [t.me/VisionAssistantPro](https://t.me/VisionAssistantPro)
- **Issues de GitHub:** Para informes de errores y solicitudes de funciones.

## 5. Patrocinadores del proyecto

Un sincero agradecimiento a los miembros de la comunidad que apoyan el desarrollo y mantenimiento continuo de este proyecto mediante sus generosas contribuciones económicas:

*   **@Alyabani94**
*   **Ali Alamri**

*Si deseas apoyar el proyecto económicamente y ver tu nombre aquí, puedes encontrar la opción **Donar** en el menú Herramientas de NVDA (submenú Vision Assistant) o durante el proceso de configuración tras la instalación.*

---

## Cambios para la versión 6.0

*   **Etiquetado semántico con IA:** Los usuarios ahora pueden etiquetar de forma permanente botones e iconos sin nombre usando IA. Presiona **L** para etiquetar el objeto navegador actual (compatible con foco por Tab y navegación por objetos) o **Mayús+L** para escanear y etiquetar toda la aplicación de una vez.
*   **Gestor de etiquetas inteligente:** Se añadió un nuevo diálogo de Gestor de etiquetas completamente accesible (disponible con **Mayús+L** si ya existen etiquetas) para ver, renombrar o eliminar etiquetas personalizadas en bloque.
*   **Análisis directo de archivos (sin diálogo de apertura):** El complemento ahora es lo suficientemente inteligente para detectar si estás enfocado en un archivo PDF o imagen en el Explorador de archivos de Windows. Al presionar **F (Acción inteligente de archivo)** o **D (Lector de documentos)** sobre un archivo resaltado, lo procesará de inmediato sin abrir el diálogo estándar de "Abrir".

## Cambios para la versión 5.6

*   **Motor OCR "Ninguno (Extraer capa de texto)" añadido:** Los usuarios ahora pueden extraer texto directamente de PDFs con texto sin usar créditos de IA, lo que mejora significativamente la velocidad y la privacidad para documentos basados en texto.
*   **Precisión del Explorador de UI mejorada:** Se mejoró el prompt del Explorador de UI para identificar mejor los tipos de elementos (como elementos de lista) e informar con precisión los estados como "(Marcado)", "(Seleccionado)" o "(Expandido)", ignorando los componentes del sistema Windows como la barra de tareas y el reloj.
*   **Recordatorio de configuración tras la instalación:** Se añadió una notificación después de la instalación para guiar a los usuarios al menú de configuración y configurar sus claves API y preferencias.

## Cambios para la versión 5.5.2

*   **Corrección del problema de escritura del Operador IA:** Se resolvió un error donde se escribía la letra 'v' en lugar de pegar texto en ciertos sistemas. Esta corrección aborda conflictos de temporización que ocurrían durante alta carga del sistema.
*   **Estabilidad mejorada:** Se añadió manejo robusto de errores para operaciones del portapapeles para evitar cierres inesperados del complemento cuando el portapapeles del sistema está temporalmente bloqueado por otras aplicaciones.
*   **Optimización de temporización:** Se ajustaron los retrasos internos para eventos de teclado para garantizar mayor fiabilidad en diferentes velocidades de sistema y mejor compatibilidad con gestores de portapapeles de terceros.

## Cambios para la versión 5.5 (La actualización de automatización)

*   **Operador IA (Control autónomo - Mayús+A):** Esta es la joya de la corona de la v5.5. Vision Assistant Pro ha pasado de ser un asistente pasivo a convertirse en tu **Operador IA** personal. Ya no solo describe la pantalla, sino que toma el control.
    *   *Cómo funciona:* Ahora puedes dar instrucciones verbales para operar tu PC. Por ejemplo, en una aplicación completamente inaccesible donde tu lector de pantalla permanece en silencio, puedes presionar **Mayús+A** y escribir: *"Haz clic en el botón Configuración"* o *"Encuentra el campo de búsqueda, escribe 'Últimas noticias' y presiona Enter."* La IA identifica visualmente los elementos, mueve el ratón y ejecuta la tarea por ti.
    *   *Nota de rendimiento:* Esta función está optimizada para **Gemini 3.0 Flash (Vista previa)**, ofreciendo respuestas increíblemente rápidas e inteligentes capaces de manejar incluso los diseños de UI más complejos.
    *   **⚠️ Advertencia de uso de API:** Dado que el Operador IA necesita "ver" exactamente lo que ocurre para ser preciso, envía una captura de pantalla de alta resolución en cada paso. Ten en cuenta que el uso frecuente consumirá tu cuota de API mucho más rápido que las tareas estándar basadas en texto.
*   **Explorador visual de UI (E):** ¿Cansado de navegar por "botones sin etiqueta"? Presiona **E** para activar el Explorador de UI. La IA escaneará toda la ventana y generará una lista de cada elemento en el que se puede hacer clic que detecte, incluyendo iconos, gráficos y menús. Simplemente elige un elemento de la lista y el Operador IA hará clic por ti. Es como tener una "capa accesible" sobre cualquier aplicación.
*   **Acción inteligente de archivo contextual (F):** La tecla "F" ha sido completamente renovada. Ya no asume que solo quieres OCR. Cuando seleccionas una sola imagen, ahora pregunta inteligentemente tu intención: puedes elegir una **Descripción visual detallada** para entender la escena o una **Extracción de texto estructurada (OCR)** para leer. El menú se adapta dinámicamente según el tipo de archivo y tu motor de IA activo.
*   **Optimización del núcleo:** Se realizó una limpieza profunda de la lógica interna del complemento, eliminando funciones heredadas no utilizadas y código redundante. Esto resulta en una experiencia más liviana, rápida y confiable para todos los usuarios.

## Cambios para la versión 5.0

* **Arquitectura multi-proveedor:** Se añadió compatibilidad completa con **OpenAI**, **Groq** y **Mistral** junto a Google Gemini. Los usuarios ahora pueden elegir su backend de IA preferido.
* **Enrutamiento avanzado de modelos:** Los usuarios de proveedores nativos (Gemini, OpenAI, etc.) ahora pueden seleccionar modelos específicos de una lista desplegable para diferentes tareas (OCR, STT, TTS).
* **Configuración avanzada de endpoints:** Los usuarios de proveedores personalizados pueden ingresar manualmente URLs y nombres de modelos específicos para control granular sobre servidores locales o de terceros.
* **Visibilidad inteligente de funciones:** El menú de configuración y la UI del Lector de documentos ahora ocultan automáticamente las funciones no compatibles (como TTS) según el proveedor seleccionado.
* **Obtención dinámica de modelos:** El complemento ahora obtiene la lista de modelos disponibles directamente desde la API del proveedor, garantizando compatibilidad con nuevos modelos en cuanto se publican.
* **OCR y traducción híbridos:** Se optimizó la lógica para usar Google Translate por velocidad cuando se usa OCR de Chrome, y traducción con IA cuando se usan motores Gemini/Groq/OpenAI.
* **"Reescaneo con IA" universal:** La función de reescaneo del Lector de documentos ya no está limitada a Gemini. Ahora utiliza cualquier proveedor de IA activo para reprocesar páginas.

## Cambios para la versión 4.6
* **Recuperación interactiva de resultados:** Se añadió la tecla **Espacio** a la capa de comandos, permitiendo a los usuarios reabrir instantáneamente la última respuesta de la IA en una ventana de chat para preguntas de seguimiento, incluso cuando el modo "Salida directa" está activo.
* **Centro comunitario de Telegram:** Se añadió un enlace al "Canal oficial de Telegram" en el menú Herramientas de NVDA, proporcionando una forma rápida de mantenerse al día con las últimas noticias, funciones y versiones.
* **Estabilidad de respuesta mejorada:** Se optimizó la lógica principal para las funciones de Traducción, OCR y Visión para garantizar un rendimiento más fiable y una experiencia más fluida al usar salida de voz directa.
* **Guía de interfaz mejorada:** Se actualizaron las descripciones de configuración y la documentación para explicar mejor el nuevo sistema de recuperación y cómo funciona junto con la configuración de salida directa.

## Cambios para la versión 4.5
* **Gestor de prompts avanzado:** Se introdujo un diálogo de gestión dedicado en la configuración para personalizar los prompts predeterminados del sistema y gestionar los prompts definidos por el usuario con soporte completo para agregar, editar, reordenar y previsualizar.
* **Soporte completo de proxy:** Se resolvieron problemas de conectividad de red garantizando que la configuración de proxy del usuario se aplique estrictamente a todas las solicitudes de API, incluyendo traducción, OCR y generación de voz.
* **Migración automática de datos:** Se integró un sistema de migración inteligente para actualizar automáticamente las configuraciones de prompts heredadas a un formato JSON v2 robusto en el primer uso sin pérdida de datos.
* **Compatibilidad actualizada (2025.1):** Se estableció la versión mínima requerida de NVDA en 2025.1 debido a dependencias de biblioteca en funciones avanzadas como el Lector de documentos para garantizar un rendimiento estable.
* **Interfaz de configuración optimizada:** Se simplificó la interfaz de configuración reorganizando la gestión de prompts en un diálogo separado, proporcionando una experiencia de usuario más limpia y accesible.
* **Guía de variables de prompt:** Se añadió una guía integrada dentro de los diálogos de prompt para ayudar a los usuarios a identificar y usar fácilmente variables dinámicas como [selection], [clipboard] y [screen_obj].

## Cambios para la versión 4.0.3
*   **Mayor resiliencia de red:** Se añadió un mecanismo de reintento automático para manejar mejor las conexiones a Internet inestables y los errores temporales del servidor, garantizando respuestas de IA más fiables.
*   **Diálogo visual de traducción:** Se introdujo una ventana dedicada para los resultados de traducción. Los usuarios ahora pueden navegar y leer traducciones largas línea por línea, similar a los resultados de OCR.
*   **Vista formateada agregada:** La función "Ver formateado" en el Lector de documentos ahora muestra todas las páginas procesadas en una sola ventana organizada con encabezados de página claros.
*   **Flujo de trabajo OCR optimizado:** Omite automáticamente la selección de rango de páginas para documentos de una sola página, haciendo el proceso de reconocimiento más rápido y fluido.
*   **Estabilidad de API mejorada:** Se cambió a un método de autenticación basado en encabezados más robusto, resolviendo posibles errores de "Todas las claves API fallaron" causados por conflictos de rotación de claves.
*   **Correcciones de errores:** Se resolvieron varios bloqueos potenciales, incluyendo un problema durante la terminación del complemento y un error de foco en el diálogo de chat.

## Cambios para la versión 4.0.1
*   **Lector de documentos avanzado:** Un potente visor nuevo para PDF e imágenes con selección de rango de páginas, procesamiento en segundo plano y navegación fluida con `Ctrl+Av Pág/Re Pág`.
*   **Nuevo submenú de herramientas:** Se añadió un submenú dedicado "Vision Assistant" bajo el menú Herramientas de NVDA para acceso más rápido a las funciones principales, configuración y documentación.
*   **Personalización flexible:** Ahora puedes elegir tu motor OCR preferido y voz TTS directamente desde el panel de configuración.
*   **Soporte para múltiples claves API:** Se añadió soporte para múltiples claves API de Gemini. Puedes ingresar una clave por línea o separarlas con comas en la configuración.
*   **Motor OCR alternativo:** Se introdujo un nuevo motor OCR para garantizar un reconocimiento de texto fiable incluso al alcanzar los límites de cuota de la API de Gemini.
*   **Rotación inteligente de claves API:** Cambia automáticamente y recuerda la clave API de funcionamiento más rápido para evitar límites de cuota.
*   **Documento a MP3/WAV:** Capacidad integrada para generar y guardar archivos de audio de alta calidad en formatos MP3 (128kbps) y WAV directamente dentro del lector.
*   **Soporte para Stories de Instagram:** Se añadió la capacidad de describir y analizar Stories de Instagram usando sus URLs.
*   **Soporte para TikTok:** Se introdujo soporte para vídeos de TikTok, permitiendo descripción visual completa y transcripción de audio de clips.
*   **Diálogo de actualización rediseñado:** Presenta una nueva interfaz accesible con un cuadro de texto desplazable para leer claramente los cambios de versión antes de instalar.
*   **Estado y UX unificados:** Se estandarizaron los diálogos de archivo en todo el complemento y se mejoró el comando 'L' para informar el progreso en tiempo real.

## Cambios para la versión 3.6.0
*   **Sistema de ayuda:** Se añadió un comando de ayuda (`H`) dentro de la Capa de comandos para proporcionar una lista de fácil acceso de todos los atajos y sus funciones.
*   **Análisis de vídeo en línea:** Se amplió el soporte para incluir vídeos de **Twitter (X)**. También se mejoró la detección de URL y la estabilidad para una experiencia más fiable.
*   **Contribución al proyecto:** Se añadió un diálogo de donación opcional para usuarios que deseen apoyar las actualizaciones futuras y el crecimiento continuo del proyecto.

## Cambios para la versión 3.5.0
\*   \*\*Capa de comandos:\*\* Se introdujo un sistema de Capa de comandos (predeterminado: `NVDA+Mayús+V`) para agrupar atajos bajo una sola tecla maestra. Por ejemplo, en lugar de presionar `NVDA+Control+Mayús+T` para traducción, ahora presionas `NVDA+Mayús+V` seguido de `T`.
\*   \*\*Análisis de vídeo en línea:\*\* Se añadió una nueva función para analizar vídeos de YouTube e Instagram directamente proporcionando una URL.

## Cambios para la versión 3.1.0
*   **Modo de salida directa:** Se añadió una opción para omitir el diálogo de chat y escuchar las respuestas de la IA directamente por voz para una experiencia más rápida y fluida.
*   **Integración con el portapapeles:** Se añadió una nueva configuración para copiar automáticamente las respuestas de la IA al portapapeles.

## Cambios para la versión 3.0

*   **Nuevos idiomas:** Se añadieron traducciones al **persa** y al **vietnamita**.
*   **Modelos de IA ampliados:** Se reorganizó la lista de selección de modelos con prefijos claros (`[Gratuito]`, `[Pro]`, `[Auto]`) para ayudar a los usuarios a distinguir entre modelos gratuitos y de pago. Se añadió soporte para **Gemini 3.0 Pro** y **Gemini 2.0 Flash Lite**.
*   **Estabilidad del dictado:** Se mejoró significativamente la estabilidad del Dictado inteligente. Se añadió una verificación de seguridad para ignorar clips de audio de menos de 1 segundo, evitando alucinaciones de la IA y errores vacíos.
*   **Manejo de archivos:** Se corrigió un problema donde la carga de archivos con nombres en idiomas distintos al inglés fallaba.
*   **Optimización de prompts:** Se mejoró la lógica de traducción y se estructuraron los resultados de Visión.

## Cambios para la versión 2.9

*   **Se añadieron traducciones al francés y al turco.**
*   **Vista formateada:** Se añadió un botón "Ver formateado" en los diálogos de chat para ver la conversación con estilos correctos (encabezados, negrita, código) en una ventana estándar navegable.
*   **Configuración de Markdown:** Se añadió una nueva opción "Limpiar Markdown en el chat" en la Configuración. Desmarcándola, los usuarios pueden ver la sintaxis Markdown sin procesar (por ejemplo, `**`, `#`) en la ventana de chat.
*   **Gestión de diálogos:** Se corrigió un problema donde las ventanas de "Refinar texto" o chat se abrían varias veces o no se enfocaban correctamente.
*   **Mejoras de UX:** Se estandarizaron los títulos de los diálogos de archivo a "Abrir" y se eliminaron los anuncios de voz redundantes (por ejemplo, "Abriendo menú...") para una experiencia más fluida.

## Cambios para la versión 2.8
* Se añadió traducción al italiano.
* **Informe de estado:** Se añadió un nuevo comando (NVDA+Control+Mayús+I) para anunciar el estado actual del complemento (por ejemplo, "Cargando...", "Analizando...").
* **Exportación HTML:** El botón "Guardar contenido" en los diálogos de resultado ahora guarda la salida como un archivo HTML formateado, preservando estilos como encabezados y negrita.
* **UI de configuración:** Se mejoró el diseño del panel de configuración con agrupación accesible.
* **Nuevos modelos:** Se añadió soporte para gemini-flash-latest y gemini-flash-lite-latest.
* **Idiomas:** Se añadió nepalí a los idiomas compatibles.
* **Lógica del menú Refinar:** Se corrigió un error crítico donde los comandos de "Refinar texto" fallaban si el idioma de la interfaz de NVDA no era inglés.
* **Dictado:** Se mejoró la detección de silencio para evitar salida de texto incorrecta cuando no hay entrada de voz.
* **Configuración de actualización:** "Buscar actualizaciones al iniciar" ahora está desactivado por defecto para cumplir con las políticas de la tienda de complementos.
* Limpieza de código.

## Cambios para la versión 2.7
* Se migró la estructura del proyecto a la plantilla oficial de complementos de NV Access para mejor cumplimiento de estándares.
* Se implementó lógica de reintento automático para errores HTTP 429 (Límite de tasa) para garantizar fiabilidad durante alto tráfico.
* Se optimizaron los prompts de traducción para mayor precisión y mejor manejo de la lógica de "Intercambio inteligente".
* Se actualizó la traducción al ruso.

## Cambios para la versión 2.6
* Se añadió soporte de traducción al ruso (gracias a nvda-ru).
* Se actualizaron los mensajes de error para proporcionar comentarios más descriptivos sobre la conectividad.
* Se cambió el idioma de destino predeterminado a inglés.

## Cambios para la versión 2.5
* Se añadió el comando nativo de OCR de archivo (NVDA+Control+Mayús+F).
* Se añadió el botón "Guardar chat" a los diálogos de resultado.
* Se implementó soporte completo de localización (i18n).
* Se migró la retroalimentación de audio al módulo de tonos nativo de NVDA.
* Se cambió a la API de archivos de Gemini para un mejor manejo de archivos PDF y de audio.
* Se corrigió un bloqueo al traducir texto que contenía llaves.

## Cambios para la versión 2.1.1
* Se corrigió un problema donde la variable [file_ocr] no funcionaba correctamente dentro de los Prompts personalizados.

## Cambios para la versión 2.1
* Se estandarizaron todos los atajos para usar NVDA+Control+Mayús para eliminar conflictos con el diseño de portátil de NVDA y las teclas de acceso rápido del sistema.

## Cambios para la versión 2.0
* Se implementó el sistema de actualización automática integrado.
* Se añadió caché inteligente de traducción para recuperación instantánea de texto previamente traducido.
* Se añadió memoria de conversación para refinar resultados contextualmente en los diálogos de chat.
* Se añadió el comando dedicado de traducción desde portapapeles (NVDA+Control+Mayús+Y).
* Se optimizaron los prompts de IA para aplicar estrictamente la salida en el idioma de destino.
* Se corrigió un bloqueo causado por caracteres especiales en el texto de entrada.

## Cambios para la versión 1.5
* Se añadió soporte para más de 20 nuevos idiomas.
* Se implementó el diálogo interactivo de Refinamiento para preguntas de seguimiento.
* Se añadió la función nativa de Dictado inteligente.
* Se añadió la categoría "Vision Assistant" al diálogo de Gestos de entrada de NVDA.
* Se corrigieron bloqueos de COMError en aplicaciones específicas como Firefox y Word.
* Se añadió mecanismo de reintento automático para errores del servidor.

## Cambios para la versión 1.0
* Versión inicial.

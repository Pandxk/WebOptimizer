# 🚀 WebOptimizer 3.0 (Pro Edition)

**WebOptimizer** es una herramienta de grado de producción construida en Python diseñada para resolver uno de los mayores problemas del desarrollo web y SEO: el peso de las imágenes. 

Esta aplicación web local permite a cualquier usuario subir lotes de imágenes (PNG, JPEG, JPG), redimensionarlas inteligentemente y comprimirlas al formato de nueva generación **WebP**, reduciendo su peso hasta en un 85% sin pérdida visual perceptible.

## ✨ Características Principales
* **Redimensionamiento Inteligente Automático (LANCZOS):** Detecta imágenes excesivamente grandes y las escala dinámicamente a un máximo de 1920px (Full HD) preservando la relación de aspecto y la máxima nitidez.
* **Privacidad por Diseño (EXIF Stripping):** El motor limpia quirúrgicamente todos los metadatos ocultos (Coordenadas GPS, perfiles ICC y datos de cámara) de las imágenes procesadas.
* **UX/UI Fluida (Gradio Blocks):** Interfaz oscura, minimalista y libre de fricción. Cuenta con "Revelación Progresiva" (los botones aparecen conforme los necesitas).
* **Renderizado con Feedback en Vivo:** Implementa generadores (Yield) en el backend para mostrar una barra de progreso que indica paso a paso qué está haciendo el motor.
* **Empaquetado Inteligente:** Si subes una sola foto, te devuelve un archivo WebP directo. Si subes un lote, lo procesa y te devuelve un archivo `.zip` con todo empaquetado.
* **Telemetría y Analítica Integrada:** Listo para producción. El frontend soporta inyección de tags de Google Analytics/Meta Pixel en la cabecera.

## 🛠️ Tecnologías Utilizadas
* **Python 3.x**
* **Gradio 4+ / 5+** (Para el renderizado de la Interfaz Web Reactiva)
* **Pillow (PIL)** (Motor de procesamiento interno para compresión WebP y remuestreo Lanczos)

## 📦 Instalación y Ejecución Local
1. Clona este repositorio:
   ```bash
   git clone https://github.com/Pandxk/WebOptimizer.git
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta el servidor local directamente con el archivo `Iniciar_Aplicacion.bat` o mediante consola:
   ```bash
   python app.py
   ```
4. Abre tu navegador y visita `http://127.0.0.1:7860`.

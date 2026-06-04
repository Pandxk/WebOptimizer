# pyrefly: ignore [missing-import]
import gradio as gr
# pyrefly: ignore [missing-import]
from PIL import Image
import io
import os
import zipfile
import tempfile
import time

# Script de analítica para producción (Google Analytics, Meta Pixel, etc.)
TRACKING_HTML = """
<!-- Google Analytics Placeholder -->
<script>
    console.log("🚀 WebPOptimizer Analytics Active");
    // window.dataLayer = window.dataLayer || [];
    // function gtag(){dataLayer.push(arguments);}
    // gtag('js', new Date());
    // gtag('config', 'G-XXXXXXXXXX');
</script>
"""

def toggle_ui(files):
    """
    Controla la interactividad de la interfaz. Bloquea los botones y controles 
    si no hay archivos subidos para evitar errores y mejorar la experiencia de usuario.
    """
    is_interactive = bool(files and len(files) > 0)
    return [
        gr.update(interactive=is_interactive), # quality_slider
        gr.update(interactive=is_interactive), # resize_checkbox
        gr.update(interactive=is_interactive), # btn
        gr.update(interactive=is_interactive), # btn_reset
        gr.update(visible=is_interactive),     # warning_text
        gr.update(visible=False),              # Oculto el botón de descarga si se cambian los archivos
        gr.update(interactive=is_interactive)  # log_out
    ]

def clear_all():
    """Limpia toda la interfaz visual para empezar de cero."""
    return [
        None, 
        80,   
        True, 
        None, 
        gr.update(visible=False), 
        gr.update(value="", interactive=False)
    ]

def process_images(files, quality, resize_img, progress=gr.Progress()):
    if not files:
        yield None, gr.update(visible=False), "Por favor, sube al menos una imagen."
        return
    
    progress(0, desc="Iniciando motor WebP...")
    time.sleep(0.2)
    
    # Creo un directorio temporal para almacenar las imágenes y el ZIP de forma segura
    temp_dir = tempfile.mkdtemp()
    log_text = ""
    first_image_path = None
    is_batch = len(files) > 1
    
    zip_path = os.path.join(temp_dir, "imagenes_optimizadas.zip")
    zipf = zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) if is_batch else None
    savings_list = []
    
    try:
        for i, f in enumerate(files):
            try:
                # 1. LECTURA Y PREPARACIÓN
                progress(((i + 0.1) / len(files)), desc=f"Procesando imagen {i+1} de {len(files)}... (Lectura)")
                orig_name = os.path.basename(f) if isinstance(f, str) else getattr(f, 'orig_name', os.path.basename(f.name))
                file_path = f if isinstance(f, str) else f.name
                
                original_size_kb = os.path.getsize(file_path) / 1024.0
                image = Image.open(file_path)
                time.sleep(0.1) 
                
                # 2. REDIMENSIONAMIENTO INTELIGENTE
                # Reduzco imágenes excesivamente grandes para web usando el algoritmo LANCZOS para no perder nitidez
                if resize_img:
                    max_size = 1920
                    if image.width > max_size or image.height > max_size:
                        progress(((i + 0.25) / len(files)), desc=f"Procesando imagen {i+1} de {len(files)}... (Escalado Inteligente)")
                        ratio = min(max_size / image.width, max_size / image.height)
                        new_width = int(image.width * ratio)
                        new_height = int(image.height * ratio)
                        image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                        time.sleep(0.1)
                
                # 3. PRIVACIDAD Y LIMPIEZA DE COLOR
                progress(((i + 0.4) / len(files)), desc=f"Procesando imagen {i+1} de {len(files)}... (Limpieza y Color)")
                
                # Elimino los metadatos (EXIF/GPS) para proteger la privacidad del usuario y ahorrar más kilobytes
                image.info.pop('exif', None)
                image.info.pop('icc_profile', None)
                
                # Evito fondos negros al convertir PNGs transparentes, rellenándolos con color blanco sólido
                if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
                    background = Image.new("RGB", image.size, (255, 255, 255))
                    if image.mode == 'RGBA':
                        background.paste(image, mask=image.split()[3])
                    elif image.mode == 'LA':
                        background.paste(image, mask=image.split()[1])
                    else:
                        background.paste(image)
                    image = background
                else:
                    image = image.convert("RGB")
                time.sleep(0.1)
                
                # 4. COMPRESIÓN A WEBP
                progress(((i + 0.7) / len(files)), desc=f"Procesando imagen {i+1} de {len(files)}... (Compresión WebP al {quality}%)")
                output_buffer = io.BytesIO()
                
                # Exif=b"" y icc_profile=b"" garantiza que WebP no guarde cabeceras basura
                image.save(output_buffer, format="WEBP", quality=quality, optimize=True, exif=b"", icc_profile=b"")
                
                optimized_size_kb = len(output_buffer.getvalue()) / 1024.0
                savings_kb = original_size_kb - optimized_size_kb
                savings_percent = (savings_kb / original_size_kb) * 100 if original_size_kb > 0 else 0
                savings_list.append(savings_percent)
                time.sleep(0.15)
                
                # 5. EMPAQUETADO FINAL
                progress(((i + 0.9) / len(files)), desc=f"Procesando imagen {i+1} de {len(files)}... (Guardando)")
                base_name = os.path.splitext(orig_name)[0]
                new_filename = f"{base_name}_opt.webp"
                
                # Si el usuario subió más de 1 archivo, lo inyecto en el paquete ZIP
                if is_batch:
                    zipf.writestr(new_filename, output_buffer.getvalue())
                
                # Extraigo la primera imagen en alta resolución para renderizarla de muestra en la pantalla
                if i == 0:
                    first_image_path = os.path.join(temp_dir, new_filename)
                    with open(first_image_path, "wb") as f_out:
                        f_out.write(output_buffer.getvalue())
                
                log_text += f"✅ {orig_name}: {original_size_kb:.1f}KB -> {optimized_size_kb:.1f}KB (Ahorro: {savings_percent:.1f}%)\n"
                
                # Imprimo el progreso en tiempo real (Barra interactiva + Log visual) usando generadores (yield)
                yield first_image_path, gr.update(visible=False), log_text
                
            except Exception as e:
                log_text += f"❌ Error al procesar {orig_name}: {str(e)}\n"
                yield first_image_path, gr.update(visible=False), log_text
                continue
    finally:
        if zipf:
            zipf.close()
            
    progress(1.0, desc="¡Renderizado completado con éxito!")
    time.sleep(0.3)
    
    # 6. TELEMETRÍA INTERNA (Registro anónimo de métricas de uso para auditar en el servidor)
    try:
        avg_savings = sum(savings_list) / len(savings_list) if savings_list else 0
        output_format = "ZIP_BATCH" if is_batch else "SINGLE_WEBP"
        print(f"[TELEMETRY - {time.strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Lote Procesado | Archivos: {len(files)} | Ahorro Promedio: {avg_savings:.1f}% | Salida: {output_format} | Calidad: {quality}% | Resized: {resize_img}")
    except Exception as e:
        print(f"[TELEMETRY] Error guardando métricas de servidor: {e}")
    
    # Decido si devuelvo el archivo WebP directo (cuando suben 1 foto) o el paquete ZIP múltiple
    if is_batch:
        yield first_image_path, gr.update(value=zip_path, visible=True, label="📦 Descargar ZIP Optimizadas"), log_text
    else:
        yield first_image_path, gr.update(value=first_image_path, visible=True, label="📥 Descargar WebP Optimizado"), log_text

# Inyección de CSS estricto para pulir la interfaz eliminando iconos nativos innecesarios de Gradio
custom_css = """
a[download] svg, button[aria-label*="Download"], button[aria-label*="Share"], button[aria-label*="fullscreen"] {
    display: none !important;
    opacity: 0 !important;
    pointer-events: none !important;
}
.image-button, .svelte-1b05v1e {
    display: none !important;
}
.file-preview a {
    pointer-events: none !important;
    cursor: default !important;
}
#boton_descarga_maestro {
    display: flex !important;
}
.progress-bar {
    background-color: #f97316 !important;
}
"""

# Construcción de la Interfaz Visual
with gr.Blocks(title="WebPOptimizer 3.0", css=custom_css, head=TRACKING_HTML) as demo:
    gr.Markdown("# 🚀 WebPOptimizer 3.0 (Pro Edition)")
    gr.Markdown("Sube tus imágenes, ajusta la configuración y obtén archivos ultraligeros listos para producción con privacidad garantizada.")
    
    with gr.Row():
        with gr.Column():
            files_in = gr.File(label="Sube tus imágenes aquí (PNG, JPEG, JPG)", file_count="multiple", type="filepath")
            with gr.Row():
                quality_slider = gr.Slider(minimum=10, maximum=100, step=1, value=80, label="Nivel de calidad WebP", interactive=False)
                resize_checkbox = gr.Checkbox(label="Redimensionar para Web (Max 1920px)", value=True, interactive=False)
            btn = gr.Button("🚀 Optimizar y Convertir todo el lote", variant="primary", interactive=False)
            btn_reset = gr.Button("🔄 Limpiar todo y empezar de nuevo", variant="secondary", interactive=False)
            warning_text = gr.Markdown("<p style='text-align: center; color: #f97316; font-size: 0.9em;'>⏳ <i>Nota: Mientras más imágenes subas, más tardará el renderizado. ¡Ten paciencia!</i></p>", visible=False)
            
        with gr.Column():
            gr.Markdown("### 👁️ Muestra de Alta Calidad (Primer Archivo)")
            image_out = gr.Image(label="Vista Previa a Resolución Completa", type="filepath", format="webp")

            gr.Markdown("### 🎉 Resultados")
            btn_download = gr.DownloadButton("📥 Descargar Resultado", visible=False, variant="primary", elem_id="boton_descarga_maestro")
            log_out = gr.Textbox(label="Reporte de Optimización", lines=5, interactive=False)
            
    # Mapeo de Eventos (Reactividad)
    files_in.change(
        fn=toggle_ui, 
        inputs=[files_in], 
        outputs=[quality_slider, resize_checkbox, btn, btn_reset, warning_text, btn_download, log_out]
    )
    
    btn.click(
        fn=process_images, 
        inputs=[files_in, quality_slider, resize_checkbox], 
        outputs=[image_out, btn_download, log_out]
    )
    
    btn_reset.click(
        fn=clear_all,
        inputs=[],
        outputs=[files_in, quality_slider, resize_checkbox, image_out, btn_download, log_out]
    )

if __name__ == "__main__":
    # Arranca el servidor web local
    demo.launch(server_name="127.0.0.1", server_port=7860, inbrowser=True)

import time
import os
import io
import random
from PIL import Image

def run_stress_test():
    print("=== INICIANDO TEST DE ESTRES WEBP (WebPOptimizer 2.0) ===")
    num_images = 20
    width, height = 1920, 1080
    
    print(f"1. Generando {num_images} imágenes sintéticas Full HD (1920x1080)...")
    images = []
    
    # Creamos imágenes de ruido puro para desafiar al compresor WebP
    # (Las imágenes con mucho ruido son las más difíciles de comprimir)
    for i in range(num_images):
        img = Image.effect_noise((width, height), 50).convert("RGB")
        images.append(img)
        
    print("2. Iniciando compresión secuencial simulando app.py...")
    start_time = time.time()
    
    total_original_bytes = 0
    total_webp_bytes = 0
    
    for i, img in enumerate(images):
        # Simular peso original (JPEG a 95% de calidad)
        jpg_buf = io.BytesIO()
        img.save(jpg_buf, format="JPEG", quality=95)
        total_original_bytes += len(jpg_buf.getvalue())
        
        # Lógica exacta de nuestra app.py
        webp_buf = io.BytesIO()
        img.save(webp_buf, format="WEBP", quality=80, optimize=True)
        total_webp_bytes += len(webp_buf.getvalue())
        
    end_time = time.time()
    total_time = end_time - start_time
    
    print("\n=== RESULTADOS DEL TEST DE ESTRES ===")
    print(f"Total de imágenes procesadas: {num_images}")
    print(f"Resolución de prueba: {width}x{height} (Full HD)")
    print(f"Tiempo Total de renderizado: {total_time:.2f} segundos")
    print(f"Rendimiento Promedio: {total_time/num_images:.2f} segundos por imagen")
    print(f"Peso Original Total (JPEG simulado): {total_original_bytes / (1024*1024):.2f} MB")
    print(f"Peso Optimizado Total (WebP): {total_webp_bytes / (1024*1024):.2f} MB")
    print(f"Porcentaje de Ahorro: {(1 - total_webp_bytes/total_original_bytes)*100:.2f}%")
    print("=====================================")

if __name__ == '__main__':
    run_stress_test()

@echo off
title WebPOptimizer Gradio Server
echo ==============================================
echo Instalando dependencias necesarias (Gradio)...
echo ==============================================
C:/Users/Andres/AppData/Local/Python/bin/python.exe -m pip install -r requirements.txt
echo.
echo ==============================================
echo Iniciando WebPOptimizer 2.0 (Version Gradio)...
echo ==============================================
echo La aplicacion deberia abrirse en tu navegador en un momento.
echo Si no abre automaticamente, entra a: http://127.0.0.1:7860
echo.
echo Por favor, no cierres esta ventana negra mientras usas la app.
echo Para detener el sistema, presiona Ctrl + C.
echo ==============================================
echo.
C:/Users/Andres/AppData/Local/Python/bin/python.exe c:/Users/Andres/Documents/PROYECTOS/Conversor/app.py
pause

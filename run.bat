@echo off
cd C:\BOT

:loop
echo [SISTEMA] Iniciando proceso de Python... >> registro_consola.txt
python main.py >> registro_consola.txt 2>&1
echo [ERROR CRITICO] El proceso se detuvo. Reiniciando en 5 segundos... >> registro_consola.txt
timeout /t 5 /nobreak > nul
goto loop
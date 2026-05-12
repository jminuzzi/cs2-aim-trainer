@echo off
echo Criando executavel do Treinador de Mira...
pip install pyinstaller pygame
pyinstaller --onefile --windowed --name "TreinadorMira" --icon=NONE treinador_mira.py
echo.
echo Executavel criado na pasta dist/
echo.
pause

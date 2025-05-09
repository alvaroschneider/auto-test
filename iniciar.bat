@echo off
cls
echo ===============================
echo        AUTOEVALUADOR
echo ===============================
echo.
echo Selecciona la cantidad de preguntas:
echo.
echo 1 - 32 preguntas
echo 2 - 64 preguntas
echo 3 - 96 preguntas
echo 4 - Todas (144 preguntas)
echo.

set /p opcion=Ingresá tu opción (1/2/3/4): 

if "%opcion%"=="1" (
    set cantidad=32
) else if "%opcion%"=="2" (
    set cantidad=64
) else if "%opcion%"=="3" (
    set cantidad=96
) else (
    set cantidad=144
)

echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat

echo.
python autotest.py %cantidad%

pause

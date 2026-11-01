@echo off
REM ============================================================
REM  iniciar-todo.bat - Arranca todo el proyecto en Windows (sin admin)
REM  1) MySQL como proceso   2) API FastAPI (8000)
REM  3) API Express (3000)   4) Frontend presU (5173)   5) Navegador
REM  PostgreSQL debe estar corriendo (servicio o proceso propio).
REM ============================================================
setlocal
set "RAIZ=%~dp0"
title Iniciar todo - Prestamos entre estudiantes (presU)

if not exist "%RAIZ%api-fastapi\.env" copy "%RAIZ%api-fastapi\.env.example" "%RAIZ%api-fastapi\.env" >nul
if not exist "%RAIZ%api-express\.env" copy "%RAIZ%api-express\.env.example" "%RAIZ%api-express\.env" >nul

echo [1/5] Iniciando MySQL (C:\Users\POMBO\mysql-data)...
start "MySQL local (no cierres esta ventana)" "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysqld.exe" --defaults-file="C:\Users\POMBO\mysql-data-config\my.ini" --console
timeout /t 8 /nobreak >nul

echo [2/5] Iniciando API FastAPI en http://localhost:8000 ...
if not exist "%RAIZ%api-fastapi\.venv\Scripts\python.exe" (
  echo    Creando entorno virtual con Python 3.12...
  pushd "%RAIZ%api-fastapi"
  py -3.12 -m venv .venv
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  popd
)
start "API FastAPI :8000" cmd /k "cd /d "%RAIZ%api-fastapi" && .venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

echo [3/5] Iniciando API Express en http://localhost:3000 ...
if not exist "%RAIZ%api-express\node_modules" (
  pushd "%RAIZ%api-express"
  call npm install
  popd
)
start "API Express :3000" cmd /k "cd /d "%RAIZ%api-express" && npm run dev"

echo [4/5] Iniciando frontend presU en http://localhost:5173 ...
if not exist "%RAIZ%presU\node_modules" (
  pushd "%RAIZ%presU"
  call npm install
  popd
)
start "Frontend presU :5173" cmd /k "cd /d "%RAIZ%presU" && npm run dev"

echo [5/5] Esperando a que todo arranque...
timeout /t 12 /nobreak >nul
start "" http://localhost:5173

echo Listo. Cierra las ventanas abiertas para detener cada servicio.
endlocal

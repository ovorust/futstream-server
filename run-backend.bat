@echo off
REM Script para executar o backend da aplicação

echo ========================================
echo  StreamPicker - Backend FastAPI
echo ========================================
echo.

REM Verificar se o ambiente virtual existe
if not exist "venv\" (
    echo [!] Ambiente virtual nao encontrado
    echo [*] Criando ambiente virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
    
    echo [*] Instalando dependencias...
    pip install -r requirements.txt
    
    echo [*] Instalando navegador Playwright...
    playwright install chromium
) else (
    call venv\Scripts\activate.bat
)

echo.
echo [*] Iniciando servidor FastAPI em http://localhost:8000
echo [*] Documentacao em http://localhost:8000/docs
echo.
echo [PRESSIONE Ctrl+C PARA PARAR]
echo.

python server.py

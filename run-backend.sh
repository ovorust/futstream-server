#!/bin/bash
# Script para executar o backend da aplicação

echo "========================================"
echo "  StreamPicker - Backend FastAPI"
echo "========================================"
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "[!] Ambiente virtual nao encontrado"
    echo "[*] Criando ambiente virtual..."
    python3 -m venv venv
    source venv/bin/activate
    
    echo "[*] Instalando dependencias..."
    pip install -r requirements.txt
    
    echo "[*] Instalando navegador Playwright..."
    playwright install chromium
else
    source venv/bin/activate
fi

echo ""
echo "[*] Iniciando servidor FastAPI em http://localhost:8000"
echo "[*] Documentacao em http://localhost:8000/docs"
echo ""
echo "[PRESSIONE Ctrl+C PARA PARAR]"
echo ""

python server.py

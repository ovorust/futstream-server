# StreamPicker - Web Application

Aplicação web para streaming de jogos ao vivo com arquitetura client-server.

## Estrutura

- **Backend**: FastAPI (Python) em `server.py`
- **Frontend**: React em `src/App.js`

## Requisitos

- Python 3.9+
- Node.js 16+
- npm ou yarn

## Instalação

### 1. Backend (Python)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Instalar navegador Playwright
playwright install chromium
```

### 2. Frontend (React)

```bash
# Instalar dependências npm
npm install
```

## Executando a Aplicação

### Terminal 1 - Backend

```bash
# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Executar servidor FastAPI
python server.py
```

O backend estará disponível em `http://localhost:8000`
- Health check: `http://localhost:8000/api/health`
- Documentação interativa: `http://localhost:8000/docs`

### Terminal 2 - Frontend

```bash
# Executar aplicação React
npm start
```

O frontend estará disponível em `http://localhost:3000`

## APIs do Backend

### GET `/api/health`
Verifica se a API está online.

**Response:**
```json
{"status": "ok"}
```

### GET `/api/games`
Retorna lista de jogos ao vivo disponíveis.

**Response:**
```json
[
  {
    "title": "Flamengo x Vasco ao vivo",
    "url": "https://multicanaishd.deals/futebol/..."
  }
]
```

### GET `/api/players?game_url=<url>`
Retorna lista de players disponíveis para um jogo específico.

**Parameters:**
- `game_url` (string, obrigatório): URL do jogo

**Response:**
```json
[
  {
    "label": "Player 1",
    "url": "https://..."
  }
]
```

## Estrutura de Pastas

```
unwrapped/
├── server.py                 # Backend FastAPI
├── requirements.txt          # Dependências Python
├── package.json              # Dependências Node.js
├── public/                   # Arquivos estáticos
│   └── index.html
└── src/
    ├── App.js               # Componente principal React
    ├── App.css              # Estilos da aplicação
    ├── index.js             # Entry point React
    ├── index.css            # Estilos globais
    └── ...
```

## Funcionalidades

✅ Listar jogos ao vivo em tempo real  
✅ Selecionar um jogo para ver players disponíveis  
✅ Abrir stream em nova aba  
✅ Interface escura com tema customizado  
✅ Feedback de carregamento com spinner  
✅ Responsiva (desktop e tablet)

## Troubleshooting

### Erro: "Cannot connect to http://localhost:8000"
- Certifique-se de que o servidor Python está rodando
- Verifique se a porta 8000 está disponível

### Erro: "Module not found" (Python)
- Ative o ambiente virtual
- Execute `pip install -r requirements.txt`

### Erro de CORS no browser
- O backend está configurado para aceitar requisições de `localhost:3000`
- Certifique-se de que está acessando via `localhost` e não `127.0.0.1`

## Desenvolvimento

Para adicionar novas funcionalidades:

1. **Backend**: Adicione novos endpoints em `server.py`
2. **Frontend**: Adicione novos componentes em `src/`
3. Ambos estão configurados para hot-reload durante desenvolvimento

## Licença

Este projeto é fornecido como está para fins educacionais.

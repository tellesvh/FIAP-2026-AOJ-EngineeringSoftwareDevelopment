from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import time

app = FastAPI()

# MOCKS DE MICROSERVIÇOS INTERNOS
@app.get("/api/v1/catalogo")
async def get_catalogo():
    return {"produtos": [
        {"id": 1, "nome": "Sabre de Luz", "preco": 1500.0},
        {"id": 2, "nome": "Capa da Invisibilidade", "preco": 3000.0}
    ]}

@app.get("/api/v1/estoque/{produto_id}")
async def get_estoque(produto_id: int):
    # Simulando um microserviço de estoque
    return {"id": produto_id, "disponivel": True, "entrega": "2 dias"}

# --- MISSÃO BFF: O aluno deve consolidar Catalogo + Estoque aqui ---
@app.get("/api/bff/home")
async def bff_home():
    return {
        "vitrine": [
            {"id": 1, "nome": "Sabre de Luz", "preco": 1500.0, "estoque": "Disponível"},
            {"id": 2, "nome": "Capa da Invisibilidade", "preco": 3000.0, "estoque": "Disponível"}
        ],
        "timestamp": time.time()
    }

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

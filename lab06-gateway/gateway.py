from fastapi import FastAPI, Request
import time
import httpx
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# MOCKS DE MICROSERVIÇOS INTERNOS (Simulando o Backend)
@app.get("/usuarios/me")
async def get_user():
    return {"id": 1, "nome": "Rafael Matsuyama", "perfil": "Premium"}


@app.get("/pedidos/recentes")
async def get_recent_orders():
    return {"itens": [{"id": 101, "total": 50.0}, {"id": 102, "total": 120.0}]}


# --- LAB 06: ENDPOINT VULNERÁVEL (BOT) ---
@app.get("/precos/lista")
@limiter.limit("5/second") # Máximo de 5 chamadas por segundo por IP
async def listar_precos(request: Request):
    return {"precos": [10.0, 20.0, 30.0], "status": "protegido"}


# --- LAB 06: MISSÃO BFF (O aluno deve criar o /mobile-home) ---
# O aluno deverá implementar o endpoint agregador conforme o roteiro.
BASE_URL = "http://localhost:8000"


@app.get("/mobile-home")
async def bff_mobile_home():
    print("[GATEWAY] Consolidando dados para Mobile...")

    # Em um cenário real, estas seriam chamadas para Microserviços diferentes
    async with httpx.AsyncClient() as client:
        # Chamada 1: Dados do Usuário
        res_user = await client.get(f"{BASE_URL}/usuarios/me")
        # Chamada 2: Últimos Pedidos
        res_orders = await client.get(f"{BASE_URL}/pedidos/recentes")

    return {
        "usuario": res_user.json(),
        "pedidos": res_orders.json()["itens"],
        "timestamp_gateway": time.time(),
    }

import requests
from tenacity import retry, stop_after_attempt, wait_fixed


# Função de Fallback (Socorro)
def fallback_seguro(retry_state):
    print("!!! ALERTA: Anti-Fraude instável. Acionando Fallback de Segurança !!!")
    return {
        "status": "ANALISE_MANUAL",
        "codigo": 202,
        "mensagem": "Pagamento recebido. Aguarde análise manual devido à instabilidade técnica.",
    }


class CheckoutService:
    def __init__(self, antifraude_url="http://localhost:8080/v1/validar"):
        self.antifraude_url = antifraude_url

    @retry(
        stop=stop_after_attempt(3),  # Tenta apenas 3 vezes
        wait=wait_fixed(0.1),  # Espera só 100ms entre elas
        retry_error_callback=fallback_seguro,  # Se falhar tudo, chama o socorro
    )
    def processar_pagamento(self, transacao):
        # IMPORTANTE: Reduza o timeout para 0.5s para forçar a falha rápida!
        response = requests.get(self.antifraude_url, timeout=0.5)
        return response.json()

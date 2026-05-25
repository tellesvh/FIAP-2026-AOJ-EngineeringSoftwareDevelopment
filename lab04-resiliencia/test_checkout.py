import pytest
import time
import responses
from pytest_bdd import scenario, given, when, then, parsers
from checkout_service import CheckoutService

@responses.activate
@scenario('resiliencia.feature', 'O Anti-Fraude está instável e deve falhar rápido')
def test_resiliencia_antifraude():
    pass

@pytest.fixture
def checkout():
    return CheckoutService(antifraude_url="http://api-antifraude/v1/validar")

@given('que o serviço de Anti-Fraude está com latência de 10s')
def setup_antifraude_lento():
    def request_callback(request):
        # Simula o lag real na rede que causará a falha no teste original
        time.sleep(2.0) 
        return (200, {}, '{"status": "OK"}')

    responses.add_callback(
        responses.GET,
        "http://api-antifraude/v1/validar",
        callback=request_callback,
        content_type='application/json',
    )

@when(parsers.parse('eu tento processar um pagamento de "{valor}"'), target_fixture="resultado")
def processar_pagamento(checkout, valor):
    start_time = time.time()
    try:
        res = checkout.processar_pagamento({"valor": valor})
        duration = time.time() - start_time
        return {"response": res, "duration": duration}
    except Exception as e:
        duration = time.time() - start_time
        return {"error": str(e), "duration": duration}

@then(parsers.parse('o sistema deve responder em menos de {limite:f}s'))
def validar_tempo_resposta(resultado, limite):
    assert resultado["duration"] < limite, f"Sistema muito lento: {resultado['duration']}s"

@then(parsers.parse('deve retornar o status "{status}"'))
def validar_status(resultado, status):
    if "error" in resultado:
        pytest.fail(f"Erro inesperado: {resultado['error']}")
    
    # Se o aluno não implementar o fallback, o status vindo do mock será "OK"
    # O teste espera "ANALISE_MANUAL" (que é o resultado do Fallback do Circuit Breaker)
    assert resultado["response"]["status"] == status

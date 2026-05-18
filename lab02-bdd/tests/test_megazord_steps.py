from pytest_bdd import scenarios, given, when, then, parsers
from src.calculadoras import CalculadoraDeEnergia

# Informa ao pytest-bdd onde está o arquivo de texto (Gherkin)
scenarios("../features/megazord.feature")


# GIVEN: O Setup (Estado inicial)
@given(
    parsers.parse('que o cliente é tipo "{tipo_cliente}"'), target_fixture="contexto"
)
def setup_cliente(tipo_cliente):
    # Passamos os dados via um dicionário que funciona como a "memória" do teste
    return {"tipo_cliente": tipo_cliente}


@given(parsers.parse('a missão será na região "{regiao}"'))
def setup_regiao(contexto, regiao):
    contexto["regiao"] = regiao


# WHEN: A Ação do Sistema
@when(
    parsers.parse("o Megazord calcular o custo de uma missão de valor {valor_base:d}")
)
def acao_calcular(contexto, valor_base):
    calculadora = CalculadoraDeEnergia()
    # Executa a nossa classe refatorada do Lab 01
    contexto["custo_final"] = calculadora.calcular_total(
        valor_base, contexto["tipo_cliente"], contexto["regiao"]
    )


# THEN: A Validação (Asserts)
@then(parsers.parse("o custo final de energia deve ser {valor_esperado:d}"))
def checar_resultado(contexto, valor_esperado):
    assert contexto["custo_final"] == valor_esperado

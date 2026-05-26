import time


class PagamentoAPI:
    def cobrar(self, pedido_id, valor):
        print(f"   [API Pagamento] Cobrando R$ {valor} do pedido {pedido_id}... OK!")
        return {"status": "COBRADO"}

    def estornar(self, pedido_id, valor):
        print(
            f"   [API Pagamento] Realizando ESTORNO de R$ {valor} do pedido {pedido_id}... OK!"
        )
        return {"status": "ESTORNADO"}


class EstoqueAPI:
    def reservar(self, pedido_id, produto_id):
        # SIMULAÇÃO DE ERRO: O estoque sempre falha para forçar a SAGA
        print(f"   [API Estoque] Tentando reservar produto {produto_id}... ERRO 500!")
        raise Exception("Serviço de Estoque Indisponível (Timeout)")


class OrquestradorSaga:
    def __init__(self):
        self.pagamento_api = PagamentoAPI()
        self.estoque_api = EstoqueAPI()

    def processar_pedido_completo(self, pedido_id, valor, produto_id):
        print(f"\n[SAGA] Iniciando processamento do pedido {pedido_id}...")

        # Passo 1: Cobrar o Cliente
        # Se falhar aqui, não tem problema, o fluxo para.
        self.pagamento_api.cobrar(pedido_id, valor)

        # Passo 2: Tentar reservar o Estoque
        try:
            # O estoque é instável e vai falhar!
            self.estoque_api.reservar(pedido_id, produto_id)
            return {"status": "SUCESSO_TOTAL"}

        except Exception as e:
            print(f"[SAGA] Falha Crítica no Estoque detectada: {e}")
            print(f"[SAGA] Iniciando Transação Compensatória (Rollback)...")

            # --- O CORAÇÃO DO SAGA ---
            # Como falhou no passo 2, DEVEMOS desfazer o passo 1.
            resultado_estorno = self.pagamento_api.estornar(pedido_id, valor)

            if resultado_estorno["status"] == "ESTORNADO":
                return {"status": "CANCELADO_COM_ESTORNO", "motivo": "Falta de estoque"}
            else:
                # O Pior Cenário: O estorno também falhou!
                # Isso requer intervenção humana imediata (Dead Letter Queue/Alertas)
                return {"status": "INCONSISTENTE_FATAL", "motivo": "Falha no estorno"}

import uuid


class RepositorioPedido:
    def salvar(self, valor_final: float):
        pedido_id = str(uuid.uuid4())[:8]
        print(f"[LOG] Gravando dados no cristal de memória {pedido_id}...")
        print(f"[STATUS] Energia Final Requerida: R$ {valor_final:.2f}")

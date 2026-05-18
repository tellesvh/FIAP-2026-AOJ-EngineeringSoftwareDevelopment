class ItemInventario:
    """
    DOMÍNIO ANÊMICO: Saco de dados, sem comportamento.
    """

    def __init__(self, nome: str, preco: float):
        self.nome = nome
        self.preco = preco


class Inventario:
    """
    DOMÍNIO ANÊMICO: Apenas uma lista boba, não controla nada.
    """

    def __init__(self):
        self.itens = []

    def calcular_valor_total(self, aplicar_imposto: bool) -> float:
        total = 0.0
        for item in self.itens:
            if item.nome.startswith("Poção") and aplicar_imposto:
                total += item.preco * 1.10  # 10% de imposto
            else:
                total += item.preco
        return total

    def adicionar_novo_item(self, nome: str, preco: float):
        novo_item = ItemInventario(nome, preco)
        self.itens.append(novo_item)


class TaverneiroService:
    """
    O PROBLEMA: Faz todo o trabalho, violando Information Expert e Creator.
    """

    def vender_pocao(self, inventario: Inventario):
        print("Taverneiro: 'Aqui está sua poção, forasteiro!'")
        # Delega a criação para o próprio Inventario
        inventario.adicionar_novo_item("Poção de Cura", 50.0)

    def vender_espada(self, inventario: Inventario):
        print("Taverneiro: 'Esta é uma lâmina afiada!'")
        novo_item = ItemInventario("Espada Longa", 150.0)
        inventario.itens.append(novo_item)

    def calcular_total_mochila(
        self, inventario: Inventario, aplicar_imposto: bool
    ) -> float:
        # O Taverneiro não faz mais a conta na mão, ele só pergunta pro Inventário!
        return inventario.calcular_valor_total(aplicar_imposto)


if __name__ == "__main__":
    mochila = Inventario()
    servico = TaverneiroService()

    servico.vender_pocao(mochila)
    servico.vender_espada(mochila)

    valor_total = servico.calcular_total_mochila(mochila)
    print(f"O valor total devido é de: {valor_total} peças de ouro.")

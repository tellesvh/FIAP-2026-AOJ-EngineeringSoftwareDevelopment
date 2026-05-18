from desconto import DescontoComum, DescontoPremium, DescontoVIP
from frete import FreteNorte, FreteNordeste, FretePadrao, FreteSul
from repositorio_pedido import RepositorioPedido
from servico_notificacao import ServicoNotificacao


class ThunderMegazord:
    """
    THUNDER MEGAZORD: Uma classe gigante que faz tudo ao mesmo tempo.
    Sua missão é desmontar este Megazord em componentes menores e especializados (SOLID).

    Violações:
    - SRP: Valida, calcula desconto, calcula frete, salva no banco e envia e-mail.
    - OCP: Adicionar novos descontos ou regiões exige abrir este peito de metal e soldar novo código.
    - DIP: Totalmente acoplado a implementações concretas de IO e Log.
    """

    def processar_comando_central(self, pedido_data: dict) -> bool:
        print("--- INICIANDO PROTOCOLO MEGAZORD ---")

        # 1. Sensores de Validação
        if not pedido_data.get("itens"):
            print("[ALERTA] Sistema sem munição (pedido sem itens)")
            return False

        # 2. Núcleo de Desconto (OCP Nightmare)
        valor_total = pedido_data.get("valor_total", 0.0)
        tipo_cliente = pedido_data.get("tipo_cliente", "comum")

        estrategias_desconto = {
            "vip": DescontoVIP(),
            "premium": DescontoPremium(),
            "comum": DescontoComum(),
        }

        estrategia_atual = estrategias_desconto.get(tipo_cliente, DescontoComum())
        valor_total = estrategia_atual.calcular(valor_total)

        # 3. Propulsores de Frete (OCP Nightmare)
        regiao = pedido_data.get("regiao", "sudeste")

        estrategias_frete = {
            "norte": FreteNorte(),
            "nordeste": FreteNordeste(),
            "sul": FreteSul(),
        }

        estrategia_frete_atual = estrategias_frete.get(regiao, FretePadrao())
        frete = estrategia_frete_atual.calcular()

        valor_final = valor_total + frete

        RepositorioPedido().salvar(valor_final)
        ServicoNotificacao().notificar(pedido_data.get("email"))

        print("--- OPERAÇÃO MEGAZORD CONCLUÍDA ---")
        return True


if __name__ == "__main__":
    megazord = ThunderMegazord()
    missao = {
        "itens": ["Espada Thunder", "Escudo"],
        "valor_total": 5000.0,
        "tipo_cliente": "vip",
        "regiao": "norte",
        "email": "zordon@alameda.com",
    }
    megazord.processar_comando_central(missao)

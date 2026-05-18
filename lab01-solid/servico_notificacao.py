class ServicoNotificacao:
    def notificar(self, email: str):
        if email:
            print(f"[SINAL] Enviando telemetria para {email}...")

import json

# --- OBSERVERS ---
class ConsoleObserver:
    def update(self, mensagem):
        print(f"[Console] {mensagem}")

class ArquivoObserver:
    def __init__(self, arquivo="log.txt"):
        self.arquivo = arquivo

    def update(self, mensagem):
        with open(self.arquivo, "a") as f:
            f.write(mensagem + "\n")

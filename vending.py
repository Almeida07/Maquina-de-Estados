from enum import Enum


class Estado(Enum):
    OCIOSA = "OCIOSA"
    COM_CREDITO = "COM_CREDITO"
    DISPENSANDO = "DISPENSANDO"
    FORA_DE_SERVICO = "FORA_DE_SERVICO"


class TransicaoInvalida(Exception):
    pass


class MaquinaVenda:
    PRECO = 300  # centavos

    def __init__(self):
        self.estado = Estado.OCIOSA
        self.credito = 0
        self.devolvido = 0  # valor devolvido ao cliente na última operação

    def _exigir(self, *permitidos):
        if self.estado not in permitidos:
            raise TransicaoInvalida(f"Evento inválido em {self.estado.name}")

    def inserir_moeda(self, valor):
        self._exigir(Estado.OCIOSA, Estado.COM_CREDITO)
        self.credito += valor
        self.estado = Estado.COM_CREDITO            # T1 / T2

    def selecionar(self):
        self._exigir(Estado.COM_CREDITO)
        if self.credito >= self.PRECO:
            self.estado = Estado.DISPENSANDO        # T3
        # senão permanece em COM_CREDITO             # T4

    def cancelar(self):
        self._exigir(Estado.COM_CREDITO)
        self.devolvido, self.credito = self.credito, 0
        self.estado = Estado.OCIOSA                 # T5

    def dispensa_ok(self):
        self._exigir(Estado.DISPENSANDO)
        self.devolvido = self.credito - self.PRECO
        self.credito = 0
        self.estado = Estado.OCIOSA                 # T6

    def falha_mecanica(self):
        self._exigir(Estado.DISPENSANDO)
        self.devolvido, self.credito = self.credito, 0
        self.estado = Estado.FORA_DE_SERVICO        # T7

    def reparar(self):
        self._exigir(Estado.FORA_DE_SERVICO)
        self.estado = Estado.OCIOSA                 # T8

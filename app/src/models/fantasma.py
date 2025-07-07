import random

class Fantasma:
    def __init__(self, id, chunk, tipo):
        if tipo not in ["minerador", "construtor"]:
            raise ValueError("Tipo deve ser 'minerador' ou 'construtor'.")

        self.id = id
        self.chunk = chunk
        self.tipo = tipo
        self.ativo = True
        self.acao_realizada = False
        self.tipo_construcao = None

    def minerar(self, material):
        if self.tipo != "minerador" or self.acao_realizada:
            return None

        self.acao_realizada = True

        tabela = {
            "madeira": (20, 30),
            "pedra": (10, 20),
            "ferro": (5, 10),
            "carvão": (3, 6),
            "redstone": (1, 3),
            "diamante": (0, 1),
        }

        if material not in tabela:
            raise ValueError("Material inválido.")

        return {material: random.randint(*tabela[material])}

    def construir(self, tipo, recursos, destino_chunk=None):
        if self.tipo != "construtor" or self.acao_realizada:
            return "Não pode construir."

        custos = {
            "totem": {"pedra": 10, "carvão": 3, "redstone": 1},
            "ponte": {"madeira": 15, "pedra": 10}
        }

        if tipo not in custos:
            return "Construção inválida."

        for recurso, qtd in custos[tipo].items():
            if recursos.get(recurso, 0) < qtd:
                return f"Faltam {qtd - recursos.get(recurso, 0)} de {recurso}"

        self.acao_realizada = True
        self.tipo_construcao = tipo

        for recurso, qtd in custos[tipo].items():
            recursos[recurso] -= qtd

        if tipo == "ponte" and destino_chunk:
            return f"Ponte construída de {self.chunk} para {destino_chunk}"
        return f"Totem construído em {self.chunk}"

    def to_dict(self):
        return {
            "id": self.id,
            "chunk": self.chunk,
            "tipo": self.tipo,
            "ativo": self.ativo,
            "acao_realizada": self.acao_realizada,
            "tipo_construcao": self.tipo_construcao
        }

    def __repr__(self):
        return (
            f"Fantasma(id={self.id}, tipo='{self.tipo}', chunk='{self.chunk}', "
            f"ativo={self.ativo}, acao_realizada={self.acao_realizada}, "
            f"tipo_construcao={self.tipo_construcao})"
        )

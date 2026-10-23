from .livro import Livro


class Estante:
    __codigo_estante: str
    livros: list[Livro]

    def __init__(self, codigo_estante: str) -> None:
        pass

    def adicionar_livro(self, livro: Livro) -> None:
        pass

    def listar_livros(self) -> list[Livro]:
        pass

    def obter_livro(self, isbn: str) -> Livro:
        pass
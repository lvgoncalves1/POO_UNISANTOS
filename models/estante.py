from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .livro import Livro


class Estante:
    def __init__(self, codigo_estante: str) -> None:
        self._codigo_estante: str = codigo_estante
        self.livros: list[Livro] = []

    def adicionar_livro(self, livro: Livro) -> None:
        self.livros.append(livro)

    def listar_livros(self) -> list[Livro]:
        return self.livros

    def obter_livro(self, isbn: str) -> Livro | None:
        for livro in self.livros:
            if livro.isbn == isbn:
                return livro
        return None
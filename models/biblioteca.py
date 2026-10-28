from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from .usuario import Usuario
    from .estante import Estante
    from .emprestimo import Emprestimo
    from .livro import Livro


class Biblioteca:
    def __init__(self, id: UUID, nome: str) -> None:
        self._id: UUID = id
        self.nome: str = nome
        self._usuarios: list[Usuario] = []
        self._estantes: list[Estante] = []
        self._emprestimos: list[Emprestimo] = []

    def adicionar_estante(self, estante: Estante):
        self._estantes.append(estante)

    def adicionar_usuario(self, usuario: Usuario) -> None:
        self._usuarios.append(usuario)

    def buscar_livro(self, isbn: str) -> Livro | None:
        for estante in self._estantes:
            livro = estante.obter_livro(isbn)

        if livro is not None:
            return livro

        return None

    def registrar_emprestimo(self, emprestimo: Emprestimo) -> None:
        self._emprestimos.append(emprestimo)

    def registrar_devolucao(self, emprestimo: Emprestimo) -> None:
        for emp in self._emprestimos:
            if emp.id == emprestimo.id:
                emp.devolver()
                return
        raise ValueError("Empréstimo não encontrado nos registros da biblioteca.")
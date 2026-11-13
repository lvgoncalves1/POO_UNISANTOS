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

    def buscar_usuario(self, usuario_id: UUID) -> Usuario | None:
        for usuario in self._usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def listar_usuarios(self) -> list[Usuario]:
        return list(self._usuarios)

    def remover_usuario(self, usuario: Usuario) -> None:
        for emp in self._emprestimos:
            if emp.usuario is usuario and emp.data_devolucao is None:
                raise ValueError("Não é possível excluir um usuário com empréstimo pendente.")
        self._usuarios.remove(usuario)

    def buscar_livro(self, isbn: str) -> Livro | None:
        for estante in self._estantes:
            livro = estante.obter_livro(isbn)
            if livro is not None:
                return livro

        return None

    def listar_livros(self) -> list[Livro]:
        return [livro for estante in self._estantes for livro in estante.listar_livros()]

    def remover_livro(self, livro: Livro) -> None:
        if not livro.disponivel:
            raise ValueError("Não é possível excluir um livro que está emprestado no momento.")
        for estante in self._estantes:
            if livro in estante.listar_livros():
                estante.remover_livro(livro)
                return
        raise ValueError("Livro não encontrado.")

    def buscar_estante(self, codigo_estante: str) -> Estante | None:
        for estante in self._estantes:
            if estante.codigo_estante == codigo_estante:
                return estante
        return None

    def listar_estantes(self) -> list[Estante]:
        return list(self._estantes)

    def listar_emprestimos(self) -> list[Emprestimo]:
        return list(self._emprestimos)

    def registrar_emprestimo(self, emprestimo: Emprestimo) -> None:
        self._emprestimos.append(emprestimo)

    def registrar_devolucao(self, emprestimo: Emprestimo) -> None:
        for emp in self._emprestimos:
            if emp.id == emprestimo.id:
                emp.devolver()
                return
        raise ValueError("Empréstimo não encontrado nos registros da biblioteca.")
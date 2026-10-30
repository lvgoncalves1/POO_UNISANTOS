from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Bibliotecario, Emprestimo, Estante, Livro, Usuario


class BibliotecaService:

    def __init__(self, bibliotecario: Bibliotecario) -> None:
        self._bibliotecario: Bibliotecario = bibliotecario

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        self._bibliotecario.biblioteca.adicionar_usuario(usuario)

    def cadastrar_livro(self, estante: Estante, livro: Livro) -> None:
        self._bibliotecario.cadastrar_livro(estante, livro)

    def buscar_livro(self, isbn: str) -> Livro | None:
        return self._bibliotecario.biblioteca.buscar_livro(isbn)

    def emprestar(self, usuario: Usuario, isbn: str) -> Emprestimo | None:
        livro = self.buscar_livro(isbn)
        if livro is None:
            print(f"Livro com ISBN '{isbn}' não encontrado.")
            return None
        return usuario.solicitar_emprestimo(self._bibliotecario, livro)

    def devolver(self, emprestimo: Emprestimo) -> None:
        self._bibliotecario.registrar_devolucao(emprestimo)

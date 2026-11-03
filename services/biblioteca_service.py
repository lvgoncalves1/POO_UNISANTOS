from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Bibliotecario, Emprestimo, Estante, Livro, Usuario


class BibliotecaService:
    def __init__(self, bibliotecario: Bibliotecario, estante_padrao: Estante) -> None:
        self._bibliotecario: Bibliotecario = bibliotecario
        self.estante_padrao: Estante = estante_padrao

    @property
    def nome_biblioteca(self) -> str:
        return self._bibliotecario.biblioteca.nome

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        self._bibliotecario.biblioteca.adicionar_usuario(usuario)

    def cadastrar_livro(self, livro: Livro) -> None:
        self._bibliotecario.cadastrar_livro(self.estante_padrao, livro)

    def listar_livros(self) -> list[Livro]:
        return self.estante_padrao.listar_livros()

    def listar_usuarios(self) -> list[Usuario]:
        return self._bibliotecario.biblioteca._usuarios

    def listar_emprestimos(self) -> list[Emprestimo]:
        return self._bibliotecario.biblioteca._emprestimos

    def buscar_livro(self, isbn: str) -> Livro | None:
        return self._bibliotecario.biblioteca.buscar_livro(isbn)

    def realizar_emprestimo(self, nome_usuario: str, isbn: str) -> Emprestimo | None:
        livro = self.buscar_livro(isbn)
        usuario = next((u for u in self.listar_usuarios() if u.nome == nome_usuario), None)
        if not usuario or not livro:
            raise ValueError("Usuário ou Livro não encontrado.")
        return usuario.solicitar_emprestimo(self._bibliotecario, livro)

    def devolver_livro(self, isbn: str) -> None:
        for emp in self.listar_emprestimos():
            if emp.livro.isbn == isbn and emp.data_devolucao is None:
                self._bibliotecario.registrar_devolucao(emp)
                return
        raise ValueError("Nenhum empréstimo pendente para este ISBN.")

    def buscar_livros_por_titulo(self, termo: str) -> list[Livro]:
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            return self.listar_livros()
        return [
            livro for livro in self.listar_livros()
            if termo_limpo in livro.titulo.lower()
        ]
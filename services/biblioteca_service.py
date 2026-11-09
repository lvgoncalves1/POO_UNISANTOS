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

    def buscar_livros_por_titulo(self, termo: str) -> list[Livro]:
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            return self.listar_livros()
        return [
            livro for livro in self.listar_livros()
            if termo_limpo in livro.titulo.lower()
        ]

    def listar_usuarios(self) -> list[Usuario]:
        return self._bibliotecario.biblioteca._usuarios

    def listar_emprestimos(self) -> list[Emprestimo]:
        return self._bibliotecario.biblioteca._emprestimos

    def buscar_livro(self, isbn: str) -> Livro | None:
        return self._bibliotecario.biblioteca.buscar_livro(isbn)

    def atualizar_livro(self, isbn: str, novo_titulo: str, novo_autor: str) -> None:
        livro = self.buscar_livro(isbn)
        livro.titulo = novo_titulo.strip()
        livro.autor = novo_autor.strip()

    def remover_livro(self, isbn: str) -> None:
        livro = self.buscar_livro(isbn)
        if not livro.disponivel:
            raise ValueError("Não é possível excluir um livro que está emprestado no momento.")
        self.estante_padrao.livros.remove(livro)

    def buscar_usuario_por_id(self, usuario_id: str) -> Usuario:
        for u in self.listar_usuarios():
            if str(u._id) == str(usuario_id):
                return u
        raise ValueError("Usuário não encontrado.")

    def atualizar_usuario(self, usuario_id: str, novo_nome: str, novo_email: str) -> None:
        usuario = self.buscar_usuario_por_id(usuario_id)
        usuario.nome = novo_nome.strip()
        usuario.email = novo_email.strip()

    def remover_usuario(self, usuario_id: str) -> None:
        usuario = self.buscar_usuario_por_id(usuario_id)
        for emp in self.listar_emprestimos():
            if emp.usuario == usuario and emp.data_devolucao is None:
                raise ValueError("Não é possível excluir um usuário com empréstimo pendente.")
        self._bibliotecario.biblioteca._usuarios.remove(usuario)

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
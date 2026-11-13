from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID

from models import Estante

if TYPE_CHECKING:
    from models import Biblioteca, Bibliotecario, Emprestimo, Livro, Usuario
    from repositories import EmprestimoRepository, LivroRepository, UsuarioRepository


class BibliotecaService:
    def __init__(
        self,
        bibliotecario: Bibliotecario,
        estante_padrao: Estante,
        repositorio_livros: LivroRepository,
        repositorio_usuarios: UsuarioRepository,
        repositorio_emprestimos: EmprestimoRepository,
    ) -> None:
        self._bibliotecario: Bibliotecario = bibliotecario
        self.estante_padrao: Estante = estante_padrao
        self._repositorio_livros: LivroRepository = repositorio_livros
        self._repositorio_usuarios: UsuarioRepository = repositorio_usuarios
        self._repositorio_emprestimos: EmprestimoRepository = repositorio_emprestimos

    @property
    def _biblioteca(self) -> Biblioteca:
        return self._bibliotecario.biblioteca

    @property
    def nome_biblioteca(self) -> str:
        return self._biblioteca.nome

    def carregar_dados(self) -> None:
        for codigo_estante, livro in self._repositorio_livros.listar_todos():
            estante = self._biblioteca.buscar_estante(codigo_estante) or Estante(codigo_estante)
            self._bibliotecario.cadastrar_livro(estante, livro)

        for usuario in self._repositorio_usuarios.listar_todos():
            self._biblioteca.adicionar_usuario(usuario)

        usuarios = {usuario.id: usuario for usuario in self.listar_usuarios()}
        livros = {livro.isbn: livro for livro in self.listar_livros()}
        for emprestimo in self._repositorio_emprestimos.listar_todos(usuarios, livros):
            self._biblioteca.registrar_emprestimo(emprestimo)

    def cadastrar_usuario(self, usuario: Usuario) -> None:
        self._biblioteca.adicionar_usuario(usuario)
        self._repositorio_usuarios.adicionar(usuario)

    def cadastrar_livro(self, livro: Livro) -> None:
        self._bibliotecario.cadastrar_livro(self.estante_padrao, livro)
        self._repositorio_livros.adicionar(livro, self.estante_padrao.codigo_estante)

    def listar_livros(self) -> list[Livro]:
        return self._biblioteca.listar_livros()

    def buscar_livros_por_titulo(self, termo: str) -> list[Livro]:
        termo_limpo = termo.strip().lower()
        if not termo_limpo:
            return self.listar_livros()
        return [
            livro for livro in self.listar_livros()
            if termo_limpo in livro.titulo.lower()
        ]

    def listar_usuarios(self) -> list[Usuario]:
        return self._biblioteca.listar_usuarios()

    def listar_emprestimos(self) -> list[Emprestimo]:
        return self._biblioteca.listar_emprestimos()

    def buscar_livro(self, isbn: str) -> Livro | None:
        return self._biblioteca.buscar_livro(isbn)

    def obter_livro(self, isbn: str) -> Livro:
        livro = self.buscar_livro(isbn)
        if livro is None:
            raise ValueError("Livro não encontrado.")
        return livro

    def atualizar_livro(self, isbn: str, novo_titulo: str, novo_autor: str) -> None:
        livro = self.obter_livro(isbn)
        livro.titulo = novo_titulo
        livro.autor = novo_autor
        self._repositorio_livros.atualizar(livro)

    def remover_livro(self, isbn: str) -> None:
        livro = self.obter_livro(isbn)
        self._biblioteca.remover_livro(livro)
        self._repositorio_livros.remover(livro)

    def buscar_usuario_por_id(self, usuario_id: str) -> Usuario:
        try:
            usuario = self._biblioteca.buscar_usuario(UUID(usuario_id))
        except ValueError:
            usuario = None
        if usuario is None:
            raise ValueError("Usuário não encontrado.")
        return usuario

    def atualizar_usuario(self, usuario_id: str, novo_nome: str, novo_email: str) -> None:
        usuario = self.buscar_usuario_por_id(usuario_id)
        usuario.nome = novo_nome
        usuario.email = novo_email
        self._repositorio_usuarios.atualizar(usuario)

    def remover_usuario(self, usuario_id: str) -> None:
        usuario = self.buscar_usuario_por_id(usuario_id)
        self._biblioteca.remover_usuario(usuario)
        self._repositorio_usuarios.remover(usuario)

    def realizar_emprestimo(self, usuario_id: str, isbn: str) -> Emprestimo | None:
        usuario = self.buscar_usuario_por_id(usuario_id)
        livro = self.obter_livro(isbn)
        emprestimo = usuario.solicitar_emprestimo(self._bibliotecario, livro)
        if emprestimo is not None:
            self._repositorio_emprestimos.adicionar(emprestimo)
        return emprestimo

    def devolver_livro(self, isbn: str) -> None:
        for emp in self.listar_emprestimos():
            if emp.livro.isbn == isbn and emp.data_devolucao is None:
                self._bibliotecario.registrar_devolucao(emp)
                self._repositorio_emprestimos.atualizar(emp)
                return
        raise ValueError("Nenhum empréstimo pendente para este ISBN.")

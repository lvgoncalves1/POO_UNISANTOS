from abc import ABC, abstractmethod

from models import Livro

from .banco_sqlite import BancoSQLite


class LivroRepository(ABC):
    @abstractmethod
    def adicionar(self, livro: Livro, codigo_estante: str) -> None:
        pass

    @abstractmethod
    def atualizar(self, livro: Livro) -> None:
        pass

    @abstractmethod
    def remover(self, livro: Livro) -> None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[tuple[str, Livro]]:
        """Retorna pares (código da estante, livro)."""


class SQLiteLivroRepository(LivroRepository):
    def __init__(self, banco: BancoSQLite) -> None:
        self._conexao = banco.conexao

    def adicionar(self, livro: Livro, codigo_estante: str) -> None:
        with self._conexao:
            self._conexao.execute(
                "INSERT INTO livros (isbn, titulo, autor, codigo_estante) VALUES (?, ?, ?, ?)",
                (livro.isbn, livro.titulo, livro.autor, codigo_estante),
            )

    def atualizar(self, livro: Livro) -> None:
        with self._conexao:
            self._conexao.execute(
                "UPDATE livros SET titulo = ?, autor = ? WHERE isbn = ?",
                (livro.titulo, livro.autor, livro.isbn),
            )

    def remover(self, livro: Livro) -> None:
        with self._conexao:
            self._conexao.execute("DELETE FROM livros WHERE isbn = ?", (livro.isbn,))

    def listar_todos(self) -> list[tuple[str, Livro]]:
        linhas = self._conexao.execute(
            """
            SELECT l.isbn, l.titulo, l.autor, l.codigo_estante,
                   NOT EXISTS (
                       SELECT 1 FROM emprestimos e
                       WHERE e.livro_isbn = l.isbn AND e.data_devolucao IS NULL
                   ) AS disponivel
            FROM livros l
            ORDER BY l.rowid
            """
        ).fetchall()
        return [
            (
                linha["codigo_estante"],
                Livro(linha["isbn"], linha["titulo"], linha["autor"], bool(linha["disponivel"])),
            )
            for linha in linhas
        ]

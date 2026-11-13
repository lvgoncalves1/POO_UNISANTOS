from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from models import Emprestimo, Livro, Usuario

from .banco_sqlite import BancoSQLite


class EmprestimoRepository(ABC):
    @abstractmethod
    def adicionar(self, emprestimo: Emprestimo) -> None:
        pass

    @abstractmethod
    def atualizar(self, emprestimo: Emprestimo) -> None:
        pass

    @abstractmethod
    def listar_todos(
        self, usuarios: dict[UUID, Usuario], livros: dict[str, Livro]
    ) -> list[Emprestimo]:
        """Recria os empréstimos ligando-os aos usuários e livros já carregados."""


class SQLiteEmprestimoRepository(EmprestimoRepository):
    def __init__(self, banco: BancoSQLite) -> None:
        self._conexao = banco.conexao

    def adicionar(self, emprestimo: Emprestimo) -> None:
        with self._conexao:
            self._conexao.execute(
                "INSERT INTO emprestimos "
                "(id, usuario_id, livro_isbn, data_inicio, data_prevista, data_devolucao) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (
                    str(emprestimo.id),
                    str(emprestimo.usuario.id),
                    emprestimo.livro.isbn,
                    emprestimo.data_inicio.isoformat(),
                    emprestimo.data_prevista.isoformat(),
                    _data_ou_none(emprestimo.data_devolucao),
                ),
            )

    def atualizar(self, emprestimo: Emprestimo) -> None:
        with self._conexao:
            self._conexao.execute(
                "UPDATE emprestimos SET data_devolucao = ? WHERE id = ?",
                (_data_ou_none(emprestimo.data_devolucao), str(emprestimo.id)),
            )

    def listar_todos(
        self, usuarios: dict[UUID, Usuario], livros: dict[str, Livro]
    ) -> list[Emprestimo]:
        linhas = self._conexao.execute("SELECT * FROM emprestimos ORDER BY rowid").fetchall()
        return [
            Emprestimo(
                UUID(linha["id"]),
                usuarios[UUID(linha["usuario_id"])],
                livros[linha["livro_isbn"]],
                date.fromisoformat(linha["data_inicio"]),
                date.fromisoformat(linha["data_prevista"]),
                date.fromisoformat(linha["data_devolucao"]) if linha["data_devolucao"] else None,
            )
            for linha in linhas
        ]


def _data_ou_none(data: date | None) -> str | None:
    return data.isoformat() if data else None

import sqlite3
from abc import ABC, abstractmethod
from uuid import UUID

from models import Aluno, Professor, Usuario, Visitante

from .banco_sqlite import BancoSQLite


class UsuarioRepository(ABC):
    @abstractmethod
    def adicionar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def atualizar(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def remover(self, usuario: Usuario) -> None:
        pass

    @abstractmethod
    def listar_todos(self) -> list[Usuario]:
        pass


class SQLiteUsuarioRepository(UsuarioRepository):
    def __init__(self, banco: BancoSQLite) -> None:
        self._conexao = banco.conexao

    def adicionar(self, usuario: Usuario) -> None:
        colunas = self._para_colunas(usuario)
        with self._conexao:
            self._conexao.execute(
                f"INSERT INTO usuarios ({', '.join(colunas)}) "
                f"VALUES ({', '.join('?' for _ in colunas)})",
                tuple(colunas.values()),
            )

    def atualizar(self, usuario: Usuario) -> None:
        with self._conexao:
            self._conexao.execute(
                "UPDATE usuarios SET nome = ?, email = ? WHERE id = ?",
                (usuario.nome, usuario.email, str(usuario.id)),
            )

    def remover(self, usuario: Usuario) -> None:
        with self._conexao:
            self._conexao.execute("DELETE FROM usuarios WHERE id = ?", (str(usuario.id),))

    def listar_todos(self) -> list[Usuario]:
        linhas = self._conexao.execute("SELECT * FROM usuarios ORDER BY rowid").fetchall()
        return [self._criar_usuario(linha) for linha in linhas]

    def _para_colunas(self, usuario: Usuario) -> dict[str, str]:
        colunas = {"id": str(usuario.id), "nome": usuario.nome, "email": usuario.email}
        if isinstance(usuario, Aluno):
            colunas.update(tipo="aluno", matricula=usuario.matricula)
        elif isinstance(usuario, Professor):
            colunas.update(
                tipo="professor",
                registro_funcional=usuario.registro_funcional,
                departamento=usuario.departamento,
            )
        elif isinstance(usuario, Visitante):
            colunas.update(tipo="visitante", cpf=usuario.cpf)
        else:
            raise ValueError(f"Tipo de usuário não suportado: {type(usuario).__name__}")
        return colunas

    def _criar_usuario(self, linha: sqlite3.Row) -> Usuario:
        id, nome, email = UUID(linha["id"]), linha["nome"], linha["email"]
        if linha["tipo"] == "aluno":
            return Aluno(id, nome, email, linha["matricula"])
        if linha["tipo"] == "professor":
            return Professor(id, nome, email, linha["registro_funcional"], linha["departamento"])
        return Visitante(id, nome, email, linha["cpf"])

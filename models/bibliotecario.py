from __future__ import annotations
from typing import TYPE_CHECKING
from uuid import UUID, uuid4
from datetime import date, timedelta

from .emprestimo import Emprestimo
from .pessoa import Pessoa

if TYPE_CHECKING:
    from .biblioteca import Biblioteca
    from .estante import Estante
    from .livro import Livro
    from .usuario import Usuario


class Bibliotecario(Pessoa):
    def __init__(self, id: UUID, nome: str, email: str, registro: str, biblioteca: Biblioteca) -> None:
        super().__init__(id, nome, email)
        self._registro: str = registro
        self.biblioteca: Biblioteca = biblioteca

    def cadastrar_livro(self, estante: Estante, livro: Livro) -> None:
        if estante not in self.biblioteca.listar_estantes():
            self.biblioteca.adicionar_estante(estante)

        estante.adicionar_livro(livro)

    def realizar_emprestimo(self, usuario: Usuario, livro: Livro) -> Emprestimo:
        livro.emprestar()
        data_hoje = date.today()
        prevista = data_hoje + timedelta(days=usuario.obter_prazo_emprestimo())
        novo_emprestimo = Emprestimo(uuid4(), usuario, livro, data_hoje, prevista)
        self.biblioteca.registrar_emprestimo(novo_emprestimo)
        return novo_emprestimo

    def registrar_devolucao(self, emprestimo: Emprestimo) -> None:
        self.biblioteca.registrar_devolucao(emprestimo)

    @property
    def registro(self) -> str:
        return self._registro
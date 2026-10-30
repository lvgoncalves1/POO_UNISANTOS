from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID

from utils import formatar_data_br

if TYPE_CHECKING:
    from .usuario import Usuario
    from .livro import Livro


class Emprestimo:
    def __init__(
        self,
        id: UUID,
        usuario: Usuario,
        livro: Livro,
        data_inicio: date,
        data_prevista: date,
        data_devolucao: date | None = None,
    ) -> None:
        self._id: UUID = id
        self.usuario: Usuario = usuario
        self.livro: Livro = livro
        self.data_inicio: date = data_inicio
        self.data_prevista: date = data_prevista
        self.data_devolucao: date | None = data_devolucao

    def devolver(self) -> None:
        if self.data_devolucao is not None:
            raise ValueError("Empréstimo já foi devolvido")

        self.data_devolucao = date.today()
        self.livro.devolver()

    def verificar_atraso(self) -> bool:
        data_referencia = self.data_devolucao or date.today()
        
        if data_referencia > self.data_prevista:
            dias = (data_referencia - self.data_prevista).days
            print(f"Livro '{self.livro.titulo}' está atrasado em {dias} dia(s)")
            return True
        return False

    @property
    def id(self) -> UUID:
        return self._id

    def __repr__(self) -> str:
        inicio_br = formatar_data_br(self.data_inicio)
        prevista_br = formatar_data_br(self.data_prevista)
        devolucao_br = (
            formatar_data_br(self.data_devolucao)
            if self.data_devolucao
            else "Pendente"
        )
        return (
            f"Empréstimo [Livro: {self.livro.titulo} | Usuário: {self.usuario.nome} | "
            f"Início: {inicio_br} | Prevista: {prevista_br} | Devolução: {devolucao_br}]"
        )

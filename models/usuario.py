from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

from .pessoa import Pessoa

if TYPE_CHECKING:
    from .bibliotecario import Bibliotecario
    from .livro import Livro
    from .emprestimo import Emprestimo


class Usuario(Pessoa, ABC):
    def __init__(self, id: UUID, nome: str, email: str) -> None:
        super().__init__(id, nome, email)

    def solicitar_emprestimo(self, bibliotecario: Bibliotecario, livro: Livro) -> Emprestimo | None:
        try:
            return bibliotecario.realizar_emprestimo(self, livro)
        except ValueError as e:
            print(f"Erro ao emprestar '{livro.titulo}': {e}")
            return None

    @abstractmethod
    def obter_prazo_emprestimo(self) -> int:
        pass
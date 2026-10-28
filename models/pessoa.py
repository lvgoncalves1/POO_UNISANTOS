from abc import ABC
from uuid import UUID


class Pessoa(ABC):
    def __init__(self, id: UUID, nome: str, email: str) -> None:
        self._id: UUID = id
        self.nome: str = nome
        self.email: str = email
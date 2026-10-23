from abc import ABC
from uuid import UUID, uuid4


class Pessoa(ABC):
    __id: UUID
    nome: str
    email: str

    def __init__(self, nome: str, email: str) -> None:
        pass
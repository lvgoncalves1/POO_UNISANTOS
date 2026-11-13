from abc import ABC
from uuid import UUID

from utils import validar_texto_obrigatorio


class Pessoa(ABC):
    def __init__(self, id: UUID, nome: str, email: str) -> None:
        self._id: UUID = id
        self.nome = nome
        self.email = email

    @property
    def id(self) -> UUID:
        return self._id

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valor: str) -> None:
        self._nome: str = validar_texto_obrigatorio(valor, "nome")

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str) -> None:
        self._email: str = validar_texto_obrigatorio(valor, "e-mail")

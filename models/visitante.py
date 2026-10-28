from uuid import UUID
from .usuario import Usuario


class Visitante(Usuario):
    def __init__(self, id: UUID, nome: str, email: str, cpf: str) -> None:
        super().__init__(id, nome, email)
        self._cpf: str = cpf

    def obter_prazo_emprestimo(self) -> int:
        return 3
from uuid import UUID
from .usuario import Usuario


class Aluno(Usuario):
    def __init__(self, id: UUID, nome: str, email: str, matricula: str) -> None:
        super().__init__(id, nome, email)
        self._matricula: str = matricula

    def obter_prazo_emprestimo(self) -> int:
        return 7
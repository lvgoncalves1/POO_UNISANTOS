from uuid import UUID
from .usuario import Usuario


class Professor(Usuario):
    def __init__(self, id: UUID, nome: str, email: str, registro_funcional: str, departamento: str) -> None:
        super().__init__(id, nome, email)
        self._registro_funcional: str = registro_funcional
        self.departamento: str = departamento

    def obter_prazo_emprestimo(self) -> int:
        return 30
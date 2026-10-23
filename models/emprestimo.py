from datetime import date, timedelta
from uuid import UUID, uuid4
from .aluno import Aluno
from .livro import Livro


class Emprestimo:
    __id: UUID
    aluno: Aluno
    livro: Livro
    data_inicio: date
    data_prevista: date
    data_devolucao: date | None

    def __init__(self, aluno: Aluno, livro: Livro) -> None:
        pass

    def devolver(self) -> None:
        pass

    def verificar_atraso(self) -> bool:
        pass
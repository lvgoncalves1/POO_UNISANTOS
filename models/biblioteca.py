from uuid import UUID, uuid4
from .aluno import Aluno
from .emprestimo import Emprestimo
from .estante import Estante
from .livro import Livro


class Biblioteca:
    __id: UUID
    nome: str
    __alunos: list[Aluno]
    __estantes: list[Estante]
    __emprestimos: list[Emprestimo]

    def __init__(self, nome: str) -> None:
        pass

    def adicionar_aluno(self, aluno: Aluno) -> None:
        pass

    def buscar_livro(self, isbn: str) -> Livro:
        pass

    def registrar_emprestimo(self, emprestimo: Emprestimo) -> None:
        pass

    def registrar_devolucao(self, emprestimo: Emprestimo) -> None:
        pass
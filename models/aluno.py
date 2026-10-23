from typing import TYPE_CHECKING
from .pessoa import Pessoa
from .livro import Livro

if TYPE_CHECKING:
    from .bibliotecario import Bibliotecario
    from .emprestimo import Emprestimo


class Aluno(Pessoa):
    __matricula: str

    def __init__(self, nome: str, email: str, matricula: str) -> None:
        super().__init__(nome, email)
        self.__matricula = matricula

    def solicitar_emprestimo(
        self, bibliotecario: "Bibliotecario", livro: Livro
    ) -> "Emprestimo | None":
        pass
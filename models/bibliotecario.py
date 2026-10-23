from typing import TYPE_CHECKING
from .pessoa import Pessoa
from .emprestimo import Emprestimo
from .estante import Estante
from .livro import Livro

if TYPE_CHECKING:
    from .aluno import Aluno
    from .biblioteca import Biblioteca


class Bibliotecario(Pessoa):
    __registro: str
    biblioteca: "Biblioteca"

    def __init__(
        self, nome: str, email: str, registro: str, biblioteca: "Biblioteca"
    ) -> None:
        pass

    def cadastrar_livro(self, estante: Estante, livro: Livro) -> None:
        pass

    def realizar_emprestimo(
        self, aluno: "Aluno", livro: Livro
    ) -> Emprestimo | None:
        pass

    def registrar_devolucao(self, emprestimo: Emprestimo) -> None:
        pass
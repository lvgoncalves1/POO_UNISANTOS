class Livro:
    __isbn: str
    titulo: str
    autor: str
    __disponivel: bool

    def __init__(self, isbn: str, titulo: str, autor: str) -> None:
        pass

    @property
    def isbn(self) -> str:
        pass

    def verificar_disponibilidade(self) -> bool:
        pass

    def emprestar(self) -> None:
        pass

    def devolver(self) -> None:
        pass
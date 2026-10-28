class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, disponivel: bool = True) -> None:
        self._isbn: str = isbn
        self.titulo: str = titulo
        self.autor: str = autor
        self._disponivel: bool = disponivel

    def emprestar(self) -> None:
        if self._disponivel:
            self._disponivel = False
        else:
            raise ValueError("Livro já emprestado")

    def devolver(self) -> None:
        if not self._disponivel:
            self._disponivel = True
        else:
            raise ValueError("Livro não foi emprestado")

    @property
    def isbn(self) -> str:
        return self._isbn

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def __repr__(self) -> str:
        status = "Disponível" if self._disponivel else "Emprestado"
        return f"Livro(isbn='{self._isbn}', titulo='{self.titulo}', status='{status}')"
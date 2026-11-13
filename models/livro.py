from utils import validar_texto_obrigatorio


class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, disponivel: bool = True) -> None:
        self._isbn: str = validar_texto_obrigatorio(isbn, "ISBN")
        self.titulo = titulo
        self.autor = autor
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
    def titulo(self) -> str:
        return self._titulo

    @titulo.setter
    def titulo(self, valor: str) -> None:
        self._titulo: str = validar_texto_obrigatorio(valor, "título")

    @property
    def autor(self) -> str:
        return self._autor

    @autor.setter
    def autor(self, valor: str) -> None:
        self._autor: str = validar_texto_obrigatorio(valor, "autor")

    @property
    def disponivel(self) -> bool:
        return self._disponivel

    def __repr__(self) -> str:
        status = "Disponível" if self._disponivel else "Emprestado"
        return f"Livro(isbn='{self._isbn}', titulo='{self.titulo}', status='{status}')"

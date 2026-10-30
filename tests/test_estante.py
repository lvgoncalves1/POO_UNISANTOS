from models import Livro


def test_fluxo_estante_e_livro(estante):
    livro = Livro(isbn="978-85", titulo="Engenharia de Software", autor="Pressman")

    estante.adicionar_livro(livro)

    assert len(estante.listar_livros()) == 1
    assert estante.obter_livro("978-85").titulo == "Engenharia de Software"


def test_estante_comeca_vazia(estante):
    assert estante.listar_livros() == []


def test_obter_livro_inexistente_retorna_none(estante, livro):
    estante.adicionar_livro(livro)
    assert estante.obter_livro("nao-existe") is None


def test_obter_livro_entre_varios(estante):
    livros = [Livro(str(i), f"Livro {i}", "Autor") for i in range(3)]
    for livro in livros:
        estante.adicionar_livro(livro)

    assert estante.obter_livro("2") is livros[2]

from uuid import uuid4
from models import Aluno, Biblioteca, Bibliotecario, Estante, Livro


def test_criacao_entidades_e_heranca():
    biblioteca = Biblioteca(id=uuid4(), nome="Biblioteca Central")
    aluno = Aluno(
        id=uuid4(),
        nome="Lucas",
        email="lucas@unisantos.br",
        matricula="7047031",
    )
    bib = Bibliotecario(
        id=uuid4(),
        nome="Carlos",
        email="carlos@bib.br",
        registro="REG-01",
        biblioteca=biblioteca,
    )

    assert aluno.nome == "Lucas"
    assert bib.nome == "Carlos"


def test_fluxo_estante_e_livro():
    estante = Estante(codigo_estante="EST-A1")
    livro = Livro(
        isbn="978-85", titulo="Engenharia de Software", autor="Pressman"
    )

    estante.adicionar_livro(livro)

    assert len(estante.listar_livros()) == 1
    assert estante.obter_livro("978-85").titulo == "Engenharia de Software"


def test_cadastro_e_busca_na_biblioteca():
    biblioteca = Biblioteca(id=uuid4(), nome="Biblioteca Central")
    aluno = Aluno(
        id=uuid4(), nome="Leonardo", email="leo@email.com", matricula="111222"
    )
    estante = Estante(codigo_estante="EST-B2")
    livro = Livro(isbn="123-456", titulo="Sistemas Digitais", autor="Tocci")

    biblioteca.adicionar_usuario(aluno)
    bibliotecario = Bibliotecario(
        id=uuid4(),
        nome="Ana",
        email="ana@bib.br",
        registro="REG-02",
        biblioteca=biblioteca,
    )
    bibliotecario.cadastrar_livro(estante, livro)

    livro_encontrado = biblioteca.buscar_livro("123-456")
    assert livro_encontrado is not None
    assert livro_encontrado.titulo == "Sistemas Digitais"
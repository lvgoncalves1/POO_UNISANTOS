import pytest

from models import Livro


def test_livro_comeca_disponivel(livro):
    assert livro.disponivel is True


def test_emprestar_livro_fica_indisponivel(livro):
    livro.emprestar()
    assert livro.disponivel is False


def test_emprestar_livro_ja_emprestado_gera_erro(livro):
    livro.emprestar()
    with pytest.raises(ValueError, match="Livro já emprestado"):
        livro.emprestar()


def test_devolver_livro_emprestado_fica_disponivel(livro):
    livro.emprestar()
    livro.devolver()
    assert livro.disponivel is True


def test_devolver_livro_nao_emprestado_gera_erro(livro):
    with pytest.raises(ValueError, match="Livro não foi emprestado"):
        livro.devolver()


def test_isbn_e_disponivel_sao_somente_leitura(livro):
    with pytest.raises(AttributeError):
        livro.isbn = "000"
    with pytest.raises(AttributeError):
        livro.disponivel = False


def test_repr_mostra_status(livro):
    assert "Disponível" in repr(livro)
    livro.emprestar()
    assert "Emprestado" in repr(livro)


@pytest.mark.parametrize("campo", ["isbn", "titulo", "autor"])
def test_livro_nao_aceita_campo_vazio(campo):
    dados = {"isbn": "1", "titulo": "Título", "autor": "Autor", campo: "   "}
    with pytest.raises(ValueError, match="obrigatório"):
        Livro(**dados)


def test_livro_remove_espacos_extras():
    livro = Livro("  1  ", "  Título  ", "  Autor  ")
    assert (livro.isbn, livro.titulo, livro.autor) == ("1", "Título", "Autor")


def test_atualizar_titulo_vazio_gera_erro_e_mantem_valor(livro):
    with pytest.raises(ValueError, match="obrigatório"):
        livro.titulo = "   "
    assert livro.titulo == "Sistemas Digitais"

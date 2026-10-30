import pytest


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

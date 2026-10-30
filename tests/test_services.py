import pytest

from services import BibliotecaService


@pytest.fixture
def service(bibliotecario):
    return BibliotecaService(bibliotecario)


def test_service_fluxo_completo(service, biblioteca, estante, livro, aluno):
    service.cadastrar_usuario(aluno)
    service.cadastrar_livro(estante, livro)

    emprestimo = service.emprestar(aluno, "123-456")
    assert emprestimo is not None
    assert livro.disponivel is False

    service.devolver(emprestimo)
    assert livro.disponivel is True
    assert aluno in biblioteca._usuarios


def test_service_emprestar_isbn_inexistente_retorna_none(service, aluno, capsys):
    assert service.emprestar(aluno, "nao-existe") is None
    assert "não encontrado" in capsys.readouterr().out

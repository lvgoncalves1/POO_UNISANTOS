from uuid import uuid4

import pytest

from models import Livro, Visitante
from services import BibliotecaService


@pytest.fixture
def service(
    bibliotecario,
    estante,
    livro,
    aluno,
    repositorio_livros,
    repositorio_usuarios,
    repositorio_emprestimos,
):
    service = BibliotecaService(
        bibliotecario, estante, repositorio_livros, repositorio_usuarios, repositorio_emprestimos
    )
    service.cadastrar_livro(livro)
    service.cadastrar_usuario(aluno)
    return service


def test_cadastrar_e_listar_livros(service):
    service.cadastrar_livro(Livro("999", "Refactoring", "Fowler"))

    assert [l.isbn for l in service.listar_livros()] == ["123-456", "999"]


def test_buscar_livros_por_titulo_ignora_maiusculas(service):
    assert [l.isbn for l in service.buscar_livros_por_titulo("  SISTEMAS ")] == ["123-456"]
    assert service.buscar_livros_por_titulo("inexistente") == []
    assert len(service.buscar_livros_por_titulo("")) == 1


def test_atualizar_livro(service, livro):
    service.atualizar_livro("123-456", "Sistemas Digitais 2", "Tocci e Widmer")

    assert (livro.titulo, livro.autor) == ("Sistemas Digitais 2", "Tocci e Widmer")


@pytest.mark.parametrize(
    "operacao",
    [
        lambda s: s.atualizar_livro("nao-existe", "T", "A"),
        lambda s: s.remover_livro("nao-existe"),
        lambda s: s.obter_livro("nao-existe"),
    ],
)
def test_operacoes_com_livro_inexistente_geram_erro(service, operacao):
    with pytest.raises(ValueError, match="Livro não encontrado"):
        operacao(service)


def test_remover_livro(service):
    service.remover_livro("123-456")

    assert service.listar_livros() == []


@pytest.mark.parametrize("usuario_id", ["abc", "", str(uuid4())])
def test_buscar_usuario_com_id_invalido_ou_inexistente(service, usuario_id):
    with pytest.raises(ValueError, match="Usuário não encontrado"):
        service.buscar_usuario_por_id(usuario_id)


def test_atualizar_e_remover_usuario(service, aluno):
    service.atualizar_usuario(str(aluno.id), "Lucas Silva", "lucas.silva@unisantos.br")
    assert (aluno.nome, aluno.email) == ("Lucas Silva", "lucas.silva@unisantos.br")

    service.remover_usuario(str(aluno.id))
    assert service.listar_usuarios() == []


def test_emprestimo_usa_id_e_nao_nome(service, aluno):
    xara = Visitante(uuid4(), aluno.nome, "outro@email.com", "000.000.000-00")
    service.cadastrar_usuario(xara)

    emprestimo = service.realizar_emprestimo(str(xara.id), "123-456")

    assert emprestimo.usuario is xara


def test_emprestar_e_devolver_por_isbn(service, aluno, livro):
    service.realizar_emprestimo(str(aluno.id), "123-456")
    assert livro.disponivel is False

    service.devolver_livro("123-456")
    assert livro.disponivel is True

    with pytest.raises(ValueError, match="Nenhum empréstimo pendente"):
        service.devolver_livro("123-456")

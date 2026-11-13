from datetime import date
from uuid import uuid4

import pytest

from models import Emprestimo, Estante, Livro


def test_cadastro_e_busca_na_biblioteca(biblioteca, bibliotecario, aluno, estante, livro):
    biblioteca.adicionar_usuario(aluno)
    bibliotecario.cadastrar_livro(estante, livro)

    livro_encontrado = biblioteca.buscar_livro("123-456")
    assert livro_encontrado is not None
    assert livro_encontrado.titulo == "Sistemas Digitais"


def test_buscar_livro_sem_estantes_retorna_none(biblioteca):
    assert biblioteca.buscar_livro("123-456") is None


def test_buscar_livro_inexistente_retorna_none(bibliotecario, biblioteca, estante, livro):
    bibliotecario.cadastrar_livro(estante, livro)
    assert biblioteca.buscar_livro("nao-existe") is None


def test_buscar_livro_em_qualquer_estante(bibliotecario, biblioteca):
    estante_a = Estante("A1")
    estante_b = Estante("B1")
    livro_a = Livro("111", "Arquitetura Limpa", "Robert Martin")
    livro_b = Livro("222", "Padrões de Projeto", "GoF")

    bibliotecario.cadastrar_livro(estante_a, livro_a)
    bibliotecario.cadastrar_livro(estante_b, livro_b)

    assert biblioteca.buscar_livro("111") is livro_a
    assert biblioteca.buscar_livro("222") is livro_b


def test_cadastrar_livro_nao_duplica_estante(bibliotecario, biblioteca, estante):
    bibliotecario.cadastrar_livro(estante, Livro("1", "Livro 1", "Autor"))
    bibliotecario.cadastrar_livro(estante, Livro("2", "Livro 2", "Autor"))

    assert biblioteca.listar_estantes().count(estante) == 1
    assert len(estante.listar_livros()) == 2


def test_registrar_devolucao_de_emprestimo_desconhecido_gera_erro(biblioteca, aluno, livro):
    emprestimo = Emprestimo(uuid4(), aluno, livro, date.today(), date.today())

    with pytest.raises(ValueError, match="Empréstimo não encontrado"):
        biblioteca.registrar_devolucao(emprestimo)


def test_listar_estantes_devolve_copia_e_protege_a_lista_interna(
    bibliotecario, biblioteca, estante, livro
):
    bibliotecario.cadastrar_livro(estante, livro)

    biblioteca.listar_estantes().clear()

    assert biblioteca.listar_estantes() == [estante]


def test_nao_permite_isbn_duplicado(bibliotecario, biblioteca, estante, livro):
    bibliotecario.cadastrar_livro(estante, livro)

    with pytest.raises(ValueError, match="Já existe um livro com o ISBN '123-456'"):
        bibliotecario.cadastrar_livro(Estante("B1"), Livro("123-456", "Outro", "Autor"))

    assert len(biblioteca.listar_livros()) == 1


def test_buscar_usuario_por_id(biblioteca, aluno):
    biblioteca.adicionar_usuario(aluno)

    assert biblioteca.buscar_usuario(aluno.id) is aluno
    assert biblioteca.buscar_usuario(uuid4()) is None


def test_remover_usuario_sem_pendencias(biblioteca, aluno):
    biblioteca.adicionar_usuario(aluno)

    biblioteca.remover_usuario(aluno)

    assert biblioteca.listar_usuarios() == []


def test_nao_remove_usuario_com_emprestimo_pendente(
    biblioteca, bibliotecario, aluno, estante, livro
):
    biblioteca.adicionar_usuario(aluno)
    bibliotecario.cadastrar_livro(estante, livro)
    bibliotecario.realizar_emprestimo(aluno, livro)

    with pytest.raises(ValueError, match="empréstimo pendente"):
        biblioteca.remover_usuario(aluno)

    assert biblioteca.listar_usuarios() == [aluno]


def test_remover_livro_de_qualquer_estante(bibliotecario, biblioteca):
    livro_b = Livro("222", "Padrões de Projeto", "GoF")
    bibliotecario.cadastrar_livro(Estante("A1"), Livro("111", "Arquitetura Limpa", "Martin"))
    bibliotecario.cadastrar_livro(Estante("B1"), livro_b)

    biblioteca.remover_livro(livro_b)

    assert biblioteca.buscar_livro("222") is None
    assert len(biblioteca.listar_livros()) == 1


def test_nao_remove_livro_emprestado(bibliotecario, biblioteca, aluno, estante, livro):
    bibliotecario.cadastrar_livro(estante, livro)
    bibliotecario.realizar_emprestimo(aluno, livro)

    with pytest.raises(ValueError, match="emprestado"):
        biblioteca.remover_livro(livro)

    assert biblioteca.buscar_livro("123-456") is livro


def test_remover_usuario_ou_livro_apaga_historico_de_emprestimos(
    bibliotecario, biblioteca, aluno, professor, estante, livro
):
    outro_livro = Livro("999", "Refactoring", "Fowler")
    biblioteca.adicionar_usuario(aluno)
    biblioteca.adicionar_usuario(professor)
    bibliotecario.cadastrar_livro(estante, livro)
    bibliotecario.cadastrar_livro(estante, outro_livro)
    bibliotecario.registrar_devolucao(bibliotecario.realizar_emprestimo(aluno, livro))
    bibliotecario.registrar_devolucao(bibliotecario.realizar_emprestimo(professor, outro_livro))

    biblioteca.remover_usuario(aluno)
    assert [e.usuario for e in biblioteca.listar_emprestimos()] == [professor]

    biblioteca.remover_livro(outro_livro)
    assert biblioteca.listar_emprestimos() == []


def test_buscar_estante_por_codigo(bibliotecario, biblioteca, estante, livro):
    bibliotecario.cadastrar_livro(estante, livro)

    assert biblioteca.buscar_estante("EST-A1") is estante
    assert biblioteca.buscar_estante("nao-existe") is None


@pytest.mark.parametrize("listar", ["listar_usuarios", "listar_livros", "listar_emprestimos"])
def test_listagens_devolvem_copia(bibliotecario, biblioteca, aluno, estante, livro, listar):
    biblioteca.adicionar_usuario(aluno)
    bibliotecario.cadastrar_livro(estante, livro)
    bibliotecario.realizar_emprestimo(aluno, livro)

    getattr(biblioteca, listar)().clear()

    assert len(getattr(biblioteca, listar)()) == 1

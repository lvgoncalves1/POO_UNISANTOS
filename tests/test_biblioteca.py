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

    assert biblioteca._estantes.count(estante) == 1
    assert len(estante.listar_livros()) == 2


def test_registrar_devolucao_de_emprestimo_desconhecido_gera_erro(biblioteca, aluno, livro):
    emprestimo = Emprestimo(uuid4(), aluno, livro, date.today(), date.today())

    with pytest.raises(ValueError, match="Empréstimo não encontrado"):
        biblioteca.registrar_devolucao(emprestimo)

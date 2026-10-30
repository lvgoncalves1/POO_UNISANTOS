from datetime import date, timedelta
from uuid import uuid4

import pytest

from models import Emprestimo


@pytest.fixture
def livro_cadastrado(bibliotecario, estante, livro):
    bibliotecario.cadastrar_livro(estante, livro)
    return livro


@pytest.mark.parametrize(
    "fixture_usuario, dias", [("aluno", 7), ("professor", 30), ("visitante", 3)]
)
def test_data_prevista_depende_do_tipo_de_usuario(
    request, bibliotecario, livro_cadastrado, fixture_usuario, dias
):
    usuario = request.getfixturevalue(fixture_usuario)

    emprestimo = bibliotecario.realizar_emprestimo(usuario, livro_cadastrado)

    assert emprestimo.data_inicio == date.today()
    assert emprestimo.data_prevista == date.today() + timedelta(days=dias)


def test_realizar_emprestimo_registra_na_biblioteca(
    biblioteca, bibliotecario, aluno, livro_cadastrado
):
    emprestimo = bibliotecario.realizar_emprestimo(aluno, livro_cadastrado)

    assert emprestimo in biblioteca._emprestimos
    assert emprestimo.usuario is aluno
    assert emprestimo.livro is livro_cadastrado
    assert emprestimo.data_devolucao is None
    assert livro_cadastrado.disponivel is False


def test_solicitar_emprestimo_de_livro_indisponivel_retorna_none(
    bibliotecario, aluno, visitante, livro_cadastrado, capsys
):
    aluno.solicitar_emprestimo(bibliotecario, livro_cadastrado)

    resultado = visitante.solicitar_emprestimo(bibliotecario, livro_cadastrado)

    assert resultado is None
    assert "Erro ao emprestar" in capsys.readouterr().out


def test_devolucao_libera_livro_e_registra_data(bibliotecario, aluno, livro_cadastrado):
    emprestimo = aluno.solicitar_emprestimo(bibliotecario, livro_cadastrado)

    bibliotecario.registrar_devolucao(emprestimo)

    assert emprestimo.data_devolucao == date.today()
    assert livro_cadastrado.disponivel is True


def test_emprestimo_nao_pode_ser_devolvido_duas_vezes(aluno, livro):
    livro.emprestar()
    data_original = date.today() - timedelta(days=2)
    emprestimo = Emprestimo(
        uuid4(),
        aluno,
        livro,
        data_inicio=date.today() - timedelta(days=5),
        data_prevista=date.today() + timedelta(days=2),
        data_devolucao=data_original,
    )

    with pytest.raises(ValueError, match="já foi devolvido"):
        emprestimo.devolver()

    assert emprestimo.data_devolucao == data_original


def test_livro_pode_ser_emprestado_de_novo_apos_devolucao(
    bibliotecario, aluno, professor, livro_cadastrado
):
    emprestimo = aluno.solicitar_emprestimo(bibliotecario, livro_cadastrado)
    bibliotecario.registrar_devolucao(emprestimo)

    assert professor.solicitar_emprestimo(bibliotecario, livro_cadastrado) is not None


def test_emprestimo_dentro_do_prazo_nao_esta_atrasado(aluno, livro):
    hoje = date.today()
    emprestimo = Emprestimo(uuid4(), aluno, livro, hoje, hoje + timedelta(days=7))

    assert emprestimo.verificar_atraso() is False


def test_emprestimo_pendente_apos_prazo_esta_atrasado(aluno, livro, capsys):
    hoje = date.today()
    emprestimo = Emprestimo(
        uuid4(), aluno, livro, hoje - timedelta(days=10), hoje - timedelta(days=3)
    )

    assert emprestimo.verificar_atraso() is True
    assert "atrasado em 3 dia(s)" in capsys.readouterr().out


def test_devolucao_feita_apos_prazo_esta_atrasada(aluno, livro):
    hoje = date.today()
    emprestimo = Emprestimo(
        uuid4(),
        aluno,
        livro,
        data_inicio=hoje - timedelta(days=20),
        data_prevista=hoje - timedelta(days=13),
        data_devolucao=hoje - timedelta(days=10),
    )

    assert emprestimo.verificar_atraso() is True


def test_repr_formata_datas_em_padrao_brasileiro(aluno, livro):
    emprestimo = Emprestimo(uuid4(), aluno, livro, date(2026, 3, 1), date(2026, 3, 8))

    texto = repr(emprestimo)

    assert "Início: 01/03/2026" in texto
    assert "Prevista: 08/03/2026" in texto
    assert "Devolução: Pendente" in texto

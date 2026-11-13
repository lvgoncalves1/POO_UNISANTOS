import pytest
from uuid import uuid4

from models import Aluno, Pessoa, Usuario


def test_criacao_entidades_e_heranca(aluno, bibliotecario):
    assert aluno.nome == "Lucas"
    assert bibliotecario.nome == "Ana"


def test_usuarios_herdam_de_usuario_e_pessoa(aluno, professor, visitante):
    for usuario in (aluno, professor, visitante):
        assert isinstance(usuario, Usuario)
        assert isinstance(usuario, Pessoa)


def test_bibliotecario_e_pessoa_mas_nao_usuario(bibliotecario):
    assert isinstance(bibliotecario, Pessoa)
    assert not isinstance(bibliotecario, Usuario)


def test_usuario_e_abstrato():
    with pytest.raises(TypeError):
        Usuario(id=uuid4(), nome="X", email="x@x.com")


@pytest.mark.parametrize(
    "fixture_usuario, prazo_esperado",
    [("aluno", 7), ("professor", 30), ("visitante", 3)],
)
def test_polimorfismo_prazo_emprestimo(request, fixture_usuario, prazo_esperado):
    usuario = request.getfixturevalue(fixture_usuario)
    assert usuario.obter_prazo_emprestimo() == prazo_esperado


def test_encapsulamento_atributos_privados(bibliotecario):
    aluno = Aluno(id=uuid4(), nome="Lucas", email="l@l.com", matricula="RA-1")

    assert aluno.matricula == "RA-1"
    with pytest.raises(AttributeError):
        aluno.matricula = "RA-2"
    assert bibliotecario.registro == "REG-02"
    with pytest.raises(AttributeError):
        bibliotecario.registro = "OUTRO"


def test_pessoa_expoe_id_somente_leitura(aluno):
    assert aluno.id == aluno._id
    with pytest.raises(AttributeError):
        aluno.id = uuid4()


def test_pessoa_nao_aceita_nome_ou_email_vazio(aluno):
    with pytest.raises(ValueError, match="nome"):
        aluno.nome = "   "
    with pytest.raises(ValueError, match="e-mail"):
        aluno.email = ""
    assert aluno.nome == "Lucas"

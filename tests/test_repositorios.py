from datetime import date
from uuid import uuid4

import pytest

from models import Aluno, Emprestimo, Livro, Professor, Visitante
from repositories import BancoSQLite, SQLiteLivroRepository, SQLiteUsuarioRepository


def test_livro_adicionar_atualizar_e_remover(repositorio_livros, livro):
    repositorio_livros.adicionar(livro, "EST-A1")
    livro.titulo = "Sistemas Digitais 2"
    repositorio_livros.atualizar(livro)

    [(codigo_estante, carregado)] = repositorio_livros.listar_todos()
    assert codigo_estante == "EST-A1"
    assert (carregado.isbn, carregado.titulo, carregado.autor) == (
        "123-456",
        "Sistemas Digitais 2",
        "Tocci",
    )

    repositorio_livros.remover(livro)
    assert repositorio_livros.listar_todos() == []


def test_isbn_e_chave_primaria(repositorio_livros, livro):
    repositorio_livros.adicionar(livro, "EST-A1")

    with pytest.raises(Exception, match="UNIQUE"):
        repositorio_livros.adicionar(Livro("123-456", "Outro", "Autor"), "EST-B1")


def test_usuarios_voltam_com_a_subclasse_e_dados_corretos(
    repositorio_usuarios, aluno, professor, visitante
):
    for usuario in (aluno, professor, visitante):
        repositorio_usuarios.adicionar(usuario)

    carregados = repositorio_usuarios.listar_todos()

    assert [type(u) for u in carregados] == [Aluno, Professor, Visitante]
    assert [u.id for u in carregados] == [aluno.id, professor.id, visitante.id]
    assert [u.obter_prazo_emprestimo() for u in carregados] == [7, 30, 3]
    assert carregados[0].matricula == "7047031"
    assert (carregados[1].registro_funcional, carregados[1].departamento) == (
        "FUNC-99",
        "Computação",
    )
    assert carregados[2].cpf == "123.456.789-00"


def test_usuario_atualizar_e_remover(repositorio_usuarios, aluno):
    repositorio_usuarios.adicionar(aluno)
    aluno.nome = "Lucas Silva"
    repositorio_usuarios.atualizar(aluno)

    assert repositorio_usuarios.listar_todos()[0].nome == "Lucas Silva"

    repositorio_usuarios.remover(aluno)
    assert repositorio_usuarios.listar_todos() == []


@pytest.fixture
def emprestimo_salvo(repositorio_livros, repositorio_usuarios, repositorio_emprestimos, aluno, livro):
    repositorio_livros.adicionar(livro, "EST-A1")
    repositorio_usuarios.adicionar(aluno)
    emprestimo = Emprestimo(
        uuid4(), aluno, livro, date(2026, 11, 1), date(2026, 11, 8)
    )
    repositorio_emprestimos.adicionar(emprestimo)
    return emprestimo


def test_emprestimo_e_recriado_ligado_ao_usuario_e_livro(
    repositorio_emprestimos, emprestimo_salvo, aluno, livro
):
    [carregado] = repositorio_emprestimos.listar_todos({aluno.id: aluno}, {livro.isbn: livro})

    assert carregado.id == emprestimo_salvo.id
    assert carregado.usuario is aluno
    assert carregado.livro is livro
    assert (carregado.data_inicio, carregado.data_prevista) == (date(2026, 11, 1), date(2026, 11, 8))
    assert carregado.data_devolucao is None


def test_disponibilidade_do_livro_vem_dos_emprestimos_pendentes(
    repositorio_livros, repositorio_emprestimos, emprestimo_salvo
):
    [(_, livro)] = repositorio_livros.listar_todos()
    assert livro.disponivel is False

    emprestimo_salvo.data_devolucao = date(2026, 11, 5)
    repositorio_emprestimos.atualizar(emprestimo_salvo)

    [(_, livro)] = repositorio_livros.listar_todos()
    assert livro.disponivel is True


def test_remover_usuario_apaga_seu_historico_de_emprestimos(
    repositorio_usuarios, repositorio_emprestimos, emprestimo_salvo, aluno, livro
):
    repositorio_usuarios.remover(aluno)

    assert repositorio_emprestimos.listar_todos({}, {livro.isbn: livro}) == []


def test_dados_continuam_salvos_ao_reabrir_o_banco(tmp_path, bibliotecario, estante, aluno):
    caminho = str(tmp_path / "teste.db")

    banco = BancoSQLite(caminho)
    SQLiteLivroRepository(banco).adicionar(Livro("1", "Livro", "Autor"), "A1")
    SQLiteUsuarioRepository(banco).adicionar(aluno)
    banco.fechar()

    banco = BancoSQLite(caminho)
    assert [l.isbn for _, l in SQLiteLivroRepository(banco).listar_todos()] == ["1"]
    assert [u.id for u in SQLiteUsuarioRepository(banco).listar_todos()] == [aluno.id]
    banco.fechar()

import re

import pytest

from main import criar_app


@pytest.fixture
def cliente():
    app = criar_app(":memory:")
    app.testing = True
    return app.test_client()


def pagina(cliente) -> str:
    return cliente.get("/").get_data(as_text=True)


def mensagem(cliente) -> str:
    alerta = re.search(r'<div class="alerta">(.*?)</div>', pagina(cliente), re.S)
    return alerta.group(1) if alerta else ""


def id_do_usuario(cliente, nome: str) -> str:
    padrao = rf'/usuarios/excluir/([0-9a-f-]{{36}})" method="POST" data-nome="{nome}"'
    return re.search(padrao, pagina(cliente)).group(1)


def test_pagina_inicial_lista_dados_iniciais(cliente):
    html = pagina(cliente)

    assert "Arquitetura Limpa" in html
    assert "Mariana" in html


def test_crud_de_livro(cliente):
    cliente.post("/livros", data={"isbn": "444", "titulo": "TDD", "autor": "Kent Beck"})
    assert "TDD" in cliente.get("/?q=tdd").get_data(as_text=True)

    cliente.post("/livros/editar/444", data={"titulo": "TDD na Prática", "autor": "Beck"})
    assert "TDD na Prática" in pagina(cliente)

    cliente.post("/livros/excluir/444")
    assert "TDD na Prática" not in pagina(cliente)


def test_crud_de_usuario(cliente):
    cliente.post(
        "/usuarios",
        data={"nome": "Ana", "email": "ana@x.com", "tipo": "aluno", "documento": "RA-9"},
    )
    usuario_id = id_do_usuario(cliente, "Ana")

    cliente.post(f"/usuarios/editar/{usuario_id}", data={"nome": "Ana Maria", "email": "am@x.com"})
    assert "am@x.com" in pagina(cliente)

    cliente.post(f"/usuarios/excluir/{usuario_id}")
    assert "am@x.com" not in pagina(cliente)


@pytest.mark.parametrize(
    "url, dados",
    [
        ("/livros/editar/999", {"titulo": "T", "autor": "A"}),
        ("/livros/excluir/999", {}),
        ("/usuarios/excluir/id-invalido", {}),
        ("/devolver/999", {}),
    ],
)
def test_registro_inexistente_mostra_erro_sem_quebrar(cliente, url, dados):
    resposta = cliente.post(url, data=dados)

    assert resposta.status_code == 302
    assert "Erro:" in mensagem(cliente)


@pytest.mark.parametrize(
    "dados",
    [
        {"isbn": "111", "titulo": "Duplicado", "autor": "X"},
        {"isbn": "555", "titulo": "   ", "autor": "X"},
    ],
)
def test_cadastro_de_livro_invalido_mostra_erro(cliente, dados):
    cliente.post("/livros", data=dados)

    assert "Erro:" in mensagem(cliente)
    html = pagina(cliente)
    assert html.count("<td>111</td>") == 1
    assert "<td>555</td>" not in html


def test_emprestimo_pelo_formulario_usa_id_do_usuario(cliente):
    cliente.post("/emprestar", data={"usuario": id_do_usuario(cliente, "Mariana"), "isbn": "111"})

    assert "Empréstimo realizado" in mensagem(cliente)
    assert "Usuário: Mariana" in pagina(cliente)


def test_titulo_com_aspas_nao_injeta_javascript(cliente):
    cliente.post("/livros", data={"isbn": "666", "titulo": "x');alert(1);//", "autor": "a"})

    form = re.search(r'<form action="/livros/excluir/666"[^>]*>', pagina(cliente)).group(0)
    onsubmit = re.search(r'onsubmit="([^"]*)"', form).group(1)
    assert "alert(1)" not in onsubmit


def test_dados_persistem_apos_reiniciar_a_aplicacao(tmp_path):
    caminho = str(tmp_path / "biblioteca.db")
    antes = criar_app(caminho).test_client()

    antes.post("/livros", data={"isbn": "444", "titulo": "TDD", "autor": "Kent Beck"})
    antes.post("/livros/editar/111", data={"titulo": "Arquitetura Limpa 2", "autor": "Martin"})
    antes.post("/livros/excluir/333")
    antes.post(
        "/usuarios",
        data={"nome": "Ana", "email": "ana@x.com", "tipo": "professor", "documento": "F-1"},
    )
    antes.post("/emprestar", data={"usuario": id_do_usuario(antes, "Ana"), "isbn": "222"})

    depois = criar_app(caminho).test_client()
    html = pagina(depois)

    assert "TDD" in html
    assert "Arquitetura Limpa 2" in html
    assert "Entendendo Algoritmos" not in html
    assert "<td>Professor</td>" in html and "Ana" in html
    assert "Usuário: Ana" in html
    assert "/devolver/222" in html
    assert html.count("<td>111</td>") == 1


def test_dados_iniciais_nao_sao_duplicados_ao_reiniciar(tmp_path):
    caminho = str(tmp_path / "biblioteca.db")
    criar_app(caminho)

    html = pagina(criar_app(caminho).test_client())

    assert html.count("<td>111</td>") == 1
    assert html.count("<td>Mariana</td>") == 1

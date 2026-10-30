from uuid import uuid4

import pytest

from models import (
    Aluno,
    Biblioteca,
    Bibliotecario,
    Estante,
    Livro,
    Professor,
    Visitante,
)


@pytest.fixture
def biblioteca():
    return Biblioteca(id=uuid4(), nome="Biblioteca Central")


@pytest.fixture
def bibliotecario(biblioteca):
    return Bibliotecario(
        id=uuid4(),
        nome="Ana",
        email="ana@bib.br",
        registro="REG-02",
        biblioteca=biblioteca,
    )


@pytest.fixture
def estante():
    return Estante(codigo_estante="EST-A1")


@pytest.fixture
def livro():
    return Livro(isbn="123-456", titulo="Sistemas Digitais", autor="Tocci")


@pytest.fixture
def aluno():
    return Aluno(
        id=uuid4(), nome="Lucas", email="lucas@unisantos.br", matricula="7047031"
    )


@pytest.fixture
def professor():
    return Professor(
        id=uuid4(),
        nome="Dr. Silva",
        email="silva@unisantos.br",
        registro_funcional="FUNC-99",
        departamento="Computação",
    )


@pytest.fixture
def visitante():
    return Visitante(
        id=uuid4(), nome="Mariana", email="mari@gmail.com", cpf="123.456.789-00"
    )

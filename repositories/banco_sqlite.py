import sqlite3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS livros (
    isbn           TEXT PRIMARY KEY,
    titulo         TEXT NOT NULL,
    autor          TEXT NOT NULL,
    codigo_estante TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS usuarios (
    id                 TEXT PRIMARY KEY,
    tipo               TEXT NOT NULL CHECK (tipo IN ('aluno', 'professor', 'visitante')),
    nome               TEXT NOT NULL,
    email              TEXT NOT NULL,
    matricula          TEXT,
    registro_funcional TEXT,
    departamento       TEXT,
    cpf                TEXT
);

CREATE TABLE IF NOT EXISTS emprestimos (
    id             TEXT PRIMARY KEY,
    usuario_id     TEXT NOT NULL REFERENCES usuarios (id) ON DELETE CASCADE,
    livro_isbn     TEXT NOT NULL REFERENCES livros (isbn) ON DELETE CASCADE,
    data_inicio    TEXT NOT NULL,
    data_prevista  TEXT NOT NULL,
    data_devolucao TEXT
);
"""


class BancoSQLite:

    def __init__(self, caminho: str) -> None:
        self._conexao: sqlite3.Connection = sqlite3.connect(caminho, check_same_thread=False)
        self._conexao.row_factory = sqlite3.Row
        self._conexao.execute("PRAGMA foreign_keys = ON")
        self._conexao.executescript(ESQUEMA)

    @property
    def conexao(self) -> sqlite3.Connection:
        return self._conexao

    def fechar(self) -> None:
        self._conexao.close()

from uuid import uuid4
from models import Livro, Aluno, Professor, Visitante
from services import BibliotecaService


class BibliotecaController:
    def __init__(self, service: BibliotecaService) -> None:
        self._service: BibliotecaService = service

    def obter_dados_painel(self, busca: str = "") -> dict:
        livros = (
            self._service.buscar_livros_por_titulo(busca)
            if busca
            else self._service.listar_livros()
        )
        return {
            "nome_biblioteca": self._service.nome_biblioteca,
            "livros": livros,
            "livros_disponiveis": [l for l in self._service.listar_livros() if l.disponivel],
            "usuarios": self._service.listar_usuarios(),
            "emprestimos": self._service.listar_emprestimos(),
            "termo_busca": busca,
        }

    def criar_livro(self, isbn: str, titulo: str, autor: str) -> str:
        novo_livro = Livro(isbn.strip(), titulo.strip(), autor.strip())
        self._service.cadastrar_livro(novo_livro)
        return f"Livro '{titulo}' cadastrado com sucesso!"

    def editar_livro(self, isbn: str, titulo: str, autor: str) -> str:
        self._service.atualizar_livro(isbn, titulo, autor)
        return f"Livro (ISBN: {isbn}) atualizado com sucesso!"

    def excluir_livro(self, isbn: str) -> str:
        self._service.remover_livro(isbn)
        return f"Livro (ISBN: {isbn}) excluído com sucesso!"

    def criar_usuario(self, nome: str, email: str, tipo: str, doc: str, depto: str = "") -> str:
        novo_id = uuid4()
        if tipo == "aluno":
            usuario = Aluno(novo_id, nome, email, doc)
        elif tipo == "professor":
            usuario = Professor(novo_id, nome, email, doc, depto or "Geral")
        else:
            usuario = Visitante(novo_id, nome, email, doc)
        self._service.cadastrar_usuario(usuario)
        return f"Usuário '{nome}' ({tipo.capitalize()}) cadastrado!"

    def editar_usuario(self, usuario_id: str, nome: str, email: str) -> str:
        self._service.atualizar_usuario(usuario_id, nome, email)
        return f"Dados do usuário '{nome}' atualizados com sucesso!"

    def excluir_usuario(self, usuario_id: str) -> str:
        self._service.remover_usuario(usuario_id)
        return "Usuário excluído com sucesso!"

    def emprestar(self, nome_usuario: str, isbn: str) -> str:
        emp = self._service.realizar_emprestimo(nome_usuario, isbn)
        if emp is None:
            return "Erro: Este livro já está emprestado no momento."
        return f"Empréstimo realizado! Devolução prevista: {emp.data_prevista.strftime('%d/%m/%Y')}"

    def devolver(self, isbn: str) -> str:
        self._service.devolver_livro(isbn)
        return "Livro devolvido com sucesso!"
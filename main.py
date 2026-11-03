from uuid import uuid4
from flask import Flask
from models import Biblioteca, Bibliotecario, Estante, Livro, Aluno, Professor, Visitante
from services import BibliotecaService
from controllers import BibliotecaController
from routes import criar_rotas


def criar_app() -> Flask:
    app = Flask(__name__)
    app.secret_key = "chave-secreta-unisantos"
    
    bib = Biblioteca(uuid4(), "BibliotecAI")
    estante = Estante("A1")
    bib.adicionar_estante(estante)
    bibliotecario = Bibliotecario(uuid4(), "Carlos", "carlos@bib.com", "BIB-01", bib)

    service = BibliotecaService(bibliotecario, estante)
    service.cadastrar_livro(Livro("111", "Arquitetura Limpa", "Robert Martin"))
    service.cadastrar_livro(Livro("222", "Padrões de Projeto", "GoF"))
    service.cadastrar_livro(Livro("333", "Entendendo Algoritmos", "Aditya Bhargava"))

    service.cadastrar_usuario(Aluno(uuid4(), "Lucas", "lucas@edu.com", "RA-001"))
    service.cadastrar_usuario(Professor(uuid4(), "Dr. Silva", "silva@edu.com", "FUNC-99", "Computação"))
    service.cadastrar_usuario(Visitante(uuid4(), "Mariana", "mari@gmail.com", "123.456.789-00"))

    controller = BibliotecaController(service)
    app.register_blueprint(criar_rotas(controller))

    return app


if __name__ == "__main__":
    app = criar_app()
    app.run(debug=True)
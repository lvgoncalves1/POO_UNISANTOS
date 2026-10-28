from uuid import uuid4
from models import (
    Biblioteca,
    Bibliotecario,
    Estante,
    Livro,
    Aluno,
    Professor,
    Visitante,
)


def main() -> None:
    bib = Biblioteca(uuid4(), "Biblioteca Central")
    estante_tech = Estante("A1")
    bib.adicionar_estante(estante_tech)

    bibliotecario = Bibliotecario(
        id=uuid4(),
        nome="Carlos",
        email="carlos@bib.com",
        registro="BIB-01",
        biblioteca=bib,
    )

    livro1 = Livro("111", "Arquitetura Limpa", "Robert Martin")
    livro2 = Livro("222", " Padrões de Projeto", "GoF")
    livro3 = Livro("333", "Entendendo Algoritmos", "Aditya Bhargava")

    bibliotecario.cadastrar_livro(estante_tech, livro1)
    bibliotecario.cadastrar_livro(estante_tech, livro2)
    bibliotecario.cadastrar_livro(estante_tech, livro3)

    aluno = Aluno(uuid4(), "Lucas", "lucas@edu.com", "RA-001")
    professor = Professor(uuid4(), "Dr. Silva", "silva@edu.com", "FUNC-99", "Computação")
    visitante = Visitante(uuid4(), "Mariana", "mari@gmail.com", "123.456.789-00")

    bib.adicionar_usuario(aluno)
    bib.adicionar_usuario(professor)
    bib.adicionar_usuario(visitante)

    print("=== Realizando Empréstimos ===")
    emp_aluno = aluno.solicitar_emprestimo(bibliotecario, bib.buscar_livro("111"))
    emp_prof = professor.solicitar_emprestimo(bibliotecario, bib.buscar_livro("222"))
    emp_visit = visitante.solicitar_emprestimo(bibliotecario, bib.buscar_livro("333"))

    print("Aluno:    ", emp_aluno)
    print("Professor:", emp_prof)
    print("Visitante:", emp_visit)

    print("\n=== Testando Livro Indisponível ===")
    visitante.solicitar_emprestimo(bibliotecario, bib.buscar_livro("111"))

    print("\n=== Realizando Devolução ===")
    if emp_aluno:
        bibliotecario.registrar_devolucao(emp_aluno)
        print("Após devolução:", emp_aluno)
        print("Livro 111 disponível novamente?", livro1.disponivel)


if __name__ == "__main__":
    main()
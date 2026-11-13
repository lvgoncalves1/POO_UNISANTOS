from flask import Blueprint, render_template, request, redirect, url_for, flash
from controllers import BibliotecaController


def criar_rotas(controller: BibliotecaController) -> Blueprint:
    bp = Blueprint("biblioteca", __name__)

    @bp.route("/", methods=["GET"])
    def index():
        termo_busca = request.args.get("q", "")
        dados = controller.obter_dados_painel(termo_busca)
        return render_template("index.html", **dados)

    @bp.route("/livros", methods=["POST"])
    def cadastrar_livro():
        try:
            msg = controller.criar_livro(
                request.form["isbn"],
                request.form["titulo"],
                request.form["autor"],
            )
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/livros/editar/<isbn>", methods=["POST"])
    def editar_livro(isbn: str):
        try:
            msg = controller.editar_livro(
                isbn,
                request.form["titulo"],
                request.form["autor"],
            )
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/livros/excluir/<isbn>", methods=["POST"])
    def excluir_livro(isbn: str):
        try:
            msg = controller.excluir_livro(isbn)
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/usuarios", methods=["POST"])
    def cadastrar_usuario():
        try:
            msg = controller.criar_usuario(
                request.form["nome"],
                request.form["email"],
                request.form["tipo"],
                request.form["documento"],
                request.form.get("departamento", ""),
            )
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/usuarios/editar/<usuario_id>", methods=["POST"])
    def editar_usuario(usuario_id: str):
        try:
            msg = controller.editar_usuario(
                usuario_id,
                request.form["nome"],
                request.form["email"],
            )
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/usuarios/excluir/<usuario_id>", methods=["POST"])
    def excluir_usuario(usuario_id: str):
        try:
            msg = controller.excluir_usuario(usuario_id)
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/emprestar", methods=["POST"])
    def emprestar():
        try:
            msg = controller.emprestar(request.form["usuario"], request.form["isbn"])
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    @bp.route("/devolver/<isbn>", methods=["POST"])
    def devolver(isbn: str):
        try:
            msg = controller.devolver(isbn)
            flash(msg)
        except ValueError as e:
            flash(f"Erro: {e}")
        return redirect(url_for("biblioteca.index"))

    return bp
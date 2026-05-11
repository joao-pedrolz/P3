from flask import render_template, url_for, jsonify, request, redirect
from flask_login import login_required, login_user, logout_user, current_user
from .database import db
from .forms import FormLogin, FormCriarConta, FormNovoLivro
from livrosp3 import bcrypt

from .models import (
    Livro,
    Propriedades,
    Usuario
)

def init_routes(app):

    # ROTAS HTML

    @app.route("/", methods=["GET", "POST"])
    def homepage():
        form_login = FormLogin()
        if form_login.validate_on_submit():
            usuario = Usuario.query.filter_by(email=form_login.email.data).first()
            if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
                login_user(usuario)
                return redirect(url_for("pagina_biblioteca"))
        return render_template("homepage.html",form_login=form_login)


    @app.route("/cadastro", methods=["GET", "POST"])
    def cadastro():
        form_criar_conta = FormCriarConta()

        if form_criar_conta.validate_on_submit():
            senha_criptografada = bcrypt.generate_password_hash(
                form_criar_conta.senha.data
            ).decode("utf-8")

            usuario = Usuario(
                email=form_criar_conta.email.data,
                senha=senha_criptografada
            )

            db.session.add(usuario)
            db.session.commit()
            login_user(usuario, remember=True)

            return redirect(url_for("pagina_biblioteca"))

        return render_template(
            "cadastro.html",
            form_criar_conta=form_criar_conta
        )


    @app.route("/biblioteca", methods=["GET"])
    @login_required
    def pagina_biblioteca():
        livros = Livro.query.all()
        return render_template(
            "biblioteca.html",
            biblioteca=[livro.to_dict() for livro in livros]
        )


    @app.route("/biblioteca/novo", methods=["GET", "POST"])
    @login_required
    def pagina_novo_livro():
        form_novo_livro = FormNovoLivro()

        if form_novo_livro.validate_on_submit():
            novo_livro = Livro(
                titulo=form_novo_livro.titulo.data,
                )

            db.session.add(novo_livro)
            db.session.commit()

            return redirect(url_for("pagina_biblioteca"))

        return render_template(
            "novo_livro.html",
            form_novo_livro=form_novo_livro
        )

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("homepage"))
    
    @app.route("/biblioteca/<int:id>", methods=["GET"])
    @login_required
    def pagina_livro(id):
        livro = Livro.query.get_or_404(id)

        propriedades = Propriedades.query.filter_by(
            livro_id=livro.id
        ).all()

        return render_template(
            "livro.html",
            livro=livro,
            propriedades=propriedades,
        )
    
    @app.route("/biblioteca/<int:id>/editar", methods=["GET", "POST"])
    @login_required
    def editar_livro(id):
        livro = Livro.query.get_or_404(id)

        propriedades = Propriedades.query.filter_by(
            livro_id=livro.id
        ).all()

        if request.method == "POST":
            livro.titulo = request.form.get("titulo")

            for propriedade in propriedades:
                novo_valor = request.form.get(f"propriedade_{propriedade.id}")
                if novo_valor is not None:
                    propriedade.valor = novo_valor

            db.session.commit()

            return redirect(url_for("pagina_livro", id=livro.id))

        return render_template(
            "editar_livro.html",
            livro=livro,
            propriedades=propriedades
        )

    @app.route("/biblioteca/<int:id>/propriedade/nova", methods=["GET", "POST"])
    @login_required
    def nova_propriedade(id):
        livro = Livro.query.get_or_404(id)

        if request.method == "POST":
            atributo = request.form.get("atributo")
            valor = request.form.get("valor")

            nova = Propriedades(
                livro_id=livro.id,
                atributo=atributo,
                valor=valor
            )

            db.session.add(nova)
            db.session.commit()

            return redirect(url_for("pagina_livro", id=livro.id))

        return render_template("nova_propriedade.html", livro=livro)

    @app.route("/biblioteca/<int:id>/excluir", methods=["POST"])
    @login_required
    def excluir_livro(id):
        livro = Livro.query.get_or_404(id)


        propriedades = Propriedades.query.filter_by(livro_id=livro.id).all()

        for propriedade in propriedades:
            db.session.delete(propriedade)

        db.session.delete(livro)
        db.session.commit()

        return redirect(url_for("pagina_biblioteca"))

    # ROTAS API

    # LISTAR LIVROS
    @app.route("/api/biblioteca", methods=["GET"])
    def api_listar_livros():
        livros = Livro.query.all()
        return jsonify([livro.to_dict() for livro in livros]), 200

    # PEGAR LIVRO POR ID
    @app.route("/api/biblioteca/<int:id>", methods=["GET"])
    def api_obter_livro_por_id(id):
        livro = Livro.query.get_or_404(id)
        return jsonify(livro.to_dict()), 200

    #CRIAR LIVRO
    @app.route("/api/biblioteca", methods=["POST"])
    def api_criar_livro():
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "Envie um JSON no body da requisição"}), 400

        titulo = dados.get("titulo")

        if not titulo:
            return jsonify({"erro": "Campo obrigatório: título "}), 400

        novo_livro = Livro(titulo=titulo)

        db.session.add(novo_livro)
        db.session.commit()

        return jsonify(novo_livro.to_dict()), 201

    # editar livro
    @app.route("/api/biblioteca/<int:id>", methods=["PUT"])
    def api_editar_livro(id):
        livro = Livro.query.get_or_404(id)
        dados = request.get_json(silent=True)

        if not dados:
            return jsonify({"erro": "Envie um JSON válido"}), 400

        livro.titulo = dados.get("titulo", livro.titulo)

        db.session.commit()

        return jsonify(livro.to_dict()), 200

    # EXCLUIR LIVRO
    @app.route("/api/biblioteca/<int:id>", methods=["DELETE"])
    def api_excluir_livro(id):
        livro = Livro.query.get_or_404(id)

        db.session.delete(livro)
        db.session.commit()

        return jsonify({"mensagem": "Livro excluído com sucesso"}), 200
    
    # LISTAR PROPRIEDADES
    @app.route("/api/propriedades", methods=["GET"])
    def api_listar_propriedades():
        propriedades = Propriedades.query.all()

        return jsonify([
            {"id": propriedades.id, "propriedade": propriedades.atributo, "valor": propriedades.valor}
            for propriedades in propriedades
        ]), 200
    
    # INCLUIR PROPRIEDADE
    @app.route("/api/propriedades", methods=["POST"])
    def api_criar_propriedade():
        dados = request.get_json(silent=True)

        if not dados or not dados.get("atributo") or not dados.get("valor") or not dados.get("livro_id"):
            return jsonify({"erro": "ID, Atributo e Valor são obrigatórios"}), 400

        propriedade = Propriedades(
            livro_id=dados["livro_id"],
            atributo=dados["atributo"],
            valor=dados["valor"]
        )
        db.session.add(propriedade)
        db.session.commit()
        return jsonify({
            "id": propriedade.id,
            "livro_id": propriedade.livro_id,
            "atributo": propriedade.atributo,
            "valor": propriedade.valor
        }), 201

    # editar propriedade
    @app.route("/api/propriedades/<int:id>", methods=["PUT"])
    def api_editar_propriedade(id):
        propriedade = Propriedades.query.get_or_404(id)
        dados = request.get_json(silent=True)
        if not dados:
            return jsonify({"erro": "Envie um JSON válido"}), 400

        propriedade.atributo = dados.get("atributo", propriedade.atributo)
        propriedade.valor = dados.get("valor", propriedade.valor)
        propriedade.livro_id = dados.get("livro_id", propriedade.livro_id)

        db.session.commit()
        return jsonify(propriedade.to_dict()), 200

    # EXCLUIR PROPRIEDADE
    @app.route("/api/propriedades/<int:id>", methods=["DELETE"])
    def api_excluir_propriedade(id):
        propriedade = Propriedades.query.get_or_404(id)

        db.session.delete(propriedade)
        db.session.commit()

        return jsonify({"mensagem": "Propriedade excluída com sucesso"}), 200
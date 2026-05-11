from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from livrosp3.models import Usuario

class FormLogin(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    botao = SubmitField("Fazer Login")

class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmar Senha", validators=[DataRequired(), EqualTo("senha")])
    botao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario: 
            return ValidationError("Email já cadastrado, faça login para continuar")

class FormNovoLivro(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired()])
    autor = StringField("Autor")
    editora = StringField("Editora")
    paginas = StringField("Número de páginas")
    tipo_de_capa = StringField("Tipo de capa")
    botao = SubmitField("Cadastrar Livro")
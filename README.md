# Biblioteca P3 — API e site de cadastro de livros

Projeto acadêmico em **Python/Flask**: cadastro de livros com propriedades livres (autor, idioma, páginas…),
login de usuários e uma **API REST** com os mesmos dados. Banco relacional **SQLite** via SQLAlchemy, com
migrações Alembic (Flask-Migrate).

## Funcionalidades

- Cadastro e login de usuários (senha com hash bcrypt, sessão com Flask-Login)
- CRUD de livros e de propriedades de cada livro pelo site (templates Jinja + Flask-WTF)
- API JSON:

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/biblioteca` | lista os livros |
| GET | `/api/biblioteca/<id>` | um livro com suas propriedades |
| POST | `/api/biblioteca` | cria um livro |
| PUT | `/api/biblioteca/<id>` | altera um livro |
| DELETE | `/api/biblioteca/<id>` | exclui um livro |
| GET/POST | `/api/propriedades` | lista / cria propriedades |
| PUT/DELETE | `/api/propriedades/<id>` | altera / exclui uma propriedade |

## Executar

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python criar_banco.py      # cria o banco SQLite em instance/
python main.py             # http://127.0.0.1:5000
```

Defina `SECRET_KEY` no ambiente para uso fora do desenvolvimento.

## Estrutura

```
livrosp3/      __init__.py (app factory) · models.py · routes.py · forms.py · templates/
migrations/    migrações Alembic
criar_banco.py cria as tabelas · main.py inicia o servidor
```

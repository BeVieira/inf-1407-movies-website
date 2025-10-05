# inf-1407-movies-website

## Projeto: Catálogo de Filmes (INF-1407)

### Resumo / Escopo

Este repositório contém uma aplicação web construída com Django que implementa um catálogo de filmes. O site permite pesquisar filmes (integração com The Movie Database - TMDB), visualizar detalhes e organizar filmes em listas pessoais.

Principais funcionalidades:

- Página principal com busca por título e exibição de filmes (resultados de busca ou filmes populares).
- Autenticação: cadastro (signup), login e logout.
- CRUD de listas de filmes: criar, editar, deletar listas; adicionar e remover filmes de listas.
- Exibição das listas do usuário na sidebar com rolagem horizontal de posters.
- Management command para popular o banco a partir da API do TMDB.

---

## Manual de uso (como usar o site)

### Pré-requisitos

- Python 3.10+ (desenvolvido com Python 3.12)
- Virtualenv recomendado
- Arquivo `.env` na pasta `movies/` com as variáveis:
	- SECRET_KEY=alguma_coisa_secreta
	- TMDB_API_KEY=SEU_API_KEY_DO_TMDB

### Instalação e execução (modo desenvolvimento)

1. Criar e ativar um virtualenv:

```bash
python -m venv venv
source venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Aplicar migrations e executar o servidor:

```bash
python movies/manage.py migrate
python movies/manage.py runserver
```

4. Abrir no navegador: `http://127.0.0.1:8000/`

### Fluxo de uso (o que você pode fazer)

- Pesquisar filmes por título usando a barra de busca.
- Clicar em um filme para ver a página de detalhes.
- Criar uma conta (signup) e efetuar login.
- Criar e gerenciar listas pessoais (Minhas Listas) e adicionar/remover filmes.
- Visualizar as listas na barra lateral; cada lista exibe posters dos filmes em uma fila horizontal rolável.

---

## O que foi implementado

Funcionalidades implementadas e testadas manualmente (PASS):

- Cadastro de usuários (signup) e login. (formulários funcionais)
- Busca de filmes por título (integração parcial com TMDB via `services.py`).
- Exibição de filmes populares quando não há busca.
- CRUD básico de listas (criar, editar, deletar) e remoção de filmes de listas.
- Sidebar com as listas do usuário, cada uma com uma linha horizontal de posters (scroll). Hover aplicado aos posters.
- Correções de templates que causavam TemplateSyntaxError e adição de um filtro (`movie_extras.normalize_poster`) para normalizar paths de poster.

Funcionalidades parcialmente testadas / observações:

- Management command `populate_movies` foi implementado para importar filmes do TMDB; requer API key válida e uso manual (`python movies/manage.py populate_movies`).
- O filtro de template para normalizar posters deve estar disponível após reiniciar o servidor; se aparecer o erro "'movie_extras' is not a registered tag library", reinicie o servidor.

---

## Estrutura do projeto (principais arquivos)

- `movies/` - config do projeto e `manage.py`
- `moviesApp/` - app principal
	- `models.py` — modelos `Movie` e `MovieList`
	- `views.py` — views responsivas para a UI (index, detalhes, listas)
	- `services.py` — integração com TMDB (buscar, detalhes, salvar)
	- `templates/` — templates para `movies`, `auth`, `lists`
	- `static/` — arquivos CSS e assets
	- `templatetags/movie_extras.py` — filtro para normalização de poster

---

## Comandos úteis

- Migrar: `python movies/manage.py migrate`
- Popular DB (TMDB): `python movies/manage.py populate_movies`
- Limpar/normalizar posters (exemplo manual no shell):

```bash
python movies/manage.py shell
```
no shell:

```python
from moviesApp.models import Movie
from moviesApp.templatetags.movie_extras import normalize_poster
for m in Movie.objects.all():
		clean = normalize_poster(m.poster, 'w200')
		if clean:
				m.poster = clean
				m.save(update_fields=['poster'])
```

---

## Membros do grupo

- Bernardo Vieira Santos e João Victor Francisco


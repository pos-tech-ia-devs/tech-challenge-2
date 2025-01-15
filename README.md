# Otimização de carteira Criptos com Algoritmo genéticos

## Instalar e Rodar o projeto

O projeto está usando o [poetry](https://python-poetry.org/) para fazer gerenciamento das dependências. Ele é mais moderno e performático em comparação a Anaconda.

### Iniciar o projeto

Todas as dependências estão no arquivo `pyproject.toml`, antes de instalar precisa iniciar o ambiente virtual do poetry:

```bash
poetry init
```

> Isso irá gerar uma pasta `tech_challenge_2/__pycache__`

Após rodar iniciar o `venv`, poderá instalar as dependências:

```bash
poetry install
```

### Organização de pastas

O Poetry gera uma estrutura padrão dos projetos, quando você o cria com o comando

```bash
poetry new PROJECT_NAME
```

Ele irá criar uma pasta na raiz com o nome do projeto, essa pasta será seu source e será criada no padrão snake_case.

### Adicionar uma nova lib

Processo parecido como qualquer package manager:

```bash
poetry add LIB_QUE_DESEJAR
```

No arquivo `pyproject.toml` será adicionada na sessão `[tool.poetry.dependencies]` se for de uma dependência de prod, se for de dev irá para `[tool.poetry.dev-dependencies]`

### Rodar o projeto

Também temos uma sessão para scripts no `pyproject.toml`

```
[tool.poetry.scripts]
dev = "tech_challenge_2.app:main"
```

Para rodar basta:

```bash
poetry run dev
```

**Explicando:**
Para criar um novo script você terá que seguir a estrutura:

```
[tool.poetry.scripts]
NOME_DO_COMANDO = "NOME_DO_SOURCE.ARQUIVO_QUE_DESEJA:METODO_QUE_DEVE_SER_CHAMADO"
```

### Rodar o streamlit

Para rodar a parte visual:

```bash
streamlit run tech_challenge_2/view.py
```

## Entendendo sobre o projeto

Toda explicação está [aqui](tech_challenge_2/README.md)!

---

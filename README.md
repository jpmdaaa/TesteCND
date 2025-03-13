# Sistema de Análise e Recomendação de Filmes

Este projeto consiste em dois scripts Python que interagem com a API The Movie Database (TMDB) para analisar dados de filmes e fornecer recomendações de filmes.

## Pré-requisitos

* Python 3.6 ou superior
* Uma chave de API do TMDB (obtenha uma em [https://developer.themoviedb.org/](https://developer.themoviedb.org/))

## Instalação

1. Clone este repositório ou baixe o arquivo ZIP
2. Instale as dependências necessárias:

```
pip install -r requirements.txt
```

## Scripts

### 1. Análise de Dados de Filmes (`teste_1.py`)

Este script analisa uma lista de filmes e gera estatísticas sobre a participação de atores, frequência de gêneros e desempenho de bilheteria.

#### Configuração

Dentro do arquivo `teste_1.py`, defina os seguintes parâmetros antes de executar o script:

```
# Defina sua chave API
API_KEY = "SUA_CHAVE_API"

# Defina os IDs dos filmes a serem analisados
MOVIE_IDS = [550, 11, 13]

# Defina o formato de saída: "json" ou "csv"
OUTPUT_FORMAT = "json"

# Diretório para salvar os resultados (se aplicável)
OUTPUT_DIR = "."
```

#### Execução

Após configurar os parâmetros, execute o script com:

```
python teste_1.py
```

Os resultados serão salvos no formato e diretório especificados.

---

### 2. Sistema de Recomendação de Filmes (`teste_2.py`)

Este script recomenda 5 filmes com base em um único filme de entrada, considerando similaridade de gênero, elenco e popularidade.

#### Configuração

Dentro do arquivo `teste_2.py`, defina os seguintes parâmetros antes de executar o script:

```
# Defina sua chave API
API_KEY = "SUA_CHAVE_API"

# Defina o ID do filme de entrada
MOVIE_ID = 550

# Defina o arquivo de saída para as recomendações
OUTPUT_FILE = "recomendacoes.json"
```

#### Execução

Após configurar os parâmetros, execute o script com:

```
python teste_2.py
```

Os resultados serão salvos no arquivo especificado.

---

## Descrição dos Arquivos

* `<span>teste_1.py`: Script de análise de filmes
* `<span>teste_2.py`: Script de recomendação de filmes
* `<span>requirements.txt`: Lista de dependências Python
* `<span>README.md`: Este arquivo de documentação

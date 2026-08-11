# Radar Tech Brasil

Inteligencia de dados sobre o mercado formal de tecnologia no Brasil usando microdados publicos do Novo CAGED e a Classificacao Brasileira de Ocupacoes.

## Problema

Dados publicos de mercado de trabalho sao ricos, mas chegam em arquivos grandes, com codigos pouco amigaveis e estrutura voltada para publicacao, nao para analise direta. Este projeto transforma esses dados em bases tratadas, agregados analiticos, documentacao tecnica e dashboard.

## Objetivo

Analisar admissoes, desligamentos, saldo de empregos, ocupacoes, categorias tech, remuneracao, escolaridade, idade e distribuicao geografica de profissionais de tecnologia no Brasil.

## Resultados Atuais

Janela analisada:

```text
202507 a 202606
```

Indicadores calculados:

```text
Registros tech: 668.686
Admissoes tech: 340.719
Desligamentos tech: 327.967
Saldo tech: 12.752
Ocupacoes CBO tech: 39
Categorias tech: 9
```

Esses resultados dependem do mapeamento CBO tech versionado em `data/external/cbo_tech_mapping.csv`.

## Arquitetura

```text
Novo CAGED + CBO
        |
        v
Python ETL
        |
        v
Dados processados
        |
        +--> Agregados CSV
        |        |
        |        v
        |   Streamlit Dashboard
        |
        +--> PostgreSQL
                 |
                 v
             SQL / Views
```

## Estrutura

```text
data/raw/caged/       arquivos originais do Novo CAGED
data/raw/cbo/         arquivos originais da CBO
data/processed/       dados tratados e agregados
data/external/        mapeamentos e dominios versionados
src/                  codigo Python do pipeline
sql/                  DDL, views e consultas analiticas
dashboard/            aplicacao Streamlit
tests/                testes automatizados
docs/                 metodologia, dicionario e status
notebooks/            analise exploratoria
```

## Tecnologias

- Python
- Pandas
- NumPy
- SQLAlchemy
- PostgreSQL
- Plotly
- Streamlit
- Pytest
- Jupyter

## Ambiente

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Copie `.env.example` para `.env` e ajuste credenciais locais. O arquivo `.env` nao deve ser versionado.

## Pipeline Principal

Baixar CBO:

```bash
python -m src.download_sources --source cbo
```

Baixar uma competencia do Novo CAGED:

```bash
python -m src.download_sources --source caged-mov --year-month 202606
```

Inspecionar arquivo real:

```bash
python -m src.inspect_caged --file data/raw/caged/CAGEDMOV202606.txt --rows 1000
```

Rodar janela inicial completa:

```bash
python -m src.pipeline_multi
python -m src.consolidate_aggregates --input-dir data/processed --output-dir data/processed
python -m src.enrich_aggregates
python -m src.generate_insights
```

## Dashboard

```bash
streamlit run dashboard/app.py
```

Abas disponiveis:

```text
Visao Geral
Mercado
Profissoes
Salarios
Estados
Perfil Profissional
Metodologia
```

![Dashboard Radar Tech Brasil](docs/assets/dashboard_overview.png)

## PostgreSQL

Subir PostgreSQL local com Docker, quando disponivel:

```bash
docker compose up -d
```

Validar conexao:

```bash
python -m src.check_database
```

Carregar dimensoes e agregados:

```bash
python -m src.load
```

Carregar fato detalhada de uma competencia:

```bash
python -m src.load --load-fact --fact-file data/processed/tech_cagedmov202606.csv
```

SQL versionado:

```text
sql/create_tables.sql
sql/views.sql
sql/analysis_queries.sql
```

## Analise Exploratoria

Notebook narrativo:

```text
notebooks/01_exploracao.ipynb
notebooks/01_exploracao_executado.ipynb
```

Abrir Jupyter:

```bash
jupyter notebook
```

## Documentacao

```text
docs/fontes_dados.md
docs/metodologia.md
docs/metodologia_cbo_tech.md
docs/dicionario_dados.md
docs/modelagem_postgresql.md
docs/pipeline_multicompetencia.md
docs/janela_12_meses_tech.md
docs/insights_iniciais.md
docs/status_projeto.md
```

## Testes

```bash
pytest
```

Status atual:

```text
19 tests passed
```

## Limites e Decisoes

- A versao inicial usa Novo CAGED e CBO.
- RAIS, IBGE e Banco Central ficam para versoes futuras.
- O mapeamento CBO tech e conservador e versionado.
- Salarios iguais a zero e salarios extremos sao marcados por flags, nao removidos automaticamente.
- Media e mediana salarial usam apenas salarios maiores que zero e sem `flag_salario_extremo`.
- Dominios marcados como `pendente_layout_oficial` devem ser revisados antes de uso definitivo.

## Proximos Passos

1. Validar dominios pendentes contra layout oficial do Novo CAGED.
2. Executar carga real no PostgreSQL quando houver servidor local disponivel.
3. Carregar fato detalhada para as 12 competencias.
4. Migrar o dashboard de CSV para views PostgreSQL.
5. Adicionar screenshots do dashboard ao README.
6. Revisar mapeamento CBO tech com criterios qualitativos adicionais.
7. Preparar publicacao no GitHub com commits pequenos e historico limpo.

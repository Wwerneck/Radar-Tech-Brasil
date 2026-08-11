# Modelagem PostgreSQL

## Objetivo

Preparar um modelo relacional para análise do mercado tech no Novo CAGED, com dimensões, fato detalhada e tabelas agregadas para consumo rápido no dashboard.

## Schema

```text
radar
```

## Tabelas Principais

```text
radar.dim_tempo
radar.dim_ocupacao
radar.dim_localidade
radar.fato_movimentacao_tech
```

## Tabelas Agregadas

```text
radar.agg_tech_overview_mensal
radar.agg_tech_by_category_mensal
radar.agg_tech_by_uf_mensal
radar.agg_tech_by_occupation_mensal
radar.agg_tech_by_age_group_mensal
radar.agg_tech_by_education_mensal
```

## Estratégia

- A fato detalhada usa `row_hash` único para suportar carga idempotente futura.
- As dimensões separam tempo, ocupação e localidade.
- As agregações mensais são carregadas para acelerar dashboard e consultas iniciais.
- A primeira carga Python prioriza dimensão de ocupação e agregados consolidados.
- A carga detalhada da fato será implementada depois da validação da modelagem no PostgreSQL.

## Arquivos SQL

```text
sql/create_tables.sql
sql/views.sql
sql/analysis_queries.sql
```

## Carga

```powershell
python -m src.load
```

Antes de executar, configure `.env` com:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=radar_tech
DB_USER=postgres
DB_PASSWORD=sua_senha
```

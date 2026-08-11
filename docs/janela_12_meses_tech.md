# Janela Inicial de 12 Meses - Tech

## Período

```text
202507 a 202606
```

## Pipeline Executado

```powershell
python -m src.pipeline_multi
python -m src.consolidate_aggregates --input-dir data/processed --output-dir data/processed
```

## Validação do Manifesto

O manifesto contém 60 etapas concluídas:

```text
12 competências x 5 etapas = 60
```

Etapas por competência:

```text
download
extract
process
enrich
aggregate
```

Nenhuma etapa pendente foi identificada.

## Agregados Consolidados

```text
data/processed/agg_tech_overview_mensal.csv
data/processed/agg_tech_by_category_mensal.csv
data/processed/agg_tech_by_uf_mensal.csv
data/processed/agg_tech_by_occupation_mensal.csv
data/processed/agg_tech_by_age_group_mensal.csv
data/processed/agg_tech_by_education_mensal.csv
```

## KPIs da Janela

| Métrica | Valor |
|---|---:|
| Registros tech | 668.686 |
| Admissões tech | 340.719 |
| Desligamentos tech | 327.967 |
| Saldo de empregos tech | 12.752 |

## Série Mensal

| Competência | Registros tech | Admissões | Desligamentos | Saldo | Remuneração média | Remuneração mediana |
|---|---:|---:|---:|---:|---:|---:|
| 202507 | 57.760 | 29.980 | 27.780 | 2.200 | 5.358,06 | 2.838,91 |
| 202508 | 58.713 | 30.364 | 28.349 | 2.015 | 5.435,27 | 2.986,55 |
| 202509 | 58.042 | 30.334 | 27.708 | 2.626 | 5.486,39 | 2.986,54 |
| 202510 | 60.592 | 31.000 | 29.592 | 1.408 | 5.411,52 | 2.900,00 |
| 202511 | 51.324 | 27.564 | 23.760 | 3.804 | 5.430,84 | 2.997,27 |
| 202512 | 48.027 | 21.341 | 26.686 | -5.345 | 5.106,84 | 2.614,07 |
| 202601 | 55.496 | 28.692 | 26.804 | 1.888 | 5.472,61 | 2.900,00 |
| 202602 | 53.577 | 27.132 | 26.445 | 687 | 5.176,04 | 2.714,88 |
| 202603 | 59.653 | 30.850 | 28.803 | 2.047 | 5.346,43 | 2.800,00 |
| 202604 | 57.690 | 29.251 | 28.439 | 812 | 5.627,76 | 2.967,49 |
| 202605 | 53.429 | 26.409 | 27.020 | -611 | 5.588,61 | 3.000,00 |
| 202606 | 54.383 | 27.802 | 26.581 | 1.221 | 5.497,17 | 2.947,76 |

## Observações

- A remuneração média e mediana excluem salários iguais a zero e registros com `flag_salario_extremo`.
- A janela permite análise temporal inicial, mas ainda depende da modelagem PostgreSQL para consultas performáticas e dashboard.
- Dez competências apresentaram saldo positivo e duas apresentaram saldo negativo.

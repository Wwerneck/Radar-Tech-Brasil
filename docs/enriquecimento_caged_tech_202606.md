# Enriquecimento CAGED Tech - 202606

## Objetivo

Juntar a base processada do Novo CAGED com o mapeamento versionado de ocupações tech da CBO e gerar uma base filtrada apenas com registros de tecnologia.

## Entradas

```text
data/processed/processed_cagedmov202606.csv
data/external/cbo_tech_mapping.csv
```

## Saída

```text
data/processed/tech_cagedmov202606.csv
```

## Comando

```powershell
python -m src.enrich_caged --processed-caged data/processed/processed_cagedmov202606.csv --mapping data/external/cbo_tech_mapping.csv --output data/processed/tech_cagedmov202606.csv --chunksize 200000
```

## Resultado

| Métrica | Valor |
|---|---:|
| Registros CAGED processados | 4.295.101 |
| Registros tech enriquecidos | 54.383 |
| Ocupações tech mapeadas | 39 |
| Categorias tech | 9 |

## Agregações Geradas

```text
data/processed/agg_tech_overview_202606.csv
data/processed/agg_tech_by_category_202606.csv
data/processed/agg_tech_by_uf_202606.csv
data/processed/agg_tech_by_occupation_202606.csv
```

## Definição das Métricas

- `total_admissoes`: quantidade de registros com `tipo_saldo = admissao`.
- `total_desligamentos`: quantidade de registros com `tipo_saldo = desligamento`.
- `saldo_empregos`: admissões menos desligamentos.
- `remuneracao_media`: média de `salario` considerando apenas salários maiores que zero e sem `flag_salario_extremo`.
- `remuneracao_mediana`: mediana de `salario` considerando apenas salários maiores que zero e sem `flag_salario_extremo`.
- `ocupacoes_analisadas`: quantidade distinta de códigos CBO tech.

## KPIs 202606

| Métrica | Valor |
|---|---:|
| Total de registros tech | 54.383 |
| Admissões | 27.802 |
| Desligamentos | 26.581 |
| Saldo de empregos | 1.221 |
| Remuneração média | 5.497,17 |
| Remuneração mediana | 2.947,76 |
| Ocupações analisadas | 39 |
| Categorias tech | 9 |

## Observações

Estes números representam apenas a competência `202606`. Ainda não devem ser usados para inferir tendências, crescimento mensal ou comportamento anual.


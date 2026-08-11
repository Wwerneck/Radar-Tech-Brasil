# Transformação Inicial do Novo CAGED - 202606

## Objetivo

Criar a primeira camada processada do arquivo `CAGEDMOV202606.txt`, mantendo todos os registros e aplicando somente transformações conservadoras.

## Comando Executado

```powershell
python -m src.process_caged --file data/raw/caged/CAGEDMOV202606.txt --chunksize 100000 --output data/processed/processed_cagedmov202606.csv
```

## Resultado

| Métrica | Valor |
|---|---:|
| Linhas de entrada | 4.295.101 |
| Linhas de saída | 4.295.101 |
| Colunas de saída | 40 |

Nenhum registro foi descartado.

## Transformações Aplicadas

- Renomeação das colunas para ASCII e `snake_case`.
- Seleção das 28 colunas analíticas candidatas identificadas na inspeção.
- Conversão de inteiros para tipo nullable.
- Conversão de `salario`, `valor_salario_fixo` e `horas_contratuais` de decimal brasileiro para número.
- Criação de `ano`, `mes` e `ano_mes`.
- Criação de `tipo_saldo` a partir de `saldo_movimentacao`.
- Criação de `faixa_etaria`.
- Criação de flags de qualidade.

## Flags de Qualidade

| Flag | Registros |
|---|---:|
| `flag_idade_ausente` | 1.449 |
| `flag_idade_invalida` | 0 |
| `flag_salario_zero` | 49.288 |
| `flag_salario_extremo` | 1.849 |
| `flag_horas_invalidas` | 0 |
| `flag_uf_invalida` | 1.676 |
| `flag_cbo_invalida` | 0 |

## Distribuição de Tipo de Saldo

| Tipo | Registros |
|---|---:|
| admissao | 2.220.131 |
| desligamento | 2.074.970 |

## Distribuição de Faixa Etária

| Faixa | Registros |
|---|---:|
| Ate 20 | 584.700 |
| 21-25 | 797.567 |
| 26-30 | 726.033 |
| 31-35 | 581.044 |
| 36-40 | 502.368 |
| 41-50 | 724.608 |
| 51+ | 377.332 |
| Nao informado | 1.449 |

## Decisões

- Salário zero e salário acima de 100.000 foram marcados como flags, não excluídos.
- UFs fora dos 27 códigos oficiais foram marcadas como inválidas. O código observado deve ser investigado contra o layout oficial antes de qualquer exclusão.
- A tradução detalhada de `tipo_movimentacao` ainda não foi feita, pois depende do layout/dicionário oficial.
- A classificação CBO tech ainda não foi aplicada nesta etapa.


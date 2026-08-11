# Profiling Completo do Novo CAGED - 202606

## Execução

Arquivo analisado:

```text
data/raw/caged/CAGEDMOV202606.txt
```

Comando:

```powershell
python -m src.profile_caged --file data/raw/caged/CAGEDMOV202606.txt --chunksize 100000
```

Resultado JSON:

```text
data/processed/profile_cagedmov202606.json
```

## Resumo

| Métrica | Valor |
|---|---:|
| Linhas processadas | 4.295.101 |
| Tamanho do arquivo TXT | 427,31 MB |
| Separador | `;` |
| Encoding | `utf-8` |
| Colunas | 28 |
| Duplicadas dentro das partições de leitura | 10.485 |

Observação: a contagem de duplicadas foi calculada dentro de cada chunk, não globalmente entre chunks. A deduplicação final exige definição de chave natural ou hash de linha.

## Valores Ausentes

Somente `idade` apresentou valores ausentes no arquivo completo:

| Campo | Nulos |
|---|---:|
| `idade` | 1.449 |

Nenhuma linha deve ser removida automaticamente por causa disso. A primeira regra proposta é preservar o registro e marcar a faixa etária como `Não informado` quando a idade estiver ausente.

## Ranges Numéricos

| Campo | Mínimo | Máximo |
|---|---:|---:|
| `idade` | 14 | 98 |
| `horascontratuais` | 0 | 60 |
| `salário` | 0,00 | 30.063.428,00 |
| `valorsaláriofixo` | 0,00 | 30.063.428,00 |

Decisão pendente: salário igual a zero e salários extremos devem ser tratados como valores a investigar, não removidos automaticamente.

## Movimentações

Distribuição de `saldomovimentação`:

| Código | Quantidade |
|---:|---:|
| 1 | 2.220.131 |
| -1 | 2.074.970 |

Distribuição de `tipomovimentação`:

| Código | Quantidade |
|---:|---:|
| 97 | 2.218.680 |
| 31 | 882.797 |
| 40 | 760.047 |
| 43 | 338.644 |
| 32 | 63.327 |
| 90 | 20.812 |
| 60 | 6.098 |
| 98 | 2.526 |
| 35 | 1.451 |
| 50 | 614 |
| 33 | 105 |

A tradução dos códigos depende do layout oficial do Novo CAGED e não será inferida manualmente.

## Cardinalidade

| Campo | Valores distintos |
|---|---:|
| `competênciamov` | 1 |
| `uf` | 28 |
| `município` | 5.488 |
| `cbo2002ocupação` | 2.497 |
| `tipomovimentação` | 11 |
| `saldomovimentação` | 2 |
| `idade` | 84 |
| `salário` | 272.951 |

## Top UFs por Quantidade de Registros

| Código UF | Quantidade |
|---:|---:|
| 35 | 1.381.985 |
| 31 | 457.529 |
| 41 | 325.677 |
| 33 | 283.714 |
| 42 | 273.188 |
| 43 | 247.532 |
| 29 | 165.669 |
| 52 | 159.676 |
| 23 | 115.453 |
| 26 | 109.624 |

Esses códigos seguem padrão IBGE, mas a tabela de domínio deve ser criada explicitamente na etapa de transformação.

## Decisões para a Próxima Etapa

- Normalizar nomes de colunas para ASCII no dataset processado.
- Converter `salário`, `valorsaláriofixo` e `horascontratuais` para número decimal.
- Criar validações para idade, salário, horas, competência, UF, CBO e códigos de movimentação.
- Preservar registros com valores suspeitos e criar flags de qualidade.
- Não traduzir códigos categóricos sem layout oficial ou tabela de domínio versionada.
- Criar uma versão processada inicial filtrando apenas colunas analíticas candidatas.


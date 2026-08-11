# Dicionário de Dados

## Base Processada CAGED

Arquivo de referência:

```text
data/processed/processed_cagedmovYYYYMM.csv
```

| Campo | Tipo lógico | Origem | Descrição | Transformação | Exemplo |
|---|---|---|---|---|---|
| `competencia_mov` | inteiro | `competênciamov` | Competência da movimentação. | Renomeado. | `202606` |
| `regiao` | inteiro | `região` | Código da região. | Renomeado. | `3` |
| `uf` | inteiro | `uf` | Código IBGE da UF. | Renomeado. | `35` |
| `municipio` | inteiro | `município` | Código IBGE do município. | Renomeado. | `355030` |
| `secao` | texto | `seção` | Seção CNAE. | Espaços removidos. | `J` |
| `subclasse` | inteiro | `subclasse` | Subclasse CNAE. | Renomeado. | `6201501` |
| `saldo_movimentacao` | inteiro | `saldomovimentação` | Indicador sintético de admissão ou desligamento. | Renomeado. | `1` |
| `cbo_2002_ocupacao` | inteiro | `cbo2002ocupação` | Código CBO 2002. | Renomeado. | `212405` |
| `categoria` | inteiro | `categoria` | Código da categoria do vínculo. | Renomeado. | `101` |
| `grau_instrucao` | inteiro | `graudeinstrução` | Código de escolaridade. | Renomeado. | `9` |
| `idade` | inteiro nullable | `idade` | Idade do trabalhador. | Convertido para inteiro nullable. | `31` |
| `horas_contratuais` | decimal | `horascontratuais` | Horas contratuais. | Vírgula decimal convertida. | `44.00` |
| `raca_cor` | inteiro | `raçacor` | Código de raça/cor. | Renomeado. | `1` |
| `sexo` | inteiro | `sexo` | Código de sexo. | Renomeado. | `1` |
| `tipo_empregador` | inteiro | `tipoempregador` | Tipo de empregador. | Renomeado. | `0` |
| `tipo_estabelecimento` | inteiro | `tipoestabelecimento` | Tipo de estabelecimento. | Renomeado. | `1` |
| `tipo_movimentacao` | inteiro | `tipomovimentação` | Código detalhado da movimentação. | Renomeado. | `97` |
| `tipo_deficiencia` | inteiro | `tipodedeficiência` | Código de deficiência. | Renomeado. | `0` |
| `ind_trab_intermitente` | inteiro | `indtrabintermitente` | Indicador de trabalho intermitente. | Renomeado. | `0` |
| `ind_trab_parcial` | inteiro | `indtrabparcial` | Indicador de trabalho parcial. | Renomeado. | `0` |
| `salario` | decimal | `salário` | Salário informado. | Vírgula decimal convertida. | `5000.00` |
| `tamanho_estabelecimento_jan` | inteiro | `tamestabjan` | Tamanho do estabelecimento em janeiro. | Renomeado. | `4` |
| `indicador_aprendiz` | inteiro | `indicadoraprendiz` | Indicador de aprendiz. | Renomeado. | `0` |
| `origem_informacao` | inteiro | `origemdainformação` | Origem da informação. | Renomeado. | `1` |
| `competencia_dec` | inteiro | `competênciadec` | Competência de declaração. | Renomeado. | `202606` |
| `indicador_fora_prazo` | inteiro | `indicadordeforadoprazo` | Indicador de declaração fora do prazo. | Renomeado. | `0` |
| `unidade_salario_codigo` | inteiro | `unidadesaláriocódigo` | Unidade de salário. | Renomeado. | `5` |
| `valor_salario_fixo` | decimal | `valorsaláriofixo` | Valor fixo de salário. | Vírgula decimal convertida. | `5000.00` |

## Colunas Derivadas

| Campo | Tipo lógico | Origem | Descrição | Transformação | Exemplo |
|---|---|---|---|---|---|
| `ano` | inteiro | `competencia_mov` | Ano da competência. | Divisão inteira por 100. | `2026` |
| `mes` | inteiro | `competencia_mov` | Mês da competência. | Módulo por 100. | `6` |
| `ano_mes` | texto | `competencia_mov` | Competência em texto. | Conversão para string. | `202606` |
| `tipo_saldo` | texto | `saldo_movimentacao` | Tipo sintético de movimento. | `1 = admissao`, `-1 = desligamento`. | `admissao` |
| `faixa_etaria` | texto | `idade` | Faixa etária inicial. | Regra em `src/transform.py`. | `26-30` |

## Flags de Qualidade

| Campo | Tipo lógico | Regra |
|---|---|---|
| `flag_idade_ausente` | booleano | `idade` nula. |
| `flag_idade_invalida` | booleano | `idade < 14` ou `idade > 100`. |
| `flag_salario_zero` | booleano | `salario = 0`. |
| `flag_salario_extremo` | booleano | `salario > 100000`. |
| `flag_horas_invalidas` | booleano | `horas_contratuais < 0` ou `horas_contratuais > 60`. |
| `flag_uf_invalida` | booleano | UF fora dos 27 códigos oficiais. |
| `flag_cbo_invalida` | booleano | CBO fora do padrão numérico esperado. |

## Base Tech Enriquecida

Arquivo de referência:

```text
data/processed/tech_cagedmovYYYYMM.csv
```

| Campo | Tipo lógico | Origem | Descrição |
|---|---|---|---|
| `codigo_cbo` | texto | CBO mapping | Código CBO com seis dígitos. |
| `ocupacao` | texto | CBO oficial | Título oficial da ocupação. |
| `familia_cbo` | texto | CBO oficial | Código da família CBO. |
| `familia_cbo_titulo` | texto | CBO oficial | Título oficial da família CBO. |
| `categoria_tech` | texto | `cbo_tech_mapping.csv` | Categoria analítica de tecnologia. |
| `criterio` | texto | `cbo_tech_mapping.csv` | Justificativa de inclusão no recorte tech. |
| `versao_mapeamento` | texto | `cbo_tech_mapping.csv` | Versão do mapeamento CBO tech. |

## Agregados Mensais

Arquivos de referência:

```text
data/processed/agg_tech_overview_mensal.csv
data/processed/agg_tech_by_category_mensal.csv
data/processed/agg_tech_by_uf_mensal.csv
data/processed/agg_tech_by_occupation_mensal.csv
data/processed/agg_tech_by_age_group_mensal.csv
data/processed/agg_tech_by_education_mensal.csv
data/processed/agg_tech_by_uf_mensal_enriched.csv
data/processed/agg_tech_by_education_mensal_enriched.csv
```

| Campo | Descrição |
|---|---|
| `competencia` | Competência mensal no formato `YYYYMM`. |
| `total_registros_tech` | Total de registros classificados como tecnologia no mês. |
| `total_admissoes` | Total de admissões tech no mês. |
| `total_desligamentos` | Total de desligamentos tech no mês. |
| `saldo_empregos` | Admissões menos desligamentos. |
| `remuneracao_media` | Média salarial com salários válidos. |
| `remuneracao_mediana` | Mediana salarial com salários válidos. |
| `ocupacoes_analisadas` | Quantidade de ocupações CBO tech distintas. |
| `categorias_tech` | Quantidade de categorias tech distintas. |
| `registros` | Quantidade de registros no agrupamento. |
| `admissoes` | Admissões no agrupamento. |
| `desligamentos` | Desligamentos no agrupamento. |
| `uf_sigla` | Sigla da UF adicionada por `data/external/uf_mapping.csv`. |
| `uf_nome` | Nome da UF adicionado por `data/external/uf_mapping.csv`. |
| `regiao_nome` | Nome da região adicionado por `data/external/uf_mapping.csv`. |
| `escolaridade` | Rótulo de escolaridade adicionado por `data/external/education_mapping.csv`. |

## Tabelas de Domínio

```text
data/external/uf_mapping.csv
data/external/education_mapping.csv
data/external/movement_type_mapping.csv
data/external/gender_mapping.csv
data/external/race_color_mapping.csv
data/external/salary_unit_mapping.csv
```

Esses arquivos tornam o enriquecimento reproduzível e evitam dicionários hardcoded no dashboard.

Os domínios marcados como `pendente_layout_oficial` devem ser revisados contra o layout oficial antes de uso analítico definitivo.

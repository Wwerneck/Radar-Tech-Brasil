# Colunas Processadas do CAGED

| Campo | Origem | Descrição |
|---|---|---|
| `competencia_mov` | `competênciamov` | Competência da movimentação no formato `YYYYMM`. |
| `regiao` | `região` | Código da região. |
| `uf` | `uf` | Código da unidade federativa. |
| `municipio` | `município` | Código do município. |
| `secao` | `seção` | Seção CNAE. |
| `subclasse` | `subclasse` | Subclasse CNAE. |
| `saldo_movimentacao` | `saldomovimentação` | Indicador sintético de admissão ou desligamento. |
| `cbo_2002_ocupacao` | `cbo2002ocupação` | Código CBO 2002 da ocupação. |
| `categoria` | `categoria` | Código de categoria do vínculo. |
| `grau_instrucao` | `graudeinstrução` | Código de escolaridade. |
| `idade` | `idade` | Idade do trabalhador. |
| `horas_contratuais` | `horascontratuais` | Horas contratuais convertidas para número. |
| `raca_cor` | `raçacor` | Código de raça/cor. |
| `sexo` | `sexo` | Código de sexo. |
| `tipo_empregador` | `tipoempregador` | Código de tipo de empregador. |
| `tipo_estabelecimento` | `tipoestabelecimento` | Código de tipo de estabelecimento. |
| `tipo_movimentacao` | `tipomovimentação` | Código detalhado da movimentação. |
| `tipo_deficiencia` | `tipodedeficiência` | Código de tipo de deficiência. |
| `ind_trab_intermitente` | `indtrabintermitente` | Indicador de trabalho intermitente. |
| `ind_trab_parcial` | `indtrabparcial` | Indicador de trabalho parcial. |
| `salario` | `salário` | Salário convertido para número. |
| `tamanho_estabelecimento_jan` | `tamestabjan` | Faixa de tamanho do estabelecimento em janeiro. |
| `indicador_aprendiz` | `indicadoraprendiz` | Indicador de aprendiz. |
| `origem_informacao` | `origemdainformação` | Origem da informação. |
| `competencia_dec` | `competênciadec` | Competência de declaração. |
| `indicador_fora_prazo` | `indicadordeforadoprazo` | Indicador de declaração fora do prazo. |
| `unidade_salario_codigo` | `unidadesaláriocódigo` | Unidade de salário informada. |
| `valor_salario_fixo` | `valorsaláriofixo` | Valor de salário fixo convertido para número. |
| `ano` | Derivada | Ano extraído de `competencia_mov`. |
| `mes` | Derivada | Mês extraído de `competencia_mov`. |
| `ano_mes` | Derivada | Competência como texto `YYYYMM`. |
| `tipo_saldo` | Derivada | `admissao` quando saldo é `1`; `desligamento` quando saldo é `-1`. |
| `faixa_etaria` | Derivada | Faixa etária inicial para análise exploratória. |
| `flag_idade_ausente` | Derivada | Marca idade ausente. |
| `flag_idade_invalida` | Derivada | Marca idade menor que 14 ou maior que 100. |
| `flag_salario_zero` | Derivada | Marca salário igual a zero. |
| `flag_salario_extremo` | Derivada | Marca salário maior que 100.000. |
| `flag_horas_invalidas` | Derivada | Marca horas contratuais fora de 0 a 60. |
| `flag_uf_invalida` | Derivada | Marca UF fora dos 27 códigos oficiais. |
| `flag_cbo_invalida` | Derivada | Marca CBO fora do padrão numérico esperado. |


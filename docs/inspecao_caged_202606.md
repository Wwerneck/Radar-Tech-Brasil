# Inspeção Inicial do Novo CAGED - 202606

## Arquivo Inspecionado

| Item | Valor |
|---|---|
| Arquivo compactado | `CAGEDMOV202606.7z` |
| Arquivo extraído | `CAGEDMOV202606.txt` |
| Origem | FTP oficial do MTE |
| Competência | `202606` |
| Tamanho do TXT | 427,31 MB |
| Separador detectado | `;` |
| Encoding detectado | `utf-8` |
| Linhas da amostra | 1.000 |
| Hash SHA-256 do TXT | `ff9ee116b70fd13e3978358f71e48a915d42256c2d1f877adbaa82f0b8610131` |

## Colunas Encontradas

```text
competênciamov
região
uf
município
seção
subclasse
saldomovimentação
cbo2002ocupação
categoria
graudeinstrução
idade
horascontratuais
raçacor
sexo
tipoempregador
tipoestabelecimento
tipomovimentação
tipodedeficiência
indtrabintermitente
indtrabparcial
salário
tamestabjan
indicadoraprendiz
origemdainformação
competênciadec
indicadordeforadoprazo
unidadesaláriocódigo
valorsaláriofixo
```

## Tipos Observados na Amostra

A maior parte das colunas foi inferida como `int64`. As colunas abaixo vieram como texto por usarem vírgula decimal:

```text
horascontratuais
salário
valorsaláriofixo
```

## Valores Nulos na Amostra

Nenhuma coluna apresentou valores nulos nas 1.000 linhas analisadas.

Isso não autoriza assumir ausência de nulos no arquivo completo. A validação completa será feita em leitura por chunks.

## Cardinalidade na Amostra

Campos com cardinalidade especialmente relevantes:

| Campo | Valores distintos na amostra |
|---|---:|
| `competênciamov` | 1 |
| `região` | 5 |
| `uf` | 26 |
| `município` | 449 |
| `seção` | 19 |
| `saldomovimentação` | 2 |
| `cbo2002ocupação` | 263 |
| `graudeinstrução` | 11 |
| `idade` | 55 |
| `tipomovimentação` | 7 |
| `salário` | 697 |

## Seleção Inicial de Colunas Candidatas

Estas colunas parecem suficientes para a primeira versão analítica, sujeitas à validação no arquivo completo:

| Coluna original | Uso pretendido |
|---|---|
| `competênciamov` | dimensão tempo da movimentação |
| `competênciadec` | competência declarada, útil para auditoria |
| `indicadordeforadoprazo` | controle de carga e revisão |
| `região` | dimensão geográfica |
| `uf` | dimensão geográfica |
| `município` | dimensão geográfica |
| `seção` | setor econômico agregado |
| `subclasse` | setor econômico detalhado |
| `saldomovimentação` | admissão/desligamento/saldo |
| `tipomovimentação` | classificação do evento trabalhista |
| `cbo2002ocupação` | ligação com CBO e categorias tech |
| `categoria` | categoria do trabalhador/vínculo |
| `graudeinstrução` | perfil profissional |
| `idade` | perfil profissional e faixa etária |
| `sexo` | perfil profissional, se documentado e utilizado com cuidado |
| `horascontratuais` | contexto do vínculo |
| `salário` | remuneração informada |
| `valorsaláriofixo` | remuneração fixa informada |
| `unidadesaláriocódigo` | unidade de referência salarial |
| `indtrabintermitente` | característica do vínculo |
| `indtrabparcial` | característica do vínculo |
| `indicadoraprendiz` | identificação de aprendizes |

## Decisões Provisórias

- A versão inicial deve começar com `CAGEDMOV`, deixando `CAGEDFOR` e `CAGEDEXC` para a etapa de revisão incremental.
- O período recomendado para a primeira versão é `202507` a `202606`, as 12 competências completas mais recentes encontradas no FTP em 11/08/2026.
- As colunas com acentos serão normalizadas apenas no dataset processado. Os arquivos brutos permanecem intactos.
- Salário e horas devem ser convertidos de texto com vírgula decimal para número decimal.
- Códigos categóricos não devem ser traduzidos sem consultar layout/dicionário oficial.

## Próxima Etapa

Construir profiling por chunks para o arquivo completo, incluindo:

- total de linhas;
- nulos por coluna;
- cardinalidade global;
- mínimos e máximos de idade, salário e horas;
- frequências de códigos categóricos;
- validação de competência, UF, CBO e movimentação.


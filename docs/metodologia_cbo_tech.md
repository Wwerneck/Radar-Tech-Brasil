# Metodologia de Classificação CBO Tech

## Objetivo

Identificar ocupações de tecnologia no Novo CAGED usando a CBO oficial como referência, com critérios explícitos e versionados.

## Fontes

- `data/raw/cbo/cbo2002_ocupacao.csv`
- `data/raw/cbo/cbo2002_familia.csv`
- `data/processed/processed_cagedmov202606.csv`

## Arquivo Gerado

```text
data/external/cbo_tech_mapping.csv
```

## Versão

```text
v0.2
```

## Critério Geral

A classificação inicial usa uma lista explícita de códigos CBO, validada contra a tabela oficial de ocupações e enriquecida com a família CBO oficial.

Foram incluídas ocupações cuja descrição ou família indica atuação direta em:

- desenvolvimento de sistemas;
- dados e banco de dados;
- infraestrutura computacional;
- redes e comunicação de dados;
- suporte técnico de TI;
- segurança da informação;
- gestão de tecnologia;
- pesquisa ou docência superior em computação.

## O Que Foi Evitado

Não foi usada apenas busca por palavras-chave. A busca textual foi utilizada somente para levantar candidatos, porque termos como `rede`, `sistema` ou `programação` geram falsos positivos em ocupações não relacionadas a tecnologia.

Exemplos de falsos positivos evitados:

- ocupações de pesca com termo `rede`;
- irrigação com termo `sistema`;
- programação e controle de produção fora de TI;
- programação visual gráfica sem vínculo direto com tecnologia da informação.

## Categorias

| Categoria | Definição |
|---|---|
| Desenvolvimento de Software | Ocupações de análise, desenvolvimento, testes e engenharia de aplicações. |
| Dados e Banco de Dados | Ocupações de ciência de dados e administração de banco de dados. |
| Infraestrutura | Ocupações de equipamentos, sistemas operacionais, operação computacional e hardware. |
| Redes | Ocupações de redes, telecomunicações e comunicação de dados. |
| Suporte Tecnico | Ocupações de atendimento, suporte computacional e manutenção de informática. |
| Seguranca da Informacao | Ocupações de segurança da informação, proteção de dados e governança relacionada. |
| Cloud e DevOps | Ocupações de arquitetura de soluções de TI. |
| Gestao de Tecnologia | Cargos de gestão, coordenação e direção de TI. |
| Outras ocupacoes de Tecnologia | Pesquisa, docência e ocupações técnicas correlatas que não se encaixam nas categorias anteriores. |

## Cobertura em 202606

| Categoria | Ocupações | Registros no CAGED 202606 |
|---|---:|---:|
| Cloud e DevOps | 1 | 267 |
| Dados e Banco de Dados | 2 | 658 |
| Desenvolvimento de Software | 5 | 17.447 |
| Gestao de Tecnologia | 7 | 2.787 |
| Infraestrutura | 5 | 3.454 |
| Outras ocupacoes de Tecnologia | 2 | 189 |
| Redes | 11 | 14.620 |
| Seguranca da Informacao | 3 | 811 |
| Suporte Tecnico | 3 | 14.150 |

Total de registros mapeados como tecnologia em `202606`: 54.383.

## Revisão v0.2

A versão `v0.2` manteve a lista conservadora de códigos da `v0.1` e adicionou o campo `status_revisao`.

Não houve inclusão automática por palavra-chave. A decisão foi preservar rastreabilidade e evitar falsos positivos até uma revisão qualitativa mais ampla com layout oficial e documentação complementar.

## Limitações

- O mapeamento inicial é conservador e pode subcontar ocupações híbridas.
- Alguns cargos de engenharia, eletrônica ou telecomunicações podem envolver tecnologia, mas só foram incluídos quando a ocupação tem relação direta com TI, computação, redes ou comunicação de dados.
- A CBO não descreve stack, senioridade, modelo remoto ou especialidade moderna como DevOps em todos os casos.
- A classificação deve ser revisada conforme novas competências e análises qualitativas.

## Processo de Revisão

Toda alteração no mapeamento deve registrar:

- código CBO;
- ocupação oficial;
- família CBO;
- categoria tech;
- justificativa;
- versão do mapeamento.

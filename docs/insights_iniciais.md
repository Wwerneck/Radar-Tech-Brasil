# Insights Iniciais

## Escopo

Período analisado: `202507` a `202606`.

## Insight 1

O mercado tech mapeado apresentou saldo positivo na janela analisada.

Evidência: foram 340.719 admissões e 327.967 desligamentos, com saldo de 12.752 vínculos.

Possível explicação: as ocupações classificadas como tecnologia mantiveram volume de admissões superior ao de desligamentos na maior parte dos meses.

Implicação: há sinal de expansão líquida no recorte analisado.

Limitação: isso não prova causalidade e depende do mapeamento CBO tech `v0.1`.

## Insight 2

O saldo mensal não foi uniformemente positivo.

Evidência: o maior saldo ocorreu em `202511` com 3.804; o menor ocorreu em `202512` com -5.345.

Possível explicação: movimentos sazonais e ciclos de contratação podem afetar competências específicas.

Implicação: análises de tendência devem usar série mensal, não apenas totais acumulados.

Limitação: a janela possui 12 competências e ainda não incorpora RAIS ou outras fontes.

## Insight 3

A categoria com maior volume foi `Desenvolvimento de Software`.

Evidência: a categoria somou 219.152 registros e saldo de 6.366.

Possível explicação: ocupações de maior capilaridade tendem a concentrar mais movimentações formais.

Implicação: o dashboard deve permitir separar volume de saldo, pois uma categoria grande não necessariamente tem o maior saldo relativo.

Limitação: categorias dependem da metodologia CBO tech versionada.

## Insight 4

A ocupação com maior volume foi `Analista de desenvolvimento de sistemas`.

Evidência: CBO `212405` teve 138.835 registros no período.

Possível explicação: cargos generalistas de análise e desenvolvimento aparecem com alta frequência nos registros formais.

Implicação: rankings por ocupação são úteis para priorizar análises de salário, localidade e saldo.

Limitação: CBO não captura stack, senioridade nem modalidade remota.

## Insight 5

A UF com maior volume foi código `35`.

Evidência: a UF somou 277.644 registros e saldo de 6.252.

Possível explicação: concentração econômica e populacional pode influenciar a distribuição dos vínculos formais.

Implicação: a análise geográfica deve comparar volume, saldo e remuneração separadamente.

Limitação: a tabela atual ainda usa códigos de UF; a próxima melhoria é enriquecer com siglas e regiões nominais.

## Nota Sobre Remuneração

Média e mediana salarial usam apenas salários maiores que zero e removem registros marcados com `flag_salario_extremo`.

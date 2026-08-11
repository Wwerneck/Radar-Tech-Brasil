# Metodologia

## Fonte dos Dados

A primeira versão do Radar Tech Brasil usará microdados públicos do Novo CAGED e a tabela da Classificação Brasileira de Ocupações (CBO).

## Período Analisado

Resultado ainda não calculado. O período será documentado após inclusão dos primeiros arquivos reais em `data/raw/caged/`.

## Critérios

As regras iniciais de seleção de colunas e transformação foram definidas após inspeção do arquivo `CAGEDMOV202606.txt`.

A classificação inicial de ocupações de tecnologia está documentada em `docs/metodologia_cbo_tech.md` e versionada em `data/external/cbo_tech_mapping.csv`.

## Limitações

Esta versão ainda trabalha com uma competência do Novo CAGED. Resultados de tendência, crescimento e séries temporais dependem da carga das 12 competências planejadas.

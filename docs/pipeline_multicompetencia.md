# Pipeline Multi-Competência

## Objetivo

Preparar a execução reproduzível da janela inicial de 12 competências do Novo CAGED:

```text
202507 a 202606
```

## Orquestrador

```text
src/pipeline_multi.py
```

O pipeline executa, por competência:

```text
download
extração
processamento
enriquecimento CBO tech
agregações
manifesto
```

## Idempotência

O arquivo abaixo registra etapas concluídas:

```text
data/processed/manifest.json
```

Cada etapa recebe uma chave:

```text
download:YYYYMM
extract:YYYYMM
process:YYYYMM
enrich:YYYYMM
aggregate:YYYYMM
```

Ao executar novamente, etapas marcadas como `complete` são puladas, a menos que seja usado `--overwrite`.

## Comandos

Rodar uma competência já baixada localmente:

```powershell
python -m src.pipeline_multi --competences 202606 --skip-download
```

Rodar uma competência com download:

```powershell
python -m src.pipeline_multi --competences 202605
```

Rodar a janela inicial completa:

```powershell
python -m src.pipeline_multi
```

Forçar reprocessamento:

```powershell
python -m src.pipeline_multi --competences 202606 --overwrite
```

## Validação Realizada

Foi executado o pipeline para `202606` usando arquivos locais.

Resultado:

- `processed_cagedmov202606.csv` regenerado;
- `tech_cagedmov202606.csv` regenerado;
- agregações `202606` regeneradas;
- `manifest.json` criado;
- segunda execução pulou etapas já concluídas.

## Observação de Espaço em Disco

Cada competência pode gerar arquivos grandes. A primeira competência gerou:

```text
processed_cagedmov202606.csv: ~752 MB
tech_cagedmov202606.csv: ~19 MB
```

Antes de rodar as 12 competências completas, confirme espaço disponível em disco.


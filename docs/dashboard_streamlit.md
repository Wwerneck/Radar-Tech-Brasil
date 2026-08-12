# Dashboard Streamlit

## Arquivo

```text
dashboard/app.py
```

## Como Executar

```powershell
streamlit run dashboard/app.py
```

Ou usando o Python do ambiente virtual:

```powershell
.\.venv\Scripts\streamlit.exe run dashboard/app.py
```

## Dados Consumidos

```text
data/processed/agg_tech_overview_mensal.csv
data/processed/agg_tech_by_category_mensal.csv
data/processed/agg_tech_by_uf_mensal_enriched.csv
data/processed/agg_tech_by_occupation_mensal.csv
data/processed/agg_tech_by_age_group_mensal.csv
data/processed/agg_tech_by_education_mensal_enriched.csv
data/external/uf_centroids.csv
```

## Paginas

- Visao Geral
- Mercado
- Profissoes
- Salarios
- Estados
- Perfil Profissional
- Insights
- Metodologia

## Recursos

- Periodo exibido em formato brasileiro `MM/AAAA`.
- Filtros opcionais por categoria, regiao, UF, ocupacao, faixa etaria e escolaridade.
- Cards de contexto com maior e menor saldo mensal, categoria lider e UF com maior volume.
- Rotulos amigaveis nas metricas dos graficos.
- Evolucao salarial com legenda explicativa para media e mediana.
- Downloads CSV das principais tabelas analiticas.
- Mapa geografico por UF com volume e saldo de empregos.
- Aba de insights automaticos com leitura descritiva do periodo filtrado.
- Aba de metodologia com fontes, recorte, criterios salariais e limitacoes.

## Observacao

A versao atual le agregados CSV locais. Quando o PostgreSQL estiver disponivel, a camada de leitura pode ser substituida por queries nas views `radar.vw_*`.

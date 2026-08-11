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
data/processed/agg_tech_by_uf_mensal.csv
data/processed/agg_tech_by_occupation_mensal.csv
data/processed/agg_tech_by_age_group_mensal.csv
data/processed/agg_tech_by_education_mensal.csv
```

## Páginas

- Visão Geral
- Mercado
- Profissões
- Salários
- Estados
- Perfil Profissional
- Metodologia

## Observação

A primeira versão lê agregados CSV locais. Quando o PostgreSQL estiver disponível, a camada de leitura pode ser substituída por queries nas views `radar.vw_*`.

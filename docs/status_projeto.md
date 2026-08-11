# Status do Projeto

## Concluído

- Estrutura profissional do projeto.
- Ambiente Python com dependências versionadas.
- Download oficial da CBO.
- Download oficial do Novo CAGED.
- Inspeção real de arquivo CAGED.
- Profiling completo por chunks.
- Transformação inicial do CAGED.
- Mapeamento versionado CBO tech `v0.2`.
- Enriquecimento da base tech.
- Pipeline multi-competência para `202507` a `202606`.
- Agregados mensais consolidados.
- Modelagem PostgreSQL inicial.
- Dashboard Streamlit inicial.
- Tabelas de domínio para UF e escolaridade.
- Insights iniciais documentados.
- Testes automatizados.

## Dados Processados

| Item | Valor |
|---|---:|
| Competências | 12 |
| Janela | `202507` a `202606` |
| Registros tech | 668.686 |
| Admissões tech | 340.719 |
| Desligamentos tech | 327.967 |
| Saldo tech | 12.752 |

## Validação Atual

```text
17 tests passed
```

## Pendências Técnicas

- Executar carga real no PostgreSQL quando houver servidor disponível.
- Implementar carga detalhada da fato `radar.fato_movimentacao_tech`.
- Revisar domínios pendentes contra layout oficial.
- Expandir notebook EDA com novas análises conforme o projeto evoluir.
- Refinar dashboard visualmente e migrar leitura para PostgreSQL.

## Nota de Versionamento CBO

O arquivo `data/external/cbo_tech_mapping.csv` está em `v0.2`. Como a lista de códigos foi preservada em relação à versão anterior, os agregados consolidados não foram alterados numericamente.

## Próximos Passos Recomendados

1. Criar tabelas de domínio para UF, região, escolaridade e movimentação.
2. Enriquecer agregados e dashboard com nomes amigáveis.
3. Criar notebook `01_exploracao.ipynb` com narrativa analítica.
4. Implementar carga PostgreSQL detalhada por chunks.
5. Preparar README final para GitHub.

CREATE OR REPLACE VIEW radar.vw_kpis_mensais AS
SELECT
    competencia,
    total_registros_tech,
    total_admissoes,
    total_desligamentos,
    saldo_empregos,
    remuneracao_media,
    remuneracao_mediana,
    ocupacoes_analisadas,
    categorias_tech
FROM radar.agg_tech_overview_mensal;

CREATE OR REPLACE VIEW radar.vw_saldo_por_categoria AS
SELECT
    competencia,
    categoria_tech,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos,
    remuneracao_media,
    remuneracao_mediana
FROM radar.agg_tech_by_category_mensal;

CREATE OR REPLACE VIEW radar.vw_saldo_por_uf AS
SELECT
    competencia,
    uf,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos,
    remuneracao_media,
    remuneracao_mediana
FROM radar.agg_tech_by_uf_mensal;

CREATE OR REPLACE VIEW radar.vw_saldo_por_uf_enriched AS
SELECT
    competencia,
    uf,
    uf_sigla,
    uf_nome,
    regiao_nome,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos,
    remuneracao_media,
    remuneracao_mediana
FROM radar.agg_tech_by_uf_mensal_enriched;

CREATE OR REPLACE VIEW radar.vw_ocupacoes_tech AS
SELECT
    o.codigo_cbo,
    o.ocupacao,
    o.familia_cbo,
    o.familia_cbo_titulo,
    o.categoria_tech,
    o.criterio,
    o.versao_mapeamento
FROM radar.dim_ocupacao AS o;

CREATE OR REPLACE VIEW radar.vw_perfil_faixa_etaria AS
SELECT
    competencia,
    faixa_etaria,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos
FROM radar.agg_tech_by_age_group_mensal;

CREATE OR REPLACE VIEW radar.vw_perfil_escolaridade AS
SELECT
    competencia,
    grau_instrucao,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos
FROM radar.agg_tech_by_education_mensal;

CREATE OR REPLACE VIEW radar.vw_perfil_escolaridade_enriched AS
SELECT
    competencia,
    grau_instrucao,
    escolaridade,
    registros,
    admissoes,
    desligamentos,
    saldo_empregos
FROM radar.agg_tech_by_education_mensal_enriched;

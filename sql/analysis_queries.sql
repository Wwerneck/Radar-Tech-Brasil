-- KPIs mensais da janela analisada.
SELECT
    competencia,
    total_admissoes,
    total_desligamentos,
    saldo_empregos,
    remuneracao_media,
    remuneracao_mediana
FROM radar.vw_kpis_mensais
ORDER BY competencia;

-- Saldo acumulado por categoria tech.
SELECT
    categoria_tech,
    SUM(admissoes) AS admissoes,
    SUM(desligamentos) AS desligamentos,
    SUM(saldo_empregos) AS saldo_empregos,
    ROUND(AVG(remuneracao_media), 2) AS media_das_medias_mensais
FROM radar.vw_saldo_por_categoria
GROUP BY categoria_tech
ORDER BY saldo_empregos DESC;

-- Ranking de ocupações por admissões.
SELECT
    codigo_cbo,
    ocupacao,
    categoria_tech,
    SUM(admissoes) AS admissoes,
    SUM(desligamentos) AS desligamentos,
    SUM(saldo_empregos) AS saldo_empregos
FROM radar.agg_tech_by_occupation_mensal
GROUP BY codigo_cbo, ocupacao, categoria_tech
ORDER BY admissoes DESC
LIMIT 20;

-- Estados com maior saldo acumulado.
SELECT
    uf,
    SUM(admissoes) AS admissoes,
    SUM(desligamentos) AS desligamentos,
    SUM(saldo_empregos) AS saldo_empregos
FROM radar.vw_saldo_por_uf
GROUP BY uf
ORDER BY saldo_empregos DESC
LIMIT 20;

-- Meses com saldo negativo.
SELECT
    competencia,
    total_admissoes,
    total_desligamentos,
    saldo_empregos
FROM radar.vw_kpis_mensais
WHERE saldo_empregos < 0
ORDER BY competencia;

-- Perfil por faixa etária na janela.
SELECT
    faixa_etaria,
    SUM(registros) AS registros,
    SUM(admissoes) AS admissoes,
    SUM(desligamentos) AS desligamentos,
    SUM(saldo_empregos) AS saldo_empregos
FROM radar.vw_perfil_faixa_etaria
GROUP BY faixa_etaria
ORDER BY registros DESC;

-- Perfil por escolaridade na janela.
SELECT
    grau_instrucao,
    SUM(registros) AS registros,
    SUM(admissoes) AS admissoes,
    SUM(desligamentos) AS desligamentos,
    SUM(saldo_empregos) AS saldo_empregos
FROM radar.vw_perfil_escolaridade
GROUP BY grau_instrucao
ORDER BY grau_instrucao;

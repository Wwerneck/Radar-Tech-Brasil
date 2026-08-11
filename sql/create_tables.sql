CREATE SCHEMA IF NOT EXISTS radar;

CREATE TABLE IF NOT EXISTS radar.etl_file_manifest (
    manifest_id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    competence CHAR(6) NOT NULL,
    file_name TEXT NOT NULL,
    file_hash TEXT,
    status TEXT NOT NULL,
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB NOT NULL DEFAULT '{}'::JSONB,
    CONSTRAINT uq_etl_file_manifest UNIQUE (source_name, competence, file_name)
);

CREATE TABLE IF NOT EXISTS radar.dim_tempo (
    tempo_id INTEGER PRIMARY KEY,
    ano SMALLINT NOT NULL,
    mes SMALLINT NOT NULL CHECK (mes BETWEEN 1 AND 12),
    ano_mes CHAR(6) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS radar.dim_ocupacao (
    ocupacao_id BIGSERIAL PRIMARY KEY,
    codigo_cbo CHAR(6) NOT NULL UNIQUE,
    ocupacao TEXT NOT NULL,
    familia_cbo CHAR(4) NOT NULL,
    familia_cbo_titulo TEXT NOT NULL,
    categoria_tech TEXT NOT NULL,
    criterio TEXT NOT NULL,
    versao_mapeamento TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS radar.dim_localidade (
    localidade_id BIGSERIAL PRIMARY KEY,
    uf INTEGER NOT NULL,
    municipio INTEGER NOT NULL,
    regiao INTEGER,
    CONSTRAINT uq_dim_localidade UNIQUE (uf, municipio)
);

CREATE TABLE IF NOT EXISTS radar.dim_uf (
    uf INTEGER PRIMARY KEY,
    uf_sigla CHAR(2) NOT NULL UNIQUE,
    uf_nome TEXT NOT NULL,
    regiao_nome TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS radar.dim_escolaridade (
    grau_instrucao INTEGER PRIMARY KEY,
    escolaridade TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS radar.fato_movimentacao_tech (
    fato_id BIGSERIAL PRIMARY KEY,
    row_hash CHAR(64) NOT NULL UNIQUE,
    tempo_id INTEGER NOT NULL REFERENCES radar.dim_tempo (tempo_id),
    ocupacao_id BIGINT NOT NULL REFERENCES radar.dim_ocupacao (ocupacao_id),
    localidade_id BIGINT NOT NULL REFERENCES radar.dim_localidade (localidade_id),
    competencia_dec INTEGER,
    secao CHAR(1),
    subclasse INTEGER,
    saldo_movimentacao SMALLINT NOT NULL CHECK (saldo_movimentacao IN (-1, 1)),
    tipo_saldo TEXT NOT NULL CHECK (tipo_saldo IN ('admissao', 'desligamento')),
    tipo_movimentacao INTEGER,
    categoria INTEGER,
    grau_instrucao INTEGER,
    idade INTEGER,
    faixa_etaria TEXT,
    horas_contratuais NUMERIC(6, 2),
    raca_cor INTEGER,
    sexo INTEGER,
    tipo_empregador INTEGER,
    tipo_estabelecimento INTEGER,
    tipo_deficiencia INTEGER,
    ind_trab_intermitente INTEGER,
    ind_trab_parcial INTEGER,
    indicador_aprendiz INTEGER,
    origem_informacao INTEGER,
    indicador_fora_prazo INTEGER,
    unidade_salario_codigo INTEGER,
    salario NUMERIC(14, 2),
    valor_salario_fixo NUMERIC(14, 2),
    flag_idade_ausente BOOLEAN NOT NULL,
    flag_idade_invalida BOOLEAN NOT NULL,
    flag_salario_zero BOOLEAN NOT NULL,
    flag_salario_extremo BOOLEAN NOT NULL,
    flag_horas_invalidas BOOLEAN NOT NULL,
    flag_uf_invalida BOOLEAN NOT NULL,
    flag_cbo_invalida BOOLEAN NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_overview_mensal (
    competencia CHAR(6) PRIMARY KEY,
    total_registros_tech BIGINT NOT NULL,
    total_admissoes BIGINT NOT NULL,
    total_desligamentos BIGINT NOT NULL,
    saldo_empregos BIGINT NOT NULL,
    remuneracao_media NUMERIC(14, 2),
    remuneracao_mediana NUMERIC(14, 2),
    ocupacoes_analisadas INTEGER NOT NULL,
    categorias_tech INTEGER NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_category_mensal (
    competencia CHAR(6) NOT NULL,
    categoria_tech TEXT NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    ocupacoes INTEGER NOT NULL,
    remuneracao_media NUMERIC(14, 2),
    remuneracao_mediana NUMERIC(14, 2),
    saldo_empregos BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, categoria_tech)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_uf_mensal (
    competencia CHAR(6) NOT NULL,
    uf INTEGER NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    remuneracao_media NUMERIC(14, 2),
    remuneracao_mediana NUMERIC(14, 2),
    saldo_empregos BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, uf)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_uf_mensal_enriched (
    competencia CHAR(6) NOT NULL,
    uf INTEGER NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    remuneracao_media NUMERIC(14, 2),
    remuneracao_mediana NUMERIC(14, 2),
    saldo_empregos BIGINT NOT NULL,
    uf_sigla CHAR(2),
    uf_nome TEXT,
    regiao_nome TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, uf)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_occupation_mensal (
    competencia CHAR(6) NOT NULL,
    codigo_cbo CHAR(6) NOT NULL,
    ocupacao TEXT NOT NULL,
    categoria_tech TEXT NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    remuneracao_media NUMERIC(14, 2),
    remuneracao_mediana NUMERIC(14, 2),
    saldo_empregos BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, codigo_cbo)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_age_group_mensal (
    competencia CHAR(6) NOT NULL,
    faixa_etaria TEXT NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    saldo_empregos BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, faixa_etaria)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_education_mensal (
    competencia CHAR(6) NOT NULL,
    grau_instrucao INTEGER NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    saldo_empregos BIGINT NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, grau_instrucao)
);

CREATE TABLE IF NOT EXISTS radar.agg_tech_by_education_mensal_enriched (
    competencia CHAR(6) NOT NULL,
    grau_instrucao INTEGER NOT NULL,
    registros BIGINT NOT NULL,
    admissoes BIGINT NOT NULL,
    desligamentos BIGINT NOT NULL,
    saldo_empregos BIGINT NOT NULL,
    escolaridade TEXT,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (competencia, grau_instrucao)
);

CREATE INDEX IF NOT EXISTS idx_fato_movimentacao_tech_tempo
    ON radar.fato_movimentacao_tech (tempo_id);

CREATE INDEX IF NOT EXISTS idx_fato_movimentacao_tech_ocupacao
    ON radar.fato_movimentacao_tech (ocupacao_id);

CREATE INDEX IF NOT EXISTS idx_fato_movimentacao_tech_localidade
    ON radar.fato_movimentacao_tech (localidade_id);

CREATE INDEX IF NOT EXISTS idx_fato_movimentacao_tech_tipo_saldo
    ON radar.fato_movimentacao_tech (tipo_saldo);

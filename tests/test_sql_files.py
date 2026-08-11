from pathlib import Path


def test_create_tables_sql_defines_core_schema() -> None:
    sql = Path("sql/create_tables.sql").read_text(encoding="utf-8")

    assert "CREATE SCHEMA IF NOT EXISTS radar" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.dim_tempo" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.dim_ocupacao" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.dim_uf" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.dim_escolaridade" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.fato_movimentacao_tech" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.agg_tech_by_age_group_mensal" in sql
    assert "CREATE TABLE IF NOT EXISTS radar.agg_tech_by_education_mensal" in sql
    assert "row_hash CHAR(64) NOT NULL UNIQUE" in sql


def test_views_sql_defines_dashboard_views() -> None:
    sql = Path("sql/views.sql").read_text(encoding="utf-8")

    assert "CREATE OR REPLACE VIEW radar.vw_kpis_mensais" in sql
    assert "CREATE OR REPLACE VIEW radar.vw_saldo_por_categoria" in sql
    assert "CREATE OR REPLACE VIEW radar.vw_perfil_faixa_etaria" in sql
    assert "CREATE OR REPLACE VIEW radar.vw_perfil_escolaridade" in sql
    assert "CREATE OR REPLACE VIEW radar.vw_saldo_por_uf_enriched" in sql
    assert "CREATE OR REPLACE VIEW radar.vw_perfil_escolaridade_enriched" in sql

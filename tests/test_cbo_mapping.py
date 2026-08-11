from pathlib import Path

import pandas as pd

from src.cbo_mapping import build_cbo_tech_mapping


def test_build_cbo_tech_mapping_uses_official_titles(tmp_path: Path) -> None:
    occupation_path = tmp_path / "ocupacao.csv"
    family_path = tmp_path / "familia.csv"

    pd.DataFrame(
        [
            {"CODIGO": "123605", "TITULO": "Diretor de tecnologia da informação"},
            {"CODIGO": "142135", "TITULO": "Oficial de proteção de dados pessoais (dpo)"},
            {"CODIGO": "142505", "TITULO": "Gerente de infraestrutura de tecnologia da informação"},
            {"CODIGO": "142510", "TITULO": "Gerente de desenvolvimento de sistemas"},
            {"CODIGO": "142515", "TITULO": "Gerente de operação de tecnologia da informação"},
            {"CODIGO": "142520", "TITULO": "Gerente de projetos de tecnologia da informação"},
            {"CODIGO": "142525", "TITULO": "Gerente de segurança da informação"},
            {"CODIGO": "142530", "TITULO": "Gerente de suporte técnico de tecnologia da informação"},
            {"CODIGO": "142535", "TITULO": "Tecnólogo em gestão da tecnologia da informação"},
            {"CODIGO": "203105", "TITULO": "Pesquisador em ciências da computação e informática"},
            {"CODIGO": "211220", "TITULO": "Cientista de dados"},
            {"CODIGO": "212205", "TITULO": "Engenheiro de aplicativos em computação"},
            {"CODIGO": "212210", "TITULO": "Engenheiro de equipamentos em computação"},
            {"CODIGO": "212215", "TITULO": "Engenheiros de sistemas operacionais em computação"},
            {"CODIGO": "212305", "TITULO": "Administrador de banco de dados"},
            {"CODIGO": "212310", "TITULO": "Administrador de redes"},
            {"CODIGO": "212315", "TITULO": "Administrador de sistemas operacionais"},
            {"CODIGO": "212320", "TITULO": "Administrador em segurança da informação"},
            {"CODIGO": "212405", "TITULO": "Analista de desenvolvimento de sistemas"},
            {"CODIGO": "212410", "TITULO": "Analista de redes e de comunicação de dados"},
            {"CODIGO": "212415", "TITULO": "Analista de sistemas de automação"},
            {"CODIGO": "212420", "TITULO": "Analista de suporte computacional"},
            {"CODIGO": "212425", "TITULO": "Arquiteto de soluções de tecnologia da informação"},
            {"CODIGO": "212430", "TITULO": "Analista de testes de tecnologia da informação"},
            {"CODIGO": "214350", "TITULO": "Engenheiro de redes de comunicação"},
            {"CODIGO": "234120", "TITULO": "Professor de computação (no ensino superior)"},
            {"CODIGO": "313220", "TITULO": "Técnico em manutenção de equipamentos de informática"},
            {"CODIGO": "313305", "TITULO": "Técnico de comunicação de dados"},
            {"CODIGO": "313310", "TITULO": "Técnico de rede (telecomunicações)"},
            {"CODIGO": "317110", "TITULO": "Desenvolvedor de sistemas de tecnologia da informação (técnico)"},
            {"CODIGO": "317205", "TITULO": "Operador de computador"},
            {"CODIGO": "317210", "TITULO": "Técnico de suporte ao usuário de tecnologia da informação"},
            {"CODIGO": "372205", "TITULO": "Operador de rede de teleprocessamento"},
            {"CODIGO": "731110", "TITULO": "Montador de equipamentos eletrônicos (computadores e equipamentos auxiliares)"},
            {"CODIGO": "731320", "TITULO": "Instalador-reparador de linhas e aparelhos de telecomunicações"},
            {"CODIGO": "731325", "TITULO": "Instalador-reparador de redes e cabos telefônicos"},
            {"CODIGO": "731330", "TITULO": "Reparador de aparelhos de telecomunicações em laboratório"},
            {"CODIGO": "732105", "TITULO": "Eletricista de manutenção de linhas elétricas, telefônicas e de comunicação de dados"},
            {"CODIGO": "732130", "TITULO": "Instalador-reparador de redes telefônicas e de comunicação de dados"},
        ]
    ).to_csv(occupation_path, sep=";", index=False, encoding="latin1")

    pd.DataFrame(
        [
            {"CODIGO": "1236", "TITULO": "Diretores de tecnologia da informação"},
            {"CODIGO": "1421", "TITULO": "Gerentes administrativos, financeiros, de riscos e afins"},
            {"CODIGO": "1425", "TITULO": "Gerentes de tecnologia da informação"},
            {"CODIGO": "2031", "TITULO": "Pesquisadores das ciências naturais e exatas"},
            {"CODIGO": "2112", "TITULO": "Profissionais de estatística e afins"},
            {"CODIGO": "2122", "TITULO": "Engenheiros em computação"},
            {"CODIGO": "2123", "TITULO": "Administradores de tecnologia da informação"},
            {"CODIGO": "2124", "TITULO": "Analistas de tecnologia da informação"},
            {"CODIGO": "2143", "TITULO": "Engenheiros eletricistas, eletrônicos e afins"},
            {"CODIGO": "2341", "TITULO": "Professores de matemática, estatística e informática do ensino superior"},
            {"CODIGO": "3132", "TITULO": "Técnicos em eletrônica"},
            {"CODIGO": "3133", "TITULO": "Técnicos em telecomunicações"},
            {"CODIGO": "3171", "TITULO": "Técnicos de desenvolvimento de sistemas e aplicações"},
            {"CODIGO": "3172", "TITULO": "Técnicos de suporte e monitoração ao usuário de tecnologia da informação."},
            {"CODIGO": "3722", "TITULO": "Operadores de rede de teleprocessamento e afins"},
            {"CODIGO": "7311", "TITULO": "Montadores de equipamentos eletroeletrônicos"},
            {"CODIGO": "7313", "TITULO": "Instaladores-reparadores de linhas e equipamentos de telecomunicações"},
            {"CODIGO": "7321", "TITULO": "Instaladores e reparadores de linhas e cabos elétricos, telefônicos e de comunicação de dados"},
        ]
    ).to_csv(family_path, sep=";", index=False, encoding="latin1")

    result = build_cbo_tech_mapping(occupation_path, family_path)

    assert "codigo_cbo" in result.columns
    assert result.loc[result["codigo_cbo"] == "212405", "categoria_tech"].item() == "Desenvolvimento de Software"
    assert result["ocupacao"].isna().sum() == 0


import streamlit as st
import pandas as pd
from io import BytesIO
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Saúde e Educação no Território",
    page_icon="🏙️",
    layout="wide"
)

# Carregamento da base tratada
df = pd.read_csv(
    "data/processed/indicadores_distritos.csv"
)
# ============================================================
# REFERÊNCIAS DO MUNICÍPIO
# ============================================================

populacao_municipio = df["populacao_2022"].sum()
educacao_municipio = df["qtd_educacao"].sum()
saude_municipio = df["qtd_saude"].sum()

educacao_100mil_municipio = (
    educacao_municipio / populacao_municipio * 100000
)

saude_100mil_municipio = (
    saude_municipio / populacao_municipio * 100000
)

# Título e apresentação
st.title("Saúde e Educação no Território")

st.write(
    """
    Análise da distribuição territorial de equipamentos públicos de
    educação e Unidades Básicas de Saúde (UBS) nos distritos do
    município de São Paulo.
    """
)

st.caption(
    "Os indicadores representam a quantidade de equipamentos por "
    "100 mil habitantes e não medem capacidade, qualidade ou demanda "
    "dos serviços."
)

# ============================================================
# FILTROS
# ============================================================

st.sidebar.header("Filtros")

subprefeituras = ["Todas"] + sorted(
    df["nm_subprefeitura"].dropna().unique().tolist()
)

subprefeitura_selecionada = st.sidebar.selectbox(
    "Subprefeitura",
    subprefeituras
)

if subprefeitura_selecionada == "Todas":
    df_filtrado = df.copy()
else:
    df_filtrado = df[
        df["nm_subprefeitura"] == subprefeitura_selecionada
    ].copy()

distritos = ["Todos"] + sorted(
    df_filtrado["nm_distrito_municipal"].unique().tolist()
)

distrito_selecionado = st.sidebar.selectbox(
    "Distrito",
    distritos
)

if distrito_selecionado != "Todos":
    df_filtrado = df_filtrado[
        df_filtrado["nm_distrito_municipal"] == distrito_selecionado
    ].copy()

# ============================================================
# INDICADORES PRINCIPAIS
# ============================================================

populacao_total = df_filtrado["populacao_2022"].sum()
total_educacao = df_filtrado["qtd_educacao"].sum()
total_saude = df_filtrado["qtd_saude"].sum()

educacao_100mil = (
    total_educacao / populacao_total * 100000
    if populacao_total > 0 else 0
)

saude_100mil = (
    total_saude / populacao_total * 100000
    if populacao_total > 0 else 0
)

st.subheader("Indicadores")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "População 2022",
    f"{populacao_total:,.0f}".replace(",", ".")
)

col2.metric(
    "Equipamentos de Educação",
    f"{total_educacao:,.0f}".replace(",", ".")
)

col3.metric(
    "UBS",
    f"{total_saude:,.0f}".replace(",", ".")
)

col4.metric(
    "Educação / 100 mil hab.",
    f"{educacao_100mil:.1f}"
)

col5.metric(
    "UBS / 100 mil hab.",
    f"{saude_100mil:.1f}"
)

# ============================================================
# COMPARAÇÃO ENTRE DISTRITOS
# ============================================================

# st.subheader("Comparação entre distritos")

# df_grafico = df_filtrado[
#     [
#         "nm_distrito_municipal",
#         "educacao_por_100mil",
#         "saude_por_100mil"
#     ]
# ].copy()

# df_grafico = df_grafico.rename(
#     columns={
#         "nm_distrito_municipal": "Distrito",
#         "educacao_por_100mil": "Educação",
#         "saude_por_100mil": "UBS"
#     }
# )

# df_grafico = df_grafico.set_index("Distrito")

# st.bar_chart(
#     df_grafico,
#     x_label="Distrito",
#     y_label="Equipamentos por 100 mil habitantes"
# )

# =========================================================
# GRÁFICOS DE COMPARAÇÃO TERRITORIAL
# =========================================================

if distrito_selecionado == "Todos":

    col_educacao, col_saude = st.columns(2)

    # -------------------------
    # EDUCAÇÃO
    # -------------------------
    with col_educacao:
        st.subheader("Educação por distrito")

        dados_educacao = df_filtrado.sort_values(
    "nm_distrito_municipal"
)

        fig_educacao = px.bar(
            dados_educacao,
            x="educacao_por_100mil",
            y="nm_distrito_municipal",
            orientation="h",
            labels={
                "educacao_por_100mil": "Equipamentos por 100 mil habitantes",
                "nm_distrito_municipal": "Distrito"
            }
        )

        fig_educacao.update_layout(
            height=max(400, len(dados_educacao) * 25),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_educacao.update_yaxes(autorange="reversed")

        with st.container(height=600):
            st.plotly_chart(
                fig_educacao,
                width="stretch"
            )

    # -------------------------
    # SAÚDE
    # -------------------------
    with col_saude:
        st.subheader("Saúde por distrito")

        dados_saude = df_filtrado.sort_values(
    "nm_distrito_municipal"
)

        fig_saude = px.bar(
            dados_saude,
            x="saude_por_100mil",
            y="nm_distrito_municipal",
            orientation="h",
            labels={
                "saude_por_100mil": "UBS por 100 mil habitantes",
                "nm_distrito_municipal": "Distrito"
            }
        )

        fig_saude.update_layout(
            height=max(400, len(dados_saude) * 25),
            showlegend=False,
            margin=dict(l=10, r=10, t=10, b=10)
        )
        fig_saude.update_yaxes(autorange="reversed")

        with st.container(height=600):
            st.plotly_chart(
                fig_saude,
                width="stretch"
            )
# ============================================================
# RESUMO DA ANÁLISE
# ============================================================

st.subheader("Resumo da análise")

if distrito_selecionado != "Todos":

    posicao_educacao = (
        "acima" if educacao_100mil > educacao_100mil_municipio
        else "abaixo" if educacao_100mil < educacao_100mil_municipio
        else "igual"
    )

    posicao_saude = (
        "acima" if saude_100mil > saude_100mil_municipio
        else "abaixo" if saude_100mil < saude_100mil_municipio
        else "igual"
    )
    st.write(
        f"""
        O distrito de **{distrito_selecionado.title()}** possui população de
        **{populacao_total:,.0f} habitantes**, com **{total_educacao} equipamentos
        de educação** e **{total_saude} UBS**.

        Em relação à população, são **{educacao_100mil:.1f} equipamentos de educação
        por 100 mil habitantes**, valor **{posicao_educacao} da referência municipal
        de {educacao_100mil_municipio:.1f}**.

        Para UBS, o distrito apresenta **{saude_100mil:.1f} unidades por 100 mil
        habitantes**, valor **{posicao_saude} da referência municipal de
        {saude_100mil_municipio:.1f}**.
        """.replace(",", ".")
    )

elif subprefeitura_selecionada != "Todas":
    st.write(
        f"""
        Na Subprefeitura de **{subprefeitura_selecionada.title()}**, os distritos
        selecionados somam **{populacao_total:,.0f} habitantes**,
        **{total_educacao} equipamentos de educação** e **{total_saude} UBS**.

        Os indicadores agregados são **{educacao_100mil:.1f} equipamentos de
        educação** e **{saude_100mil:.1f} UBS por 100 mil habitantes**.
        """.replace(",", ".")
    )

else:
    st.write(
        f"""
        No município de São Paulo, a base analisada reúne
        **{total_educacao} equipamentos de educação** e **{total_saude} UBS**,
        considerando uma população de **{populacao_total:,.0f} habitantes**.

        Os indicadores municipais correspondem a **{educacao_100mil:.1f}
        equipamentos de educação** e **{saude_100mil:.1f} UBS por 100 mil
        habitantes**.
        """.replace(",", ".")
    )

st.caption(
    "Os resultados descrevem a distribuição territorial dos equipamentos "
    "presentes nas bases utilizadas. Não representam capacidade de atendimento, "
    "qualidade do serviço ou demanda da população."
)

# ============================================================
# DOWNLOAD EM EXCEL
# ============================================================

arquivo_excel = BytesIO()

with pd.ExcelWriter(
    arquivo_excel,
    engine="openpyxl"
) as writer:
    df_filtrado.to_excel(
        writer,
        index=False,
        sheet_name="Dados"
    )

st.download_button(
    label="Baixar dados filtrados (Excel)",
    data=arquivo_excel.getvalue(),
    file_name="saude_educacao_distritos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
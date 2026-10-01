import geopandas as gpd
import pandas as pd
import unicodedata
import os
os.makedirs("data/processed", exist_ok=True)

# Caminho da base de Educação Infantil
arquivo_infantil = "data/raw/equipamento_educacao_infantil_rede_publica_v2.geojson"

# Leitura do arquivo GeoJSON
gdf_infantil = gpd.read_file(arquivo_infantil)

# Caminho da base de Ensino Fundamental e Médio
arquivo_fundamental = "data/raw/equipamento_educacao_fundamental_rede_publica_v2.geojson"

# Leitura do arquivo
gdf_fundamental = gpd.read_file(arquivo_fundamental)

# Caminho da base de unidades educacionais dos CEUs
arquivo_ceu = "data/raw/equipamento_educacao_ceu_v2.geojson"

# Leitura do arquivo
gdf_ceu = gpd.read_file(arquivo_ceu)


# print("Quantidade de registros:", len(gdf_infantil))
# print("CRS:", gdf_infantil.crs)
# print("\nColunas:")
# print(gdf_infantil.columns.tolist())
# print("\nPrimeiros registros:")
# print(gdf_infantil.head())

# colunas_interesse = [
#     "cd_identificador",
#     "nm_tipo_equipamento",
#     "tx_tipo_equipamento",
#     "nm_classe_equipamento",
#     "nm_esfera_administrativa_equipamento",
#     "nm_equipamento",
#     "tx_endereco_equipamento",
#     "nm_bairro_equipamento",
#     "cd_cep_equipamento",
#     "geometry"
# ]

# print("\nCampos de interesse:")
# print(gdf_infantil[colunas_interesse].head())
# print("\nQuantidade por tipo de equipamento:")
# print(gdf_infantil["nm_tipo_equipamento"].value_counts())
# print("\n--- ENSINO FUNDAMENTAL E MÉDIO ---")
# print("Quantidade de registros:", len(gdf_fundamental))
# print("CRS:", gdf_fundamental.crs)

# print("\nQuantidade por tipo de equipamento:")
# print(gdf_fundamental["nm_tipo_equipamento"].value_counts())
# print("\n--- CEUs ---")
# print("Quantidade de registros:", len(gdf_ceu))
# print("CRS:", gdf_ceu.crs)

# print("\nQuantidade por tipo de equipamento:")
# print(gdf_ceu["nm_tipo_equipamento"].value_counts())

# print("\n--- COMPARAÇÃO DAS COLUNAS ---")

# print(
#     "Infantil x Fundamental:",
#     list(gdf_infantil.columns) == list(gdf_fundamental.columns)
# )

# print(
#     "Infantil x CEU:",
#     list(gdf_infantil.columns) == list(gdf_ceu.columns)
# )

# print(
#     "Fundamental x CEU:",
#     list(gdf_fundamental.columns) == list(gdf_ceu.columns)
# )

# Identificação do grupo de cada equipamento
# gdf_infantil["grupo_educacao"] = "Educação Infantil"
# gdf_fundamental["grupo_educacao"] = "Ensino Fundamental e Médio"
# gdf_ceu["grupo_educacao"] = "CEU" """

# # Conferência
# print("\n--- GRUPOS CRIADOS ---")
# print(gdf_infantil["grupo_educacao"].value_counts())
# print(gdf_fundamental["grupo_educacao"].value_counts())
# print(gdf_ceu["grupo_educacao"].value_counts())

# # Verificar possível duplicidade dos CEUs nas outras bases

# ids_infantil = set(gdf_infantil["cd_equipamento_base_origem"].dropna())
# ids_fundamental = set(gdf_fundamental["cd_equipamento_base_origem"].dropna())
# ids_ceu = set(gdf_ceu["cd_equipamento_base_origem"].dropna())

# print("\n--- VERIFICAÇÃO DE CEUs REPETIDOS ---")
# print("CEUs encontrados na base Infantil:", len(ids_ceu & ids_infantil))
# print("CEUs encontrados na base Fundamental:", len(ids_ceu & ids_fundamental))

# Verificar possíveis repetições pelo nome do equipamento

# nomes_infantil = set(
#     gdf_infantil["nm_equipamento"].dropna().str.strip().str.upper()
# )

# nomes_fundamental = set(
#     gdf_fundamental["nm_equipamento"].dropna().str.strip().str.upper()
# )

# nomes_ceu = set(
#     gdf_ceu["nm_equipamento"].dropna().str.strip().str.upper()
# )

# print("\n--- VERIFICAÇÃO PELO NOME ---")
# print("CEUs com nome encontrado na base Infantil:", len(nomes_ceu & nomes_infantil))
# print("CEUs com nome encontrado na base Fundamental:", len(nomes_ceu & nomes_fundamental))

# Identificação do grupo de cada equipamento
gdf_infantil["grupo_educacao"] = "Educação Infantil"
gdf_fundamental["grupo_educacao"] = "Ensino Fundamental e Médio"
gdf_ceu["grupo_educacao"] = "CEU"

# Consolidação das bases de Educação
gdf_educacao = pd.concat(
    [gdf_infantil, gdf_fundamental, gdf_ceu],
    ignore_index=True
)

# print("\n--- BASE DE EDUCAÇÃO CONSOLIDADA ---")
# print("Total de registros:", len(gdf_educacao))
# print(gdf_educacao["grupo_educacao"].value_counts())

# Leitura da base de distritos
arquivo_distritos = "data/raw/distrito_municipal_v2.geojson"
gdf_distritos = gpd.read_file(arquivo_distritos)

# print("\n--- BASE DE DISTRITOS ---")
# print("Quantidade de registros:", len(gdf_distritos))
# print("CRS:", gdf_distritos.crs)
# print("Colunas:", gdf_distritos.columns.tolist())

# Cruzamento espacial dos equipamentos com os distritos
gdf_educacao = gpd.sjoin(
    gdf_educacao,
    gdf_distritos[["nm_distrito_municipal", "geometry"]],
    how="left",
    predicate="within"
)

# print("\n--- DISTRITOS ASSOCIADOS AOS EQUIPAMENTOS ---")
# print("Total de equipamentos:", len(gdf_educacao))
# print(
#     "Equipamentos sem distrito:",
#     gdf_educacao["nm_distrito_municipal"].isna().sum()
# )

# # Conferência da quantidade de equipamentos por distrito
# print("\n--- EQUIPAMENTOS POR DISTRITO ---")
# print(
#     gdf_educacao["nm_distrito_municipal"]
#     .value_counts()
#     .sort_index()
# )

# Leitura da aba de população usando o cabeçalho correto
arquivo_populacao = "data/raw/314_01_censo_r5-sub-distr_pop-abs_1950-2022_final_1715805105.xlsx"
df_populacao = pd.read_excel(
    arquivo_populacao,
    sheet_name="Pop314_01_1950-2022",
    header=4
)

# print("\n--- BASE DE POPULAÇÃO COM CABEÇALHO CORRETO ---")
# print("Colunas:", df_populacao.columns.tolist())
# print(df_populacao.head(10))
# Leitura da base de subprefeituras
arquivo_subprefeituras = "data/raw/subprefeitura_v2.geojson"
gdf_subprefeituras = gpd.read_file(arquivo_subprefeituras)

# print("\n--- BASE DE SUBPREFEITURAS ---")
# print("Quantidade:", len(gdf_subprefeituras))
# print("Colunas:", gdf_subprefeituras.columns.tolist())

# Associar cada distrito à sua subprefeitura
gdf_distritos = gdf_distritos.merge(
    gdf_subprefeituras[
        ["cd_identificador_subprefeitura", "nm_subprefeitura"]
    ],
    on="cd_identificador_subprefeitura",
    how="left"
)

# print("\n--- DISTRITOS E SUBPREFEITURAS ---")
# print(
#     gdf_distritos[
#         ["nm_distrito_municipal", "nm_subprefeitura"]
#     ].head(15)
# )

# print("Distritos sem subprefeitura:",
#       gdf_distritos["nm_subprefeitura"].isna().sum())

# Preparar população de 2022
df_pop_2022 = df_populacao[
    ["Unidades territoriais", "2022"]
].copy()

df_pop_2022.columns = ["nm_distrito_municipal", "populacao_2022"]

# Manter somente os 96 distritos
df_pop_2022 = df_pop_2022[
    df_pop_2022["nm_distrito_municipal"].str.upper().isin(
        gdf_distritos["nm_distrito_municipal"]
    )
]

# print("\n--- POPULAÇÃO DOS DISTRITOS ---")
# print("Distritos encontrados:", len(df_pop_2022))

# Verificar distritos que não encontraram correspondência na população
nomes_excel = df_populacao["Unidades territoriais"].dropna().str.upper()

distritos_faltantes = gdf_distritos[
    ~gdf_distritos["nm_distrito_municipal"].isin(nomes_excel)
]["nm_distrito_municipal"]

# print("\n--- DISTRITOS NÃO ENCONTRADOS NO EXCEL ---")
# print(distritos_faltantes.to_list())
# print("Total:", len(distritos_faltantes))

# Função para padronizar nomes territoriais
def normalizar_nome(texto):
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c))

# Criar chave padronizada nas duas bases
gdf_distritos["chave_distrito"] = (
    gdf_distritos["nm_distrito_municipal"].apply(normalizar_nome)
)

df_populacao["chave_distrito"] = (
    df_populacao["Unidades territoriais"].apply(normalizar_nome)
)

# Selecionar somente os registros correspondentes aos 96 distritos
df_pop_2022 = df_populacao[
    df_populacao["chave_distrito"].isin(gdf_distritos["chave_distrito"])
][["chave_distrito", "2022"]].copy()

# print("\n--- POPULAÇÃO APÓS PADRONIZAÇÃO ---")
# print("Distritos encontrados:", len(df_pop_2022))

# Juntar população de 2022 aos distritos
gdf_distritos = gdf_distritos.merge(
    df_pop_2022,
    on="chave_distrito",
    how="left"
)

# Renomear a coluna de população
gdf_distritos = gdf_distritos.rename(
    columns={"2022": "populacao_2022"}
)

# print("\n--- BASE TERRITORIAL FINAL ---")
# print(
#     gdf_distritos[
#         ["nm_distrito_municipal", "nm_subprefeitura", "populacao_2022"]
#     ].head(10)
# )

# print("\nDistritos:", len(gdf_distritos))
# print("Sem população:", gdf_distritos["populacao_2022"].isna().sum())

# ============================================================
# INDICADORES DE EDUCAÇÃO POR DISTRITO
# ============================================================

# Conta quantos equipamentos de educação existem em cada distrito
educacao_por_distrito = (
    gdf_educacao
    .groupby("nm_distrito_municipal")
    .size()
    .reset_index(name="qtd_educacao")
)

# Junta a quantidade de equipamentos à base territorial
gdf_distritos = gdf_distritos.merge(
    educacao_por_distrito,
    on="nm_distrito_municipal",
    how="left"
)

# Distritos sem equipamento recebem zero
gdf_distritos["qtd_educacao"] = (
    gdf_distritos["qtd_educacao"]
    .fillna(0)
    .astype(int)
)

# Converte a população de 2022 para formato numérico
gdf_distritos["populacao_2022"] = (
    gdf_distritos["populacao_2022"]
    .astype(str)
    .str.replace(".", "", regex=False)
    .astype(int)
)

# Indicador: equipamentos de educação por 100 mil habitantes
gdf_distritos["educacao_por_100mil"] = (
    gdf_distritos["qtd_educacao"]
    / gdf_distritos["populacao_2022"]
    * 100000
)

# print("\n--- INDICADORES DE EDUCAÇÃO ---")
# print(
#     gdf_distritos[
#         [
#             "nm_distrito_municipal",
#             "nm_subprefeitura",
#             "populacao_2022",
#             "qtd_educacao",
#             "educacao_por_100mil"
#         ]
#     ].head(10)
# )

# print("\nDistritos:", len(gdf_distritos))

# ============================================================
# VALIDAÇÃO FINAL DA BASE DE EDUCAÇÃO
# ============================================================

# print("\n--- VALIDAÇÃO FINAL DA EDUCAÇÃO ---")

# print("Total de registros:", len(gdf_educacao))

# print(
#     "Sem distrito:",
#     gdf_educacao["nm_distrito_municipal"].isna().sum()
# )

# print(
#     "Soma dos equipamentos nos 96 distritos:",
#     gdf_distritos["qtd_educacao"].sum()
# )

# print(
#     "Distritos sem equipamentos:",
#     (gdf_distritos["qtd_educacao"] == 0).sum()
# )

# ============================================================
# SALVAR BASE TRATADA DE EDUCAÇÃO
# ============================================================

df_educacao_distrito = gdf_distritos[
    [
        "nm_distrito_municipal",
        "nm_subprefeitura",
        "populacao_2022",
        "qtd_educacao",
        "educacao_por_100mil"
    ]
].copy()

df_educacao_distrito.to_csv(
    "data/processed/educacao_por_distrito.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo salvo: data/processed/educacao_por_distrito.csv")
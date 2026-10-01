import geopandas as gpd
import pandas as pd
import unicodedata

# ============================================================
# INTEGRAÇÃO FINAL
# Distrito + Subprefeitura + População + Educação + Saúde
# ============================================================

# Bases territoriais
gdf_distritos = gpd.read_file(
    "data/raw/distrito_municipal_v2.geojson"
)

gdf_subprefeituras = gpd.read_file(
    "data/raw/subprefeitura_v2.geojson"
)

# Base de saúde já tratada
df_saude = pd.read_csv(
    "data/processed/saude_por_distrito.csv"
)

print("\n--- INÍCIO DA INTEGRAÇÃO FINAL ---")
print("Distritos:", len(gdf_distritos))
print("Subprefeituras:", len(gdf_subprefeituras))
print("Registros saúde:", len(df_saude))

# Leitura da base de Educação já tratada
df_educacao = pd.read_csv(
    "data/processed/educacao_por_distrito.csv"
)

# Integração da Educação com a Saúde
df_final = df_educacao.merge(
    df_saude,
    on="nm_distrito_municipal",
    how="left"
)

# Garantir zero para distritos sem UBS
df_final["qtd_saude"] = (
    df_final["qtd_saude"]
    .fillna(0)
    .astype(int)
)

# Indicador de UBS por 100 mil habitantes
df_final["saude_por_100mil"] = (
    df_final["qtd_saude"]
    / df_final["populacao_2022"]
    * 100000
)

# Validação da integração
print("\n--- BASE FINAL INTEGRADA ---")
print("Distritos:", len(df_final))
print("População ausente:", df_final["populacao_2022"].isna().sum())
print("Total Educação:", df_final["qtd_educacao"].sum())
print("Total UBS:", df_final["qtd_saude"].sum())

print("\nColunas finais:")
print(df_final.columns.tolist())

# ============================================================
# SALVAR BASE FINAL INTEGRADA
# ============================================================

df_final.to_csv(
    "data/processed/indicadores_distritos.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nArquivo final salvo: data/processed/indicadores_distritos.csv")
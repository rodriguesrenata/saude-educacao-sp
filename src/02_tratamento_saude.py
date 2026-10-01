import geopandas as gpd
import pandas as pd

# Caminho da base de equipamentos de saúde
arquivo_saude = "data/raw/equipamento_saude_ubs_posto_centro_v2.geojson"

# Leitura do arquivo GeoJSON
gdf_saude = gpd.read_file(arquivo_saude)

# Conferência inicial da base
# print("\n--- BASE DE SAÚDE ---")
# print("Quantidade de registros:", len(gdf_saude))
# print("CRS:", gdf_saude.crs)
# print("Colunas:")
# print(gdf_saude.columns.tolist())

# print("\n--- TIPOS DE EQUIPAMENTOS ---")
# print(gdf_saude["nm_tipo_equipamento"].value_counts(dropna=False))

# Leitura da base de distritos
arquivo_distritos = "data/raw/distrito_municipal_v2.geojson"
gdf_distritos = gpd.read_file(arquivo_distritos)

# Garantir que saúde e distritos estejam no mesmo sistema de coordenadas
gdf_saude = gdf_saude.to_crs(gdf_distritos.crs)

# Associar cada equipamento de saúde ao distrito onde está localizado
gdf_saude = gpd.sjoin(
    gdf_saude,
    gdf_distritos[["nm_distrito_municipal", "geometry"]],
    how="left",
    predicate="within"
)

# # Validação
# print("\n--- SAÚDE ASSOCIADA AOS DISTRITOS ---")
# print("Total de equipamentos:", len(gdf_saude))
# print("Equipamentos sem distrito:", gdf_saude["nm_distrito_municipal"].isna().sum())
# print("Distritos com equipamentos:", gdf_saude["nm_distrito_municipal"].nunique())

# Manter apenas os registros classificados oficialmente como UBS
gdf_saude_ubs = gdf_saude[
    gdf_saude["nm_tipo_equipamento"] == "Unidade Básica de Saúde"
].copy()

print("\n--- BASE UTILIZADA NO INDICADOR ---")
print("UBS classificadas:", len(gdf_saude_ubs))

# Quantidade de equipamentos de saúde por distrito
qtd_saude = (
    gdf_saude_ubs
    .groupby("nm_distrito_municipal")
    .size()
    .reset_index(name="qtd_saude")
)

# Manter os 96 distritos, inclusive os que não possuem unidade
gdf_distritos = gdf_distritos.merge(
    qtd_saude,
    on="nm_distrito_municipal",
    how="left"
)

# Distritos sem equipamento recebem zero
gdf_distritos["qtd_saude"] = (
    gdf_distritos["qtd_saude"]
    .fillna(0)
    .astype(int)
)

print("\n--- EQUIPAMENTOS DE SAÚDE POR DISTRITO ---")
print("Distritos:", len(gdf_distritos))
print("Total de equipamentos:", gdf_distritos["qtd_saude"].sum())
print("Distritos sem equipamento:", (gdf_distritos["qtd_saude"] == 0).sum())

# Base resumida de saúde por distrito
df_saude_distrito = gdf_distritos[
    ["nm_distrito_municipal", "qtd_saude"]
].copy()

# Criar pasta de dados tratados, caso ainda não exista
import os
os.makedirs("data/processed", exist_ok=True)

# Salvar resultado tratado
df_saude_distrito.to_csv(
    "data/processed/saude_por_distrito.csv",
    index=False,
    encoding="utf-8-sig"
)

# print("\n--- SAÍDA DE SAÚDE CONCLUÍDA ---")
# print(df_saude_distrito.head(10))
# print("\nArquivo salvo: data/processed/saude_por_distrito.csv")

# Verificar registros de saúde sem tipo informado
sem_tipo = gdf_saude[
    gdf_saude["nm_tipo_equipamento"] == "SEM TIPO"
]

print("\n--- REGISTROS SEM TIPO ---")
print(
    sem_tipo[
        [
            "nm_equipamento",
            "nm_tipo_equipamento",
            "nm_distrito_municipal"
        ]
    ]
)
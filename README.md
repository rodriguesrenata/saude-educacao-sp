# Saúde e Educação no Território

Análise da distribuição territorial de equipamentos públicos de educação e Unidades Básicas de Saúde (UBS) nos distritos do município de São Paulo.


## Aplicação publicada

**Acesse a aplicação:** [Saúde e Educação no Território](https://rodriguesrenata-saude-educacao-sp-app-trvymv.streamlit.app/)


## Problema e contexto

Informações sobre população e equipamentos públicos estão disponíveis em diferentes fontes e formatos, o que dificulta sua análise conjunta e a comparação entre os territórios do município.

Este projeto integra dados populacionais e dados de equipamentos públicos de saúde e educação, permitindo analisar sua distribuição entre os distritos e subprefeituras de São Paulo.

## Objetivo

Disponibilizar uma aplicação web interativa para consulta e comparação de indicadores territoriais de saúde e educação, relacionando a quantidade de equipamentos à população de cada território.

Foram utilizadas bases públicas do Município de São Paulo. Os dados geográficos foram obtidos no GeoSampa e os dados populacionais em base tabular disponibilizada pela Prefeitura de São Paulo.

### Educação

A análise de educação foi construída a partir de três bases distintas do GeoSampa:

- Equipamentos de Educação Infantil – Rede Pública;
- Equipamentos de Ensino Fundamental – Rede Pública;
- Centros Educacionais Unificados (CEUs).

As três bases foram utilizadas para compor o conjunto de equipamentos educacionais analisados no projeto.

**Fonte:** GeoSampa – Prefeitura de São Paulo  
**Acesso:** [GeoSampa – Mapa Digital da Cidade de São Paulo](https://geosampa.prefeitura.sp.gov.br/)

### Saúde

Para a área da saúde, foi utilizada a camada de equipamentos de saúde do GeoSampa referente a UBS/Posto/Centro de Saúde.

Para este projeto, foi definido como recorte de análise considerar somente os registros identificados como **Unidade Básica de Saúde (UBS)**.

**Fonte:** GeoSampa – Prefeitura de São Paulo  
**Acesso:** [GeoSampa – Mapa Digital da Cidade de São Paulo](https://geosampa.prefeitura.sp.gov.br/)

### Distritos

Foi utilizada a camada geográfica de **Distritos Municipais** para representar os limites dos distritos e realizar a associação territorial dos equipamentos.

São considerados os **96 distritos do município de São Paulo**.

**Fonte:** GeoSampa – Prefeitura de São Paulo / SMUL / GEOINFO  
**Metadados:** [Distrito – GeoSampa](https://metadados.geosampa.prefeitura.sp.gov.br/geonetwork/srv/api/records/51f75eab-6d90-451e-9f80-c21c1ac72630)

### Subprefeituras

Foi utilizada a camada geográfica de **Subprefeituras** para relacionar os distritos às respectivas divisões administrativas e permitir a filtragem dos dados por subprefeitura na aplicação.

**Fonte:** GeoSampa – Prefeitura de São Paulo / SMUL / GEOINFO  
**Metadados:** [Subprefeituras – GeoSampa](https://metadados.geosampa.prefeitura.sp.gov.br/geonetwork/srv/api/records/289e684e-b2be-453d-8d2d-68ec629cd3dc)

### População

A base utilizada foi a tabela **“População – Município de São Paulo, regiões, subprefeituras e distritos municipais – 1950, 1960, 1970, 1980, 1991, 2000, 2010 e 2022”**, disponibilizada pelo InfoCidade da Prefeitura de São Paulo.

Para o projeto, foram selecionados os dados referentes ao ano de 2022 e aos 96 distritos municipais. Os dados de 2022 têm como referência o Censo Demográfico 2022 do IBGE.

**Fonte:** Prefeitura de São Paulo – InfoCidade / Censo Demográfico 2022 – IBGE  
**Acesso:** [InfoCidade – População](https://prefeitura.sp.gov.br/licenciamento/w/desenvolvimento_urbano/dados_estatisticos/info_cidade/demografia/260265)

## Metodologia e tratamento dos dados

O desenvolvimento foi dividido em etapas de coleta, validação, tratamento, integração e construção dos indicadores. O objetivo foi manter o processo organizado e reproduzível, preservando as bases originais na pasta `data/raw` e gerando uma base final tratada em `data/processed`.

### 1. Tratamento dos dados de educação

As três bases de educação foram carregadas separadamente e tiveram sua estrutura verificada antes da consolidação.

Foram analisados aspectos como sistema de coordenadas, quantidade de registros, colunas disponíveis e tipos de equipamentos. Como as bases apresentavam estrutura compatível, elas foram consolidadas para formar o conjunto de equipamentos educacionais utilizado na análise.

Após a consolidação, foram considerados **4.787 registros de equipamentos de educação**.

A localização geográfica de cada equipamento foi utilizada para identificar o distrito correspondente por meio de associação espacial com os polígonos dos distritos municipais.

Como validação, foi verificado que:

- os 4.787 equipamentos foram associados a um distrito;
- nenhum registro ficou sem distrito;
- a soma dos equipamentos distribuídos pelos distritos permaneceu igual ao total da base consolidada.

### 2. Tratamento dos dados de saúde

A base de saúde utilizada inicialmente possuía **483 registros** na camada UBS/Posto/Centro de Saúde.

Durante a análise do campo de tipo de equipamento, foram identificados **479 registros classificados como Unidade Básica de Saúde (UBS)** e **4 registros sem tipo informado**.

Como o indicador definido para o projeto é específico para UBS, foram mantidos somente os 479 registros explicitamente classificados como Unidade Básica de Saúde. Os quatro registros sem classificação foram excluídos desse indicador.

Assim como na educação, a localização geográfica das UBS foi associada aos polígonos dos distritos para determinar a qual distrito cada unidade pertence.

### 3. Tratamento dos dados populacionais

A planilha de população possui informações históricas para diferentes unidades territoriais. O cabeçalho efetivo da tabela encontra-se após as linhas iniciais de título e identificação da fonte, sendo necessária a leitura da planilha a partir da linha correspondente ao cabeçalho dos dados.

Para o projeto, foram selecionados o nome da unidade territorial e a população referente ao ano de **2022**.

Os valores populacionais foram importados inicialmente como texto, utilizando ponto como separador de milhar. Esses caracteres foram removidos e os valores convertidos para formato numérico.

Também foram identificadas diferenças de grafia entre os nomes dos distritos nas bases populacional e geográfica, principalmente relacionadas a letras maiúsculas/minúsculas e acentuação. Para permitir a integração, os nomes foram padronizados, incluindo conversão para maiúsculas e remoção de acentos.

Após a padronização, foi validada a correspondência dos **96 distritos**, sem registros com população ausente.

### 4. Integração territorial

Os dados tratados foram integrados utilizando os distritos como unidade territorial principal da análise.

As localizações dos equipamentos foram relacionadas espacialmente aos polígonos dos distritos. Posteriormente, os distritos foram associados às respectivas subprefeituras.

Ao final dessa etapa, foram validados os **96 distritos** e sua associação às **32 subprefeituras**, sem distritos sem subprefeitura.

### 5. Construção dos indicadores

Além das quantidades absolutas, foram calculados indicadores por **100 mil habitantes**, permitindo comparar territórios com tamanhos populacionais diferentes.

Os indicadores foram calculados pelas seguintes relações:

**Educação por 100 mil habitantes:**

`quantidade de equipamentos de educação / população do território × 100.000`

**UBS por 100 mil habitantes:**

`quantidade de UBS / população do território × 100.000`

Para análises agregadas por subprefeitura ou para o município, os indicadores são recalculados a partir da soma da população e da quantidade de equipamentos do território selecionado, evitando utilizar uma média simples das taxas dos distritos.

A base integrada resultante foi exportada para `data/processed/indicadores_distritos.csv` e é utilizada pela aplicação web.

## Solução desenvolvida

A solução foi desenvolvida como uma aplicação web interativa em **Streamlit**, utilizando a base integrada produzida durante o tratamento dos dados.

A aplicação permite explorar os indicadores do município de São Paulo em diferentes níveis territoriais, utilizando filtros de **subprefeitura** e **distrito**.

### Funcionalidades

A aplicação apresenta:

- filtros por subprefeitura e distrito;
- população residente em 2022 para o território selecionado;
- quantidade de equipamentos de educação;
- quantidade de Unidades Básicas de Saúde (UBS);
- indicador de equipamentos de educação por 100 mil habitantes;
- indicador de UBS por 100 mil habitantes;
- gráficos separados para educação e saúde, permitindo observar a distribuição dos indicadores entre os distritos;
- resumo automático dos principais resultados de acordo com o território selecionado;
- comparação dos indicadores do distrito selecionado com a referência do município;
- exportação dos dados filtrados em formato Excel.

Quando um distrito é analisado, os indicadores por 100 mil habitantes são comparados com os valores de referência do município. Essa comparação possui caráter descritivo e busca contextualizar o valor observado, sem estabelecer um parâmetro de suficiência ou qualidade do serviço.

A aplicação foi estruturada para funcionar diretamente pelo navegador, facilitando a consulta dos resultados sem exigir do usuário conhecimento das etapas de tratamento e integração das bases.

## Tecnologias utilizadas

O projeto foi desenvolvido principalmente em Python, utilizando as seguintes tecnologias e bibliotecas:

- **Python:** linguagem utilizada no tratamento, integração e análise dos dados e no desenvolvimento da aplicação;
- **Pandas:** manipulação, limpeza, agregação e integração dos dados tabulares;
- **GeoPandas:** leitura e tratamento das bases geográficas e realização das associações espaciais;
- **Streamlit:** desenvolvimento da aplicação web interativa;
- **Plotly:** construção dos gráficos interativos apresentados na aplicação;
- **OpenPyXL:** leitura de arquivos Excel e geração do arquivo disponibilizado para exportação na aplicação;
- **GeoJSON:** formato utilizado nas bases geográficas obtidas do GeoSampa;
- **Git/GitHub:** versionamento, documentação e disponibilização do projeto.

A escolha do Python permitiu concentrar em um mesmo fluxo o tratamento de diferentes formatos de dados, as operações espaciais, a construção dos indicadores e a preparação da base utilizada pela aplicação.

## Uso de Inteligência Artificial

Foi utilizada IA generativa, por meio do **ChatGPT**, como ferramenta de apoio durante o desenvolvimento do projeto.

A ferramenta foi utilizada principalmente para:

- esclarecer dúvidas relacionadas a Python, GeoPandas e Streamlit;
- auxiliar na identificação e correção de erros durante o desenvolvimento;
- revisar e discutir trechos de código;
- apoiar a estruturação da aplicação e da documentação;
- auxiliar na análise das alternativas técnicas durante o desenvolvimento.

As sugestões geradas pela IA foram avaliadas e testadas durante a execução do projeto. Os resultados foram conferidos com as bases tratadas e ajustados de acordo com as validações realizadas e com as decisões metodológicas adotadas para a solução.

A IA foi utilizada como ferramenta de apoio ao desenvolvimento, mantendo a validação dos dados, a definição dos indicadores, a interpretação dos resultados e as decisões finais sobre a solução dentro do processo de construção do projeto.

## Estrutura do projeto

```text
saude_educacao_sp/
│
├── app.py
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│       └── indicadores_distritos.csv
│
└── src/
    ├── 01_tratamento_educacao.py
    ├── 02_tratamento_saude.py
    └── 03_integracao_final.py
```

- `data/raw`: bases originais utilizadas no projeto;
- `data/processed`: base final tratada utilizada pela aplicação;
- `src`: scripts responsáveis pelo tratamento e integração dos dados;
- `app.py`: aplicação web desenvolvida em Streamlit.

## Como executar

Após baixar ou clonar o repositório, acesse a pasta do projeto e instale as dependências:

```bash
pip install -r requirements.txt
```

Em seguida, execute a aplicação:

```bash
streamlit run app.py
```

A aplicação será iniciada e poderá ser acessada pelo navegador.

# Painel de Evolução da COVID-19 no Brasil

## Visão Geral do Projeto

Bem-vindo ao projeto Painel de Evolução da COVID-19 no Brasil! Este projeto é uma aplicação web interativa desenvolvida com Dash e Plotly para visualizar os dados da COVID-19 no Brasil. O painel fornece uma visão abrangente da progressão da pandemia nos diferentes estados e no país como um todo, com uma variedade de recursos interativos para uma exploração detalhada dos dados.

## Funcionalidades

- **Mapa Coroplético**: Permite visualizar os dados da COVID-19 por estado com um mapa coroplético interativo.
- **Análise de Séries Temporais**: Acompanha a progressão dos casos e óbitos ao longo do tempo com gráficos de linha e de barras interativos.
- **Seleção de Dados**: Facilita a seleção e visualização de dados por diferentes datas, estados e tipos de dados (e.g., novos casos, casos totais, novos óbitos, óbitos totais).
- **Cartões Informativos**: Exibe rapidamente estatísticas chave como casos recuperados, casos em acompanhamento, casos confirmados totais, novos casos, óbitos confirmados e óbitos na data selecionada.

## Fontes de Dados

Os dados utilizados no projeto são provenientes dos repositórios oficiais de dados da COVID-19 no Brasil. O conjunto de dados inclui informações detalhadas sobre casos e óbitos em diversos estados e no país como um todo.

## Estrutura do Projeto

Todo o código necessário para executar o projeto está contido em um único arquivo Python:

- `dashboard.py`: Arquivo principal que configura o servidor Dash, o layout da aplicação, e as funções de callback que gerenciam a interatividade.

Além do arquivo `dashboard.py`, o projeto inclui os seguintes recursos:

- `assets/`: Pasta contendo imagens e outros ativos estáticos usados na aplicação.
- `geojson/`: Pasta contendo arquivos GeoJSON para visualizações de mapas.
- `datasets/`: Pasta contendo os datasets utilizados no projeto.

## Como Executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/GleysonW/Dashboard-COVID19.git

2. Navegue até o diretório do projeto:
   ```bash
   cd Dashboard-COVID19

3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt

4. Execute a aplicação:
   ```bash
   python dashboard.py

5. Abra seu navegador e vá para http://127.0.0.1:8050/ para visualizar o painel.

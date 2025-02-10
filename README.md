# Gocase Business Case Analysis

## Visão Geral
Este repositório contém três notebooks que realizam análises de um business case da empresa **Gocase**. Os notebooks processam dados extraídos de uma planilha do Google Sheets e fornecem insights baseados em diferentes dimensões: **country (país), platform (plataforma) e age (idade)**.

## Estrutura do Repositório
```
Gocase/
│── conf/
│   │── settings.py
│── credentials/
│   │── credenciais_sheets.json
│── .gitignore
│── case_gocase_by_age.ipynb
│── case_gocase_by_country.ipynb
│── case_gocase_by_platform.ipynb
│── functions.py
│── README.md
│── requirements.txt
```

## Fonte de Dados
Os dados utilizados nas análises são extraídos de uma **planilha do Google Sheets** que contém três abas principais:
- **Country**: Dados segmentados por país
- **Platform**: Dados segmentados por plataforma
- **Age**: Dados segmentados por faixa etária

Para expandir a análise de **Country**, utilizamos dados externos:
- **População**: Extraídos da API do [RestCountries](https://restcountries.com/)
- **PIB per capita**: Obtidos do [World Bank](https://data.worldbank.org/)

## Processo de Análise
1. **Extração de Dados**:
   - Os dados são importados de um **Google Sheets** usando credenciais armazenadas no arquivo `credenciais_sheets.json`.
2. **Tratamento e Limpeza**:
   - Conversão de tipos de dados
   - Remoção de valores inconsistentes ou ausentes
3. **Análise Explorátoria**:
4. **Retorno ao Google Sheets**:
   - Os dataframes resultantes são exportados para um **Named Range** no Google Sheets

## Requisitos
Para rodar os notebooks, é necessário instalar as dependências listadas em `requirements.txt`:
```bash
pip install -r requirements.txt
```
Além disso, é necessário adicionar as suas credenciais da API do google sheets com acesso a planilha desejada

## Uso
1. Configure as credenciais do Google Sheets no arquivo `credenciais_sheets.json` e adicione a permissão a planilha.
2. Execute os notebooks.
3. Os resultados serão automaticamente enviados para o Google Sheets no Named Range correspondente.


from google.oauth2 import service_account
from googleapiclient.discovery import build
import numpy as np 
import pandas as pd
import pycountry
import requests
import re


################################# GOOGLE SHEETS #######################################

def get_named_range_as_dataframe(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, NAMED_RANGE):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    service = build('sheets', 'v4', credentials=credentials)
    try:
        result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                     range=NAMED_RANGE
                                                     ).execute()
    
        values = result.get('values', [])
        if not values:
            print(f'Nenhum dado encontrado no intervalo nomeado "{NAMED_RANGE}".')
            return
        
        df = pd.DataFrame(values[1:], columns=values[0])    
        return df    
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def save_df_to_named_range(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID, NAMED_RANGE, df):

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)  
    service = build('sheets', 'v4', credentials=credentials)  

    try:
        df = df.fillna(0)
        data = [df.columns.tolist()] + df.values.tolist()  
        body = {'values': data}  

        result = service.spreadsheets().values().update(
            spreadsheetId=SPREADSHEET_ID,   
            range=NAMED_RANGE,             
            valueInputOption="USER_ENTERED",
            body=body                        
        ).execute() 
        return result

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

################################# CASTING #####################################

# Função interna para limpar valores monetários
def clean_currency(value):
    if isinstance(value, str):
        try:
            return round(float(value.replace("$", "").replace(".", "").replace(",", ".").strip()), 2)
        except ValueError:
            return np.nan  
    return round(value, 2) if isinstance(value, (int, float)) else value

# Função interna para limpar valores percentuais
def clean_percentage(value):
    
    if isinstance(value, str):  
        try:
            return round(float(value.replace("%", "").replace(",", ".").strip()), 2)/100
        except ValueError:  
            return np.nan 
    return round(value, 2) if isinstance(value, (int, float)) else value 

# Função interna para limpar valores numéricos inteiros
def clean_int_numeric(value):
    if isinstance(value, str):
        try:
            return float(value.replace(".", "").replace(",", ".").strip()) 
        except ValueError:
            return np.nan
    return value

# Função interna para limpar valores numéricos decimais
def clean_float_numeric(value):
    if isinstance(value, str):
        try:
            return float(value.replace(",", ".").strip()) 
        except ValueError:
            return np.nan
    return value

def clean_and_cast_columns(df, 
                           currency_columns=["cpc_link", "cpc_general","cpc_geral", "cost_per_1000_people_reached",
                                             "cost_per_add_to_cart", "cost_per_initiate_checkout",
                                             "cost_per_purchase", "amount_spent", "purchase_conversion_value"], 
                            percentage_columns = ["result_rate", "ctr"], 
                            float_numeric_columns = ["reach", "frequency", "initiate_checkout", "purchase"], 
                            int_numeric_columns= ["results", "links_clicks", "add_to_cart", "initiate_checkout"]):
    for col in df.columns:
        if col in currency_columns:
            df[col] = df[col].apply(clean_currency) 
        elif col in percentage_columns:
            df[col] = df[col].apply(clean_percentage)  
        elif col in int_numeric_columns:
            df[col] = df[col].apply(clean_int_numeric) 
            df[col] = pd.to_numeric(df[col], errors='coerce').astype("Int64")
        elif col in float_numeric_columns:
            df[col] = df[col].apply(clean_float_numeric) 
            df[col] = pd.to_numeric(df[col], errors='coerce').round(2)
        else:
            pass  

    return df

def convert_column_names_to_standard_english(df):
    column_mapping = {
        "Ad Set Name": "ad_set_name",
        "Age": "age",
        "Result Rate": "result_rate",
        "Result Indicator": "result_indicator",
        "Results": "results",
        "Reach": "reach",
        "Frequency": "frequency",
        "Link Clicks": "links_clicks",
        "CPC (Link) (USD)": "cpc_link",
        "CPC (All) (USD)": "cpc_general",
        "Cost per 1,000 People Reached (USD)": "cost_per_1000_people_reached",
        "CTR (All)": "ctr",
        "Add to Cart (Facebook Pixel)": "add_to_cart",
        "Cost per Add To Cart (Facebook Pixel) (USD)": "cost_per_add_to_cart",
        "Initiate Checkout (Facebook Pixel)": "initiate_checkout",
        "Cost per Initiate Checkout (Facebook Pixel) (USD)": "cost_per_initiate_checkout",
        "Purchase (Facebook Pixel)": "purchase",
        "Cost per Purchase (Facebook Pixel) (USD)": "cost_per_purchase",
        "Amount Spent (USD)": "amount_spent",
        "Purchase Conversion Value (Facebook Pixel)": "purchase_conversion_value",
        "Country": "country",
        "Platform": 'platform'
    }
    df = df.rename(columns=column_mapping)
    return df

def convert_column_standard_english_to_portuguse(df, base):
    
    column_mapping = { 
        "ad_set_name": "nome_do_conjunto_de_anuncios",            
        "age": "idade",                                      
        "result_rate": "taxa_de_resultado",                     
        "result_indicator": "indicador_de_resultado",            
        "results": "resultados",                                 
        "reach": "alcance",                               
        "frequency": "frequencia",                                
        "links_clicks": "cliques_no_link",                        
        "cpc_link": "custo_por_clique_no_link",               
        "cpc_general": "custo_por_clique_geral",              
        "cost_per_1000_people_reached": "custo_por_1000_pessoas_alcancadas", 
        "ctr": "ctr",                             
        "add_to_cart": "adicionar_ao_carrinho",                 
        "cost_per_add_to_cart": "custo_por_adicionar_ao_carrinho",   
        "initiate_checkout": "iniciar_finalizacao_da_compra",      
        "cost_per_initiate_checkout": "custo_por_iniciar_finalizacao_da_compra", 
        "purchase": "compra",                        
        "cost_per_purchase": "custo_por_compra",          
        "amount_spent": "valor_gasto",                        
        "purchase_conversion_value": "valor_conversao_compra",    
        "country": "pais",                                  
        "platform": "plataforma",
        "campaign_goal": "objetivo_da_campanha",
        "classified_campaign_goal": "objetivo_classificado_da_campanha",
        "qty_ad_sets": "quantidade_de_campanhas",
        "conversion_rate": "taxa_de_conversao",
        "cart_to_checkout_conversion": "conversao_carrinho_checkout",
        "checkout_to_purchase_conversion": "conversao_checkout_compra",  
        "gdp_per_capita": "pib_per_capita",        
        "full_country_name": "nome_completo_do_pais",      
        "country_population": "populacao_do_pais",
        "reach_to_purchase_conversion": "conversao_alcance_compra"              
    }  
    if base == 'PT':
        column_mapping_reversed = {v: k for k, v in column_mapping.items()}
        df = df.rename(columns=column_mapping_reversed) 
    else:
        df = df.rename(columns=column_mapping)
    return df  

def create_column_campaign_goal(ad_set_name):
    match_date = re.search(r'\d{2}/\d{2}/\d{4}', ad_set_name)
    if ('LC Cart-Conversion' in ad_set_name) or ('LC Cart- Conversion' in ad_set_name):
        return 'LC Cart-Conversion'
    elif 'LC Conversion' in ad_set_name:
        return 'LC Conversion'
    elif 'Viewed' in ad_set_name or 'View 1 Day' in ad_set_name:
        return 'Viewed'
    elif match_date:
        return ad_set_name[:match_date.start()].strip()
    else:
        partes = re.split(r'\s*[-–]\s*', ad_set_name)
        return partes[0].strip()

def classify_campaign(motivo,
                      engagement_list = ['Viewed', 'LC Engagement', 'Instagram Post'], 
                      conversion_list = ['LC Checkout-Conversion', 'LC Conversion', 'LC Cart-Conversion',
                                         'LC Purchase-Conversion', 'RL Cart-Conversion', 'Add to cart']):
    if motivo in conversion_list:
        return 'Conversão'
    elif motivo in engagement_list:
        return 'Engajamento/Visualização'
    else:
        return 'Outros'

################################# aux country data #####################################

def get_population_by_country(countries):
    populations = {}  
    for country in countries:  
        try:
            url = f"https://restcountries.com/v3.1/name/{country}?fullText=true"  
            response = requests.get(url)  
            response.raise_for_status()  
            data = response.json()  

            if isinstance(data, list) and data:
                populations[country] = data[0].get("population", None)
            else:
                populations[country] = None  
        except Exception as e:  
            populations[country] = None  
            print(f"Erro ao obter dados para {country}: {e}")  

    return populations  

def get_country_full_names(country_codes):
    mapping = {}  
    for code in country_codes:  
        try:
            country = pycountry.countries.get(alpha_2=code) 
            mapping[code] = country.name if country else None  
        except Exception as e:  
            mapping[code] = None  
            print(f"Erro ao processar o código {code}: {e}")  
    return mapping  

def get_gdp_per_capita(country_code):
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/NY.GDP.PCAP.CD?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        try:
            return data[1][0]['value']
        except (IndexError, KeyError, TypeError):
            return None
    else:
        return None
    
################################# analytics #####################################

def calculate_percentages_by_goal(df, main_column, classified_campaign_goal='Conversão'):
    df = df[df['classified_campaign_goal'] == classified_campaign_goal]
    
    df_agrupado = df.groupby([main_column, 'classified_campaign_goal'], as_index=False).agg(
        results=('results', 'sum'),                     
        purchase=('purchase', 'sum'),                   
        purchase_conversion_value=('purchase_conversion_value', 'sum'),  
        amount_spent=('amount_spent', 'sum'),           
        count=('results', 'size')                      
    )
    
    total_results = df_agrupado['results'].sum()              
    total_purchase = df_agrupado['purchase'].sum()   
    total_pc_value = df_agrupado['purchase_conversion_value'].sum()  
    total_spent = df_agrupado['amount_spent'].sum()                  
    
    df_agrupado['pct_results'] = df_agrupado['results'] / total_results if total_results != 0 else 0
    df_agrupado['pct_purchase'] = df_agrupado['purchase'] / total_purchase if total_purchase != 0 else 0
    df_agrupado['pct_purchase_conversion_value'] = (df_agrupado['purchase_conversion_value'] / total_pc_value) if total_pc_value != 0 else 0
    df_agrupado['pct_amount_spent'] = df_agrupado['amount_spent'] / total_spent if total_spent != 0 else 0
    df_agrupado['pct_count'] = df_agrupado['count'] / df_agrupado['count'].sum()
    
    df_formatado = df_agrupado.copy()
    for col in ['pct_results', 'pct_purchase', 'pct_purchase_conversion_value', 'pct_amount_spent', 'pct_count']:
        df_formatado[col] = (df_formatado[col]).round(2)
    
    return df_formatado
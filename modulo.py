import pandas as pd
import requests

def pegar_balanco (ticker,trimestre):
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEzNTQ4LCJpYXQiOjE3NDUzMjE1NDgsImp0aSI6ImM1ZmY3OTI1NWJmMjQxMzhiOWUxNzA0OGU4MGExYjMxIiwidXNlcl9pZCI6NjJ9.ZtWMoyT4OwABN0U38QqGXVbgyqECNcubyF7MWpjcoCc'
    headers = {'Authorization': 'JWT {}'.format(token)}
    params = {'ticker': ticker, 'ano_tri': trimestre,}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
    dados = r.json()['dados'][0]
    balanco = dados ['balanco'] 
    df= pd.DataFrame(balanco)
    return df 

def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False)
    valor = sum(df[filtro_conta & filtro_descricao]['valor'].values)
    return valor

def indicador_comparacao(df): 
        lucro = valor_contabil(df,'^3.*','lucro')
        pl = valor_contabil(df,'^2.*','patri')
        roe = lucro / pl 
        capital_oneroso = valor_contabil(df,'^2.0','^empr.stimo')+(valor_contabil(df,'^2.0','^deb.ntures'))
        investimento = capital_oneroso + pl 
        wi = capital_oneroso/investimento
        ki = 0.15
        we = pl/investimento 
        ke = 0.17 
        wacc = wi*ki + we*ke 
        eva = roe - wacc
        return{
             "roe":roe,
             "eva":eva, 
        }

import requests


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEzNTQ4LCJpYXQiOjE3NDUzMjE1NDgsImp0aSI6ImM1ZmY3OTI1NWJmMjQxMzhiOWUxNzA0OGU4MGExYjMxIiwidXNlcl9pZCI6NjJ9.ZtWMoyT4OwABN0U38QqGXVbgyqECNcubyF7MWpjcoCc'
headers = {'Authorization': 'JWT {}'.format(token)}

def pegar_preco_corrigido(ticker,data_ini,data_fim):
    params = {
    'ticker': ticker,
    'data_ini': data_ini,
    'data_fim': data_fim
    }
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido',params=params, headers=headers)
    dados = r.json()['dados']
    return pd.DataFrame(dados)

def pegar_preco_diversos(ticker,data_ini,data_fim):
    params = {
    'ticker': ticker,
    'data_ini': data_ini,
    'data_fim': data_fim
    }
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
    dados = r.json()['dados']
    return pd.DataFrame(dados)
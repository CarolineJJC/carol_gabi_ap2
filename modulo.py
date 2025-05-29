import pandas as pd
import requests
import matplotlib.pyplot as plt

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzUwNTA2NzgwLCJpYXQiOjE3NDc5MTQ3ODAsImp0aSI6IjI5MDNiYzY1YzJmMjRhMmM4ZWMyYjc1OWVmZjYxOTUzIiwidXNlcl9pZCI6NjJ9.6Ym97dsBaUXrnwCmheBQvYq-O1bIwTGkRgPojnVKVFM'
headers = {'Authorization': f'JWT {token}'}


def pegar_balanco(ticker, trimestre):
    params = {'ticker': ticker, 'ano_tri': trimestre}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco', params=params, headers=headers)
    if r.status_code != 200 or not r.json().get('dados'):
        print(f"Erro ou dados ausentes para {ticker} - {trimestre}")
        return pd.DataFrame()
    return pd.DataFrame(r.json()['dados'][0]['balanco'])

def pegar_preco_corrigido(ticker, data_ini, data_fim):
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-corrigido', params=params, headers=headers)
    if r.status_code != 200:
        print(f"Erro ao buscar preço corrigido de {ticker}")
        return pd.DataFrame()
    return pd.DataFrame(r.json().get('dados', []))

def pegar_preco_diversos(ticker, data_ini, data_fim):
    params = {'ticker': ticker, 'data_ini': data_ini, 'data_fim': data_fim}
    r = requests.get('https://laboratoriodefinancas.com/api/v1/preco-diversos', params=params, headers=headers)
    if r.status_code != 200:
        print(f"Erro ao buscar preço diversos de {ticker}")
        return pd.DataFrame()
    return pd.DataFrame(r.json().get('dados', []))


def valor_contabil(df, conta, descricao):
    filtro_conta = df['conta'].str.contains(conta, case=False, na=False)
    filtro_descricao = df['descricao'].str.contains(descricao, case=False, na=False)
    return df[filtro_conta & filtro_descricao]['valor'].sum()

def indicador_comparacao(df):
    lucro = valor_contabil(df, '^3.*', 'lucro')
    lucro
    pl = valor_contabil(df, '^2.*', 'patri')
    pl
    if pl == 0:
        return {"roe": 0, "eva": 0}
    roe = lucro / pl
    co = valor_contabil(df, '^2.0', '^empr.stimo') + valor_contabil(df, '^2.0', '^deb.ntures')
    investimento = co + pl
    wi, we = co / investimento, pl / investimento
    ki, ke = 0.15, 0.17
    wacc = wi * ki + we * ke
    eva = roe - wacc
    return {"roe": roe, "eva": eva}


def indicador_fundamentalista(df):
    ac = df[df['descricao'] == 'Ativo Circulante']['valor'].values[0]
    pc = df[df['descricao'] == 'Passivo Circulante']['valor'].values[0]
    pl = df[df['descricao'].str.contains('Patrim.nio', case=False)]['valor'].values[0]
    arlp = df[df['descricao'].str.contains('ativo realiz.vel', case=False)]['valor'].values[0]
    pnc = df[df['descricao'].str.contains('passivo n.o circulante', case=False)]['valor'].values[0]
    estoques = df[df['descricao'].str.contains('estoques', case=False)]['valor'].sum()
    caixa = df[df['descricao'].str.contains('Caixa', case=False)]['valor'].values[0]
    aplicacoes = df[df['descricao'].str.contains('aplica..es', case=False)]['valor'].values[0]
    passivo_total = df[df['descricao'].str.contains('Passivo Total', case=False)]['valor'].values[0]
    ativo_total = df[df['descricao'].str.contains('Ativo total', case=False)]['valor'].values[0]
    imobilizado = df[df['descricao'].str.contains('Imobilizado', case=False)]['valor'].values[0]
    intangivel = df[df['descricao'].str.contains('Intang.vel', case=False)]['valor'].values[0]
    investimentos = df[df['descricao'].str.contains('Investimentos', case=False)]['valor'].values[0]

    indicadores = {
        "ccl": ac - pc,
        "liquidez_corrente": ac / pc,
        "liquidez_geral": (ac + arlp) / (pc + pnc),
        "liquidez_seca": (ac - estoques) / pc,
        "liquidez_imediata": (caixa + aplicacoes) / pc,
        "endividamento": (passivo_total - pl) / passivo_total,
        "solvencia": ativo_total / (passivo_total - pl),
        "relacao_ct_cp": (passivo_total - pl) / pl,
        "composicao_endividamento": pc / (passivo_total - pl),
        "ipl": (imobilizado + intangivel + investimentos) / pl,
        "caixa": caixa,
        "aplicacoes": aplicacoes,
        "ac": ac,
        "pc": pc,
        "pl": pl,
        "disponivel": caixa + aplicacoes,
        "imobilizado": imobilizado,
        "intangivel": intangivel,
        "investimentos": investimentos
    }
    return indicadores

def print_indicadores(indicadores):
    print("\n=== Indicadores Fundamentais ===")
    for chave, valor in indicadores.items():
        print(f"{chave}: {valor:,.2f}")

def calcular_com_2023(df23, indicadores, df):
    estoque_2024 = df[df['descricao'].str.contains('estoques', case=False)]['valor'].sum()
    estoque_2023 = df23[df23['descricao'].str.contains('estoques', case=False)]['valor'].sum()
    estoque_med = (estoque_2023 + estoque_2024) / 2

    cmv = df[df['descricao'].str.contains('Custos Prods., Mercs. e Servs. Vendidos', case=False)]['valor'].values[0]
    pme = (estoque_med / -cmv) * 360
    ge = 360 / pme

    clientes_2024 = df[df['descricao'].str.contains('clientes', case=False)]['valor'].values[0]
    clientes_2023 = df23[df23['descricao'].str.contains('clientes', case=False)]['valor'].values[0]
    clientes_med = (clientes_2024 + clientes_2023) / 2
    receita = df[df['descricao'].str.contains('receitas', case=False)]['valor'].values[5]
    pmrv = (-clientes_med / receita) * 360

    fornecedores_2024 = df[df['descricao'].str.contains('fornecedores', case=False)]['valor'].values[0]
    fornecedores_2023 = df23[df23['descricao'].str.contains('fornecedores', case=False)]['valor'].values[0]
    fornecedores_med = (fornecedores_2024 + fornecedores_2023) / 2
    compras = estoque_2024 - estoque_2023 + (-cmv)
    pmpf = (fornecedores_med / compras) * 360

    co = pme + pmrv
    cf = pmpf - co
    ce = pme

    acf = indicadores['caixa'] + indicadores['aplicacoes']
    aco = indicadores['ac'] - acf

    emprestimos = df[df['descricao'].str.contains('empr.stimo', case=False)]['valor'].sum()
    debentures = df[df['descricao'].str.contains('deb.ntures', case=False)]['valor'].sum()
    pcf = emprestimos + debentures
    pco = indicadores['pc'] - pcf
    ncg = aco - pco
    st = acf - pcf

    cg = indicadores['ac'] - indicadores['pc']

    po = debentures + emprestimos
    dl = po - (indicadores['disponivel'] + indicadores['aplicacoes'])
    inv = po + indicadores['pl']
    capital_oneroso = dl + indicadores['pl']
    rdlpl = dl / (dl + indicadores['pl'])

    return {
        "cmv": cmv, "pme": pme, "ge": ge, "pmrv": pmrv, "pmpf": pmpf,
        "ciclo_operacional": co, "ciclo_financeiro": cf, "ciclo_economico": ce,
        "ncg": ncg, "st": st, "capital_giro": cg,
        "divida_liquida": dl, "investimento": inv, "capital_oneroso": capital_oneroso,
        "relacao_divida_liquida_pl": rdlpl
    }

#BACKTEST
def backtest(ticker, data_ini, data_fim):
    df_preco = pegar_preco_corrigido(ticker, data_ini, data_fim)
    df_ibov = pegar_preco_diversos("ibov", data_ini, data_fim)

    if df_preco.empty or df_ibov.empty:
        print(f"Dados insuficientes para {ticker}")
        return

    preco_ini = df_preco.iloc[0]["fechamento"]
    preco_fim = df_preco.iloc[-1]["fechamento"]
    lucro = (preco_fim / preco_ini) - 1
    print(f"[{ticker}] Lucro: {lucro:.2%}")

    preco_ini_ibov = df_ibov.iloc[0]["fechamento"]
    preco_fim_ibov = df_ibov.iloc[-1]["fechamento"]
    lucro_ibov = (preco_fim_ibov / preco_ini_ibov) - 1
    print(f"[IBOV] Lucro: {lucro_ibov:.2%}")

    df_preco = df_preco[["data", "fechamento"]].rename(columns={"fechamento": ticker})
    df_ibov = df_ibov[["data", "fechamento"]].rename(columns={"fechamento": "IBOV"})
    df_grafico = pd.merge(df_preco, df_ibov, on="data")
    df_grafico.set_index("data", inplace=True)

    df_grafico[ticker] = df_grafico[ticker] / df_grafico[ticker].iloc[0]
    df_grafico["IBOV"] = df_grafico["IBOV"] / df_grafico["IBOV"].iloc[0]

    df_grafico.plot(figsize=(10, 5), title=f"Backtest - {ticker} vs IBOV (Normalizado)")
    plt.xlabel("Data")
    plt.ylabel("Variação Normalizada")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    empresas = ["EZTC3", "CYRE3", "EVEN3", "JHSF3", "TCSA3", "GFSA3"]
    trimestre = "20244T"
    for ticker in empresas:
        print(f"\n\n{ticker}")
        df = pegar_balanco(ticker, trimestre)

        # Comparativo ROE e EVA
        comparativo = indicador_comparacao(df)
        print(f"{ticker} => ROE: {comparativo['roe']:.2%}, EVA: {comparativo['eva']:.2%}")

        # Indicadores fundamentalistas
        indicadores = indicador_fundamentalista(df)
        print_indicadores(indicadores)

        # Comparação com dados do 4T23
        df_2023 = pegar_balanco(ticker, "20234T")
        indicadores_2023 = calcular_com_2023(df_2023, indicadores, df)
        print("\nIndicadores Operacionais e de Eficiência (Comparação com 2023)")
        for chave, valor in indicadores_2023.items():
            print(f"{chave}: {valor:,.2f}")

        # Gráfico de desempenho
        backtest(ticker, "2015-05-01", "2025-03-31")



def backtest_multiplo(empresas, data_ini, data_fim):
    df_ibov = pegar_preco_diversos("ibov", data_ini, data_fim)
    if df_ibov.empty:
        print("Erro ao buscar dados do IBOV.")
        return

    df_ibov = df_ibov[["data", "fechamento"]].rename(columns={"fechamento": "IBOV"})

    df_final = df_ibov.copy()

    for ticker in empresas:
        df_preco = pegar_preco_corrigido(ticker, data_ini, data_fim)
        if df_preco.empty:
            print(f"Dados ausentes para {ticker}.")
            continue

        df_preco = df_preco[["data", "fechamento"]].rename(columns={"fechamento": ticker})
        df_final = pd.merge(df_final, df_preco, on="data", how="inner")

    df_final.set_index("data", inplace=True)

    # Normalizar todos os preços para comparar performance
    for col in df_final.columns:
        df_final[col] = df_final[col] / df_final[col].iloc[0]

    df_final.plot(figsize=(14, 6), title="Backtest Comparativo - Empresas vs IBOV")
    plt.xlabel("Data")
    plt.ylabel("Variação Normalizada")
    plt.grid(True)
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
print("\n\nGRÁFICO COMPARATIVO MULTIEMPRESAS")
backtest_multiplo(empresas, "2015-05-01", "2025-03-31")



def roe_eva_por_anos_selecionados(empresas, anos=[2015, 2020, 2024]):
    resultados = []

    for ticker in empresas:
        for ano in anos:
            try:
                df = pegar_balanco(ticker, f"{ano}4T")
                if df.empty:
                    print(f"Dados ausentes: {ticker} - {ano}4T")
                    continue
                comp = indicador_comparacao(df)
                resultados.append({
                    "empresa": ticker,
                    "ano": ano,
                    "roe": comp["roe"],
                    "eva": comp["eva"]
                })
            except Exception as e:
                print(f"Erro em {ticker} - {ano}: {e}")
                continue

    return pd.DataFrame(resultados)



    anos_alvo = [2015, 2020, 2024]
    df_resumo = roe_eva_por_anos_selecionados(empresas, anos_alvo)

    print("\n=== ROE & EVA por Empresa nos anos 2015, 2020 e 2024 ===")
    print(df_resumo)

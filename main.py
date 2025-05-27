from modulo import (pegar_balanco,indicador_comparacao,pegar_preco_corrigido,pegar_preco_diversos)
import pandas as pd 



def main (): 
    list_ticker = ["CYRE3", "GFSA3", "TCSA3", "EVEN3","JHSF3", "EZTC3"]
    list_tri = ["20194T"]
    df_comparacao = pd.DataFrame()
    for ticker in list_ticker: 
        for trimestre in list_tri: 
            #ticker = "EZTC3"
           #trimestre = "20194T"
            df = pegar_balanco(ticker,trimestre)
            comparacao = indicador_comparacao(df)
            df_final = pd.DataFrame()
            df_final["ticker"]=[ticker]
            df_final["roe"]=comparacao["roe"]
            df_final["eva"]=comparacao["eva"]
            df_comparacao=pd.concat([df_comparacao,df_final],axis=0, ignore_index=True)
    print (df_comparacao)





    #Backtest (fazer 5 anos de backtest)
    ticker =  "JHSF3"
    data_ini = "2019-04-01"
    data_fim = "2020-03-31"
    df_preco= pegar_preco_corrigido(ticker,data_ini,data_fim)
    preco_ini = df_preco[0:1]["fechamento"].iloc[0]
    preco_fim = df_preco[-1:]["fechamento"].iloc[0]
    lucro = (preco_fim/preco_ini)-1
    print(lucro)

    #Ibovespa 
    ticker = "ibov"
    df_ibov = pegar_preco_diversos(ticker, data_ini, data_fim)
    preco_ini = df_ibov[0:1]["fechamento"].iloc[0]
    preco_fim = df_ibov[-1:]["fechamento"].iloc[0]
    lucro_ibov= (preco_fim/preco_ini)-1
    print(lucro_ibov)
    df_ibov = df_ibov[["data","fechamento"]]
    df_ibov = df_ibov.rename(columns={"fechamento": "ibov"})

    df_preco = df_preco[["data","fechamento"]]
    df_preco = df_preco.rename(columns={"fechamento": "JHSF3"})
    df_grafico = pd.merge(df_preco, df_ibov)
    df_grafico.plot()

main()




# #20244T
#  ticker       roe       eva
# 0  CYRE3  0.386169  0.227167 #Alta rentabilidade e forte geração de valor econômico.
# 1  GFSA3 -0.041724 -0.198063 #ROE e EVA negativos → prejuízo e destruição de valor.
# 2  TCSA3 -0.783068 -0.937495 #Ambos extremamente negativos → pior desempenho.
# 3  EVEN3  0.127131 -0.032225 #ROE positivo modesto, mas destrói valor.
# 4  JHSF3  0.295226  0.138970 #ROE e EVA positivos → rentável e gera valor.
# 5  EZTC3  0.175592  0.011944 #ROE moderado, EVA levemente positivo → rentável, mas geração de valor quase nula.

# 1º lugar: CYRE3
# 2º lugar: JHSF3 
# 3º lugar: EZTC3  

# #20234T
#   ticker       roe       eva
# 0  CYRE3  0.260170  0.101577
# 1  GFSA3 -0.228983 -0.384907
# 2  TCSA3 -0.206407 -0.361832
# 3  EVEN3  0.237017  0.076625
# 4  JHSF3  0.190645  0.033460
# 5  EZTC3  0.104609 -0.060054

# #Redimento da empresa Cyrela: 0.9188524513259853
# #Comparar com o Ibovespa no mesmo período: 0.262053474671448

#   ticker       roe       eva
# 0  CYRE3  0.206481  0.046474
# 1  GFSA3 -0.031510 -0.189107
# 2  TCSA3 -0.554318 -0.715840
# 3  EVEN3  0.152058 -0.005950
# 4  JHSF3  0.215795  0.055991
# 5  EZTC3  0.152491 -0.017082
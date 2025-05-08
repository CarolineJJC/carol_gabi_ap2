import pandas as pd
import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEzNTQ4LCJpYXQiOjE3NDUzMjE1NDgsImp0aSI6ImM1ZmY3OTI1NWJmMjQxMzhiOWUxNzA0OGU4MGExYjMxIiwidXNlcl9pZCI6NjJ9.ZtWMoyT4OwABN0U38QqGXVbgyqECNcubyF7MWpjcoCc'
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'EZTC3', 'ano_tri': '20244T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados ['balanco'] 
df= pd.DataFrame(balanco)


def indicador_fundalista(df):

    #CCL  #excel: 2233724,00
    #vs code: 2233724.0
    df_valor = df[['descricao', 'valor']]
    linha1 = df_valor.loc[df_valor['descricao']=='Ativo Circulante']
    linha1
    ac = linha1['valor'].values[0]
    ac 


    linha2 = df_valor.loc[df_valor['descricao']=='Passivo Circulante']
    pc = linha2['valor'].values[0]
    pc    

    ccl = ac - pc 
    ccl


    #índice de liquidez corrente    #excel: 6,84
    #vs code: 6,84
    lc = ac/pc
    lc

        ##outra forma de resolver:
    filtro = df['descricao'].str.contains('Ativo Circulante')
    ativo_circulante = df[filtro]['valor'].values[0]

    filtro2 = df['descricao'].str.contains('Passivo Circulante')
    passivo_circulante = df[filtro2]['valor'].values[0]
    liquidez_corrente = ativo_circulante/passivo_circulante
    liquidez_corrente


    #liquidez geral:      #excel: 3,73 
    #vs code: 3,73
    pre_arlp = df[df['descricao'].str.contains('ativo realiz.vel', case=False)][["valor", "descricao"]]
    arlp = pre_arlp['valor'].values[0]
    arlp
    ac

    pre_pnc = df[df['descricao'].str.contains('passivo n.o circulante', case=False)][["valor", "descricao"]]
    pnc = pre_pnc['valor'].values[0]
    pnc

    lg = (ac+arlp)/(pc+pnc)
    print(lg)


    #liquidez seca  #excel: 3,24
    #vs code: 3,237

    pre_estoques = df[df['descricao'].str.contains('estoques', case=False)][["valor", "descricao"]]
    estoques_c = pre_estoques['valor'].values[0]
    estoques_c

    df[df['descricao'].str.contains('despesa', case=False)][["valor", "descricao"]]

    ls = (ac -estoques_c)/pc
    print(ls)    




    #liquidez imediata  #excel: 2,01  
    # #vs code: 2,01


    caixa = df[df['descricao'].str.contains('Caixa e Equivalentes de Caixa', case=False)][["valor"]].values[0][0]
    caixa
    aplicacoes = df[df['descricao'].str.contains('aplica..es', case=False)][["valor"]].values[0][0]
    aplicacoes

    disponivel = caixa +aplicacoes
    li = disponivel/pc
    li



    #endividamento  #excel: 0,244 
     #vs code: 0,24


    passivo_total = df[df['descricao'].str.contains('Passivo Total', case=False)][["valor"]].values[0][0]
    passivo_total
    pl = df[df['descricao'].str.contains('Patrim.nio l.quido consolidado', case=False)][["valor"]].values[0][0]
    pl
    passivo = passivo_total - pl
    passivo
    endividamento = passivo/(passivo+pl)
    endividamento


    #solvência #excel: 4,084   
    #vs code: 4,084

    a = df[df['descricao'].str.contains('Ativo total', case=False)][["valor"]].values[0][0]
    solv = a/passivo
    solv

    #relação ct/cp (passivo/pl) #excel: 0,32   
    #vs code: 0,32

    ctcp = passivo/pl
    ctcp

    #composição endividamento (pc/passivo)  #excel: 0,24  

    ce = pc/passivo
    ce


    #ipl (ativos fixos/pl)  #excel: 0,099
    #vs code: 0,11      ######################################################################################


    imob = df[df['descricao'].str.contains('^Imobili', case=False)]
    imobilizado = df[df['descricao'].str.contains('Imobilizado', case=False)][["valor"]].values[0][0]
    imobilizado
    int = df[df['descricao'].str.contains('^intang', case=False)]
    intangivel = df[df['descricao'].str.contains('Intangível', case=False)][["valor"]].values[0][0]
    intangivel
    invest =df[df['descricao'].str.contains('Investimentos', case=False)] [["valor"]].values[0][0]

    invest       ################valor de investimento não está vindo igual a planilha do filipe


    ipl = (imobilizado + intangivel + invest)/pl
    ipl





    #cmv   #excel:  -266.469   ###################################################
    #vs code: -1.027.729

    df[df['descricao'].str.contains('Custo', case=False)]    

    cmv = df[df['descricao'].str.contains('Custos Prods., Mercs. e Servs. Vendidos', case=False)][["valor"]].values[0][0]
    cmv        ################ valor está diferente da planilha do filipe



    #pme (estoque médio/cmv)*360  #excel: 1892,01333    ########################################################
    #vs code: 1089.33

    params2 = {'ticker': 'EZTC3', 'ano_tri': '20234T',}
    r2 = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params2, headers=headers)
    dados2 = r2.json()['dados'][0]
    balanco2 = dados2['balanco']
    df23= pd.DataFrame(balanco2)



    estoque24_1 = df[df['descricao'].str.contains('estoques', case=False)][["valor"]].values[0][0]
    estoque24_2 = df[df['descricao'].str.contains('estoques', case=False)][["valor"]].values[1][0]
    estoque24_2
    estoque_2024 = estoque24_1 + estoque24_2

    estoque23_1 = df23[df23['descricao'].str.contains('estoques', case=False)][["valor"]].values[0][0]
    estoque23_2 = df23[df23['descricao'].str.contains('estoques', case=False)][["valor"]].values[1][0]
    estoque2023= estoque23_1 + estoque23_2               

    estoque_med = (estoque2023 + estoque_2024)/2

    pme = (estoque_med/(-cmv))*360
    pme                           ########################na planilha do filipe provavelmente entram mais coisas em estoques do que o que colocamos




    #ge (360/pme)    #excel: 0,19   ###########################################################################################
    #vs code: 0,33

    ge = 360/pme        ######se pme está errado, então ge também vai estar
    ge


    #pmrv (clientes médios/receita)*360    excel: 937,83      ########################################################
    #vscode: 64,87
    clientes = df[df['descricao'].str.contains('Contas a receber de clientes', case=False)][["valor"]].values[0][0]
    clientes ############## valor de clientes está diferente (lá clientes é mesmo contas a receber de clientes?)                                     

    clientes23 = df23[df23['descricao'].str.contains('Contas a receber de clientes', case=False)][["valor"]].values[0][0]
    clientes23
    clientes_med = (clientes + clientes23)/2

    receita = df[df['descricao'].str.contains('receitas', case=False)][["valor"]].values[5][0]
    receita   #############esse valor também está diferente. tenho que ver se é receita líquida

    pmrv = ((-clientes_med)/receita)*360
    pmrv



    #pmpf (fornecedores médio/compras)*360         #compras = estoque final-inicial + cmv
    #excel: 0,4  ###############################################################################################
    #vs code: 18,2

    fornecedores24 = df[df['descricao'].str.contains('fornecedores', case=False)][["valor"]].values[0][0]
    fornecedores24
    fornecedores23 =  df23[df23['descricao'].str.contains('fornecedores', case=False)][["valor"]].values[0][0]                    #23 não está vindo 23

    fornecedores_med = (fornecedores24 + fornecedores23)/2
    fornecedores_med   #certo

    compras =  estoque_2024 - estoque2023 +(- cmv)       #####se estoques e cmv estão diferentes, vai dar errado mesmo

    pmpf = (fornecedores_med/compras)*360
    pmpf


    #ciclo operacional (pme + pmrv)    #excel: 2829,84   ###########################################################
    #vs code: 1154,198
    co = pme + pmrv        
    co                       ## pmrv está errado


    #ciclo financeiro   #excel: 2829,392713
    #vs code: -1135,99
    cf = pmpf-co
    cf            #pmpf está errado


    #ciclo econômico   #excel: 1892,01333    #######################################################################
    #vs code: 1089,33
    ce = pme
    ce                #pme está errado 


    #ncg (aco - pco)    #excel: 1.623.065
    #vs code: 1.594.745

    acf = caixa + aplicacoes
caixa
aplicacoes

    aco = ac - acf   #confirmar fórmula na planilha do filipe
    aco
    acf #certo
    ac #certo


    emprestimos1 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[0][0]
    emprestimos2 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[1][0]
    div = df[df['descricao'].str.contains('dividendos', case=False)][["valor"]].values[1][0]
    pr = df[df['descricao'].str.contains('partes rel', case=False)][["valor"]].values[6][0]
    debentures = df[df['descricao'].str.contains('deb.ntures', case=False)][["valor"]].values[0][0]


    pcf = emprestimos1 + emprestimos2 + div + pr + debentures
    pco = pc - pcf
                              #revisar antes planilha do filipe para ver o que entra em pcf e pco
    ngc = aco - pco
    ngc



    #st (acf - pcf)  #excel: 649.766    ################################################################
    #vs code: 638979.0
    st = acf - pcf
    st                       #acf e pcf têm que estar certos para dar certo




    #capital de giro      #excel: 2233724
    #vs code: 2233724.0
    cg = ac-pc
    cg



############################################ continuar depois revisão a partir daqui ###########################################################


    #divida líquida (po-(disponivel + aplicacoes))   #excel: 365950    ####################################################################
    #vs code: 803281.0

    debent1 = df[df['descricao'].str.contains('deb.ntures', case=False)][["valor"]].values[0][0]
    debent2 = df[df['descricao'].str.contains('deb.ntures', case=False)][["valor"]].values[1][0]
    emprestimos1 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[0][0]
    emprestimos2 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[1][0]
    emprestimos3 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[2][0]
    emprestimos4 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[3][0]

    po = debent1+debent2+emprestimos1+emprestimos2+emprestimos3+emprestimos4
    po

    dl = po - (disponivel+aplicacoes)
    dl

    #investimento (po + pl)  #excel: 6019508   ########################################################################
    #vs code: 7155890.0

    inv = po + pl
    inv

    #capital oneroso (divida liquida + pl)  #excel: 5249076
    #vs code: 5686407.0

    co = dl + pl
    co

    #relação divida liquida pl (divida liquida / divida liquida + pl)  #excel: 0,074941748  ############################################################
    #vs code: 0.14
    rdlpl = dl/(dl +pl)
    rdlpl
    
    indicadores = {
        "ccl": ccl,
        "liquidez_corrente": lc,
        "liquidez_geral": lg,
        "liquidez_seca": ls,
        "liquidez_imediata": li,
        "endividamento": endividamento,
        "solvencia": solv,
        "relacao_ct_cp": ctcp,
        "composicao_endividamento": ce,
        "ipl": ipl,
        "cmv": cmv,
        "pme": pme,
        "ge": ge,
        "pmrv": pmrv,
        "pmpf": pmpf,
        "ciclo_operacional": co,
        "ciclo_financeiro": cf,
        "ciclo_economico": ce,
        "ncg": ngc,
        "st": st,
        "capital_giro": cg,
        "divida_liquida": dl,
        "investimento": inv,
        "capital_oneroso": co,
        "relacao_divida_liquida_pl": rdlpl
    }
    
    return indicadores

dic_eztec = indicador_fundalista(df)
dic_eztec = indicador_fundalista(df)
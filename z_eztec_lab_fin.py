import pandas as pd
import requests

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ3OTEzNTQ4LCJpYXQiOjE3NDUzMjE1NDgsImp0aSI6ImM1ZmY3OTI1NWJmMjQxMzhiOWUxNzA0OGU4MGExYjMxIiwidXNlcl9pZCI6NjJ9.ZtWMoyT4OwABN0U38QqGXVbgyqECNcubyF7MWpjcoCc'
headers = {'Authorization': 'JWT {}'.format(token)}
params = {'ticker': 'EZTC3', 'ano_tri': '20244T',}
r = requests.get('https://laboratoriodefinancas.com/api/v1/balanco',params=params, headers=headers)
dados = r.json()['dados'][0]
balanco = dados ['balanco'] 
df= pd.DataFrame(balanco)

#CCL
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


#índice de liquidez corrente
lc = ac/pc
lc

    ##outra forma de resolver:
filtro = df['descricao'].str.contains('Ativo Circulante')
ativo_circulante = df[filtro]['valor'].values[0]

filtro2 = df['descricao'].str.contains('Passivo Circulante')
passivo_circulante = df[filtro2]['valor'].values[0]
liquidez_corrente = ativo_circulante/passivo_circulante
liquidez_corrente


#liquidez geral:
pre_arlp = df[df['descricao'].str.contains('ativo realiz.vel', case=False)][["valor", "descricao"]]
arlp = pre_arlp['valor'].values[0]

pre_pnc = df[df['descricao'].str.contains('ativo n.o circulante', case=False)][["valor", "descricao"]]
pnc = pre_pnc['valor'].values[0]

lg = (ac+arlp)/(pc+pnc)
print(lg)


#liquidez seca
pre_estoques = df[df['descricao'].str.contains('estoques', case=False)][["valor", "descricao"]]
estoques_c = pre_estoques['valor'].values[0]
estoques_c

df[df['descricao'].str.contains('despesa', case=False)][["valor", "descricao"]]

ls = (ac -estoques_c)/pc
print(ls)    




#liquidez imediata
caixa = df[df['descricao'].str.contains('Caixa e Equivalentes de Caixa', case=False)][["valor"]].values[0][0]
aplicacoes = df[df['descricao'].str.contains('aplica..es', case=False)][["valor"]].values[0][0]

disponivel = caixa +aplicacoes
li = disponivel/pc
li



#endividamento
passivo_total = df[df['descricao'].str.contains('Passivo Total', case=False)][["valor"]].values[0][0]
passivo_total
pl = df[df['descricao'].str.contains('Patrim.nio l.quido consolidado', case=False)][["valor"]].values[0][0]
pl
endividamento = passivo_total/(passivo_total+pl)]
endividamento

#solvência 
a = df[df['descricao'].str.contains('Ativo total', case=False)][["valor"]].values[0][0]
solv = a/passivo_total
solv

#relação ct/cp (passivo/pl)
ctcp = passivo_total/pl
ctcp

#composição endividamento (pc/passivo)
ce = pc/passivo_total
ce

#ipl (ativos fixos/pl)   ######################################################################################
imob = df[df['descricao'].str.contains('^Imobili', case=False)]
imobilizado = df[df['descricao'].str.contains('Imobilizado', case=False)][["valor"]].values[0][0]
imobilizado
int = df[df['descricao'].str.contains('^intang', case=False)]
intangivel = df[df['descricao'].str.contains('Intangível', case=False)][["valor"]].values[0][0]
intangivel
invest =df[df['descricao'].str.contains('Investimentos', case=False)][["valor"]].values[0][0]
invest    


ipl = (imobilizado + intangivel + invest)/pl
ipl





#cmv 
df[df['descricao'].str.contains('Custo', case=False)]    

cmv = df[df['descricao'].str.contains('Custos Prods., Mercs. e Servs. Vendidos', case=False)][["valor"]].values[0][0]
cmv


#pme (estoque médio/cmv)*360   ###################################
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
pme                           ########################





#ge (360/pme)  ou  (cmv/estoque médio)
ge = 360/pme
ge


#pmrv (clientes médios/receita)*360          ########################################################
clientes = df[df['descricao'].str.contains('Contas a receber de clientes', case=False)][["valor"]].values[0][0]
clientes                                      

clientes23 = df23[df23['descricao'].str.contains('Contas a receber de clientes', case=False)][["valor"]].values[0][0]
clientes23
clientes_med = (clientes + clientes23)/2

receita = df[df['descricao'].str.contains('receitas', case=False)][["valor"]].values[5][0]
receita

pmrv = ((-clientes_med)/receita)*360
pmrv
                                                ###################


#pmpf (fornecedores médio/compras)*360         #compras = estoque final-inicial + cmv
fornecedores24 = df[df['descricao'].str.contains('fornecedores', case=False)][["valor"]].values[0][0]
fornecedores24
fornecedores23 =  df23[df23['descricao'].str.contains('fornecedores', case=False)][["valor"]].values[0][0]                    #23 não está vindo 23

fornecedores_med = (fornecedores24 + fornecedores23)/2

compras =  estoque_2024 - estoque2023 +(- cmv)

pmpf = (fornecedores_med/compras)*360
pmpf


#ciclo operacional (pme + pmrv)
co = pme + pmrv
co


#ciclo financeiro
cf = pmpf-co
cf


#ciclo econômico
ce = pme
ce

#ncg (aco - pco)
acf = caixa + aplicacoes
aco = ac - acf


emprestimos1 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[0][0]
emprestimos2 = df[df['descricao'].str.contains('empr.stimo', case=False)][["valor"]].values[1][0]
div = df[df['descricao'].str.contains('dividendos', case=False)][["valor"]].values[1][0]
pr = df[df['descricao'].str.contains('partes rel', case=False)][["valor"]].values[6][0]
debentures = df[df['descricao'].str.contains('deb.ntures', case=False)][["valor"]].values[0][0]


pcf = emprestimos1 + emprestimos2 + div + pr + debentures
pco = pc - pcf

ngc = aco - pco
ngc



#st (acf - pcf)
st = acf - pcf
st 

#capital de giro
cg = ac-pc
cg


#divida líquida (po-(disponivel + aplicacoes))
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

#investimento (po + pl)
inv = po + pl
inv

#capital oneroso (divida liquida + pl)
co = dl + pl
co

#relação divida liquida pl (divida liquida / divida liquida + pl)
rdlpl = dl/(dl +pl)
rdlpl
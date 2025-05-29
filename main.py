from modulo import (
    backtest,
    pegar_balanco,
    indicador_comparacao,
    pegar_preco_corrigido,
    pegar_preco_diversos
)
import pandas as pd


def main():
    list_ticker = ["CYRE3", "GFSA3", "TCSA3", "EVEN3", "JHSF3", "EZTC3"]
    trimestre = "20244T"
    df_comparacao = pd.DataFrame()

    print("INDICADORES FUNDAMENTALISTAS")
    for ticker in list_ticker:
        df = pegar_balanco(ticker, trimestre)
        comparacao = indicador_comparacao(df)
        df_comparacao = pd.concat([
            df_comparacao,
            pd.DataFrame([{
                "ticker": ticker,
                "roe": comparacao["roe"],
                "eva": comparacao["eva"]
            }])
        ], ignore_index=True)

    print(df_comparacao)

    print("\nBACKTEST DAS AÇÕES")
    intervalos = [
        ("2024-05-01", "2025-03-31"),
        ("2020-05-01", "2025-03-31"),
        ("2015-05-01", "2025-03-31"),
    ]

    for ticker in list_ticker:
        for data_ini, data_fim in intervalos:
            print(f"\n[ticker: {ticker}] {data_ini} a {data_fim}")
            backtest(ticker, data_ini, data_fim)


if __name__ == "__main__":
    main()
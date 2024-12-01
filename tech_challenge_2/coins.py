import os
import pandas as pd
import numpy as np

path_name = "quotations"
coins = []


def get_coins():
    for file in os.listdir(path_name):
        if file.endswith(".csv"):
            coins.append(file.split(".")[0])
    return coins


def get_coin_return(coin_name):
    df = pd.read_csv(f"{path_name}/{coin_name}.csv")
    df["Data"] = pd.to_datetime(df["Data"], format="%d.%m.%Y")

    df = df.sort_values("Data")

    for col in ["Último"]:
        df[col] = (
            df[col]
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    df["Vol."] = df["Vol."].fillna("0")
    df["Vol."] = df["Vol."].str.replace(".", "", regex=False)
    df["Vol."] = df["Vol."].str.replace(",", ".", regex=False)
    df["Vol."] = df["Vol."].str.replace("K", "*1e3", regex=False)
    df["Vol."] = df["Vol."].str.replace("M", "*1e6", regex=False)
    df["Vol."] = df["Vol."].str.replace("B", "*1e9", regex=False)
    df["Vol."] = df["Vol."].map(eval)

    def safe_eval(value):
        try:
            return eval(value)
        except (SyntaxError, NameError, TypeError):
            return 0

    df["Vol."] = df["Vol."].map(safe_eval)

    df["Var%"] = df["Var%"].str.replace("%", "", regex=False)
    df["Var%"] = df["Var%"].str.replace(",", ".", regex=False).astype(float) / 100

    df["Day Return"] = df["Último"].pct_change()
    df["Log Return"] = np.log(df["Último"] / df["Último"].shift(1))

    df = df.dropna(subset=["Day Return", "Log Return"])

    return {
        "mean_day_return": df["Day Return"].mean(),
        "log_returns": df["Log Return"],
    }


def calculate_covariance_matrix(ativos):
    log_returns = pd.DataFrame()

    for ativo in ativos:
        resultados = get_coin_return(ativo)
        log_returns[ativo] = resultados["log_returns"]

    matriz_cov = log_returns.cov()
    return matriz_cov


def calculate_portfolio_sharpe(weights, mean_returns, cov_matrix, risk_free_rate):
    weights = np.array(weights)
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    risk_free_rate_daily = (1 + risk_free_rate) ** (1 / 252) - 1

    sharpe_ratio = (portfolio_return - risk_free_rate_daily) / portfolio_volatility

    return sharpe_ratio

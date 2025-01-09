import os
import pandas as pd
import numpy as np

path_name = "quotations"
coins = []


def get_coins():
    """
    Get a list of coin names from the CSV files in the specified directory.

    This function iterates through all files in the `path_name` directory,
    identifies files with a `.csv` extension, and extracts the coin name from the
    file name (excluding the extension).

    Returns:
        list: A list of coin names derived from the CSV file names.
    """
    for file in os.listdir(path_name):
        if file.endswith(".csv"):
            coins.append(file.split(".")[0])
    return coins


def clean_and_calculate_returns(df):
    """
    Clean a DataFrame and calculate daily returns.

    This function:
    - Converts the "Data" column to a datetime object.
    - Cleans and converts the "Último" column from a string to a float.
    - Sorts the DataFrame by the "Data" column.
    - Calculates the daily percentage change in the "Último" column and stores it in a new column "Retorno".

    Args:
        df (pd.DataFrame): A DataFrame containing columns "Data" and "Último".

    Returns:
        pd.DataFrame: A cleaned and processed DataFrame with an additional "Retorno" column.
    """
    df["Data"] = pd.to_datetime(df["Data"], format="%d.%m.%Y")
    df["Último"] = df["Último"].str.replace(".", "").str.replace(",", ".").astype(float)
    df = df.sort_values(by="Data").reset_index(drop=True)
    df["Retorno"] = df["Último"].pct_change()
    return df


def get_returns(coins):
    """
    Get a DataFrame of returns for a list of coins.

    This function reads CSV files for the specified coins, processes the data
    using `clean_and_calculate_returns`, and combines the "Retorno" columns
    from all coins into a single DataFrame.

    Args:
        coins (list): A list of coin names whose data will be processed.

    Returns:
        pd.DataFrame: A DataFrame containing daily returns for each coin, with
                      coins as columns and dates as rows.
    """
    dataFrames = {
        name: pd.read_csv(f"{path_name}/{coin}.csv") for name, coin in zip(coins, coins)
    }

    returns_data = {
        name: clean_and_calculate_returns(df) for name, df in dataFrames.items()
    }

    returns_df = pd.DataFrame(
        {name: df["Retorno"] for name, df in returns_data.items()}
    ).dropna()

    return returns_df


def calculate_covariance_matrix(coins):
    """
    Calculate the covariance matrix of daily returns for a list of coins.

    This function computes the covariance matrix for the daily returns
    of the specified coins using their return DataFrame.

    Args:
        coins (list): A list of coin names whose covariance matrix is to be calculated.

    Returns:
        pd.DataFrame: A covariance matrix of daily returns.
    """
    returns_df = get_returns(coins)
    return returns_df.cov()


def calculate_portfolio_sharpe(wallet, mean_returns, risk_free_rate):
    """
    Calculate the Sharpe Ratio for a portfolio.

    This function computes the Sharpe Ratio of a portfolio given its weights,
    mean returns, and a risk-free rate. It calculates portfolio return,
    portfolio volatility, and adjusts the risk-free rate to a daily equivalent.

    Args:
        wallet (dict): A dictionary containing:
                       - "weights" (list or np.ndarray): Portfolio weights.
                       - "coins" (list): Coin names in the portfolio.
        mean_returns (list or np.ndarray): Mean returns of the portfolio assets.
        risk_free_rate (float): Annualized risk-free rate as a decimal.

    Returns:
        float: The Sharpe Ratio of the portfolio.
    """
    weights = np.array(wallet["weights"])
    portfolio_return = np.dot(weights, mean_returns)
    cov_matrix = calculate_covariance_matrix(wallet["coins"])
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    # daily risk free rate
    risk_free_rate_daily = (1 + risk_free_rate) ** (1 / 252) - 1

    sharpe_ratio = (portfolio_return - risk_free_rate_daily) / portfolio_volatility

    return sharpe_ratio

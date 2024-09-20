import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.environ['FMP_API_KEY']

# Define financial statement functions
def get_income_statement(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/income-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_balance_sheet(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_cash_flow_statement(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/cash-flow-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_key_metrics(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_financial_ratios(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


def get_financial_growth(ticker, period, limit):
    try:
        url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement/{ticker}?period={period}&limit={limit}&apikey={FMP_API_KEY}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return json.dumps(response.json())
    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


# Map available functions
available_functions = {
    "get_income_statement": get_income_statement,
    "get_balance_sheet": get_balance_sheet,
    "get_cash_flow_statement": get_cash_flow_statement,
    "get_key_metrics": get_key_metrics,
    "get_financial_ratios": get_financial_ratios,
    "get_financial_growth": get_financial_growth
}

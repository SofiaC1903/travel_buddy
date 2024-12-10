import requests
import logging
from flask import Blueprint

country_bp = Blueprint('country', __name__)

logger = logging.getLogger(__name__)
REST_COUNTRIES_API_BASE = 'https://restcountries.com/v3.1'

def fetch_country_data(country: str) -> dict:
    """
    Fetch raw country data from REST Countries API.

    Args:
        country (str): Name of the country to query.

    Returns:
        dict: Parsed JSON data of the country or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()[0]  # Return the first matching country's data
    except requests.exceptions.RequestException as e:
        logger.error("Error fetching data for country %s: %s", country, str(e))
        return {"error": str(e)}

def get_country_capital_data(country: str) -> str:
    """
    Fetch the capital city of a given country.

    Args:
        country (str): Name of the country to query.

    Returns:
        str: The capital city or 'N/A' if not available.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return "N/A"
    return data.get('capital', ['N/A'])[0]  # Return the first capital if available

def get_country_language_data(country: str) -> list:
    """
    Fetch the languages spoken in a given country.

    Args:
        country (str): Name of the country to query.

    Returns:
        list: List of languages or an empty list if not available.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return []
    return list(data.get('languages', {}).values())

def get_country_currency_data(country: str) -> list:
    """
    Fetch the currency used in a given country.

    Args:
        country (str): Name of the country to query.

    Returns:
        list: List of currencies or an empty list if not available.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return []
    return list(data.get('currencies', {}).keys())

def get_country_region_data(country: str) -> str:
    """
    Fetch the region of a given country.

    Args:
        country (str): Name of the country to query.

    Returns:
        str: The region or 'N/A' if not available.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return "N/A"
    return data.get('region', 'N/A')

def get_country_code_data(country: str) -> str:
    """
    Fetch the CCA2 code of a given country.

    Args:
        country (str): Name of the country to query.

    Returns:
        str: The CCA2 code or 'N/A' if not available.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return "N/A"
    return data.get('cca2', 'N/A')
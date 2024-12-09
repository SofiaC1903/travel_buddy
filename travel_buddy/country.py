import requests
from flask import Blueprint, jsonify

# Create a Blueprint for modularizing routes
country_bp = Blueprint('country', __name__)

REST_COUNTRIES_API_BASE = 'https://restcountries.com/v3.1'

def fetch_country_data(country):
    """
    Fetch raw country data from REST Countries API.

    Args:
        country (str): Name of the country to query.

    Returns:
        dict: Parsed JSON data of the country or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            return response.json()[0]
        else:
            return {"error": "Country not found"}
    except Exception as e:
        return {"error": str(e)}

@country_bp.route('/api/country/language/<country>', methods=['GET'])
def get_country_language(country):
    """
    Flask route to query the languages spoken in a country.
    """
    data = fetch_country_data(country)
    if "error" in data:
        return jsonify(data), 404
    languages = list(data.get('languages', {}).values())
    return jsonify({"country": country, "languages": languages}), 200

@country_bp.route('/api/country/currency/<country>', methods=['GET'])
def get_country_currency(country):
    """
    Query the currency used in a given country.
    
    Args:
        country (str): Name of the country to query.

    Returns:
        JSON response containing the country's currency or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            data = response.json()[0]
            currencies = list(data.get('currencies', {}).keys())
            return jsonify({"country": country, "currencies": currencies}), 200
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_bp.route('/api/country/capital/<country>', methods=['GET'])
def get_country_capital(country):
    """
    Query the capital city of a given country.
    
    Args:
        country (str): name of the country to query.

    Returns:
        JSON response containing the country's capital or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            data = response.json()[0]
            capital = data.get('capital', ['N/A'])[0]
            return jsonify({"country": country, "capital": capital}), 200
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_bp.route('/api/country/code/<country>', methods=['GET'])
def get_country_code(country):
    """
    Query the CCA2 code of a given country.
    
    Args:
        country (str): name of the country to query.

    Returns:
        JSON response containing the country's CCA2 code or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            data = response.json()[0]
            code = data.get('alpha2Code', 'N/A')
            return jsonify({"country": country, "CCA2 Code": code}), 200
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@country_bp.route('/api/country/region/<country>', methods=['GET'])
def get_country_region(country):
    """
    Query the region and subregion of a given country.
    
    Args:
        country (str): Name of the country to query.

    Returns:
        JSON response containing the country's region and subregion or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            data = response.json()[0]
            region = data.get('region', 'N/A')
            subregion = data.get('subregion', 'N/A')
            return jsonify({"country": country, "region": region, "subregion": subregion}), 200
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

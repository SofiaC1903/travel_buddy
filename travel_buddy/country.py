import requests
from flask import Blueprint, jsonify

country_bp = Blueprint('country', __name__)

REST_COUNTRIES_API_BASE = 'https://restcountries.com/v3.1'

# 
@country_bp.route('/api/country/language/<country>', methods=['GET'])
def get_country_language(country):
    """
    Search the currency used in a given country.
    
    Args:
        country: Name of the country to query.

    Returns:
        JSON response containing the country's currency or an error message.
    """
    try:
        response = requests.get(f'{REST_COUNTRIES_API_BASE}/name/{country}')
        if response.status_code == 200:
            data = response.json()[0]
            languages = list(data.get('languages', {}).values())
            return jsonify({"country": country, "languages": languages}), 200
        else:
            return jsonify({"error": "Country not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

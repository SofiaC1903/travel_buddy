import pytest

def test_country_language_route(client):
    """
    Test the /api/country/language/<country> route.
    """
    response = client.get('/api/country/language/France')
    assert response.status_code == 200
    data = response.get_json()
    assert "languages" in data
    assert data["languages"] == ["French"]

def test_country_currency_route(client):
    """
    Test the /api/country/currency/<country> route.
    """
    response = client.get('/api/country/currency/France')
    assert response.status_code == 200
    data = response.get_json()
    assert "currencies" in data
    assert data["currencies"] == ["EUR"]

def test_country_capital_route(client):
    """
    Test the /api/country/capital/<country> route.
    """
    response = client.get('/api/country/capital/France')
    assert response.status_code == 200
    data = response.get_json()
    assert "capital" in data
    assert data["capital"] == "Paris"

def test_country_code_route(client):
    """
    Test the /api/country/code/<country> route.
    """
    response = client.get('/api/country/code/France')
    assert response.status_code == 200
    data = response.get_json()
    assert "CCA2 Code" in data
    assert data["CCA2 Code"] == "FR"


def test_country_region_route(client):
    """
    Test the /api/country/region/<country> route.
    """
    response = client.get('/api/country/region/France')
    assert response.status_code == 200
    data = response.get_json()
    assert "region" in data
    assert "subregion" in data
    assert data["region"] == "Europe"
    assert data["subregion"] == "Western Europe"

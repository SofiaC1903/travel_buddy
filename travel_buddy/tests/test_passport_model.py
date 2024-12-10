import pytest
from ..travel_buddy.models.passport_model import PassportModel
from ..travel_buddy.models.country_model import Country

@pytest.fixture
def mock_passport_model(mocker):
    """
    Fixture to provide a mocked PassportModel instance.
    """
    # Mock the Country.get_countries method to return predefined countries
    mocker.patch(
        "travel_buddy.travel_buddy.models.country_model.Country.get_countries",
        return_value=[
            Country(
                id=1,
                country="Testland",
                capital="Test City",
                languages="Testish",
                currency="TST",
                region="Asia",
                countrycode="TL",
                deleted=False,
            ),
            Country(
                id=2,
                country="Sampleland",
                capital="Sample City",
                languages="Sampleish",
                currency="SMP",
                region="Europe",
                countrycode="SL",
                deleted=False,
            ),
        ],
    )
    return PassportModel()


def test_get_country_by_capital(mock_passport_model):
    """
    Test retrieving a country by its capital.
    """
    country = mock_passport_model.get_country_by_capital("Test City")
    assert country == "Testland"

    country = mock_passport_model.get_country_by_capital("Invalid City")
    assert country is None


def test_get_country_by_code(mock_passport_model):
    """
    Test retrieving a country by its CCA2 code.
    """
    country = mock_passport_model.get_country_by_code("TL")
    assert country == "Testland"

    country = mock_passport_model.get_country_by_code("XX")
    assert country is None

    with pytest.raises(ValueError):
        mock_passport_model.get_country_by_code("TOOLONG")


def test_get_countries_by_language(mock_passport_model):
    """
    Test retrieving countries by their language.
    """
    countries = mock_passport_model.get_countries_by_language("Testish")
    assert countries == ["Testland"]

    countries = mock_passport_model.get_countries_by_language("InvalidLang")
    assert countries == []


def test_get_countries_by_currency(mock_passport_model):
    """
    Test retrieving countries by their currency.
    """
    countries = mock_passport_model.get_countries_by_currency("TST")
    assert countries == ["Testland"]

    countries = mock_passport_model.get_countries_by_currency("InvalidCurrency")
    assert countries == []


def test_get_countries_by_region(mock_passport_model):
    """
    Test retrieving countries by their region.
    """
    countries = mock_passport_model.get_countries_by_region("Asia")
    assert countries == ["Testland"]

    countries = mock_passport_model.get_countries_by_region("InvalidRegion")
    assert countries == []
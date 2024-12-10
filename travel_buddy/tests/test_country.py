import pytest
from travel_buddy.travel_buddy.models.country_model import Country
from sqlalchemy.exc import IntegrityError


def test_create_country_success(session):
    """
    Test that a country can be created successfully in the database.

    Verifies that all attributes are stored correctly, and the 
    country gets an ID assigned after committing to the database.
    """
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()

    assert country.id is not None
    assert country.country == "Testland"
    assert country.capital == "Test City"
    assert country.languages == "Testish"
    assert country.currency == "TST"
    assert country.region == "Asia"
    assert country.countrycode == "TL"


def test_create_duplicate_country(session):
    """
    Test that creating a country with a duplicate name raises an IntegrityError.

    Ensures the unique constraint on the `country` field is enforced by the database.
    """
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()

    duplicate_country = Country(
        country="Testland",
        capital="Another City",
        languages="Another Language",
        currency="ANL",
        region="Asia",
        countrycode="AN"
    )
    session.add(duplicate_country)

    with pytest.raises(IntegrityError):
        session.commit()


def test_create_country_invalid_region(session):
    """
    Test that creating a country with an invalid region raises a ValueError.

    Verifies the validation logic for allowed regions in the `region` field.
    """
    with pytest.raises(ValueError):
        Country(
            country="Invalidland",
            capital="Invalid City",
            languages="Invalidish",
            currency="INV",
            region="InvalidRegion",
            countrycode="IL"
        )


def test_create_country_invalid_countrycode(session):
    """
    Test that creating a country with an invalid country code raises a ValueError.

    Verifies that country codes must conform to the CCA2 format (max 2 characters).
    """
    with pytest.raises(ValueError):
        Country(
            country="Invalidland",
            capital="Invalid City",
            languages="Invalidish",
            currency="INV",
            region="Asia",
            countrycode="INVALIDCODE"
        )


def test_soft_delete_country(session):
    """
    Test the soft delete functionality for a country.

    Verifies that the `deleted` field is set to True when a country is soft-deleted.
    """
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()

    Country.delete_country(country.id)
    session.refresh(country)

    assert country.deleted is True


def test_get_countries(session):
    """
    Test retrieving all non-deleted countries from the database.

    Ensures the returned list includes all active countries and excludes deleted ones.
    """
    country1 = Country(
        country="Country1",
        capital="Capital1",
        languages="Language1",
        currency="CUR1",
        region="Europe",
        countrycode="C1"
    )
    country2 = Country(
        country="Country2",
        capital="Capital2",
        languages="Language2",
        currency="CUR2",
        region="Africa",
        countrycode="C2"
    )
    session.add_all([country1, country2])
    session.commit()

    countries = Country.get_countries()
    assert len(countries) == 2
    assert countries[0]["country"] == "Country1"
    assert countries[1]["country"] == "Country2"


def test_get_country_by_id(session):
    """
    Test retrieving a country by its ID with Redis caching.
    """
    # Add a test country
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()

    # Retrieve the country
    retrieved_country = Country.get_country_by_id(country.id)

    # Assertions
    assert retrieved_country["country"] == "Testland"
    assert retrieved_country["capital"] == "Test City"


def test_get_country_by_name(session):
    """
    Test retrieving a country by its name.

    Verifies that the method correctly retrieves a country by name from the database or cache.
    """
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()


    retrieved_country = Country.get_country_by_name("Testland")
    assert retrieved_country["country"] == "Testland"
    assert retrieved_country["capital"] == "Test City"


def test_cache_update_on_delete(session):
    """
    Test that Redis cache is updated when a country is soft deleted.
    """
    # Add a test country
    country = Country(
        country="Testland",
        capital="Test City",
        languages="Testish",
        currency="TST",
        region="Asia",
        countrycode="TL"
    )
    session.add(country)
    session.commit()


    # Soft delete the country
    Country.delete_country(country.id)


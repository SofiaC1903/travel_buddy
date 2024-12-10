from dataclasses import asdict, dataclass
import logging
import travel_buddy.country as info
from typing import Any, List

from sqlalchemy import event
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import validates

from ..db import db
from ..utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


@dataclass
class Country(db.Model):
    __tablename__ = 'countries'

    id: int = db.Column(db.Integer, primary_key=True)
    country: str = db.Column(db.String(80), unique=True, nullable=False)
    capital: str = db.Column(db.String(50))
    languages: str = db.Column(db.String(50), nullable=False)
    currency: str = db.Column(db.String(10), nullable=False)
    region: str = db.Column(db.String(50), default=0)
    countrycode: str = db.Column(db.String(10), default=0)
    deleted: bool = db.Column(db.Boolean, default=False)

    @validates('countrycode')
    def validate_countrycode(self, key, value):
        if len(value) > 2:
            raise ValueError("Country code must be in CCA2 format.")
        return value

    @validates('region')

    def validate_region(self, key, value):
        if value not in ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']:
            raise ValueError("Region must be one of: 'Africa', 'Americas', 'Asia', 'Europe', 'Oceania'.")
        return value
    def __post_init__(self):
        if len(self.countrycode) > 2:
            raise ValueError("Country code must be in CCA2 format.")
        if self.region not in ['Africa','Americas', 'Asia', 'Europe','Oceania']:
            raise ValueError("Region must be one of the following: 'Africa','Americas', 'Asia', 'Europe','Oceania'.")

    @classmethod
    def create_country(cls, country: str) -> None:
        """
        Create a new country in the database.

        Args:
            country (str): The name of the country.

        Raises:
            IntegrityError: If there is a database error.
        """
        try:
            capital = info.get_country_capital_data(country)
            languages = info.get_country_language_data(country)
            currency = info.get_country_currency_data(country)
            region = info.get_country_region_data(country)
            countrycode = info.get_country_code_data(country)

            languages_str = ', '.join(languages) if languages else ''
            currency_str = ', '.join(currency) if currency else ''

            new_country = cls(
                country=country,
                capital=capital,
                languages=languages_str,
                currency=currency_str,
                region=region,
                countrycode=countrycode
            )
            db.session.add(new_country)
            db.session.commit()
            logger.info("Country successfully added to the database: %s", country)

        except Exception as e:
            db.session.rollback()
            if isinstance(e, IntegrityError):
                logger.error("Country entered twice: %s", country)
                raise ValueError(f"Country with name '{country}' already exists")
            else:
                logger.error("Database error: %s", str(e))
                raise
    
    @classmethod
    def clear_countries(cls) -> None:
        """
        Deletes all entries from the countries table.

        Raises:
            Exception: If any database error occurs.
        """
        try:
            # Explicitly drop and recreate the table
            cls.__table__.drop(db.engine)  # Drop the table
            cls.__table__.create(db.engine)  # Recreate the table

            logger.info("Countries cleared and table recreated successfully.")
        except Exception as e:
            logger.error("Error while clearing countries: %s", str(e))
            raise e
    
    @classmethod
    def delete_country(cls, country_id: int) -> None:
        """
        Soft delete a country by marking it as deleted.
        """
        country = cls.query.filter_by(id=country_id).first()
        if not country:
            logger.info("Country %s not found", country_id)
            raise ValueError(f"Country {country_id} not found")
        if country.deleted:
            logger.info("Country with ID %s has already been deleted", country_id)
            raise ValueError(f"Country with ID {country_id} has been deleted")

        country.deleted = True  # Soft delete
        db.session.commit()  # Triggers the SQLAlchemy 'after_delete' event
        logger.info("Country with ID %s marked as deleted.", country_id)

    @classmethod
    def get_countries(cls) -> List[dict[str, Any]]:
        """
        Retrieve all of the countries already added to database.

        Returns:
            List[dict]: A list of countries.
.
        """
        query = cls.query.filter_by(deleted=False)

        countries = [
            {
                'id': country.id,
                'country': country.country,
                'capital': country.capital,
                'languages': country.languages,
                'currency': country.currency,
                'region': country.region,
                'countrycode': country.countrycode,
            }
            for country in query.all()
        ]
        logger.info("Countries retrieved successfully")
        return countries

    @classmethod
    def get_country_by_id(cls, country_id: int, country_name: str = None) -> dict[str, Any]:
        """
        Retrieve a country by its ID.

        Args:
            country_id (int): The ID of the country.
            country_name (str, optional): The name of the country, if available.

        Returns:
            dict: The country data as a dictionary.

        Raises:
            ValueError: If the country does not exist or is deleted.
        """
        logger.info("Retrieving country by ID: %s", country_id)
        country = cls.query.filter_by(id=country_id).first()
        if not country or country.deleted:
            logger.info("Country with %s %s not found", "name" if country_name else "ID", country_name or country_id)
            raise ValueError(f"Country {country_name or country_id} not found")

        # Convert the country object to a dictionary and return it
        logger.info("Country retrieved from database: %s", country_id)
        return {
            "id": country.id,
            "country": country.country,
            "capital": country.capital,
            "languages": country.languages,
            "currency": country.currency,
            "region": country.region,
            "countrycode": country.countrycode,
            "deleted": country.deleted
        }

    @classmethod
    def get_country_by_name(cls, country_name: str) -> dict[str, Any]:
        """
        Retrieve a country by its name.

        Args:
            country_name (str): The name of the country.

        Returns:
            dict: The country data as a dictionary.

        Raises:
            ValueError: If the country does not exist or is deleted.
        """
        logger.info("Retrieving country by name: %s", country_name)
        country = cls.query.filter_by(country=country_name).first()
        if not country or country.deleted:
            logger.info("Country with name %s not found", country_name)
            raise ValueError(f"Country {country_name} not found")

        # Convert the country object to a dictionary and return it
        logger.info("Country retrieved from database: %s", country_name)
        return {
            "id": country.id,
            "country": country.country,
            "capital": country.capital,
            "languages": country.languages,
            "currency": country.currency,
            "region": country.region,
            "countrycode": country.countrycode,
            "deleted": country.deleted
        }
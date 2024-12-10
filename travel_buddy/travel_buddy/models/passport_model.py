import logging
import os
from typing import Any, List
from travel_buddy.travel_buddy.utils.logger import configure_logger
from travel_buddy.travel_buddy.models.country_model import Country
from travel_buddy.travel_buddy.db import db

logger = logging.getLogger(__name__)
configure_logger(logger)

class PassportModel:
    """
    A class to handle user requests for countries that speak a given language, use a given currency,
    belong to a certain region, or have a given capital or country code already entered by the user.
    """

    def __init__(self):
        """Initializes the Passport class with a list of countries already entered by user."""
        self.passport: dict[int, Country] = {country.id: country for country in Country.get_countries()}   

    def get_country_by_capital(self, capital: str) -> str:
        logger.info("Retrieving country by capital.")
        for country in self.passport.values():
            if country.capital.lower() == capital.lower():
                logger.info(f"Successfully obtained country with capital '{capital}'.")
                return country.country
        logger.info("No country in the database has that capital.")
        return None

    def get_country_by_code(self, countrycode: str) -> str:
        if len(countrycode) > 2:
            raise ValueError("Country code too long. Country code must be in CCA2 format.")
        logger.info("Retrieving country based on CCA2 code.")
        for country in self.passport.values():
            if country.countrycode.lower() == countrycode.lower():
                logger.info(f"Successfully obtained country with code '{countrycode}'.")
                return country.country
        logger.info("No country in the database uses that CCA2 code.")
        return None

    def get_countries_by_language(self, language: str) -> List[str]:
        logger.info("Retrieving countries based on language.")
        country_list = []
        for country in self.passport.values():
            if country.languages.lower() == language.lower():
                country_list.append(country.country)
                logger.info(f"Successfully obtained country that speaks '{language}'.")
        if not country_list:
            logger.info("No countries in the database speak this language.")
        return country_list

    def get_countries_by_currency(self, currency: str) -> List[str]:
        logger.info("Retrieving countries that use a given currency.")
        country_list = []
        for country in self.passport.values():
            if country.currency.lower() == currency.lower():
                country_list.append(country.country)
                logger.info(f"Successfully obtained country with currency '{currency}'.")
        if not country_list:
            logger.info("No countries in the database use this currency.")
        return country_list

    def get_countries_by_region(self, region: str) -> List[str]:
        logger.info("Retrieving countries that belong to a given region.")
        country_list = []
        for country in self.passport.values():
            if country.region.lower() == region.lower():
                country_list.append(country.country)
                logger.info(f"Successfully obtained country belonging to region '{region}'.")
        if not country_list:
            logger.info("No countries in the database belong to this region.")
        return country_list
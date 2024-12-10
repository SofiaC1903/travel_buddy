import logging
import os
from typing import Any, List
from travel_buddy.utils.logger import configure_logger
from travel_buddy.models.country_model import Country
from travel_buddy.db import db

logger = logging.getLogger(__name__)
configure_logger(logger)

class PassportModel:
    """
    A class to handle user requests for countries that speak a given language, use a given currency,
    belong to a certain region, or have a given capital or country code  already entered by the user.

    Attributes:
        A passport dictionary containing Country items with int Id number.
    """

    def __init__(self):
        """Initializes the Passport class with a list of countries already entered by user."""
        self.passport: dict[int, Country] = {country.id: country for country in Country.get_countries()}   

    def get_country_by_capital(self, capital: str) -> str:
        """
        Gets a country by its capital.

        Args:
            capital (str): The capital to filter by.

        Returns:
            str: The country name.
        """
        logger.info("Retrieving country by capital.")
        for country in self.passport.values():
            if country.capital.lower() == capital.lower():
                country = country.country
                logger.info(f"Sucessfully obtained country with capital'{capital}'.")
                return country
        
    def get_country_by_code(self, countrycode: str) -> str:
        """
        Gets country by the CCA2 country code.

        Args: 
            countrycode(str): A string of a country code in CCA2 format to filter by.
        Returns:
            str: The country name.
         Raises:
            ValueError: If the string entered isn't properly formatted in CCA2 form, longer than 2 characters.

        """
        if len(self.countrycode) > 2:
            raise ValueError("Country code too long. Country code must be in CCA2 format.")
        logger.info("Retrieving country based on CCA2 code.")
    
        for country in self.passport.values():
            if country.countrycode.lower() == countrycode.lower():
                country = country.country
                logger.info(f"Sucessfully obtained country with code'{countrycode}'.")
                return country
    ##########################################################################################################       
    def get_countries_by_language(self, language:str) -> List[dict[str, Any]]:
        """
        Gets a list of countries that speak an entered language.

        Args: 
            language(str): The language entered by the user to filter by.
        Returns:
            List[dict[str, Any]: A list of the countries that speak the given language.
        """
        logger.info("Retrieving countries based on CCA2 code.")
    
        for country in self.passport.values():
            if country.countrycode.lower() == countrycode.lower():
                country = country.country
                logger.info(f"Sucessfully obtained country with code'{countrycode}'.")
                return country
   ###################################################################################################
    def get_countries_by_currency(self, currency:str) -> List[dict[str, Any]]:
       """
        Gets a list of countries that used an entered currency.

        Args: 
            currency(str): The currency entered by the user to filter by.
        Returns:
            List[dict[str, Any]: A list of the countries that use the given currency.
        """
       logger.info("Retrieving countries that use a given currency.")
    
       for country in self.passport.values():
           if country.currency.lower() == currency.lower():
                country = country.country
                logger.info(f"Sucessfully obtained country with currency'{currency}'.")
                return country

    def get_countries_by_region(self, region:str) -> List[dict[str, Any]]:
        """
        Gets a list of countries that belong to a given region.

        Args: 
            region(str): The region entered by the user to filter by.
        Returns:
            List[dict[str, Any]: A list of the countries that belong to the given region.
        """

#List[dict[str, Any]]
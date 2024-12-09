from dataclasses import asdict, dataclass
import logging
import country as info
from typing import Any, List

from sqlalchemy import event
from sqlalchemy.exc import IntegrityError

from travel_buddy.clients.redis_client import redis_client
from travel_buddy.db import db
from travel_buddy.utils.logger import configure_logger


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
        # Validate price and difficulty
        #if price <= 0:
        #    raise ValueError(f"Invalid price: {price}. Price must be a positive number.")
        #if difficulty not in ['LOW', 'MED', 'HIGH']:
        #    raise ValueError(f"Invalid difficulty level: {difficulty}. Must be 'LOW', 'MED', or 'HIGH'.")

        # Create and commit the new country
        new_country = cls(country = country, capital= info.get_country_capital(country), languages=info.get_country_language(country), currency=info.get_country_currency(country), region=info.get_country_region(country), countrycode=info.get_country_code(country))
        try:
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
    def delete_country(cls, country_id: int) -> None:
        """
        Soft delete a country by marking it as deleted.

        Args:
            country_id (int): The ID of the country to delete.

        Raises:
            ValueError: If the meal with the given ID does not exist or is already deleted.
        """
        country = cls.query.filter_by(id=country_id).first()
        if not country:
            logger.info("Country %s not found", country_id)
            raise ValueError(f"Country {country_id} not found")
        if country.deleted:
            logger.info("Country with ID %s has already been deleted", country_id)
            raise ValueError(f"Meal with ID {country_id} has been deleted")

        country.deleted = True
        db.session.commit()
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
            ValueError: If thecountry does not exist or is deleted.
        """
        logger.info("Retrieving country by ID: %s", country_id)
        cache_key = f"country_{country_id}"
        cached_country = redis_client.hgetall(cache_key)
        if cached_country:
            logger.info("Country retrieved from cache: %s", country_id)
            country_data = {k.decode(): v.decode() for k, v in cached_country.items()}
            
            # country_data['deleted'] is a string. We need to convert it to a bool
            country_data['deleted'] = country_data.get('deleted', 'false').lower() == 'true'
            if country_data['deleted']:
                logger.info("Country with %s %s not found", "name" if country_name else "ID", country_name or country_id)
                raise ValueError(f"Country {country_name or country_id} not found")
            return country_data
        country = cls.query.filter_by(id=country_id).first()
        if not country or country.deleted:
            logger.info("Country with %s %s not found", "name" if country_name else "ID", country_name or country_id)
            raise ValueError(f"Country {country_name or country_id} not found")
        # Convert the country object to a dictionary and cache it
        logger.info("Country retrieved from database and cached: %s", country_id)
        country_dict = asdict(country)
        redis_client.hset(cache_key, mapping={k: str(v) for k, v in country_dict.items()})
        return country_dict

    @classmethod
    def get_country_by_name(cls, country_name: str) -> dict[str, Any]:
        """
        Retrieve a country by its name, using a cached association between name and ID.

        Args:
            country_name (str): The name of the country.

        Returns:
            dict: The country data as a dictionary.

        Raises:
            ValueError: If the country does not exist or is deleted.
        """
        logger.info("Retrieving country by name: %s", country_name)
        cache_key = f"country_name:{country_name}"

        # Check if name-to-ID association is cached
        country_id = redis_client.get(cache_key)
        if country_id:
            logger.info("Country ID %s retrieved from cache for name: %s", country_id.decode(), country_name)
            # Use get_country_by_id to retrieve the full country data from ID
            return cls.get_country_by_id(int(country_id.decode()), country_name)

        # Fallback to database if cache miss
        country = cls.query.filter_by(country=country_name).first()
        if not country or country.deleted:
            logger.info("Country with name %s not found", country_name)
            raise ValueError(f"Country {country_name} not found")

        # Cache the name-to-ID association and retrieve the full country data
        redis_client.set(cache_key, str(country.id))
        return cls.get_country_by_id(country.id, country_name)

def update_cache_for_country(mapper, connection, target):
    """
    Update the Redis cache for a country entry after a delete operation.

    This function is intended to be used as an SQLAlchemy event listener for the
    `after_delete` events on the Country model. When a country is
    deleted, this function will remove the entry if the meal has
    been marked as deleted.

    Args:
        mapper (Mapper): The SQLAlchemy Mapper object, which provides information
                         about the model being updated (automatically passed by SQLAlchemy).
        connection (Connection): The SQLAlchemy Connection object used for the
                                 database operation (automatically passed by SQLAlchemy).
        target (Country): The instance of the Country model that was deleted.
                        The `target` object contains the updated country data.

    Side-effects:
        - If the country is marked as deleted (`target.deleted` is True), the function
          removes the corresponding cache entry from Redis.
        - If the meal is not marked as deleted, the function updates the Redis cache
          entry with the latest country data using the `hset` command.
    """
    cache_key = f"country:{target.id}"
    if target.deleted:
        redis_client.delete(cache_key)
    else:
        redis_client.hset(
            cache_key,
            mapping={k.encode(): str(v).encode() for k, v in asdict(target).items()}
        )

# Register the listener for delete events
event.listen(Country, 'after_delete', update_cache_for_country)
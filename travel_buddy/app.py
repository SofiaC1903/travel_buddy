from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
# from flask_cors import CORS

from config import ProductionConfig
from travel_buddy.db import db
from travel_buddy.models.country_model import Country
from travel_buddy.models.passport_model import PassportModel
from travel_buddy.models.mongo_session_model import MongoSessionModel
from travel_buddy.models.user_model import User

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    country_model = Country()

    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info('Health check')
        return make_response(jsonify({'status': 'healthy'}), 200)

    ##########################################################
    #
    # User management
    #
    ##########################################################

    @app.route('/api/create-user', methods=['POST'])
    def create_user() -> Response:
        """
        Route to create a new user.

        Expected JSON Input:
            - username (str): The username for the new user.
            - password (str): The password for the new user.

        Returns:
            JSON response indicating the success of user creation.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the user to the database.
        """
        app.logger.info('Creating new user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return make_response(jsonify({'error': 'Invalid input, both username and password are required'}), 400)

            # Call the User function to add the user to the database
            app.logger.info('Adding user: %s', username)
            User.create_user(username, password)

            app.logger.info("User added: %s", username)
            return make_response(jsonify({'status': 'user added', 'username': username}), 201)
        except Exception as e:
            app.logger.error("Failed to add user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/delete-user', methods=['DELETE'])
    def delete_user() -> Response:
        """
        Route to delete a user.

        Expected JSON Input:
            - username (str): The username of the user to be deleted.

        Returns:
            JSON response indicating the success of user deletion.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue deleting the user from the database.
        """
        app.logger.info('Deleting user')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            username = data.get('username')

            if not username:
                return make_response(jsonify({'error': 'Invalid input, username is required'}), 400)

            # Call the User function to delete the user from the database
            app.logger.info('Deleting user: %s', username)
            User.delete_user(username)

            app.logger.info("User deleted: %s", username)
            return make_response(jsonify({'status': 'user deleted', 'username': username}), 200)
        except Exception as e:
            app.logger.error("Failed to delete user: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/login', methods=['POST'])
    def login():
        """
        Route to log in a user and load their combatants.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The user's password.

        Returns:
            JSON response indicating the success of the login.

        Raises:
            400 error if input validation fails.
            401 error if authentication fails (invalid username or password).
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data or 'password' not in data:
            app.logger.error("Invalid request payload for login.")
            raise BadRequest("Invalid request payload. 'username' and 'password' are required.")

        username = data['username']
        password = data['password']

        try:
            # Validate user credentials
            if not User.check_password(username, password):
                app.logger.warning("Login failed for username: %s", username)
                raise Unauthorized("Invalid username or password.")

            # Get user ID
            user_id = User.get_id_by_username(username)

            # Load user's combatants into the battle model
            MongoSessionModel.login_user(user_id, battle_model)

            app.logger.info("User %s logged in successfully.", username)
            return jsonify({"message": f"User {username} logged in successfully."}), 200

        except Unauthorized as e:
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Error during login for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    @app.route('/logout', methods=['POST'])
    def logout():
        """
        Route to log out a user and save their combatants to MongoDB.

        Expected JSON Input:
            - username (str): The username of the user.

        Returns:
            JSON response indicating the success of the logout.

        Raises:
            400 error if input validation fails or user is not found in MongoDB.
            500 error for any unexpected server-side issues.
        """
        data = request.get_json()
        if not data or 'username' not in data:
            app.logger.error("Invalid request payload for logout.")
            raise BadRequest("Invalid request payload. 'username' is required.")

        username = data['username']

        try:
            # Get user ID
            user_id = User.get_id_by_username(username)

            # Save user's combatants and clear the battle model
            MongoSessionModel.logout_user(user_id, battle_model)

            app.logger.info("User %s logged out successfully.", username)
            return jsonify({"message": f"User {username} logged out successfully."}), 200

        except ValueError as e:
            app.logger.warning("Logout failed for username %s: %s", username, str(e))
            return jsonify({"error": str(e)}), 400
        except Exception as e:
            app.logger.error("Error during logout for username %s: %s", username, str(e))
            return jsonify({"error": "An unexpected error occurred."}), 500


    ##########################################################
    #
    # Countries
    #
    ##########################################################


    @app.route('/api/create-country', methods=['POST'])
    def add_country() -> Response:
        """
        Route to add a new country to the database.

        Expected JSON Input:
            - country (str): The name of the country (country).
            - capital (str): The capital of the country (e.g., Berlin, Oslo, Panama City).
            - languages (float): The languages of a country (e.g., English, Spanish, French, etc.).
            - currency (str): The currency used by a countery (e.g., Euro, USD, Pound, etc.).
            - region(str):  The region/continent a country belongs to. (e.g., Asia, Africa, Europe, etc.).
            - country code(str): The country code in CCA2 format for a country. (e.g., 'PA', 'US', 'JM')

        Returns:
            JSON response indicating the success of the country addition.
        Raises:
            400 error if input validation fails.
            500 error if there is an issue adding the country to the database.
        """
        app.logger.info('Creating new country')
        try:
            # Get the JSON data from the request
            data = request.get_json()

            # Extract and validate required fields
            country = data.get('name')

            if not country:
                raise BadRequest("Invalid input. All fields are required with valid values.")

            # Call the Country function to add the country to the database
            app.logger.info('Adding country: %s', country)
            Country.create_country(country)

            app.logger.info("Country added: %s", country)
            return make_response(jsonify({'status': 'country added', 'country': country}), 201)
        except Exception as e:
            app.logger.error("Failed to add country: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)


    @app.route('/api/delete-country/<int:country_id>', methods=['DELETE'])
    def delete_country(country_id: int) -> Response:
        """
        Route to delete a country by its ID. This performs a soft delete by marking it as deleted.

        Path Parameter:
            - country_id (int): The ID of the country to delete.

        Returns:
            JSON response indicating success of the operation or error message.
        """
        try:
            app.logger.info(f"Deleting country by ID: {country_id}")

            Country.delete_country(country_id)
            return make_response(jsonify({'status': 'country deleted'}), 200)
        except Exception as e:
            app.logger.error(f"Error deleting country: {e}")
            return make_response(jsonify({'error': str(e)}), 500)


    @app.route('/api/clear-countries', methods=['POST'])
    def clear_countries() -> Response:
        """
        Route to clear the list of countries entered by user.

        Returns:
            JSON response indicating success of the operation.
        Raises:
            500 error if there is an issue clearing countries.
        """
        try:
            app.logger.info('Clearing all countries...')
            Country.clear_countries()
            app.logger.info('Countries cleared.')
            return make_response(jsonify({'status': 'countries cleared'}), 200)
        except Exception as e:
            app.logger.error("Failed to clear countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
    
    @app.route('/api/get-countries', methods=['GET'])
    def get_countries() -> Response:
        """
        Route to get the list of countries entered by user.

        Returns:
            JSON response with the list of countries.
        """
        try:
            app.logger.info('Getting countries...')
            countries = Country.get_countries()
            return make_response(jsonify({'status': 'success', 'countries': countries}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
        
    @app.route('/api/get-country-by-id/<int:country_id>', methods=['GET'])
    def get_country_by_id(country_id: int) -> Response:
        """
        Route to get a country by its ID.

        Path Parameter:
            - country_id (int): The ID of the country.

        Returns:
            JSON response with the country details or error message.
        """
        try:
            app.logger.info(f"Retrieving country by ID: {country_id}")

            meal = Country.get_country_by_id(country_id)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error(f"Error retrieving country by ID: {e}")
            return make_response(jsonify({'error': str(e)}), 500)


    @app.route('/api/get-country-by-name/<string:country_name>', methods=['GET'])
    def get_country_by_name(country_name: str) -> Response:
        """
        Route to get a country by its name.

        Path Parameter:
            - country_name (str): The name of the country.

        Returns:
            JSON response with the country details or error message.
        """
        try:
            app.logger.info(f"Retrieving country by name: {country_name}")

            if not country_name:
                return make_response(jsonify({'error': 'Country name is required'}), 400)

            country = Country.get_country_by_name(country_name)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error(f"Error retrieving country by name: {e}")
            return make_response(jsonify({'error': str(e)}), 500)


    @app.route('/api/init-db', methods=['POST'])
    def init_db():
        """
        Initialize or recreate database tables.

        This route initializes the database tables defined in the SQLAlchemy models.
        If the tables already exist, they are dropped and recreated to ensure a clean
        slate. Use this with caution as all existing data will be deleted.

        Returns:
            Response: A JSON response indicating the success or failure of the operation.

        Logs:
            Logs the status of the database initialization process.
        """
        try:
            with app.app_context():
                app.logger.info("Dropping all existing tables.")
                db.drop_all()  # Drop all existing tables
                app.logger.info("Creating all tables from models.")
                db.create_all()  # Recreate all tables
            app.logger.info("Database initialized successfully.")
            return jsonify({"status": "success", "message": "Database initialized successfully."}), 200
        except Exception as e:
            app.logger.error("Failed to initialize database: %s", str(e))
            return jsonify({"status": "error", "message": "Failed to initialize database."}), 500

    ############################################################
    #
    # Passport
    #
    ############################################################

    @app.route('/api/get-country-by-capital', methods=['GET'])
    def get_country_by_capital(capital) -> Response:
        """
        Route to get the a country by its capital.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting country by its capital...')
            country = PassportModel.get_country_by_capital(capital)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get country: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
        
    @app.route('/api/get-country-by-code', methods=['GET'])
    def get_country_by_code(countrycode) -> Response:
        """
        Route to get the a country by its code.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting country by its code...')
            country = PassportModel.get_country_by_code(countrycode)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get country: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/get-countries-by-language', methods=['GET'])
    def get_countries_by_language(language) -> Response:
        """
        Route to get the countries that speak a given language.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their language...')
            country = PassportModel.get_countries_by_language(language)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
    
    @app.route('/api/get-countries-by-currency', methods=['GET'])
    def get_countries_by_currency(currency) -> Response:
        """
        Route to get the countries that use a given currency.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their currency...')
            country = PassportModel.get_countries_by_currency(currency)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/get-countries-by-region', methods=['GET'])
    def get_countries_by_region(region) -> Response:
        """
        Route to get the countries that belong to a given region.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their region...')
            country = PassportModel.get_countries_by_region(region)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
        
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
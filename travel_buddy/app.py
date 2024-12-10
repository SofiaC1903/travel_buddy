from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from werkzeug.exceptions import BadRequest, Unauthorized
# from flask_cors import CORS
from sqlalchemy.sql import text

from config import ProductionConfig
from travel_buddy.db import db
from travel_buddy.models.country_model import Country
from travel_buddy.models.passport_model import PassportModel
from travel_buddy.models.user_model import User

# Load environment variables from .env file
load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    from travel_buddy.country import country_bp
    app.register_blueprint(country_bp)

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
    
    
    @app.route('/api/db-check', methods=['GET'])
    def db_check():
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'database_status': 'healthy'}),  200
        except Exception as e:
            return jsonify({'database_status': 'unhealthy', 'error': str(e)}), 500

    ##########################################################
    #
    # User management
    #
    ##########################################################

    @app.route('/api/create-account', methods=['POST'])
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
        
    @app.route('/api/login', methods=['POST'])
    def login():
        """
        Route to log in a user.

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
        try:
            # Parse and validate input
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                app.logger.error("Invalid request payload for login.")
                return jsonify({"error": "Invalid request payload. 'username' and 'password' are required."}), 400

            username = data['username'].strip()
            password = data['password']

            # Validate user credentials
            if User.check_password(username, password):
                app.logger.info("User %s logged in successfully.", username)
                return jsonify({"message": f"User {username} logged in successfully."}), 200
            else:
                app.logger.warning("Invalid credentials for username: %s", username)
                return jsonify({"error": "Invalid username or password."}), 401

        except ValueError as e:
            app.logger.warning("Login failed: %s", str(e))
            return jsonify({"error": str(e)}), 401
        except Exception as e:
            app.logger.error("Unexpected error during login: %s", str(e))
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
        """
        app.logger.info('Creating new country')

        try:
            # Get JSON data from the request
            data = request.get_json()

            # Validate required fields
            required_fields = ['country', 'capital', 'languages', 'currency', 'region', 'country_code']
            missing_fields = [field for field in required_fields if field not in data or not data[field]]
            if missing_fields:
                return make_response(jsonify({'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400)

            # # Normalize and validate the region
            # region = data['region'].strip()
            # valid_regions = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']
            # app.logger.info("Valid regions: %s", repr(valid_regions))
            # app.logger.info("what is going on: %s", valid_regions[0], region)
            # app.logger.info("Is region valid? %s", region not in valid_regions)
            # app.logger.info("Region bytes: %s", list(region.encode()))
            # app.logger.info("Valid region bytes (Africa): %s", list('Africa'.encode()))

            # if region not in valid_regions:
            #     return make_response(jsonify({'error': f"Region must be one of: {', '.join(valid_regions)}"}), 400)

            # Validate the country code length
            if len(data['country_code']) > 2:
                return make_response(jsonify({'error': "Country code must be in CCA2 format (2 characters)."}), 400)

            # Add the country using the model's create_country method
            Country.create_country(data['country'])

            app.logger.info("Country added successfully: %s", data['country'])
            return make_response(jsonify({'status': 'country added', 'country': data['country']}), 201)

        except ValueError as ve:
            app.logger.error("Validation error: %s", str(ve))
            return make_response(jsonify({'error': str(ve)}), 400)
        except Exception as e:
            app.logger.error("Unexpected error: %s", str(e))
            return make_response(jsonify({'error': 'An unexpected error occurred.'}), 500)


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
    def clear_countries():
        """
        Route to clear the list of countries entered by the user.

        Returns:
            JSON response indicating success of the operation.
            Raises a 500 error if there is an issue clearing countries.
        """
        try:
            app.logger.info('Clearing all countries...')
            Country.clear_countries()  # Call the class method
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

            country = Country.get_country_by_id(country_id)
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

    @app.route('/api/get-country-by-capital/<string:capital>', methods=['GET'])
    def get_country_by_capital(capital) -> Response:
        """
        Route to get the a country by its capital.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting country by its capital...')
            passport = PassportModel()  
            country = passport.get_country_by_capital(capital)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get country: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
        
    @app.route('/api/get-country-by-code/<string:countrycode>', methods=['GET'])
    def get_country_by_code(countrycode) -> Response:
        """
        Route to get the a country by its code.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting country by its code...')
            passport = PassportModel()
            country = passport.get_country_by_code(countrycode)
            return make_response(jsonify({'status': 'success', 'country': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get country: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/get-countries-by-language/<string:language>', methods=['GET'])
    def get_countries_by_language(language) -> Response:
        """
        Route to get the countries that speak a given language.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their language...')
            passport = PassportModel()
            country = passport.get_countries_by_language(language)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
    
    @app.route('/api/get-countries-by-currency/<string:currency>', methods=['GET'])
    def get_countries_by_currency(currency) -> Response:
        """
        Route to get the countries that use a given currency.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their currency...')
            passport = PassportModel()
            country = passport.get_countries_by_currency(currency)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)

    @app.route('/api/get-countries-by-region/<string:region>', methods=['GET'])
    def get_countries_by_region(region) -> Response:
        """
        Route to get the countries that belong to a given region.

        Returns:
            JSON response with the country.
        """
        try:
            app.logger.info('Getting countries by their region...')
            passport = PassportModel()
            country = passport.get_countries_by_region(region)
            return make_response(jsonify({'status': 'success', 'countries': country}), 200)
        except Exception as e:
            app.logger.error("Failed to get countries: %s", str(e))
            return make_response(jsonify({'error': str(e)}), 500)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
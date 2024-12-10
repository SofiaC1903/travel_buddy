# Travel Buddy

## Overview

The `User` model in the Travel Buddy application handles user account management securely and efficiently. It is built using SQLAlchemy as the ORM and stores user data in a SQLite database. The key features of the `User` model include:

- **Username Management**:
  - Ensures that usernames are unique.
  - Allows only valid usernames and enforces case sensitivity for consistency.

- **Secure Password Storage**:
  - Passwords are hashed using the SHA-256 algorithm combined with a 16-byte salt.
  - Both the salt and the hashed password are securely stored in the database.

- **Core Functionalities**:
  - **Create Users**: Add new users with a username and securely hashed password.
  - **Authenticate Users**: Verify the user's password during login.
  - **Update Passwords**: Securely update an existing user's password.
  - **Delete Users**: Remove a user from the database.

The model is designed to prioritize security, with robust error handling to manage edge cases like duplicate usernames or invalid credentials.

---

## Database Initialization

The SQLite database is automatically initialized during application startup. SQLAlchemy's `create_all` method ensures all necessary tables are created. 

### How It Works
- When the application starts, it uses `create_all` to check for missing tables and creates them if necessary.
- The database schema includes the `users` table with the following fields:
  - `id`: A unique identifier for each user.
  - `username`: A unique username for the user.
  - `salt`: A 16-byte salt used for hashing passwords.
  - `password`: The securely hashed password.

---

## Unit Tests

The project includes comprehensive unit tests to validate the functionality of the `User` model. These tests are written using `pytest` and ensure the robustness of user account management.

### Summary of Tests

- **User Creation**:
  - Tests the ability to create new users with valid data.
  - Validates that duplicate usernames are not allowed.
  - Ensures invalid inputs (e.g., empty fields) raise appropriate errors.

- **Authentication**:
  - Tests password verification for correct and incorrect passwords.
  - Ensures that non-existent users cannot be authenticated.

- **Password Updates**:
  - Verifies that existing users can update their passwords securely.
  - Checks that non-existent users cannot update passwords.

- **User Deletion**:
  - Confirms that existing users can be deleted from the database.
  - Ensures appropriate errors are raised when attempting to delete non-existent users.


## Routes
#### **1. Health Check**
- **Route Name and Path**: Health Check - `/api/health`
- **Request Type**: `GET`
- **Purpose**: Verifies the service is running and healthy.
- **Request Format**:
  - **GET Parameters**: None
- **Response Format**:
  - JSON: `{ "status": "healthy" }`
- **Example**:
  - **Request**:
    ```bash
    curl -X GET "http://localhost:5000/api/health"
    ```
  - **Response**:
    ```json
    {
      "status": "healthy"
    }
    ```

---

#### **2. Create User**
- **Route Name and Path**: Create User - `/api/create-user`
- **Request Type**: `POST`
- **Purpose**: Creates a new user in the system.
- **Request Format**:
  - **POST Body**:
    ```json
    {
      "username": "example_user",
      "password": "secure_password"
    }
    ```
- **Response Format**:
  - JSON: `{ "status": "user added", "username": "<username>" }`
- **Example**:
  - **Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "secure_password"}' "http://localhost:5000/api/create-user"
    ```
  - **Response**:
    ```json
    {
      "status": "user added",
      "username": "example_user"
    }
    ```

---

#### **3. Delete User**
- **Route Name and Path**: Delete User - `/api/delete-user`
- **Request Type**: `DELETE`
- **Purpose**: Deletes an existing user from the system.
- **Request Format**:
  - **DELETE Body**:
    ```json
    {
      "username": "example_user"
    }
    ```
- **Response Format**:
  - JSON: `{ "status": "user deleted", "username": "<username>" }`
- **Example**:
  - **Request**:
    ```bash
    curl -X DELETE -H "Content-Type: application/json" -d '{"username": "example_user"}' "http://localhost:5000/api/delete-user"
    ```
  - **Response**:
    ```json
    {
      "status": "user deleted",
      "username": "example_user"
    }
    ```

---

#### **4. Login**
- **Route Name and Path**: Login - `/login`
- **Request Type**: `POST`
- **Purpose**: Authenticates a user and loads their combatants into the battle model.
- **Request Format**:
  - **POST Body**:
    ```json
    {
      "username": "example_user",
      "password": "secure_password"
    }
    ```
- **Response Format**:
  - On Success: `{ "message": "User <username> logged in successfully." }`
  - On Failure: `{ "error": "<error message>" }`
- **Example**:
  - **Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "password": "secure_password"}' "http://localhost:5000/login"
    ```
  - **Response (Success)**:
    ```json
    {
      "message": "User example_user logged in successfully."
    }
    ```
  - **Response (Failure)**:
    ```json
    {
      "error": "Invalid username or password."
    }
    ```

---

#### **5. Update Password**
- **Route Name and Path**: Update Password - `/update-password`
- **Request Type**: `POST`
- **Purpose**: Updates a user's password.
- **Request Format**:
  - **POST Body**:
    ```json
    {
      "username": "example_user",
      "old password": "old_password",
      "new password": "new_password"
    }
    ```
- **Response Format**:
  - JSON: `{ "message": "User <username> password changed successfully." }`
- **Example**:
  - **Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user", "old password": "old_password", "new password": "new_password"}' "http://localhost:5000/update-password"
    ```
  - **Response**:
    ```json
    {
      "message": "User example_user password changed successfully."
    }
    ```

---

#### **6. Logout**
- **Route Name and Path**: Logout - `/logout`
- **Request Type**: `POST`
- **Purpose**: Logs out a user and saves their combatants.
- **Request Format**:
  - **POST Body**:
    ```json
    {
      "username": "example_user"
    }
    ```
- **Response Format**:
  - JSON: `{ "message": "User <username> logged out successfully." }`
- **Example**:
  - **Request**:
    ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"username": "example_user"}' "http://localhost:5000/logout"
    ```
  - **Response**:
    ```json
    {
      "message": "User example_user logged out successfully."
    }
    ```
Here’s a detailed breakdown of the routes in the required documentation format:  

---

#### **Route Name:** Add Country  
- **Path:** `/api/create-country`  
- **Request Type:** POST  
- **Purpose:** Adds a new country to the database.  
- **Request Format:**  
  - **POST Body:**  
    ```json
    {
      "name": "Panama",
      "capital": "Panama City",
      "languages": ["Spanish"],
      "currency": "USD",
      "region": "Americas",
      "alpha2_code": "PA"
    }
    ```  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "country added",
      "country": "Panama"
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Invalid input. All fields are required with valid values."
    }
    ```  

#### **Route Name:** Delete Country  
- **Path:** `/api/delete-country/<int:country_id>`  
- **Request Type:** DELETE  
- **Purpose:** Deletes a country by its ID (soft delete).  
- **Request Format:**  
  - Path Parameter:  
    - `country_id` (integer): The ID of the country to delete.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "country deleted"
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Error deleting country: [details]"
    }
    ```  

#### **Route Name:** Clear Countries  
- **Path:** `/api/clear-countries`  
- **Request Type:** POST  
- **Purpose:** Clears all user-entered countries.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "countries cleared"
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to clear countries: [details]"
    }
    ```  

#### **Route Name:** Get Countries  
- **Path:** `/api/get-countries`  
- **Request Type:** GET  
- **Purpose:** Retrieves all countries entered by users.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "countries": [
        {"id": 1, "name": "Panama", "capital": "Panama City", "region": "Americas"}
      ]
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get countries: [details]"
    }
    ```  

#### **Route Name:** Get Country by ID  
- **Path:** `/api/get-country-by-id/<int:country_id>`  
- **Request Type:** GET  
- **Purpose:** Fetches details of a country by its ID.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "country": {"id": 1, "name": "Panama", "capital": "Panama City"}
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Error retrieving country by ID: [details]"
    }
    ```  

#### **Route Name:** Get Country by Name  
- **Path:** `/api/get-country-by-name/<string:country_name>`  
- **Request Type:** GET  
- **Purpose:** Fetches details of a country by its name.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "country": {"id": 1, "name": "Panama", "capital": "Panama City"}
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Error retrieving country by name: [details]"
    }
    ```  

#### **Route Name:** Initialize Database  
- **Path:** `/api/init-db`  
- **Request Type:** POST  
- **Purpose:** Drops and recreates database tables to reset the database.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "message": "Database initialized successfully."
    }
    ```  
  - Error:  
    ```json
    {
      "status": "error",
      "message": "Failed to initialize database."
    }
    ```  

#### **Route Name:** Get Country by Capital  
- **Path:** `/api/get-country-by-capital/<str:capital>`  
- **Request Type:** GET  
- **Purpose:** Retrieves a country by its capital.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "country": {"name": "Panama", "capital": "Panama City"}
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get country: [details]"
    }
    ```  
#### **Route Name:** Get Country by Code
- **Path:** `/api/get-countries-by-code/<str:countrycode>`  
- **Request Type:** GET  
- **Purpose:** Retrieves country by its CCA2 code.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "countries": [{"name": "Panama", "alpha2_code": "PA"}]
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get countries by code: [details]"
    }
    ```  

#### **Route Name:** Get Countries by Language  
- **Path:** `/api/get-countries-by-language/<str:language>`  
- **Request Type:** GET  
- **Purpose:** Retrieves all countries that speak a given language.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "countries": [{"name": "Panama", "language": "Spanish"}]
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get countries by language: [details]"
    }
    ```

#### **Route Name:** Get Countries by Currency
- **Path:** `/api/get-countries-by-currency/<str:currency>`  
- **Request Type:** GET  
- **Purpose:** Retrieves all countries that use a given currency.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "countries": [{"name": "Panama", "currencies":{"PAB":{"name":"Panamanian balboa","symbol":"B/."},"USD":{"name":"United States dollar","symbol":"$"}}}]
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get countries by language: [details]"
    }
    ```

#### **Route Name:** Get Countries by Region  
- **Path:** `/api/get-countries-by-region/<str:region>`  
- **Request Type:** GET  
- **Purpose:** Retrieves all countries in a specified region.  
- **Response Format:**  
  - Success:  
    ```json
    {
      "status": "success",
      "countries": [{"name": "Panama", "region":"Americas"}]
    }
    ```  
  - Error:  
    ```json
    {
      "error": "Failed to get countries by region: [details]"
    }
    ```  

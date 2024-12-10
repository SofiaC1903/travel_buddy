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

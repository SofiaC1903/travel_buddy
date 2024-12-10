# travel_buddy

### **Routes Documentation**

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

#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5001/api"

# Flag to control whether to echo JSON output
ECHO_JSON=false

# Parse command-line arguments
while [ "$#" -gt 0 ]; do
  case $1 in
    --echo-json) ECHO_JSON=true ;;
    *) echo "Unknown parameter passed: $1"; exit 1 ;;
  esac
  shift
done

###############################################
#
# Health checks
#
###############################################

# Function to check the health of the service
check_health() {
  echo "Checking health status..."
  curl -s -X GET "$BASE_URL/health" | grep -q '"status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Service is healthy."
  else
    echo "Health check failed."
    exit 1
  fi
}

# Function to initialize the database
init_db() {
  echo "Initializing the database..."
  response=$(curl -s -X POST "$BASE_URL/init-db")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Database initialized successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Initialization Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to initialize the database."
    exit 1
  fi
}

###############################################
#
# Country Routes
#
###############################################

# Function to test getting a country by its capital
get_country_by_capital() {
  echo "Testing /api/get-country-by-capital route..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-capital?capital=Paris")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Successfully retrieved country by capital."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve country by capital."
    exit 1
  fi
}

# Function to test getting a country by its code
get_country_by_code() {
  echo "Testing /api/get-country-by-code route..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-code?countrycode=FR")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Successfully retrieved country by code."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve country by code."
    exit 1
  fi
}

# Function to test getting countries by language
get_countries_by_language() {
  echo "Testing /api/get-countries-by-language route..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-language?language=French")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Successfully retrieved countries by language."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve countries by language."
    exit 1
  fi
}

# Function to test getting countries by currency
get_countries_by_currency() {
  echo "Testing /api/get-countries-by-currency route..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-currency?currency=EUR")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Successfully retrieved countries by currency."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve countries by currency."
    exit 1
  fi
}

# Function to test getting countries by region
get_countries_by_region() {
  echo "Testing /api/get-countries-by-region route..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-region?region=Europe")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Successfully retrieved countries by region."
    if [ "$ECHO_JSON" = true ]; then
      echo "Response JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve countries by region."
    exit 1
  fi
}

###############################################
#
# User Tests
#
###############################################

# Function to create a user
create_user() {
  echo "Creating a new user (username: testuser)..."
  response=$(curl -s -X POST "$BASE_URL/create-user" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"status": "user created"'; then
    echo "User created successfully."
  else
    echo "Failed to create user."
    exit 1
  fi
}

# Function to check a user's password
check_user_password() {
  echo "Checking password for user (username: testuser)..."
  response=$(curl -s -X POST "$BASE_URL/check-password" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "password":"password123"}')
  if echo "$response" | grep -q '"status": "password correct"'; then
    echo "Password verified successfully."
  else
    echo "Password verification failed."
    exit 1
  fi
}

# Function to update a user's password
update_user_password() {
  echo "Updating password for user (username: testuser)..."
  response=$(curl -s -X POST "$BASE_URL/update-password" -H "Content-Type: application/json" \
    -d '{"username":"testuser", "new_password":"newpassword456"}')
  if echo "$response" | grep -q '"status": "password updated"'; then
    echo "Password updated successfully."
  else
    echo "Failed to update password."
    exit 1
  fi
}

# Function to delete a user
delete_user() {
  echo "Deleting user (username: testuser)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-user/testuser")
  if echo "$response" | grep -q '"status": "user deleted"'; then
    echo "User deleted successfully."
  else
    echo "Failed to delete user."
    exit 1
  fi
}


# Run all the steps in orderchmod +x smoketest.sh
check_health
init_db
create_user
check_user_password
update_user_password
check_user_password
delete_user
get_country_by_capital
get_country_by_code
get_countries_by_language
get_countries_by_currency
get_countries_by_region


echo "All tests passed successfully!"

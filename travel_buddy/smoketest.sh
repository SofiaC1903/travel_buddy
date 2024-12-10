#!/bin/bash

# Define the base URL for the Flask API
BASE_URL="http://localhost:5000/api"

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

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  curl -s -X GET "$BASE_URL/db-check" | grep -q '"database_status": "healthy"'
  if [ $? -eq 0 ]; then
    echo "Database connection is healthy."
  else
    echo "Database check failed."
    exit 1
  fi
}


##############################################
#
# Countries
#
##############################################

# Function to add a country
create_country() {
  echo "Adding a country..."
  curl -s -X POST "$BASE_URL/create-country" -H "Content-Type: application/json" \
    -d '{"country":"China"}' | grep -q '"status": "country added"'
  if [ $? -eq 0 ]; then
    echo "Country added successfully."
  else
    echo "Failed to add combatant."
    exit 1
  fi
}

# Function to delete a country by ID(1)
delete_country() {
  echo "Deleting country by ID (1)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-country/1")
  if echo "$response" | grep -q '"status": "country deleted"'; then
    echo "Country deleted successfully by ID (1)."
  else
    echo "Failed to delete country by ID (1)."
    exit 1
  fi
}

# Function to get a country by ID (1)
get_country_by_id() {
  echo "Getting country by ID (1)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-id/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully by ID (1)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON (ID 1):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by ID (1)."
    exit 1
  fi
}

# Function to get a meal by name
get_country_by_name() {
  echo "Getting country by name (China)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-name/China")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully by name (China)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON (China):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by name (China)."
    exit 1
  fi
}

############################################
#
# Country Model
#
############################################

# Function to clear the countries
clear_countries() {
  echo "Clearing countries..."
  curl -s -X POST "$BASE_URL/clear-countries" -H "Content-Type: application/json" | grep -q '"status": "countries cleared"'
  if [ $? -eq 0 ]; then
    echo "Countries cleared successfully."
  else
    echo "Failed to clear countries."
    exit 1
  fi
}

# Function to get the current list of countries
get_countries() {
  echo "Getting the current list of countries..."
  response=$(curl -s -X GET "$BASE_URL/get-countries")

  # Check if the response contains combatants or an empty list
  if echo "$response" | grep -q '"countries"'; then
    echo "Countries retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Countries JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get countries or no countries found."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error or empty response:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to get a country by its capital
get_country_by_capital() {
  echo "Getting the country with its capital..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-capital")

  # Check if the response contains combatants or an empty list
  if echo "$response" | grep -q '"countries"'; then
    echo "Countries retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Countries JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get countries or no countries found."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error or empty response:"
      echo "$response" | jq .
    fi
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
create_user
check_user_password
update_user_password
check_user_password
delete_user

check_health
init_db
create_country
get_countries
clear_countries
get_countries_by_name
get_countries_by_id
delete_countries_by_id

echo "All tests passed successfully!"

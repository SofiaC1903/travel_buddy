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
  country=$1
  echo "Adding a country($country) to country class"
  curl -s -X POST "$BASE_URL/create-country/" -H "Content-Type: application/json" \
    -H "Content-Type: application/json" \
    -d "{\"country\":\"$country\""}")"

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal added successfully."
  else
    echo "Failed to add meal. Response: $response"
    exit 1
  fi
}


# Function to delete a country by ID(1)
delete_country() {
  country_id=$1
  echo "Deleting country by ID ($country_id)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-country/$country_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal deleted successfully by ID ($country_id)."
  else
    echo "Failed to delete meal by ID ($country_id)."
    exit 1
  fi
}

# Function to get a country by ID (1)
get_country_by_id() {
  country_id=$1
  echo "Getting country by ID ($country_id)..."

  response=$(curl -s -X GET "$BASE_URL/get-country-by-id/$country_id")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully by ID ($country_id)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON (ID $country_id):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by ID ($country_id)."
    exit 1
  fi
}

# Function to get a meal by name
get_country_by_name() {
  country_name=$1

  echo "Getting country by name ($country_name)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-name/$country_name")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully by name ($country_name)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($country_name):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by name ($country_name)."
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
  response=$(curl -s -X POST "$BASE_URL/clear-countries")

  if echo "$response" | grep -q '"status": "success"'; then
    echo "Countries list cleared successfully."
  else
    echo "Failed to clear countries list."
    exit 1
  fi
}

# Function to get the current list of countries
get_countries() {
  echo "Getting the current list of countries..."
  response=$(curl -s -X GET "$BASE_URL/get-countries"\
    -H "Content-Type: application/json" \
   )

  # Check if the response contains combatants or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
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
  capital=$1

  echo "Getting the country with its capital ($capital)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-capital/$capital")

  # Check if the response contains country or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully by capital ($capital)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($capital):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by capital ($capital)."
    exit 1
  fi
}

# Function to get a country by its code
get_country_by_code() {
  code=$1

  echo "Getting the country with its CCA2 code ($code)..."

  response=$(curl -s -X GET "$BASE_URL/get-country-by-code/$code")

  # Check if the response contains country or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Country retrieved successfully with code ($code)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($code):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by code ($code)."
    exit 1
  fi
}

# Function to get a country by its language
get_countries_by_language() {
  language=$1

  echo "Getting the countries that speak given language ($language)..."

  response=$(curl -s -X GET "$BASE_URL/get-countries-by-language/$language")

  # Check if the response contains country or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Countries retrieved successfully with language ($language)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($language):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by language ($language)."
    exit 1
  fi
}

# Function to get a country by its currency
get_countries_by_currency() {
  currency=$1

  echo "Getting the countries that use a given currency ($currency)..."

  response=$(curl -s -X GET "$BASE_URL/get-countries-by-currency/$currency")

  # Check if the response contains country or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Countries retrieved successfully with currency ($currency)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($currency):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by currency ($currency)."
    exit 1
  fi
}

# Function to get a country by its region
get_countries_by_region() {
  region=$1

  echo "Getting the countries that use a given region ($region)..."

  response=$(curl -s -X GET "$BASE_URL/get-countries-by-region/$region")

  # Check if the response contains country or an empty list
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Countries retrieved successfully with region ($region)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Country JSON ($region):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get country by region ($region)."
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

# Health checks
check_health
check_db

# Clear the catalog
clear_countries

# Create countries
create_country "China" 
create_country "Germany"
create_country "Finland" 
create_country "Norway" 
create_country "United States of America" 

get_country_by_id 2
get_country_by_id 4
get_country_by_name "China"
get_country_by_name "Germany"

delete_country 3

get_countries

get_country_by_capital "Oslo"

get_country_by_code "US"

get_countries_by_language "English"

get_countries_by_currency "USD"

get_countries_by_region "Europe"

clear_countries

echo "All tests passed successfully!"

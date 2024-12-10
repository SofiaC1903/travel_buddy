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
  response=$(curl -s -X GET "$BASE_URL/health")
  if echo "$response" | grep -q '"status": "healthy"'; then
    echo "Service is healthy."
  else
    echo "Health check failed. Response: $response"
    exit 1
  fi
}

# Function to check the database connection
check_db() {
  echo "Checking database connection..."
  response=$(curl -s -X GET "$BASE_URL/db-check")
  if echo "$response" | grep -q '"database_status": "healthy"'; then
    echo "Database connection is healthy."
  else
    echo "Database check failed. Response: $response"
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
  region=$2
  echo "Adding a country ($country) in region ($region)..."
  response=$(curl -s -X POST "$BASE_URL/create-country" -H "Content-Type: application/json" \
    -d "{\"country\": \"$country\", \"capital\": \"Capital of $country\", \"languages\": [\"English\"], \"currency\": \"USD\", \"region\": \"$region\", \"country_code\": \"${country:0:2}\"}")
  if echo "$response" | grep -q '"status": "country added"'; then
    echo "Country added successfully: $country"
  else
    echo "Failed to add country: $country. Response: $response"
    exit 1
  fi
}


# Function to clear all countries
clear_countries() {
  echo "Clearing all countries..."
  response=$(curl -s -X POST "$BASE_URL/clear-countries")
  if echo "$response" | grep -q '"status": "countries cleared"'; then
    echo "Countries cleared successfully."
  else
    echo "Failed to clear countries. Response: $response"
    exit 1
  fi
}

# Function to get the current list of countries
get_countries() {
  echo "Getting the current list of countries..."
  response=$(curl -s -X GET "$BASE_URL/get-countries")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Countries retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Countries JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to retrieve countries. Response: $response"
    exit 1
  fi
}

##############################################
#
# Users
#
##############################################

check_response_users() {
  local response=$1
  local expected_status=$2
  echo "$response" | grep -q "\"status\": \"$expected_status\""
  return $?
}

# Create a user
create_user() {
  local username=$1
  local password=$2
  echo "Creating a new user (username: $username)..."
  response=$(curl -s -X POST "$BASE_URL/create-account" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")
  echo "$response"
  if check_response_users "$response" "user added"; then
    echo "User created successfully: $username"
  else
    echo "Failed to create user: $username. Response: $response"
    exit 1
  fi
}

# Get all users
get_users() {
  echo "Fetching all users..."
  response=$(curl -s -X GET "$BASE_URL/users")
  echo "$response"
  if echo "$response" | jq . >/dev/null 2>&1; then
    echo "Users fetched successfully."
  else
    echo "Failed to fetch users. Response: $response"
    exit 1
  fi
}

# Delete a user
delete_user() {
  local username=$1
  echo "Deleting user (username: $username)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-user" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\"}")
  echo "$response"
  if check_response_users "$response" "user deleted"; then
    echo "User deleted successfully: $username"
  else
    echo "Failed to delete user: $username. Response: $response"
    exit 1
  fi
}

# Log in a user
login_user() {
  local username=$1
  local password=$2
  echo "Logging in user (username: $username)..."
  response=$(curl -s -X POST "$BASE_URL/login" \
    -H "Content-Type: application/json" \
    -d "{\"username\":\"$username\", \"password\":\"$password\"}")
  echo "$response"
  if echo "$response" | grep -q "\"message\": \"User $username logged in successfully.\""; then
    echo "User logged in successfully: $username"
  else
    echo "Failed to log in user: $username. Response: $response"
    exit 1
  fi
}

##############################################
#
# passport
#
##############################################

check_response_passport() {
  local response=$1
  local key=$2
  echo "$response" | grep -q "$key"
  return $?
}

# Test: Get country by capital
get_country_by_capital() {
  local capital=$1
  echo "Getting country by capital ($capital)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-capital/$capital")
  echo "$response"
  if check_response_passport "$response" '"status": "success"'; then
    echo "Successfully fetched country by capital ($capital)."
  else
    echo "Failed to fetch country by capital ($capital). Response: $response"
    exit 1
  fi
}

# Test: Get country by code
get_country_by_code() {
  local code=$1
  echo "Getting country by code ($code)..."
  response=$(curl -s -X GET "$BASE_URL/get-country-by-code/$code")
  echo "$response"
  if check_response_passport "$response" '"status": "success"'; then
    echo "Successfully fetched country by code ($code)."
  else
    echo "Failed to fetch country by code ($code). Response: $response"
    exit 1
  fi
}

# Test: Get countries by language
get_countries_by_language() {
  local language=$1
  echo "Getting countries by language ($language)..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-language/$language")
  echo "$response"
  if check_response_passport "$response" '"status": "success"'; then
    echo "Successfully fetched countries by language ($language)."
  else
    echo "Failed to fetch countries by language ($language). Response: $response"
    exit 1
  fi
}

# Test: Get countries by currency
get_countries_by_currency() {
  local currency=$1
  echo "Getting countries by currency ($currency)..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-currency/$currency")
  echo "$response"
  if check_response_passport "$response" '"status": "success"'; then
    echo "Successfully fetched countries by currency ($currency)."
  else
    echo "Failed to fetch countries by currency ($currency). Response: $response"
    exit 1
  fi
}

# Test: Get countries by region
get_countries_by_region() {
  local region=$1
  echo "Getting countries by region ($region)..."
  response=$(curl -s -X GET "$BASE_URL/get-countries-by-region/$region")
  echo "$response"
  if check_response_passport "$response" '"status": "success"'; then
    echo "Successfully fetched countries by region ($region)."
  else
    echo "Failed to fetch countries by region ($region). Response: $response"
    exit 1
  fi
}


###############################################
#
# Run tests
#
###############################################

# health tests
check_health
check_db

# countries tests
clear_countries

create_country "Nigeria" "Africa"
create_country "USA" "Americas"
create_country "Japan" "Asia"
create_country "Germany" "Europe"
create_country "Australia" "Oceania"

get_countries
clear_countries

# user smoketests
create_user "testuser" "password123"
login_user "testuser" "password123"
delete_user "testuser"


# passport smoketests
get_country_by_capital "Abuja"
get_country_by_code "NG"
get_countries_by_language "English"
get_countries_by_currency "NGN"
get_countries_by_region "Africa"

echo "All smoketests passed successfully!"
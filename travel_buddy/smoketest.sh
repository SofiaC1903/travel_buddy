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


##############################################
#
# Meals
#
##############################################

# Function to add a meal (combatant)
create_meal() {
  echo "Adding a combatant..."
  curl -s -X POST "$BASE_URL/create-meal" -H "Content-Type: application/json" \
    -d '{"meal":"Spaghetti", "cuisine":"Italian", "price":12.5, "difficulty":"MED"}' | grep -q '"status": "combatant added"'
  if [ $? -eq 0 ]; then
    echo "Combatant added successfully."
  else
    echo "Failed to add combatant."
    exit 1
  fi
}

# Function to delete a meal by ID (1)
delete_meal_by_id() {
  echo "Deleting meal by ID (1)..."
  response=$(curl -s -X DELETE "$BASE_URL/delete-meal/1")
  if echo "$response" | grep -q '"status": "meal deleted"'; then
    echo "Meal deleted successfully by ID (1)."
  else
    echo "Failed to delete meal by ID (1)."
    exit 1
  fi
}

# Function to get a meal by ID (1)
get_meal_by_id() {
  echo "Getting meal by ID (1)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-id/1")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by ID (1)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (ID 1):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by ID (1)."
    exit 1
  fi
}

# Function to get a meal by name
get_meal_by_name() {
  echo "Getting meal by name (Spaghetti)..."
  response=$(curl -s -X GET "$BASE_URL/get-meal-by-name/Spaghetti")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Meal retrieved successfully by name (Spaghetti)."
    if [ "$ECHO_JSON" = true ]; then
      echo "Meal JSON (Spaghetti):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get meal by name (Spaghetti)."
    exit 1
  fi
}

############################################
#
# Battle
#
############################################

# Function to clear the combatants
clear_combatants() {
  echo "Clearing combatants..."
  curl -s -X POST "$BASE_URL/clear-combatants" -H "Content-Type: application/json" | grep -q '"status": "combatants cleared"'
  if [ $? -eq 0 ]; then
    echo "Combatants cleared successfully."
  else
    echo "Failed to clear combatants."
    exit 1
  fi
}

# Function to get the current list of combatants
get_combatants() {
  echo "Getting the current list of combatants..."
  response=$(curl -s -X GET "$BASE_URL/get-combatants")

  # Check if the response contains combatants or an empty list
  if echo "$response" | grep -q '"combatants"'; then
    echo "Combatants retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Combatants JSON:"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get combatants or no combatants found."
    if [ "$ECHO_JSON" = true ]; then
      echo "Error or empty response:"
      echo "$response" | jq .
    fi
    exit 1
  fi
}

# Function to prepare a combatant for battle
prep_combatant() {
  echo "Preparing combatant for battle..."
  curl -s -X POST "$BASE_URL/prep-combatant" -H "Content-Type: application/json" \
    -d '{"meal":"Spaghetti"}' | grep -q '"status": "combatant prepared"'
  if [ $? -eq 0 ]; then
    echo "Combatant prepared successfully."
  else
    echo "Failed to prepare combatant."
    exit 1
  fi
}

# Function to run a battle
run_battle() {
  echo "Running a battle..."
  curl -s -X GET "$BASE_URL/battle" | grep -q '"status": "battle complete"'
  if [ $? -eq 0 ]; then
    echo "Battle completed successfully."
  else
    echo "Failed to complete battle."
    exit 1
  fi
}

######################################################
#
# Leaderboard
#
######################################################

# Function to get the leaderboard sorted by wins
get_leaderboard_wins() {
  echo "Getting leaderboard sorted by wins..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=wins")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard by wins retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by wins):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard by wins."
    exit 1
  fi
}

# Function to get the leaderboard sorted by win percentage
get_leaderboard_win_pct() {
  echo "Getting leaderboard sorted by win percentage..."
  response=$(curl -s -X GET "$BASE_URL/leaderboard?sort=win_pct")
  if echo "$response" | grep -q '"status": "success"'; then
    echo "Leaderboard by win percentage retrieved successfully."
    if [ "$ECHO_JSON" = true ]; then
      echo "Leaderboard JSON (sorted by win percentage):"
      echo "$response" | jq .
    fi
  else
    echo "Failed to get leaderboard by win percentage."
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
check_health
init_db
create_user
check_user_password
update_user_password
check_user_password
delete_user


echo "All tests passed successfully!"

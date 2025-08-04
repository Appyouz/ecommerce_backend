#!/bin/bash
# A script to populate the database for a specific seller.
# This script uses environment variables for the API URL and the auth token.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Use the provided API_URL environment variable, or default to the local URL.
BACKEND_URL="${API_URL:-http://localhost:8000}"

# JWT access token for an admin user.
# IMPORTANT: DO NOT HARDCODE YOUR TOKEN. USE AN ENVIRONMENT VARIABLE INSTEAD.
# For example, in your terminal, run:
# export ACCESS_TOKEN="your_token_here"
# This will set the variable for your current terminal session.
ACCESS_TOKEN="${ACCESS_TOKEN}"

# --- Script Logic ---
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <seller_name> <path_to_json_file>"
    exit 1
fi

SELLER_NAME="$1"
JSON_FILE_PATH="$2"

echo "Running database population script..."
echo "-----------------------------------"
echo "Seller: $SELLER_NAME"
echo "JSON File Path: $JSON_FILE_PATH"
echo "Backend URL: $BACKEND_URL"
echo "-----------------------------------"

# Check if the ACCESS_TOKEN environment variable is set
if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: ACCESS_TOKEN environment variable must be set."
    echo "Example: export ACCESS_TOKEN=ey...xyz"
    exit 1
fi

# Execute the curl command to trigger the Django management command
curl -X POST \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d "{\"seller_name\": \"$SELLER_NAME\", \"json_path\": \"$JSON_FILE_PATH\"}" \
     "$BACKEND_URL/api/products/populate_db/"

echo ""
echo "-----------------------------------"
echo "Script finished. Check your backend logs for the output."

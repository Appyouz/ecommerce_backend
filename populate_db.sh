#!/bin/bash
 ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzU0MzEyMDQ3LCJpYXQiOjE3NTQzMDg0NDcsImp0aSI6IjE0MjM2MTQ3OTE1MjRkMWM4ZjkyNzA0MDg5NDJhOGI0IiwidXNlcl9pZCI6MX0.r98vFw_JTWG6czILb8kYCkpSDklyf4HRefNai5TmexI"
# A script to populate the database for a specific seller.
# This script uses environment variables for the API URL and the auth token.
# You can set these in your terminal or in a .env file.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
# Use the provided API_URL environment variable, or default to the local URL.
BACKEND_URL="${API_URL:-http://localhost:8000}"

# You must set a valid JWT access token from your seller account.
# You can get this by logging in and inspecting the browser's cookies or
# local storage, or by using a tool like Postman.
# ACCESS_TOKEN="${AUTH_TOKEN}"

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

# Check if required environment variables are set
if [ -z "$ACCESS_TOKEN" ]; then
    echo "Error: AUTH_TOKEN environment variable must be set."
    echo "Example: export AUTH_TOKEN=ey...xyz"
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

#!/bin/bash

# Set the path for the model response file
model_response_path="$(dirname "$(dirname "$0")")/logs/model_response.md"

# Get command line arguments
model_alias="$1"
user_prompt="$2"

# Check if --paste option is used
if [ "$3" = "--paste" ]; then
    clipboard_content=$(pbpaste)
    user_prompt+=$'\n\n```'"$clipboard_content"$'```'
fi

# Create JSON query
query=$(jq -n \
    --arg model "$model_alias" \
    --arg prompt "$user_prompt" \
    '{model_alias: $model, user_prompt: $prompt}')

# Send request to API and save response
curl -s -X POST \
    -H "Content-Type: application/json" \
    -d "$query" \
    http://127.0.0.1:8000/ \
    | jq -r ".content" > "$model_response_path"

# Display the response using glow
glow "$model_response_path"
model_content_path="$(dirname "$(dirname "$0")")/logs/model_response.md"
query="{\"model_alias\":\"$1\",\"user_prompt\":\"$2\"}"
curl -s -X POST -H "Content-Type: application/json" -d "$query" http://127.0.0.1:5000/ > "$model_content_path"
glow "$model_content_path"
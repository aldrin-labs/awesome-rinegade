#!/bin/bash

output_file="/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/data/starred_repos.json"
page=1
per_page=100
has_more=true

echo "[]" > $output_file

while $has_more; do
  echo "Fetching page $page..."
  response=$(curl -s "https://api.github.com/users/0xrinegade/starred?per_page=$per_page&page=$page")
  
  # Check if we got an empty array or error
  if [ "$(echo "$response" | jq 'length')" -eq 0 ]; then
    has_more=false
    echo "No more repositories to fetch."
  else
    # Append to our result file
    temp_file=$(mktemp)
    jq -s '.[0] + .[1]' "$output_file" <(echo "$response") > "$temp_file"
    mv "$temp_file" "$output_file"
    
    echo "Fetched $(echo "$response" | jq 'length') repositories on page $page"
    page=$((page + 1))
    
    # Add a small delay to avoid rate limiting
    sleep 1
  fi
done

echo "Total repositories fetched: $(jq 'length' $output_file)"

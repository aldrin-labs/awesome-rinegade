import requests
import json
import time
import os

# GitHub API URL for starred repositories
base_url = "https://api.github.com/users/0xrinegade/starred"

# Set up headers with a GitHub token if available
headers = {}
if 'GITHUB_TOKEN' in os.environ:
    headers['Authorization'] = f"token {os.environ['GITHUB_TOKEN']}"

# Function to fetch all starred repositories
def fetch_all_starred_repos():
    all_repos = []
    page = 1
    per_page = 100  # Maximum allowed by GitHub API
    
    while True:
        # Construct URL with pagination
        url = f"{base_url}?page={page}&per_page={per_page}"
        
        # Make the request
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            print(response.json())
            break
        
        # Parse the response
        repos = response.json()
        
        # If no repositories are returned, we've reached the end
        if not repos:
            break
        
        # Add the repositories to our list
        all_repos.extend(repos)
        
        # Print progress
        print(f"Fetched page {page}, total repositories so far: {len(all_repos)}")
        
        # Move to the next page
        page += 1
        
        # Respect GitHub's rate limits
        time.sleep(1)
    
    return all_repos

# Function to extract relevant information from repositories
def extract_repo_info(repos):
    repo_info = []
    
    for repo in repos:
        # Basic information
        info = {
            'name': repo['name'],
            'full_name': repo['full_name'],
            'html_url': repo['html_url'],
            'description': repo['description'],
            'language': repo['language'],
            'topics': repo.get('topics', []),
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'updated_at': repo['updated_at'],
            'created_at': repo['created_at'],
            'owner': {
                'login': repo['owner']['login'],
                'html_url': repo['owner']['html_url']
            }
        }
        
        # Add to our list
        repo_info.append(info)
    
    return repo_info

# Main execution
if __name__ == "__main__":
    print("Fetching starred repositories...")
    repos = fetch_all_starred_repos()
    print(f"Total repositories fetched: {len(repos)}")
    
    # Extract relevant information
    repo_info = extract_repo_info(repos)
    
    # Save to a JSON file
    with open('starred_repos.json', 'w') as f:
        json.dump(repo_info, f, indent=2)
    
    print(f"Repository information saved to starred_repos.json")
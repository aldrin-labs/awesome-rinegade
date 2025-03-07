import requests
import json
import time
import os

# Set up headers with a GitHub token if available
headers = {}
if 'GITHUB_TOKEN' in os.environ:
    headers['Authorization'] = f"token {os.environ['GITHUB_TOKEN']}"

# Function to fetch repository metadata
def fetch_repo_metadata(repo_full_name):
    # Fetch repository details
    repo_url = f"https://api.github.com/repos/{repo_full_name}"
    repo_response = requests.get(repo_url, headers=headers)
    
    if repo_response.status_code != 200:
        print(f"Error fetching repo {repo_full_name}: {repo_response.status_code}")
        return None
    
    repo_data = repo_response.json()
    
    # Fetch contributors
    contributors_url = f"https://api.github.com/repos/{repo_full_name}/contributors"
    contributors_response = requests.get(contributors_url, headers=headers)
    
    contributors_count = 0
    if contributors_response.status_code == 200:
        contributors_data = contributors_response.json()
        contributors_count = len(contributors_data)
    
    # Fetch commit count (approximation)
    commits_url = f"https://api.github.com/repos/{repo_full_name}/commits?per_page=1"
    commits_response = requests.get(commits_url, headers=headers)
    
    commit_count = 0
    if commits_response.status_code == 200 and 'link' in commits_response.headers:
        # Extract total from the Link header
        link_header = commits_response.headers['link']
        if 'rel="last"' in link_header:
            last_page = link_header.split('page=')[1].split('&')[0].split('>')[0]
            commit_count = int(last_page)
    
    # Compile metadata
    metadata = {
        'full_name': repo_full_name,
        'stars': repo_data['stargazers_count'],
        'forks': repo_data['forks_count'],
        'watchers': repo_data['watchers_count'],
        'open_issues': repo_data['open_issues_count'],
        'language': repo_data['language'],
        'topics': repo_data.get('topics', []),
        'contributors_count': contributors_count,
        'commit_count': commit_count,
        'updated_at': repo_data['updated_at'],
        'created_at': repo_data['created_at'],
        'description': repo_data['description']
    }
    
    return metadata

# Function to process all repositories
def process_all_repos(repos_file):
    # Load repositories from file
    with open(repos_file, 'r') as f:
        repos = json.load(f)
    
    all_metadata = []
    
    for i, repo in enumerate(repos):
        print(f"Processing {i+1}/{len(repos)}: {repo['full_name']}")
        
        # Fetch metadata
        metadata = fetch_repo_metadata(repo['full_name'])
        
        if metadata:
            all_metadata.append(metadata)
        
        # Respect GitHub's rate limits
        time.sleep(1)
    
    return all_metadata

# Main execution
if __name__ == "__main__":
    if not os.path.exists('starred_repos.json'):
        print("Error: starred_repos.json not found. Run fetch_starred_repos.py first.")
        exit(1)
    
    print("Fetching metadata for repositories...")
    metadata = process_all_repos('starred_repos.json')
    
    # Save to a JSON file
    with open('repo_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Metadata saved to repo_metadata.json")
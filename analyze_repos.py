import json
import os
from datetime import datetime
import re

# Read the repositories data
with open('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/data/starred_repos.json', 'r') as f:
    repos_data = json.load(f)

# Define categories based on topics and languages
language_categories = {
    'JavaScript': 'JavaScript',
    'TypeScript': 'TypeScript',
    'Rust': 'Rust',
    'Python': 'Python',
    'Go': 'Go',
    'Java': 'Java',
    'C++': 'C++',
    'C': 'C',
    'Ruby': 'Ruby',
    'PHP': 'PHP',
    'Swift': 'Swift',
    'Kotlin': 'Kotlin',
    'Solidity': 'Solidity',
    'HTML': 'Web',
    'CSS': 'Web',
    'Shell': 'Shell',
    'Jupyter Notebook': 'Data Science',
}

industry_categories = {
    # Blockchain
    'blockchain': 'Blockchain',
    'crypto': 'Blockchain',
    'cryptocurrency': 'Blockchain',
    'bitcoin': 'Blockchain',
    'ethereum': 'Blockchain',
    'solana': 'Blockchain',
    'web3': 'Blockchain',
    'defi': 'Blockchain',
    'nft': 'Blockchain',
    'smart-contracts': 'Blockchain',
    'dapp': 'Blockchain',
    'token': 'Blockchain',
    
    # Web Development
    'web': 'Web Development',
    'frontend': 'Web Development',
    'backend': 'Web Development',
    'fullstack': 'Web Development',
    'react': 'Web Development',
    'vue': 'Web Development',
    'angular': 'Web Development',
    'node': 'Web Development',
    'express': 'Web Development',
    
    # DevOps
    'devops': 'DevOps',
    'docker': 'DevOps',
    'kubernetes': 'DevOps',
    'ci-cd': 'DevOps',
    'infrastructure': 'DevOps',
    'cloud': 'DevOps',
    'aws': 'DevOps',
    'azure': 'DevOps',
    'gcp': 'DevOps',
    
    # Data Science
    'data-science': 'Data Science',
    'machine-learning': 'Data Science',
    'deep-learning': 'Data Science',
    'ai': 'Data Science',
    'artificial-intelligence': 'Data Science',
    'ml': 'Data Science',
    'data-analysis': 'Data Science',
    'data-visualization': 'Data Science',
    
    # Mobile Development
    'mobile': 'Mobile Development',
    'android': 'Mobile Development',
    'ios': 'Mobile Development',
    'flutter': 'Mobile Development',
    'react-native': 'Mobile Development',
    
    # Security
    'security': 'Security',
    'cybersecurity': 'Security',
    'hacking': 'Security',
    'pentest': 'Security',
    'encryption': 'Security',
    
    # Tools & Utilities
    'tool': 'Tools & Utilities',
    'utility': 'Tools & Utilities',
    'cli': 'Tools & Utilities',
    'library': 'Tools & Utilities',
    'framework': 'Tools & Utilities',
    
    # Gaming
    'game': 'Gaming',
    'gamedev': 'Gaming',
    'unity': 'Gaming',
    'unreal': 'Gaming',
    
    # Finance
    'finance': 'Finance',
    'trading': 'Finance',
    'investment': 'Finance',
    'fintech': 'Finance',
}

# Function to determine the category of a repository
def categorize_repo(repo):
    # Default categories
    language_category = 'Other'
    industry_category = 'Other'
    
    # Determine language category
    if repo.get('language') and repo['language'] in language_categories:
        language_category = language_categories[repo['language']]
    
    # Determine industry category based on topics, description, and name
    topics = repo.get('topics', [])
    description = (repo.get('description', '') or '').lower()
    name = repo['name'].lower()
    full_name = repo['full_name'].lower()
    
    # Check topics first
    for topic in topics:
        if topic.lower() in industry_categories:
            industry_category = industry_categories[topic.lower()]
            break
    
    # If no category found from topics, check description and name
    if industry_category == 'Other':
        # Create a combined text to search for keywords
        combined_text = f"{description} {name} {full_name}"
        
        for keyword, category in industry_categories.items():
            if keyword.lower() in combined_text:
                industry_category = category
                break
        
        # Special cases for blockchain projects
        if any(term in combined_text for term in ['solana', 'anchor', 'token', 'wallet', 'chain']):
            industry_category = 'Blockchain'
    
    return language_category, industry_category

# Process repositories
processed_repos = []
for repo in repos_data:
    language_category, industry_category = categorize_repo(repo)
    
    # Calculate quality score (simple heuristic)
    stars_weight = 0.5
    forks_weight = 0.3
    updated_weight = 0.2
    
    # Convert updated_at to days since last update
    last_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ')
    now = datetime.now()
    days_since_update = (now - last_updated).days
    
    # Normalize metrics
    normalized_stars = min(repo.get('stargazers_count', 0) / 1000, 1)
    normalized_forks = min(repo.get('forks_count', 0) / 100, 1)
    normalized_updated = max(0, 1 - (days_since_update / 365))  # Higher score for more recent updates
    
    quality_score = (
        normalized_stars * stars_weight +
        normalized_forks * forks_weight +
        normalized_updated * updated_weight
    )
    
    processed_repos.append({
        'name': repo['name'],
        'full_name': repo['full_name'],
        'description': repo.get('description', 'No description provided'),
        'url': repo['html_url'],
        'language': repo.get('language', 'Not specified'),
        'stars': repo.get('stargazers_count', 0),
        'forks': repo.get('forks_count', 0),
        'issues': repo.get('open_issues_count', 0),
        'updated_at': repo['updated_at'],
        'created_at': repo['created_at'],
        'pushed_at': repo.get('pushed_at', ''),
        'size': repo.get('size', 0),
        'topics': repo.get('topics', []),
        'language_category': language_category,
        'industry_category': industry_category,
        'quality_score': round(quality_score, 2)
    })

# Group repositories by language category
by_language = {}
for repo in processed_repos:
    if repo['language_category'] not in by_language:
        by_language[repo['language_category']] = []
    by_language[repo['language_category']].append(repo)

# Group repositories by industry category
by_industry = {}
for repo in processed_repos:
    if repo['industry_category'] not in by_industry:
        by_industry[repo['industry_category']] = []
    by_industry[repo['industry_category']].append(repo)

# Sort repositories within each category by quality score
for category in by_language:
    by_language[category].sort(key=lambda x: x['quality_score'], reverse=True)

for category in by_industry:
    by_industry[category].sort(key=lambda x: x['quality_score'], reverse=True)

# Create knowledge graph
knowledge_graph = {
    "@context": "https://schema.org",
    "@type": "Dataset",
    "name": "0xrinegade Starred Repositories",
    "description": "Knowledge graph of repositories starred by GitHub user 0xrinegade",
    "url": "https://github.com/0xrinegade?tab=stars",
    "keywords": ["GitHub", "repositories", "stars", "programming", "open-source"],
    "creator": {
        "@type": "Person",
        "name": "0xrinegade",
        "url": "https://github.com/0xrinegade"
    },
    "dateCreated": datetime.now().isoformat(),
    "categories": [
        {
            "@type": "CategoryCode",
            "name": category,
            "codeValue": re.sub(r'\s+', '-', category.lower())
        }
        for category in by_industry.keys()
    ],
    "programmingLanguages": [
        {
            "@type": "ComputerLanguage",
            "name": language
        }
        for language in by_language.keys()
    ],
    "repositories": [
        {
            "@type": "SoftwareSourceCode",
            "name": repo['name'],
            "description": repo['description'],
            "url": repo['url'],
            "programmingLanguage": repo['language'],
            "codeRepository": repo['url'],
            "dateCreated": repo['created_at'],
            "dateModified": repo['updated_at'],
            "starCount": repo['stars'],
            "forkCount": repo['forks'],
            "issueCount": repo['issues'],
            "category": repo['industry_category'],
            "qualityScore": repo['quality_score'],
            "keywords": repo['topics']
        }
        for repo in processed_repos
    ]
}

# Generate README.md content
readme_content = "# Awesome Rinegade\n\n"
readme_content += "A curated list of awesome repositories starred by [0xrinegade](https://github.com/0xrinegade?tab=stars).\n\n"
readme_content += "## Table of Contents\n\n"
readme_content += "- [By Industry](#by-industry)\n"

for category in sorted(by_industry.keys()):
    category_anchor = re.sub(r'\s+', '-', category.lower())
    readme_content += f"  - [{category}](#{category_anchor})\n"

readme_content += "- [By Language](#by-language)\n"

for language in sorted(by_language.keys()):
    language_anchor = re.sub(r'\s+', '-', language.lower())
    readme_content += f"  - [{language}](#{language_anchor})\n"

readme_content += "\n## By Industry\n\n"

# Add repositories by industry
for category in sorted(by_industry.keys()):
    readme_content += f"### {category}\n\n"
    
    # Limit to top 20 repositories per category to keep the README manageable
    top_repos = by_industry[category][:20]
    
    for repo in top_repos:
        last_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ').date().isoformat()
        readme_content += f"- [{repo['full_name']}]({repo['url']}) - {repo['description']}\n"
        readme_content += f"  - **Language:** {repo['language']} | **Stars:** {repo['stars']} | **Forks:** {repo['forks']} | **Last Updated:** {last_updated} | **Quality Score:** {repo['quality_score']}\n"
        
        if repo['topics']:
            readme_content += f"  - **Topics:** {', '.join(repo['topics'])}\n\n"
        else:
            readme_content += "  - No topics\n\n"
    
    if len(by_industry[category]) > 20:
        readme_content += f"- *And {len(by_industry[category]) - 20} more repositories in this category*\n\n"
    
    readme_content += "\n"

readme_content += "## By Language\n\n"

# Add repositories by language
for language in sorted(by_language.keys()):
    readme_content += f"### {language}\n\n"
    
    # Limit to top 20 repositories per language to keep the README manageable
    top_repos = by_language[language][:20]
    
    for repo in top_repos:
        last_updated = datetime.strptime(repo['updated_at'], '%Y-%m-%dT%H:%M:%SZ').date().isoformat()
        readme_content += f"- [{repo['full_name']}]({repo['url']}) - {repo['description']}\n"
        readme_content += f"  - **Industry:** {repo['industry_category']} | **Stars:** {repo['stars']} | **Forks:** {repo['forks']} | **Last Updated:** {last_updated} | **Quality Score:** {repo['quality_score']}\n"
        
        if repo['topics']:
            readme_content += f"  - **Topics:** {', '.join(repo['topics'])}\n\n"
        else:
            readme_content += "  - No topics\n\n"
    
    if len(by_language[language]) > 20:
        readme_content += f"- *And {len(by_language[language]) - 20} more repositories in this category*\n\n"
    
    readme_content += "\n"

# Add footer
readme_content += "## About\n\n"
readme_content += f"This list was generated by analyzing {len(processed_repos)} repositories starred by [0xrinegade](https://github.com/0xrinegade?tab=stars). "
readme_content += "The repositories are categorized by industry and programming language, and ranked by a quality score that takes into account stars, forks, and recency of updates.\n\n"
readme_content += "The knowledge graph of these repositories is available in [knowledge-graph.json-ld](knowledge-graph.json-ld).\n"

# Write the files
with open('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/knowledge-graph.json-ld', 'w') as f:
    json.dump(knowledge_graph, f, indent=2)

with open('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/README.md', 'w') as f:
    f.write(readme_content)

print(f"Processed {len(processed_repos)} repositories")
print(f"Found {len(by_industry)} industry categories")
print(f"Found {len(by_language)} language categories")
print("Files written: README.md and knowledge-graph.json-ld")

import json
import os
from collections import defaultdict
from datetime import datetime

# Function to categorize repositories
def categorize_repositories(repos):
    # Categorize by language
    by_language = defaultdict(list)
    # Categorize by industry/domain (based on topics and description)
    by_industry = defaultdict(list)
    # Categorize by purpose/category
    by_category = defaultdict(list)
    
    # Industry keywords mapping
    industry_keywords = {
        'blockchain': ['blockchain', 'crypto', 'web3', 'defi', 'nft', 'ethereum', 'bitcoin', 'solana'],
        'ai-ml': ['ai', 'machine learning', 'ml', 'deep learning', 'neural', 'nlp', 'computer vision'],
        'web-development': ['web', 'frontend', 'backend', 'fullstack', 'javascript', 'react', 'vue', 'angular'],
        'mobile': ['mobile', 'ios', 'android', 'flutter', 'react native'],
        'devops': ['devops', 'ci/cd', 'docker', 'kubernetes', 'container', 'deployment'],
        'gaming': ['game', 'gaming', 'unity', 'unreal', 'gamedev'],
        'data-science': ['data science', 'data analysis', 'analytics', 'visualization', 'pandas', 'jupyter'],
        'security': ['security', 'cybersecurity', 'encryption', 'privacy', 'authentication'],
        'iot': ['iot', 'internet of things', 'embedded', 'arduino', 'raspberry pi'],
        'finance': ['finance', 'fintech', 'banking', 'trading', 'investment'],
    }
    
    # Category keywords mapping
    category_keywords = {
        'framework': ['framework', 'library', 'sdk', 'toolkit'],
        'tool': ['tool', 'utility', 'cli', 'command-line'],
        'application': ['app', 'application', 'platform', 'service'],
        'learning-resource': ['tutorial', 'course', 'learning', 'education', 'book'],
        'database': ['database', 'db', 'sql', 'nosql', 'storage'],
        'api': ['api', 'rest', 'graphql', 'endpoint'],
    }
    
    for repo in repos:
        # Categorize by language
        language = repo.get('language') or 'Unknown'
        by_language[language].append(repo)
        
        # Categorize by industry
        description = (repo.get('description') or '').lower()
        topics = [topic.lower() for topic in repo.get('topics') or []]
        
        # Check for industry keywords in description and topics
        industry_found = False
        for industry, keywords in industry_keywords.items():
            if any(keyword in description for keyword in keywords) or \
               any(keyword in topic for keyword in keywords for topic in topics):
                by_industry[industry].append(repo)
                industry_found = True
        
        # If no specific industry found, categorize as 'other'
        if not industry_found:
            by_industry['other'].append(repo)
        
        # Categorize by purpose/category
        category_found = False
        for category, keywords in category_keywords.items():
            if any(keyword in description for keyword in keywords) or \
               any(keyword in topic for keyword in keywords for topic in topics):
                by_category[category].append(repo)
                category_found = True
        
        # If no specific category found, categorize as 'other'
        if not category_found:
            by_category['other'].append(repo)
    
    return {
        'by_language': dict(by_language),
        'by_industry': dict(by_industry),
        'by_category': dict(by_category)
    }

# Function to assess code quality (simplified)
def assess_code_quality(repo):
    # This is a simplified assessment based on available metrics
    # In a real scenario, more sophisticated analysis would be needed
    
    # Factors to consider:
    # 1. Number of stars (popularity)
    # 2. Number of contributors (community involvement)
    # 3. Recent updates (maintenance)
    # 4. Open issues ratio (issue management)
    
    stars = repo.get('stars', 0)
    contributors = repo.get('contributors_count', 0)
    
    # Calculate days since last update
    last_updated = repo.get('updated_at', '')
    days_since_update = 365  # Default to a year if no data
    
    if last_updated:
        try:
            last_updated_date = datetime.strptime(last_updated, '%Y-%m-%dT%H:%M:%SZ')
            days_since_update = (datetime.now() - last_updated_date).days
        except:
            pass
    
    # Simple scoring system
    score = 0
    
    # Stars contribution
    if stars >= 10000: score += 5
    elif stars >= 5000: score += 4
    elif stars >= 1000: score += 3
    elif stars >= 100: score += 2
    elif stars > 0: score += 1
    
    # Contributors contribution
    if contributors >= 50: score += 5
    elif contributors >= 20: score += 4
    elif contributors >= 10: score += 3
    elif contributors >= 5: score += 2
    elif contributors > 0: score += 1
    
    # Recency contribution
    if days_since_update <= 7: score += 5
    elif days_since_update <= 30: score += 4
    elif days_since_update <= 90: score += 3
    elif days_since_update <= 180: score += 2
    elif days_since_update <= 365: score += 1
    
    # Normalize to a 5-star rating
    max_score = 15
    normalized_score = min(5, max(1, round((score / max_score) * 5)))
    
    # Convert to a descriptive rating
    ratings = {
        1: "Basic",
        2: "Good",
        3: "Very Good",
        4: "Excellent",
        5: "Outstanding"
    }
    
    return ratings[normalized_score]

# Function to generate README content
def generate_readme(categorized_repos):
    readme = """# Awesome Rinegade

A curated list of awesome repositories starred by [0xrinegade](https://github.com/0xrinegade). This list categorizes repositories by programming language, industry, and purpose to help you discover valuable resources.

## Table of Contents

- [By Programming Language](#by-programming-language)
- [By Industry/Domain](#by-industrydomain)
- [By Category/Purpose](#by-categorypurpose)
- [About](#about)

"""
    
    # Add By Programming Language section
    readme += "## By Programming Language\n\n"
    
    languages = categorized_repos['by_language']
    for language, repos in sorted(languages.items()):
        if language == 'Unknown' or not repos:
            continue
            
        readme += f"### {language} ({len(repos)})\n\n"
        
        # Sort repositories by stars
        sorted_repos = sorted(repos, key=lambda x: x.get('stars', 0), reverse=True)
        
        # Take top repositories for each language (to keep README manageable)
        top_repos = sorted_repos[:20]  # Limit to 20 repos per language
        
        for repo in top_repos:
            name = repo.get('full_name', '').split('/')[-1]
            full_name = repo.get('full_name', '')
            description = repo.get('description', 'No description available')
            stars = repo.get('stars', 0)
            contributors = repo.get('contributors_count', 0)
            commits = repo.get('commit_count', 0)
            updated_at = repo.get('updated_at', '').split('T')[0] if repo.get('updated_at') else 'Unknown'
            quality = assess_code_quality(repo)
            
            readme += f"- [{full_name}](https://github.com/{full_name}) - {description}\n"
            readme += f"  - **Why you might need it**: {generate_use_case(repo)}\n"
            readme += f"  - **Metrics**: ⭐ {stars} | 👥 {contributors} contributors | 🔄 {commits} commits | 📅 Last updated: {updated_at} | 🏆 Quality: {quality}\n\n"
        
        if len(sorted_repos) > 20:
            readme += f"*...and {len(sorted_repos) - 20} more {language} repositories.*\n\n"
    
    # Add By Industry/Domain section
    readme += "## By Industry/Domain\n\n"
    
    industries = categorized_repos['by_industry']
    for industry, repos in sorted(industries.items()):
        if industry == 'other' or not repos:
            continue
            
        industry_name = industry.replace('-', ' ').title()
        readme += f"### {industry_name} ({len(repos)})\n\n"
        
        # Sort repositories by stars
        sorted_repos = sorted(repos, key=lambda x: x.get('stars', 0), reverse=True)
        
        # Take top repositories for each industry
        top_repos = sorted_repos[:15]  # Limit to 15 repos per industry
        
        for repo in top_repos:
            name = repo.get('full_name', '').split('/')[-1]
            full_name = repo.get('full_name', '')
            description = repo.get('description', 'No description available')
            language = repo.get('language', 'Unknown')
            stars = repo.get('stars', 0)
            
            readme += f"- [{full_name}](https://github.com/{full_name}) - {description} `{language}`\n"
            readme += f"  - **Why you might need it**: {generate_use_case(repo)}\n\n"
        
        if len(sorted_repos) > 15:
            readme += f"*...and {len(sorted_repos) - 15} more {industry_name} repositories.*\n\n"
    
    # Add By Category/Purpose section
    readme += "## By Category/Purpose\n\n"
    
    categories = categorized_repos['by_category']
    for category, repos in sorted(categories.items()):
        if category == 'other' or not repos:
            continue
            
        category_name = category.replace('-', ' ').title()
        readme += f"### {category_name} ({len(repos)})\n\n"
        
        # Sort repositories by stars
        sorted_repos = sorted(repos, key=lambda x: x.get('stars', 0), reverse=True)
        
        # Take top repositories for each category
        top_repos = sorted_repos[:15]  # Limit to 15 repos per category
        
        for repo in top_repos:
            name = repo.get('full_name', '').split('/')[-1]
            full_name = repo.get('full_name', '')
            description = repo.get('description', 'No description available')
            language = repo.get('language', 'Unknown')
            stars = repo.get('stars', 0)
            
            readme += f"- [{full_name}](https://github.com/{full_name}) - {description} `{language}`\n"
            readme += f"  - **Stars**: ⭐ {stars}\n\n"
        
        if len(sorted_repos) > 15:
            readme += f"*...and {len(sorted_repos) - 15} more {category_name} repositories.*\n\n"
    
    # Add About section
    readme += """## About

This awesome list is a curated collection of repositories starred by [0xrinegade](https://github.com/0xrinegade). The repositories are categorized to help you discover valuable resources based on programming languages, industries, and purposes.

The list is generated automatically using GitHub's API and includes metrics such as stars, contributors, commit count, and last updated date to help you assess the quality and activity of each repository.

A knowledge graph of these repositories is available in the [knowledge-graph.json-ld](knowledge-graph.json-ld) file, which shows relationships between repositories based on shared languages, topics, and other factors.

### How to Use This List

- Browse repositories by programming language if you're looking for resources in a specific language
- Explore repositories by industry/domain if you're interested in a particular field
- Check repositories by category/purpose if you need a specific type of tool or resource

### Contributing

This list is automatically generated based on repositories starred by 0xrinegade. If you'd like to suggest improvements to the categorization or descriptions, please open an issue or pull request.
"""
    
    return readme

# Function to generate use case description
def generate_use_case(repo):
    description = repo.get('description', '').lower()
    name = repo.get('full_name', '').split('/')[-1].lower()
    language = repo.get('language', '').lower()
    topics = [topic.lower() for topic in repo.get('topics') or []]
    
    # Framework detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['framework', 'library', 'sdk']):
        return f"A {language} framework/library for building applications with features like {', '.join(topics[:3]) if topics else 'those described above'}"
    
    # Tool detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['tool', 'utility', 'cli']):
        return f"A developer tool that helps with {description.split('.')[0] if description else 'specific tasks'}"
    
    # Application detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['app', 'application', 'platform']):
        return f"An application that provides {description.split('.')[0] if description else 'functionality as described above'}"
    
    # Learning resource detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['tutorial', 'course', 'learning', 'book']):
        return "A learning resource to help you understand and master this technology"
    
    # Database detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['database', 'db', 'sql', 'nosql']):
        return "A database solution for storing and managing your data efficiently"
    
    # API detection
    if any(keyword in description or keyword in name or keyword in topics for keyword in ['api', 'rest', 'graphql']):
        return "An API or service that you can integrate with your applications"
    
    # Generic fallback
    return f"This repository provides solutions for {description.split('.')[0] if description else 'the problems described above'}"

# Main execution
if __name__ == "__main__":
    if not os.path.exists('repo_metadata.json'):
        print("Error: repo_metadata.json not found. Run fetch_repo_metadata.py first.")
        exit(1)
    
    # Load repository metadata
    with open('repo_metadata.json', 'r') as f:
        repos = json.load(f)
    
    print(f"Loaded {len(repos)} repositories from metadata file")
    
    # Categorize repositories
    print("Categorizing repositories...")
    categorized_repos = categorize_repositories(repos)
    
    # Generate README
    print("Generating README...")
    readme_content = generate_readme(categorized_repos)
    
    # Save README
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("README.md generated successfully")
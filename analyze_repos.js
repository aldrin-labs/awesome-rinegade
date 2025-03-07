const fs = require('fs');
const path = require('path');

// Read the repositories data
const reposData = JSON.parse(fs.readFileSync('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/data/starred_repos.json', 'utf8'));

// Define categories based on topics and languages
const languageCategories = {
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
};

const industryCategories = {
  // Blockchain
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
  
  // Web Development
  'web': 'Web Development',
  'frontend': 'Web Development',
  'backend': 'Web Development',
  'fullstack': 'Web Development',
  'react': 'Web Development',
  'vue': 'Web Development',
  'angular': 'Web Development',
  'node': 'Web Development',
  'express': 'Web Development',
  
  // DevOps
  'devops': 'DevOps',
  'docker': 'DevOps',
  'kubernetes': 'DevOps',
  'ci-cd': 'DevOps',
  'infrastructure': 'DevOps',
  'cloud': 'DevOps',
  'aws': 'DevOps',
  'azure': 'DevOps',
  'gcp': 'DevOps',
  
  // Data Science
  'data-science': 'Data Science',
  'machine-learning': 'Data Science',
  'deep-learning': 'Data Science',
  'ai': 'Data Science',
  'artificial-intelligence': 'Data Science',
  'ml': 'Data Science',
  'data-analysis': 'Data Science',
  'data-visualization': 'Data Science',
  
  // Mobile Development
  'mobile': 'Mobile Development',
  'android': 'Mobile Development',
  'ios': 'Mobile Development',
  'flutter': 'Mobile Development',
  'react-native': 'Mobile Development',
  
  // Security
  'security': 'Security',
  'cybersecurity': 'Security',
  'hacking': 'Security',
  'pentest': 'Security',
  'encryption': 'Security',
  
  // Tools & Utilities
  'tool': 'Tools & Utilities',
  'utility': 'Tools & Utilities',
  'cli': 'Tools & Utilities',
  'library': 'Tools & Utilities',
  'framework': 'Tools & Utilities',
  
  // Gaming
  'game': 'Gaming',
  'gamedev': 'Gaming',
  'unity': 'Gaming',
  'unreal': 'Gaming',
  
  // Finance
  'finance': 'Finance',
  'trading': 'Finance',
  'investment': 'Finance',
  'fintech': 'Finance',
};

// Function to determine the category of a repository
function categorizeRepo(repo) {
  // Default categories
  let languageCategory = 'Other';
  let industryCategory = 'Other';
  
  // Determine language category
  if (repo.language && languageCategories[repo.language]) {
    languageCategory = languageCategories[repo.language];
  }
  
  // Determine industry category based on topics, description, and name
  const topics = repo.topics || [];
  const description = (repo.description || '').toLowerCase();
  const name = repo.name.toLowerCase();
  const fullName = repo.full_name.toLowerCase();
  
  // Check topics first
  for (const topic of topics) {
    if (industryCategories[topic.toLowerCase()]) {
      industryCategory = industryCategories[topic.toLowerCase()];
      break;
    }
  }
  
  // If no category found from topics, check description and name
  if (industryCategory === 'Other') {
    // Create a combined text to search for keywords
    const combinedText = `${description} ${name} ${fullName}`;
    
    for (const [keyword, category] of Object.entries(industryCategories)) {
      if (combinedText.includes(keyword.toLowerCase())) {
        industryCategory = category;
        break;
      }
    }
    
    // Special cases for blockchain projects
    if (combinedText.includes('solana') || 
        combinedText.includes('anchor') || 
        combinedText.includes('token') || 
        combinedText.includes('wallet') ||
        combinedText.includes('chain')) {
      industryCategory = 'Blockchain';
    }
  }
  
  return {
    languageCategory,
    industryCategory
  };
}

// Process repositories
const processedRepos = reposData.map(repo => {
  const { languageCategory, industryCategory } = categorizeRepo(repo);
  
  // Calculate quality score (simple heuristic)
  const starsWeight = 0.5;
  const forksWeight = 0.3;
  const updatedWeight = 0.2;
  
  // Convert updated_at to days since last update
  const lastUpdated = new Date(repo.updated_at);
  const now = new Date();
  const daysSinceUpdate = Math.floor((now - lastUpdated) / (1000 * 60 * 60 * 24));
  
  // Normalize metrics
  const normalizedStars = Math.min(repo.stargazers_count / 1000, 1);
  const normalizedForks = Math.min(repo.forks_count / 100, 1);
  const normalizedUpdated = Math.max(0, 1 - (daysSinceUpdate / 365)); // Higher score for more recent updates
  
  const qualityScore = (
    normalizedStars * starsWeight +
    normalizedForks * forksWeight +
    normalizedUpdated * updatedWeight
  ).toFixed(2);
  
  return {
    name: repo.name,
    full_name: repo.full_name,
    description: repo.description || 'No description provided',
    url: repo.html_url,
    language: repo.language || 'Not specified',
    stars: repo.stargazers_count,
    forks: repo.forks_count,
    issues: repo.open_issues_count,
    updated_at: repo.updated_at,
    created_at: repo.created_at,
    pushed_at: repo.pushed_at,
    size: repo.size,
    topics: repo.topics || [],
    languageCategory,
    industryCategory,
    qualityScore: parseFloat(qualityScore)
  };
});

// Group repositories by language category
const byLanguage = {};
processedRepos.forEach(repo => {
  if (!byLanguage[repo.languageCategory]) {
    byLanguage[repo.languageCategory] = [];
  }
  byLanguage[repo.languageCategory].push(repo);
});

// Group repositories by industry category
const byIndustry = {};
processedRepos.forEach(repo => {
  if (!byIndustry[repo.industryCategory]) {
    byIndustry[repo.industryCategory] = [];
  }
  byIndustry[repo.industryCategory].push(repo);
});

// Sort repositories within each category by quality score
for (const category in byLanguage) {
  byLanguage[category].sort((a, b) => b.qualityScore - a.qualityScore);
}

for (const category in byIndustry) {
  byIndustry[category].sort((a, b) => b.qualityScore - a.qualityScore);
}

// Create knowledge graph
const knowledgeGraph = {
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
  "dateCreated": new Date().toISOString(),
  "categories": Object.keys(byIndustry).map(category => ({
    "@type": "CategoryCode",
    "name": category,
    "codeValue": category.toLowerCase().replace(/\s+/g, '-')
  })),
  "programmingLanguages": Object.keys(byLanguage).map(language => ({
    "@type": "ComputerLanguage",
    "name": language
  })),
  "repositories": processedRepos.map(repo => ({
    "@type": "SoftwareSourceCode",
    "name": repo.name,
    "description": repo.description,
    "url": repo.url,
    "programmingLanguage": repo.language,
    "codeRepository": repo.url,
    "dateCreated": repo.created_at,
    "dateModified": repo.updated_at,
    "starCount": repo.stars,
    "forkCount": repo.forks,
    "issueCount": repo.issues,
    "category": repo.industryCategory,
    "qualityScore": repo.qualityScore,
    "keywords": repo.topics
  }))
};

// Generate README.md content
let readmeContent = `# Awesome Rinegade

A curated list of awesome repositories starred by [0xrinegade](https://github.com/0xrinegade?tab=stars).

## Table of Contents

- [By Industry](#by-industry)
${Object.keys(byIndustry).sort().map(category => `  - [${category}](#${category.toLowerCase().replace(/\s+/g, '-')})`).join('\n')}
- [By Language](#by-language)
${Object.keys(byLanguage).sort().map(language => `  - [${language}](#${language.toLowerCase().replace(/\s+/g, '-')})`).join('\n')}

## By Industry

`;

// Add repositories by industry
for (const category of Object.keys(byIndustry).sort()) {
  readmeContent += `### ${category}\n\n`;
  
  // Limit to top 20 repositories per category to keep the README manageable
  const topRepos = byIndustry[category].slice(0, 20);
  
  for (const repo of topRepos) {
    const lastUpdated = new Date(repo.updated_at).toISOString().split('T')[0];
    readmeContent += `- [${repo.full_name}](${repo.url}) - ${repo.description}
  - **Language:** ${repo.language} | **Stars:** ${repo.stars} | **Forks:** ${repo.forks} | **Last Updated:** ${lastUpdated} | **Quality Score:** ${repo.qualityScore}
  - ${repo.topics.length > 0 ? `**Topics:** ${repo.topics.join(', ')}` : 'No topics'}
`;
  }
  
  if (byIndustry[category].length > 20) {
    readmeContent += `- *And ${byIndustry[category].length - 20} more repositories in this category*\n`;
  }
  
  readmeContent += '\n';
}

readmeContent += `## By Language

`;

// Add repositories by language
for (const language of Object.keys(byLanguage).sort()) {
  readmeContent += `### ${language}\n\n`;
  
  // Limit to top 20 repositories per language to keep the README manageable
  const topRepos = byLanguage[language].slice(0, 20);
  
  for (const repo of topRepos) {
    const lastUpdated = new Date(repo.updated_at).toISOString().split('T')[0];
    readmeContent += `- [${repo.full_name}](${repo.url}) - ${repo.description}
  - **Industry:** ${repo.industryCategory} | **Stars:** ${repo.stars} | **Forks:** ${repo.forks} | **Last Updated:** ${lastUpdated} | **Quality Score:** ${repo.qualityScore}
  - ${repo.topics.length > 0 ? `**Topics:** ${repo.topics.join(', ')}` : 'No topics'}
`;
  }
  
  if (byLanguage[language].length > 20) {
    readmeContent += `- *And ${byLanguage[language].length - 20} more repositories in this category*\n`;
  }
  
  readmeContent += '\n';
}

// Add footer
readmeContent += `
## About

This list was generated by analyzing ${processedRepos.length} repositories starred by [0xrinegade](https://github.com/0xrinegade?tab=stars). The repositories are categorized by industry and programming language, and ranked by a quality score that takes into account stars, forks, and recency of updates.

The knowledge graph of these repositories is available in [knowledge-graph.json-ld](knowledge-graph.json-ld).
`;

// Write the files
fs.writeFileSync('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/knowledge-graph.json-ld', JSON.stringify(knowledgeGraph, null, 2));
fs.writeFileSync('/tmp/tmpeguxdbvy_run_aldrin-labs_awesome-rinegade_issue_3_e57e17fc/README.md', readmeContent);

console.log(`Processed ${processedRepos.length} repositories`);
console.log(`Found ${Object.keys(byIndustry).length} industry categories`);
console.log(`Found ${Object.keys(byLanguage).length} language categories`);
console.log('Files written: README.md and knowledge-graph.json-ld');

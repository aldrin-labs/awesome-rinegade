import json
import os
from collections import defaultdict

# Function to generate knowledge graph in JSON-LD format
def generate_knowledge_graph(repos):
    # Create the JSON-LD context
    knowledge_graph = {
        "@context": {
            "@vocab": "http://schema.org/",
            "repo": "http://schema.org/SoftwareSourceCode",
            "language": "http://schema.org/programmingLanguage",
            "topic": "http://schema.org/about",
            "industry": "http://schema.org/applicationCategory",
            "relatedTo": {
                "@id": "http://schema.org/isRelatedTo",
                "@type": "@id"
            },
            "similarTo": {
                "@id": "http://schema.org/isSimilarTo",
                "@type": "@id"
            },
            "creator": "http://schema.org/creator",
            "dateCreated": "http://schema.org/dateCreated",
            "dateModified": "http://schema.org/dateModified",
            "description": "http://schema.org/description",
            "name": "http://schema.org/name",
            "url": "http://schema.org/url",
            "starCount": "http://schema.org/interactionCount"
        },
        "@graph": []
    }
    
    # Create nodes for each repository
    for repo in repos:
        repo_node = {
            "@type": "repo",
            "@id": f"repo:{repo['full_name']}",
            "name": repo['full_name'],
            "description": repo.get('description', ''),
            "url": f"https://github.com/{repo['full_name']}",
            "language": repo.get('language', 'Unknown'),
            "dateCreated": repo.get('created_at', ''),
            "dateModified": repo.get('updated_at', ''),
            "starCount": repo.get('stars', 0),
            "topics": repo.get('topics', []),
            "creator": {
                "@type": "Person",
                "name": repo['full_name'].split('/')[0]
            }
        }
        
        knowledge_graph["@graph"].append(repo_node)
    
    # Create relationships between repositories
    # 1. By shared language
    language_groups = defaultdict(list)
    for repo in repos:
        language = repo.get('language')
        if language:
            language_groups[language].append(repo['full_name'])
    
    # 2. By shared topics
    topic_groups = defaultdict(list)
    for repo in repos:
        for topic in repo.get('topics', []):
            topic_groups[topic].append(repo['full_name'])
    
    # 3. By shared owner/creator
    owner_groups = defaultdict(list)
    for repo in repos:
        owner = repo['full_name'].split('/')[0]
        owner_groups[owner].append(repo['full_name'])
    
    # Add relationship nodes
    # Language relationships
    for language, repo_names in language_groups.items():
        if len(repo_names) > 1:  # Only create relationships if there are at least 2 repos
            for i, repo1 in enumerate(repo_names):
                for repo2 in repo_names[i+1:]:
                    relationship = {
                        "@type": "relatedTo",
                        "@id": f"relationship:language:{repo1}:{repo2}",
                        "subject": f"repo:{repo1}",
                        "object": f"repo:{repo2}",
                        "relationshipType": "shared_language",
                        "language": language
                    }
                    knowledge_graph["@graph"].append(relationship)
    
    # Topic relationships (limit to avoid explosion of relationships)
    for topic, repo_names in topic_groups.items():
        if 2 <= len(repo_names) <= 20:  # Only create relationships if there are between 2 and 20 repos
            for i, repo1 in enumerate(repo_names):
                for repo2 in repo_names[i+1:]:
                    relationship = {
                        "@type": "relatedTo",
                        "@id": f"relationship:topic:{repo1}:{repo2}:{topic}",
                        "subject": f"repo:{repo1}",
                        "object": f"repo:{repo2}",
                        "relationshipType": "shared_topic",
                        "topic": topic
                    }
                    knowledge_graph["@graph"].append(relationship)
    
    # Find similar repositories based on multiple shared topics
    repo_topics = {}
    for repo in repos:
        repo_topics[repo['full_name']] = set(repo.get('topics', []))
    
    similarity_pairs = []
    for repo1, topics1 in repo_topics.items():
        if not topics1:  # Skip repos with no topics
            continue
            
        for repo2, topics2 in repo_topics.items():
            if repo1 >= repo2:  # Avoid duplicates and self-comparisons
                continue
                
            if not topics2:  # Skip repos with no topics
                continue
                
            # Calculate Jaccard similarity
            intersection = len(topics1.intersection(topics2))
            union = len(topics1.union(topics2))
            
            if union > 0 and intersection >= 3:  # At least 3 shared topics
                similarity = intersection / union
                similarity_pairs.append((repo1, repo2, similarity, list(topics1.intersection(topics2))))
    
    # Sort by similarity and take top pairs
    similarity_pairs.sort(key=lambda x: x[2], reverse=True)
    top_similar_pairs = similarity_pairs[:1000]  # Limit to 1000 most similar pairs
    
    # Add similarity relationships
    for repo1, repo2, similarity, shared_topics in top_similar_pairs:
        relationship = {
            "@type": "similarTo",
            "@id": f"relationship:similar:{repo1}:{repo2}",
            "subject": f"repo:{repo1}",
            "object": f"repo:{repo2}",
            "similarityScore": round(similarity, 2),
            "sharedTopics": shared_topics
        }
        knowledge_graph["@graph"].append(relationship)
    
    return knowledge_graph

# Main execution
if __name__ == "__main__":
    if not os.path.exists('repo_metadata.json'):
        print("Error: repo_metadata.json not found. Run fetch_repo_metadata.py first.")
        exit(1)
    
    # Load repository metadata
    with open('repo_metadata.json', 'r') as f:
        repos = json.load(f)
    
    print(f"Loaded {len(repos)} repositories from metadata file")
    
    # Generate knowledge graph
    print("Generating knowledge graph...")
    knowledge_graph = generate_knowledge_graph(repos)
    
    # Save knowledge graph
    with open('knowledge-graph.json-ld', 'w') as f:
        json.dump(knowledge_graph, f, indent=2)
    
    print("Knowledge graph generated successfully")
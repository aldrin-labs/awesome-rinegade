import os
import subprocess
import sys

def run_script(script_name):
    print(f"\n=== Running {script_name} ===")
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running {script_name}:")
        print(result.stderr)
        return False
    
    print(result.stdout)
    return True

def main():
    # Step 1: Fetch starred repositories
    if not run_script('fetch_starred_repos.py'):
        return
    
    # Step 2: Fetch repository metadata
    if not run_script('fetch_repo_metadata.py'):
        return
    
    # Step 3: Generate README
    if not run_script('generate_readme.py'):
        return
    
    # Step 4: Generate knowledge graph
    if not run_script('generate_knowledge_graph.py'):
        return
    
    print("\n=== All tasks completed successfully ===")
    print("The awesome-rinegade list has been created with:")
    print("1. README.md - Categorized list of repositories")
    print("2. knowledge-graph.json-ld - Knowledge graph of repositories")

if __name__ == "__main__":
    main()
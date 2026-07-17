import os
import sys
import json
import urllib.request

# Path to .env relative to script directory (two levels up)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
env_file_path = os.path.join(project_dir, ".env")

def load_env(filepath):
    env_vars = {}
    if not os.path.exists(filepath):
        return env_vars
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, val = line.split('=', 1)
                env_vars[key.strip()] = val.strip().strip('"').strip("'")
    return env_vars

def fetch_linear_issue(api_key, issue_key):
    url = "https://api.linear.app/graphql"
    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key
    }
    
    query = """
    query GetIssue($id: String!) {
      issue(id: $id) {
        id
        identifier
        title
        description
        state {
          name
        }
        comments {
          nodes {
            body
            createdAt
            user {
              name
            }
          }
        }
      }
    }
    """
    
    data = {
        "query": query,
        "variables": {"id": issue_key}
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except Exception as e:
        print(f"Error fetching from Linear API: {str(e)}")
        if hasattr(e, 'read'):
            print("Response detail:", e.read().decode("utf-8"))
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 fetch_linear.py <Linear-Issue-ID> [optional_output_path]")
        print("Example: python3 fetch_linear.py NUH-1199")
        sys.exit(1)
        
    issue_key = sys.argv[1].upper()
    
    # Optional output file path
    output_path = None
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        # Default output file in the parent folder's context if exists, or inside project folder
        parent_dir = os.path.dirname(project_dir)
        workspace_md_dir = os.path.join(parent_dir, "workbooks", "md from linear")
        if os.path.exists(workspace_md_dir):
            output_path = os.path.join(workspace_md_dir, f"{issue_key}_details.md")
        else:
            output_path = os.path.join(project_dir, f"{issue_key}_details.md")

    print(f"Reading configuration from {env_file_path}...")
    env = load_env(env_file_path)
    api_key = env.get("LINEAR_API_TOKEN")
    
    if not api_key:
        print("Error: LINEAR_API_TOKEN not found in .env file.")
        sys.exit(1)
        
    print(f"Fetching issue {issue_key} from Linear API...")
    result = fetch_linear_issue(api_key, issue_key)
    
    if not result or "errors" in result:
        print("Error: Failed to fetch issue data or API returned errors.")
        print(json.dumps(result, indent=2) if result else "")
        sys.exit(1)
        
    issue = result.get("data", {}).get("issue")
    if not issue:
        print(f"Error: Issue {issue_key} not found.")
        sys.exit(1)
        
    # Build Markdown Content
    markdown_content = f"""# Linear Issue: {issue.get('identifier')} - {issue.get('title')}
**Status:** {issue.get('state', {}).get('name')}

## Description & Acceptance Criteria
{issue.get('description', 'No description provided.')}

## Comments / Discussion History
"""
    comments = issue.get("comments", {}).get("nodes", [])
    if not comments:
        markdown_content += "No comments found on this issue.\n"
    else:
        # Reverse comments so oldest is comment #1, newest is at the end
        for idx, comment in enumerate(reversed(comments), start=1):
            markdown_content += f"### Comment #{idx} by {comment.get('user', {}).get('name')} ({comment.get('createdAt')})\n"
            markdown_content += f"{comment.get('body')}\n\n"
            
    # Write to Markdown file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    print(f"Success! Linear issue data saved to: {output_path}")

if __name__ == "__main__":
    main()

import os
import git
from urllib.parse import urlparse

class GitCloner:
    def __init__(self):
        pass
    
    def clone_repository(self, repo_url, destination_dir):
        """Clone a GitHub repository to the specified directory"""
        try:
            # Parse the URL to get repository name
            parsed_url = urlparse(repo_url)
            repo_name = os.path.basename(parsed_url.path).replace('.git', '')
            
            # Create full path for cloning
            clone_path = os.path.join(destination_dir, repo_name)
            
            # Clone the repository
            git.Repo.clone_from(repo_url, clone_path)
            
            return clone_path
            
        except git.exc.GitCommandError as e:
            raise Exception(f"Failed to clone repository: {str(e)}")
        except Exception as e:
            raise Exception(f"Error during cloning: {str(e)}")
    
    def is_valid_github_url(self, url):
        """Validate if the URL is a valid GitHub repository URL"""
        try:
            parsed = urlparse(url)
            return (parsed.netloc == 'github.com' and 
                   len(parsed.path.split('/')) >= 3)
        except:
            return False

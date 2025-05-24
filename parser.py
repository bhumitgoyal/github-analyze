import os
import json
from pathlib import Path

class RepoParser:
    def __init__(self):
        self.tech_stack_indicators = {
            'Python': ['.py', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
            'JavaScript/Node.js': ['.js', '.jsx', 'package.json', '.npmrc'],
            'TypeScript': ['.ts', '.tsx', 'tsconfig.json'],
            'React': ['package.json'],  # Will check content
            'Vue.js': ['package.json'],  # Will check content
            'Angular': ['package.json', 'angular.json'],
            'Java': ['.java', 'pom.xml', 'build.gradle'],
            'C#': ['.cs', '.csproj', '.sln'],
            'Go': ['.go', 'go.mod', 'go.sum'],
            'Rust': ['.rs', 'Cargo.toml'],
            'PHP': ['.php', 'composer.json'],
            'Ruby': ['.rb', 'Gemfile'],
            'Docker': ['Dockerfile', 'docker-compose.yml'],
            'Kubernetes': ['.yaml', '.yml'],  # Will check content
        }
    
    def analyze_repository(self, repo_path):
        """Analyze repository structure and detect technologies"""
        repo_data = {
            'path': repo_path,
            'name': os.path.basename(repo_path),
            'structure': self._get_folder_structure(repo_path),
            'key_files': self._find_key_files(repo_path),
            'tech_stack': self._detect_tech_stack(repo_path),
            'file_contents': self._read_important_files(repo_path),
            'statistics': self._get_repo_statistics(repo_path)
        }
        
        return repo_data
    
    def _get_folder_structure(self, repo_path, max_depth=3):
        """Get repository folder structure"""
        structure = {}
        
        def build_tree(path, current_depth=0):
            if current_depth >= max_depth:
                return "..."
            
            items = {}
            try:
                for item in os.listdir(path):
                    if item.startswith('.') and item not in ['.env', '.gitignore', '.github']:
                        continue
                    
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        items[item + '/'] = build_tree(item_path, current_depth + 1)
                    else:
                        items[item] = os.path.getsize(item_path)
            except PermissionError:
                pass
            
            return items
        
        return build_tree(repo_path)
    
    def _find_key_files(self, repo_path):
        """Find important files in the repository"""
        key_files = {}
        important_files = [
            'README.md', 'README.txt', 'README.rst',
            'package.json', 'requirements.txt', 'setup.py',
            'Dockerfile', 'docker-compose.yml',
            'main.py', 'index.js', 'main.js', 'app.py',
            'main.tsx', 'index.tsx', 'App.tsx',
            'pom.xml', 'build.gradle', 'Cargo.toml'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            # Skip hidden directories and common build/cache directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'build', 'dist', 'target']]
            
            for file in files:
                if file in important_files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    key_files[relative_path] = file_path
        
        return key_files
    
    def _detect_tech_stack(self, repo_path):
        """Detect technologies used in the repository"""
        detected_tech = set()
        
        # Check file extensions and specific files
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'build', 'dist']]
            
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix
                
                # Check against tech stack indicators
                for tech, indicators in self.tech_stack_indicators.items():
                    if file in indicators or file_ext in indicators:
                        detected_tech.add(tech)
                        
                        # Special checks for package.json content
                        if file == 'package.json':
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    package_data = json.loads(f.read())
                                    dependencies = {**package_data.get('dependencies', {}), 
                                                  **package_data.get('devDependencies', {})}
                                    
                                    if 'react' in dependencies:
                                        detected_tech.add('React')
                                    if 'vue' in dependencies:
                                        detected_tech.add('Vue.js')
                                    if '@angular/core' in dependencies:
                                        detected_tech.add('Angular')
                                    if 'express' in dependencies:
                                        detected_tech.add('Express.js')
                            except:
                                pass
        
        return list(detected_tech)
    
    def _read_important_files(self, repo_path):
        """Read content of important files"""
        file_contents = {}
        max_file_size = 50000  # 50KB limit
        
        important_patterns = [
            'README.md', 'README.txt', 'README.rst',
            'main.py', 'app.py', 'index.js', 'main.js',
            'main.tsx', 'index.tsx', 'App.tsx',
            'package.json', 'requirements.txt', 'setup.py'
        ]
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'build', 'dist']]
            
            for file in files:
                if any(pattern in file for pattern in important_patterns):
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(file_path, repo_path)
                    
                    try:
                        if os.path.getsize(file_path) <= max_file_size:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                file_contents[relative_path] = content[:5000]  # Limit content
                    except:
                        file_contents[relative_path] = "Could not read file content"
        
        return file_contents
    
    def _get_repo_statistics(self, repo_path):
        """Get basic repository statistics"""
        stats = {
            'total_files': 0,
            'total_size': 0,
            'file_types': {},
            'largest_files': []
        }
        
        file_sizes = []
        
        for root, dirs, files in os.walk(repo_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and 
                      d not in ['node_modules', '__pycache__', 'build', 'dist']]
            
            for file in files:
                if not file.startswith('.'):
                    file_path = os.path.join(root, file)
                    try:
                        size = os.path.getsize(file_path)
                        stats['total_files'] += 1
                        stats['total_size'] += size
                        
                        # Track file types
                        ext = Path(file).suffix or 'no_extension'
                        stats['file_types'][ext] = stats['file_types'].get(ext, 0) + 1
                        
                        # Track large files
                        relative_path = os.path.relpath(file_path, repo_path)
                        file_sizes.append((relative_path, size))
                    except:
                        pass
        
        # Get top 5 largest files
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        stats['largest_files'] = file_sizes[:5]
        
        return stats

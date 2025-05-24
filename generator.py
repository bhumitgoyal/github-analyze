import markdown
from datetime import datetime

class DocumentationGenerator:
    def __init__(self):
        self.md = markdown.Markdown(extensions=['codehilite', 'fenced_code'])
    
    def generate_documentation(self, repo_data, summaries):
        """Generate comprehensive documentation in Markdown format"""
        
        # Generate Markdown documentation
        markdown_doc = self._generate_markdown(repo_data, summaries)
        
        # Convert to HTML
        html_doc = self._generate_html(markdown_doc)
        
        return {
            'markdown': markdown_doc,
            'html': html_doc,
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'repo_name': repo_data['name'],
                'tech_stack': repo_data['tech_stack']
            }
        }
    
    def _generate_markdown(self, repo_data, summaries):
        """Generate Markdown documentation"""
        
        md_content = f"""# 📊 Repository Analysis: {repo_data['name']}

*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*

---

## 🧾 Project Summary

{summaries.get('project_overview', 'Project overview not available')}

---

## 🛠️ Tech Stack

**Detected Technologies:** {', '.join(repo_data['tech_stack']) if repo_data['tech_stack'] else 'None detected'}

{summaries.get('tech_stack_explanation', 'Tech stack explanation not available')}

---

## 📂 Folder Structure

{summaries.get('structure_explanation', 'Folder structure explanation not available')}

### Directory Tree

---

## 🚀 Installation & Setup

{summaries.get('installation_guide', 'Installation guide not available')}

---

## 📜 Key Files Overview

{self._generate_files_section(repo_data, summaries)}

---

## 📊 Repository Statistics

- **Total Files:** {repo_data['statistics']['total_files']}
- **Total Size:** {self._format_size(repo_data['statistics']['total_size'])}
- **File Types:** {self._format_file_types(repo_data['statistics']['file_types'])}

### Largest Files
{self._format_largest_files(repo_data['statistics']['largest_files'])}

---

## 🔍 Quick Navigation

- [Project Summary](#project-summary)
- [Tech Stack](#tech-stack)
- [Installation](#installation--setup)
- [Key Files](#key-files-overview)
- [Statistics](#repository-statistics)

---

*This documentation was automatically generated using AI analysis. For the most up-to-date information, please refer to the repository's README and source code.*
"""
        
        return md_content
    
    def _generate_html(self, markdown_content):
        """Convert Markdown to HTML with professional dark theme styling"""
        
        html_content = self.md.convert(markdown_content)
        
        # Wrap in a complete HTML document with professional dark theme
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Repository Analysis</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border-primary: #30363d;
            --border-secondary: #21262d;
            --text-primary: #f0f6fc;
            --text-secondary: #8b949e;
            --text-muted: #656d76;
            --accent-primary: #2f81f7;
            --accent-secondary: #238636;
            --accent-warning: #d29922;
            --accent-danger: #da3633;
            --code-bg: #0d1117;
            --code-border: #30363d;
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            --gradient-primary: linear-gradient(135deg, #2f81f7 0%, #238636 100%);
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            line-height: 1.7;
            color: var(--text-primary);
            background: var(--bg-primary);
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(47, 129, 247, 0.05) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(35, 134, 54, 0.05) 0%, transparent 50%);
            min-height: 100vh;
            font-size: 16px;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-primary);
            border-radius: 12px;
            box-shadow: var(--shadow);
            margin-top: 2rem;
            margin-bottom: 2rem;
            position: relative;
        }}
        
        .container::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: var(--gradient-primary);
            border-radius: 12px 12px 0 0;
        }}
        
        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--text-primary);
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid var(--border-primary);
            background: var(--gradient-primary);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: -0.025em;
        }}
        
        h2 {{
            font-size: 1.875rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 3rem 0 1.5rem 0;
            padding-bottom: 0.75rem;
            border-bottom: 2px solid var(--accent-primary);
            position: relative;
        }}
        
        h2::before {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 0;
            width: 60px;
            height: 2px;
            background: var(--accent-secondary);
        }}
        
        h3 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
            margin: 2rem 0 1rem 0;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-secondary);
        }}
        
        p {{
            margin-bottom: 1rem;
            color: var(--text-secondary);
            line-height: 1.8;
        }}
        
        em {{
            color: var(--text-muted);
            font-style: italic;
            font-size: 0.9rem;
        }}
        
        strong {{
            color: var(--text-primary);
            font-weight: 600;
        }}
        
        code {{
            background: var(--code-bg);
            border: 1px solid var(--code-border);
            color: var(--accent-primary);
            padding: 0.25rem 0.5rem;
            border-radius: 6px;
            font-family: 'SF Mono', Monaco, 'Cascadia Code', 'Roboto Mono', Consolas, 'Courier New', monospace;
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        pre {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            padding: 1.5rem;
            overflow-x: auto;
            margin: 1rem 0;
            position: relative;
        }}
        
        pre code {{
            background: none;
            border: none;
            color: var(--text-primary);
            padding: 0;
            font-size: 0.875rem;
            line-height: 1.6;
        }}
        
        ul, ol {{
            margin: 1rem 0 1rem 2rem;
            color: var(--text-secondary);
        }}
        
        li {{
            margin-bottom: 0.5rem;
            line-height: 1.7;
        }}
        
        li::marker {{
            color: var(--accent-primary);
        }}
        
        a {{
            color: var(--accent-primary);
            text-decoration: none;
            transition: all 0.2s ease;
            border-bottom: 1px solid transparent;
        }}
        
        a:hover {{
            color: var(--text-primary);
            border-bottom-color: var(--accent-primary);
        }}
        
        hr {{
            border: none;
            height: 2px;
            background: var(--gradient-primary);
            margin: 3rem 0;
            border-radius: 1px;
            opacity: 0.8;
        }}
        
        .tech-stack {{
            background: var(--bg-tertiary);
            border: 1px solid var(--accent-primary);
            border-left: 4px solid var(--accent-primary);
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            position: relative;
            overflow: hidden;
        }}
        
        .tech-stack::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(47, 129, 247, 0.05) 0%, transparent 100%);
            pointer-events: none;
        }}
        
        .file-section {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            transition: all 0.3s ease;
        }}
        
        .file-section:hover {{
            border-color: var(--accent-primary);
            box-shadow: 0 4px 16px rgba(47, 129, 247, 0.1);
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }}
        
        .stat-card {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }}
        
        .stat-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--gradient-primary);
        }}
        
        .stat-card:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(47, 129, 247, 0.15);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: 700;
            background: var(--gradient-primary);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
            display: block;
        }}
        
        .stat-label {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        blockquote {{
            border-left: 4px solid var(--accent-secondary);
            padding: 1rem 1.5rem;
            margin: 1.5rem 0;
            background: var(--bg-tertiary);
            border-radius: 0 8px 8px 0;
            font-style: italic;
            color: var(--text-secondary);
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            background: var(--bg-tertiary);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-primary);
        }}
        
        th, td {{
            padding: 1rem;
            text-align: left;
            border-bottom: 1px solid var(--border-secondary);
        }}
        
        th {{
            background: var(--bg-primary);
            color: var(--text-primary);
            font-weight: 600;
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        td {{
            color: var(--text-secondary);
        }}
        
        tr:last-child td {{
            border-bottom: none;
        }}
        
        .navigation {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-primary);
            border-radius: 8px;
            padding: 1.5rem;
            margin: 2rem 0;
        }}
        
        .navigation ul {{
            list-style: none;
            margin: 0;
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0.5rem;
        }}
        
        .navigation li {{
            margin: 0;
        }}
        
        .navigation a {{
            display: block;
            padding: 0.75rem 1rem;
            background: var(--bg-secondary);
            border: 1px solid var(--border-secondary);
            border-radius: 6px;
            transition: all 0.2s ease;
            font-weight: 500;
        }}
        
        .navigation a:hover {{
            background: var(--accent-primary);
            color: var(--text-primary);
            border-color: var(--accent-primary);
            transform: translateX(4px);
        }}
        
        @media (max-width: 768px) {{
            .container {{
                margin: 1rem;
                padding: 1.5rem;
            }}
            
            h1 {{
                font-size: 2rem;
            }}
            
            h2 {{
                font-size: 1.5rem;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            .navigation ul {{
                grid-template-columns: 1fr;
            }}
        }}
        
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        {html_content}
    </div>
</body>
</html>
"""
        
        return full_html
    
    def _generate_files_section(self, repo_data, summaries):
        """Generate the key files section"""
        files_section = ""
        
        file_explanations = summaries.get('file_explanations', {})
        
        if not file_explanations:
            return "No key files analyzed."
        
        for file_path, explanation in file_explanations.items():
            files_section += f"""
### 📄 `{file_path}`

{explanation}

---
"""
        
        return files_section
    
    def _format_directory_tree(self, structure, prefix="", is_last=True):
        """Format directory structure as a tree"""
        tree = ""
        items = list(structure.items())
        
        for i, (name, content) in enumerate(items):
            is_last_item = i == len(items) - 1
            current_prefix = "└── " if is_last_item else "├── "
            tree += f"{prefix}{current_prefix}{name}\n"
            
            if isinstance(content, dict) and content:
                extension = "    " if is_last_item else "│   "
                tree += self._format_directory_tree(content, prefix + extension, is_last_item)
        
        return tree
    
    def _format_size(self, size_bytes):
        """Format file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"
    
    def _format_file_types(self, file_types):
        """Format file types statistics"""
        if not file_types:
            return "No file types detected"
        
        sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
        formatted = []
        
        for ext, count in sorted_types[:10]:  # Top 10 file types
            formatted.append(f"{ext}: {count}")
        
        return ", ".join(formatted)
    
    def _format_largest_files(self, largest_files):
        """Format largest files list"""
        if not largest_files:
            return "No files analyzed"
        
        formatted = ""
        for file_path, size in largest_files:
            formatted += f"- `{file_path}` ({self._format_size(size)})\n"
        
        return formatted
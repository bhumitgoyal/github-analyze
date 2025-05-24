import os
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

class RepoSummarizer:
    def __init__(self):
        self.llm = OpenAI(
            openai_api_key=os.getenv('OPENAI_API_KEY'),
            temperature=0.3,
            max_tokens=1000
        )
    
    def generate_summaries(self, repo_data):
        """Generate AI-powered summaries for different aspects of the repository"""
        summaries = {}
        
        try:
            # Project overview summary
            summaries['project_overview'] = self._generate_project_overview(repo_data)
            
            # Tech stack explanation
            summaries['tech_stack_explanation'] = self._explain_tech_stack(repo_data)
            
            # Installation instructions
            summaries['installation_guide'] = self._generate_installation_guide(repo_data)
            
            # File explanations
            summaries['file_explanations'] = self._explain_key_files(repo_data)
            
            # Folder structure explanation
            summaries['structure_explanation'] = self._explain_folder_structure(repo_data)
            
        except Exception as e:
            summaries['error'] = f"Error generating summaries: {str(e)}"
        
        return summaries
    
    def _generate_project_overview(self, repo_data):
        """Generate a comprehensive project overview"""
        prompt_template = PromptTemplate(
            input_variables=["repo_name", "readme_content", "tech_stack", "file_structure"],
            template="""
            Analyze this GitHub repository and provide a comprehensive project overview:

            Repository Name: {repo_name}
            Technologies Used: {tech_stack}
            
            README Content:
            {readme_content}
            
            Key Files Structure:
            {file_structure}
            
            Please provide:
            1. A clear, concise description of what this project does
            2. The main purpose and goals of the project
            3. Target audience or use cases
            4. Key features and functionality
            
            Write in a professional, informative tone suitable for developers.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        # Prepare input data
        readme_content = self._get_readme_content(repo_data)
        file_structure = self._format_file_structure(repo_data['key_files'])
        
        try:
            result = chain.run(
                repo_name=repo_data['name'],
                readme_content=readme_content,
                tech_stack=', '.join(repo_data['tech_stack']),
                file_structure=file_structure
            )
            return result.strip()
        except Exception as e:
            return f"Could not generate project overview: {str(e)}"
    
    def _explain_tech_stack(self, repo_data):
        """Explain the detected technology stack"""
        prompt_template = PromptTemplate(
            input_variables=["tech_stack", "package_files"],
            template="""
            Explain the technology stack used in this project:
            
            Detected Technologies: {tech_stack}
            
            Package/Config Files Content:
            {package_files}
            
            Please provide:
            1. Explanation of each technology and its role in the project
            2. How these technologies work together
            3. Benefits of this particular tech stack combination
            4. Any notable frameworks or libraries being used
            
            Keep the explanation clear and informative for developers.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        package_files = self._get_package_files_content(repo_data)
        
        try:
            result = chain.run(
                tech_stack=', '.join(repo_data['tech_stack']),
                package_files=package_files
            )
            return result.strip()
        except Exception as e:
            return f"Could not explain tech stack: {str(e)}"
    
    def _generate_installation_guide(self, repo_data):
        """Generate installation and setup instructions"""
        prompt_template = PromptTemplate(
            input_variables=["tech_stack", "config_files", "readme_content"],
            template="""
            Generate step-by-step installation and setup instructions for this project:
            
            Technologies: {tech_stack}
            
            Configuration Files Found:
            {config_files}
            
            README Content (for reference):
            {readme_content}
            
            Please provide:
            1. Prerequisites and system requirements
            2. Step-by-step installation instructions
            3. How to run the project locally
            4. Common setup issues and solutions
            5. Environment variables or configuration needed
            
            Format as clear, numbered steps that a developer can follow.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        config_files = self._get_config_files_content(repo_data)
        readme_content = self._get_readme_content(repo_data)
        
        try:
            result = chain.run(
                tech_stack=', '.join(repo_data['tech_stack']),
                config_files=config_files,
                readme_content=readme_content
            )
            return result.strip()
        except Exception as e:
            return f"Could not generate installation guide: {str(e)}"
    
    def _explain_key_files(self, repo_data):
        """Explain the purpose of key files in the repository"""
        file_explanations = {}
        
        prompt_template = PromptTemplate(
            input_variables=["file_name", "file_content", "tech_stack"],
            template="""
            Explain the purpose and functionality of this file in the context of a {tech_stack} project:
            
            File: {file_name}
            Content:
            {file_content}
            
            Please provide:
            1. What this file does and its purpose
            2. Key components or functions it contains
            3. How it fits into the overall project architecture
            4. Any important patterns or practices used
            
            Keep the explanation concise but informative.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        for file_path, content in repo_data['file_contents'].items():
            if len(content) > 100:  # Only explain files with substantial content
                try:
                    explanation = chain.run(
                        file_name=file_path,
                        file_content=content[:2000],  # Limit content length
                        tech_stack=', '.join(repo_data['tech_stack'])
                    )
                    file_explanations[file_path] = explanation.strip()
                except Exception as e:
                    file_explanations[file_path] = f"Could not explain file: {str(e)}"
        
        return file_explanations
    
    def _explain_folder_structure(self, repo_data):
        """Explain the folder structure and organization"""
        prompt_template = PromptTemplate(
            input_variables=["folder_structure", "tech_stack", "project_type"],
            template="""
            Explain the folder structure and organization of this {tech_stack} project:
            
            Folder Structure:
            {folder_structure}
            
            Please provide:
            1. Purpose of each main folder/directory
            2. How the project is organized
            3. Common patterns or conventions being followed
            4. Benefits of this particular structure
            
            Focus on the main directories and their roles in the project.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        structure_text = self._format_folder_structure(repo_data['structure'])
        
        try:
            result = chain.run(
                folder_structure=structure_text,
                tech_stack=', '.join(repo_data['tech_stack']),
                project_type=repo_data['tech_stack'][0] if repo_data['tech_stack'] else 'Unknown'
            )
            return result.strip()
        except Exception as e:
            return f"Could not explain folder structure: {str(e)}"
    
    def answer_question(self, repo_data, question):
        """Answer specific questions about the repository"""
        prompt_template = PromptTemplate(
            input_variables=["question", "repo_name", "tech_stack", "file_contents", "structure"],
            template="""
            Answer this question about the {repo_name} repository:
            
            Question: {question}
            
            Repository Information:
            - Technologies: {tech_stack}
            - File Contents: {file_contents}
            - Structure: {structure}
            
            Provide a detailed, accurate answer based on the repository information.
            If the question is about a specific file, focus on that file's content and purpose.
            If you cannot find relevant information, say so clearly.
            """
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        # Prepare context information
        file_contents_summary = ""
        for file_path, content in repo_data['file_contents'].items():
            file_contents_summary += f"\n{file_path}:\n{content[:1000]}...\n"
        
        structure_summary = self._format_folder_structure(repo_data['structure'])
        
        try:
            result = chain.run(
                question=question,
                repo_name=repo_data['name'],
                tech_stack=', '.join(repo_data['tech_stack']),
                file_contents=file_contents_summary,
                structure=structure_summary
            )
            return result.strip()
        except Exception as e:
            return f"Could not answer question: {str(e)}"
    
    # Helper methods
    def _get_readme_content(self, repo_data):
        """Extract README content"""
        for file_path, content in repo_data['file_contents'].items():
            if 'readme' in file_path.lower():
                return content
        return "No README file found"
    
    def _get_package_files_content(self, repo_data):
        """Get content of package/config files"""
        package_files = ""
        package_patterns = ['package.json', 'requirements.txt', 'setup.py', 'pom.xml', 'Cargo.toml']
        
        for file_path, content in repo_data['file_contents'].items():
            if any(pattern in file_path for pattern in package_patterns):
                package_files += f"\n{file_path}:\n{content}\n"
        
        return package_files or "No package files found"
    
    def _get_config_files_content(self, repo_data):
        """Get content of configuration files"""
        config_files = ""
        config_patterns = ['dockerfile', 'docker-compose', '.env', 'config', 'settings']
        
        for file_path, content in repo_data['file_contents'].items():
            if any(pattern in file_path.lower() for pattern in config_patterns):
                config_files += f"\n{file_path}:\n{content}\n"
        
        return config_files or "No configuration files found"
    
    def _format_file_structure(self, key_files):
        """Format key files for display"""
        if not key_files:
            return "No key files found"
        
        formatted = "Key Files:\n"
        for file_path in key_files.keys():
            formatted += f"- {file_path}\n"
        
        return formatted
    
    def _format_folder_structure(self, structure, indent=0):
        """Format folder structure for display"""
        formatted = ""
        for name, content in structure.items():
            formatted += "  " * indent + f"- {name}\n"
            if isinstance(content, dict):
                formatted += self._format_folder_structure(content, indent + 1)
        return formatted

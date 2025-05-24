import os
import tempfile
import shutil
from flask import Flask, request, jsonify, render_template, session
from dotenv import load_dotenv
from analyzer.clone import GitCloner
from analyzer.parser import RepoParser
from analyzer.summarizer import RepoSummarizer
from analyzer.generator import DocumentationGenerator

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default-secret-key')

# Store analyzed repositories in session for chatbot functionality
analyzed_repos = {}

@app.route('/')
def index():
    """Render the main interface"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_repository():
    """Analyze a GitHub repository and return comprehensive documentation"""
    try:
        data = request.get_json()
        repo_url = data.get('repo_url')
        
        if not repo_url:
            return jsonify({'error': 'Repository URL is required'}), 400
        
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Step 1: Clone repository
            cloner = GitCloner()
            repo_path = cloner.clone_repository(repo_url, temp_dir)
            
            # Step 2: Parse repository structure and detect tech stack
            parser = RepoParser()
            repo_data = parser.analyze_repository(repo_path)
            
            # Step 3: Generate AI summaries
            summarizer = RepoSummarizer()
            summaries = summarizer.generate_summaries(repo_data)
            
            # Step 4: Generate final documentation
            generator = DocumentationGenerator()
            documentation = generator.generate_documentation(repo_data, summaries)
            
            # Store for chatbot functionality
            repo_id = repo_url.split('/')[-1]  # Use repo name as ID
            analyzed_repos[repo_id] = {
                'repo_data': repo_data,
                'summaries': summaries,
                'repo_path': repo_path,
                'temp_dir': temp_dir
            }
            
            return jsonify({
                'success': True,
                'documentation': documentation,
                'repo_id': repo_id
            })
            
        except Exception as e:
            # Clean up on error
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            raise e
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_about_repo():
    """Chatbot endpoint for asking questions about analyzed repositories"""
    try:
        data = request.get_json()
        repo_id = data.get('repo_id')
        question = data.get('question')
        
        if not repo_id or not question:
            return jsonify({'error': 'Repository ID and question are required'}), 400
        
        if repo_id not in analyzed_repos:
            return jsonify({'error': 'Repository not found. Please analyze it first.'}), 404
        
        # Get repository data
        repo_info = analyzed_repos[repo_id]
        
        # Use summarizer to answer specific questions
        summarizer = RepoSummarizer()
        answer = summarizer.answer_question(repo_info['repo_data'], question)
        
        return jsonify({
            'success': True,
            'answer': answer
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cleanup/<repo_id>', methods=['DELETE'])
def cleanup_repo(repo_id):
    """Clean up temporary files for a repository"""
    try:
        if repo_id in analyzed_repos:
            temp_dir = analyzed_repos[repo_id]['temp_dir']
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            del analyzed_repos[repo_id]
            
        return jsonify({'success': True, 'message': 'Repository cleaned up'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

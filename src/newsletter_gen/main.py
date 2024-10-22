#!/usr/bin/env python
import os
from flask import Flask, request, jsonify
from crew import NewsletterGenCrew

app = Flask(__name__)

# Get port from environment variable
port = int(os.environ.get('PORT', 8080))

def load_html_template(): 
    try:
        # Updated path to be relative to the current file
        template_path = os.path.join(os.path.dirname(__file__), 'config', 'newsletter_template.html')
        with open(template_path, 'r') as file:
            html_template = file.read()
        return html_template
    except Exception as e:
        print(f"Error loading template: {str(e)}")
        return None

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/generate', methods=['POST'])
def generate_newsletter():
    try:
        data = request.get_json()
        
        if not data or 'topic' not in data or 'personal_message' not in data:
            return jsonify({
                "error": "Missing required fields. Please provide 'topic' and 'personal_message'"
            }), 400

        inputs = {
            'topic': data['topic'],
            'personal_message': data['personal_message'],
            'html_template': load_html_template()
        }

        if inputs['html_template'] is None:
            return jsonify({
                "error": "Failed to load HTML template"
            }), 500

        # Generate newsletter
        result = NewsletterGenCrew().crew().kickoff(inputs=inputs)
        
        return jsonify({
            "status": "success",
            "result": result
        }), 200

    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
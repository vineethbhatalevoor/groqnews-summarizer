from werkzeug.urls import url_encode
from flask import Flask, request, jsonify
import os
import requests  # For Groq API interactions

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Groq-Powered News Summarizer!"})

@app.route('/summarize-text', methods=['POST'])
def summarize_text():
    try:
        data = request.json
        text = data.get('text')
        length = data.get('length', 100)  # Default max tokens

        groq_api_key = os.environ.get('GROQ_API_KEY')  # Ensure this is set

        if not groq_api_key:
            return jsonify({"error": "API key is missing. Set the GROQ_API_KEY environment variable."}), 400

        # Groq API request
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "compound-beta",  # Use Groq's compound-beta model
            "messages": [
                {"role": "system", "content": "Summarize the following text"},
                {"role": "user", "content": text}
            ],
            "max_tokens": length
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",  # Corrected URL
            headers=headers, json=payload)

        if response.status_code == 200:
            summary = response.json().get('summary', 'No summary available.')
            return jsonify({'summary': summary})
        else:
            return jsonify({"error": "Groq API error.", "details": response.json()}), response.status_code

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=False)

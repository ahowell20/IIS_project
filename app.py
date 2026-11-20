import os
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from google import genai
from google.genai import types

# Load API key from .env file
load_dotenv()

app = Flask(__name__)

# Initialize Gemini Client (automatically reads GEMINI_API_KEY from environment)
client = genai.Client()

SYSTEM_INSTRUCTION = """
You are an intelligent email triage and action engine.
Analyze the incoming email (and any provided thread history) and classify it into actions.

Rules:
1. "to_be_read": Set to true if human review is needed before archiving.
2. "auto_file": Set to true ONLY if it is low-value spam, promotional, or automated transaction/receipt that requires zero human reading.
3. "target_folder": Suggest a logical folder (e.g., "Finance/Receipts", "Projects/Q3", "General/FYI").
4. Extract tasks with due dates if implied.
5. Extract meeting details (title, proposed time, duration) if a meeting is requested.
6. Provide a professional draft reply if a response is warranted.
"""

# Serve index.html from the templates folder
@app.route('/')
def home():
    return render_template('index.html')

# API endpoint for processing emails
@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    email_text = data.get('email_text', '')

    prompt = f"Analyze the following email text:\n\n{email_text}"

    schema = {
        "type": "OBJECT",
        "properties": {
            "to_be_read": {"type": "BOOLEAN"},
            "auto_file": {"type": "BOOLEAN"},
            "target_folder": {"type": "STRING"},
            "tasks": {
                "type": "ARRAY",
                "items": {
                    "type": "OBJECT",
                    "properties": {
                        "task": {"type": "STRING"},
                        "due": {"type": "STRING"}
                    },
                    "required": ["task"]
                }
            },
            "meeting": {
                "type": "OBJECT",
                "properties": {
                    "requested": {"type": "BOOLEAN"},
                    "title": {"type": "STRING"},
                    "proposed_time": {"type": "STRING"},
                    "duration": {"type": "STRING"}
                },
                "required": ["requested"]
            },
            "draft_reply": {"type": "STRING"}
        },
        "required": ["to_be_read", "auto_file", "target_folder", "tasks", "meeting"]
    }

    response = client.models.generate_content(
        model='gemini-3.8-flash',
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=schema
        ),
    )

    return jsonify(json.loads(response.text))

    @app.route('/api/redraft', methods=['POST'])
    def redraft():
        data = request.get_json()
        original_email = data.get('original_email', '')
        current_draft = data.get('current_draft', '')
        instruction = data.get('instruction', '')

        if not client:
            return jsonify({"error": "No API key configured. Using local simulation."}), 503

        prompt = f"""
        Rewrite the following email draft based on the user's instruction.
        Return ONLY the updated email body text, with no extra conversational filler or subject line.

        Original Email Received:
        {original_email}

        Current Draft:
        {current_draft}

        User's Refinement Instruction:
        {instruction}
        """

        models_to_try = ['gemini-1.5-flash', 'gemini-1.5-pro']
        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return jsonify({"new_draft": response.text.strip()})
            except Exception as e:
                print(f"⚠️ {model_name} unavailable for redraft: {e}")

        return jsonify({"error": "API temporarily unavailable. Fallback to simulation."}), 503 

if __name__ == '__main__':
    print("Starting AI Assistant Server on http://localhost:5000")
    app.run(port=5000, debug=True)
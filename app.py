from flask import Flask, render_template, request, jsonify
import cohere
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# Initialize the Cohere Client with an API Key
api = os.getenv("COHERE_API_KEY")
co = cohere.Client(api)

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        course = request.get_json().get('course')
        target = request.get_json().get('target')
        duration = request.get_json().get('duration')
        submodule = request.get_json().get('submodule')
        
        # Generate a prediction for the prompt
        prediction = co.chat(message=f'''
            You are a {course} course expert in teaching it to {target} which has a duration of {duration}.
            Can you create a content for the topic : {submodule} with detailed example.
            Give the output in json format:
            {{
                "submodule_title": "string",
                "submodule_content": "string",
                "examples": [string],
            }}
        ''', model='command', connectors=[{"id": "web-search", "name": "Web Search", "created_at": "0001-01-01T00:00:00Z", "updated_at": "0001-01-01T00:00:00Z", "continue_on_failure": True}])

        # print(prediction.text)


        # Return the predicted text in JSON format
        return prediction.text[7:-3]

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

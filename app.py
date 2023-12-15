# from flask import Flask, render_template, request, jsonify
# from flask_cors import CORS, cross_origin
# import cohere
# import os
# from dotenv import load_dotenv
# load_dotenv()

# app = Flask(__name__)
# CORS(app, support_credentials=True)

# # Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# # Initialize the Cohere Client with an API Key
# api = os.getenv("COHERE_API_KEY")
# co = cohere.Client(api)

# # @app.route('/')
# # def index():
# #     return render_template('index.html')

# @app.route('/get_response', methods=['POST'])
# def get_response():
#     try:
#         course = request.get_json().get('course')
#         target = request.get_json().get('target')
#         duration = request.get_json().get('duration')
#         submodule = request.get_json().get('submodule')
        
#         # Generate a prediction for the prompt
#         prediction = co.chat(message=f'''
#             You are a {course} course expert in teaching it to {target} which has a duration of {duration}.
#             Can you create a content for the topic : {submodule} with detailed example.
#             Give the output in json format:
#             {{
#                 "submodule_title": "string",
#                 "submodule_content": "string",
#                 "examples": [string],
#             }}
#         ''', model='command', connectors=[{"id": "web-search", "name": "Web Search", "created_at": "0001-01-01T00:00:00Z", "updated_at": "0001-01-01T00:00:00Z", "continue_on_failure": True}])

#         # print(prediction.text)


#         # Return the predicted text in JSON format
#         return prediction.text[7:-3]

#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, request, jsonify
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_COHERE_API_KEY' with your Cohere API key

# Initialize the Cohere Client with an API Key
api = os.getenv("GEMINI_API_KEY")
api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + api

# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/', methods=['POST'])
def get_response():
    try:
        course = request.get_json().get('course')
        target = request.get_json().get('target')
        duration = request.get_json().get('duration')
        module = request.get_json().get('module')
        submodules = request.get_json().get('submodulename')
        
        # submodules = " , ".join(submodules)
            # Define the request payload
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": 
                            f'''
        You are a {course} course expert in teaching it to {target} which has a duration of {duration}.
            Can you create a content of 400 words for {submodules} which belongs to module : {module} with examples if needed.
            Give the output in strictly in json format only:
            {{
                "submodule_title": "string",
                "submodule_content": "string"
            }}
        '''
                        }
                    ]
                }
            ]
        }

        # Set the headers
        headers = {
            "Content-Type": "application/json"
        }

        # Make the API call
        response = requests.post(api_url, json=payload, headers=headers)

        if response.status_code == 200:
            # Parse and print the response JSON
            response_json = response.json()
            if (response_json["candidates"][0]["content"]["parts"][0]["text"][0]=="{"):
                return (response_json["candidates"][0]["content"]["parts"][0]["text"])
            else:
                if response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="J" or response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3][0]=="j":
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
                else:
                    return (response_json["candidates"][0]["content"]["parts"][0]["text"][3:-3])
            # print(response_json["candidates"][0]["content"]["parts"][0]["text"])
            # if (response_json["candidates"][0]["content"]["parts"][0]["text"][0] == "`"):
            #     return (response_json["candidates"][0]["content"]["parts"][0]["text"][7:-3])
            # # print(json.dumps(response_json, indent=2))
            # # print(response_json)
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return json.dump(
            {
                "msg":"Error Assessing AI"
            }
            ) 

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)

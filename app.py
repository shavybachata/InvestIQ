from flask import Flask, request, jsonify
import requests
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set your OpenAI API key
OPENAI_API_KEY = "Enter your api  key"  # Replace with your actual key

# MongoDB Connection
try:
    mongo_client = MongoClient("EnterYourURL")
    db = mongo_client['my_database']  # Replace with your database name
    collection = db['people']  # Replace with your collection name
    print("Successfully connected to MongoDB.")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")

def get_openai_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Replace with the model you are using
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt},
        ]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code}, {response.text}"

@app.route('/api/get_response', methods=['POST'])
def get_response():
    if request.content_type != 'application/json':
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    try:
        data = request.json
        age = data.get('age')
        gender = data.get('gender')
        income = data.get('income')
        savings = data.get('savings')

        # Generate prompts for all types
        prompts = {
            'stocks': f"Age: {age}, Gender: {gender}, Income: {income}, Savings: {savings}. Give 5 stock options according to my profile in 40 words. and highlight risk factor",
            'crypto': f"Age: {age}, Gender: {gender}, Income: {income}, Savings: {savings}. Give 5 cryptocurrency options famous in india youth according to my profile in 40 words.and highlight risk factor",
            'property': f"Age: {age}, Gender: {gender}, Income: {income}, Savings: {savings}. Give 5 property options for investment and make money according to my profile in 40 words.and highlight risk factor",
            'policy': f"Age: {age}, Gender: {gender}, Income: {income}, Savings: {savings}. Provide relevant names of government policies of indain government according to my profile in 40 words.and highlight risk factor"
        }

        # Fetch responses for all prompts
        responses = {}
        for key, prompt in prompts.items():
            response_text = get_openai_response(prompt)
            responses[key] = response_text

            # Save to MongoDB
            collection.insert_one({
                "age": age,
                "gender": gender,
                "income": income,
                "savings": savings,
                "type": key,
                "response": response_text
            })

        return jsonify(responses)
    except Exception as e:
        return jsonify({'error': 'Invalid JSON'}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5001)

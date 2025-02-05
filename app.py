from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_URL = 'http://127.0.0.1:8000'
MAX_LIMIT_OF_CHARACTERS = 2000

@app.route('/')
def home():
  return render_template('index.html')

@app.route('/writing')
def writting():
  return render_template('writing.html')

@app.route('/api/writing', methods=['POST'])
def revise_letter():
  """ 
  do a petition to the API
  """
  data = request.json
  letter = data['letter']
  
  # do a petition to the API
  feedback = requests.post(f'{API_URL}/writing', json={'letter': letter})
  
  return feedback.json()

@app.route('/remembering')
def remembering():
  return render_template('remembering.html')

@app.route('/api/generate-vocabulary', methods=['POST'])
def generate_vocabulary():
  """ 
  do a petition to the API
  """
  data = request.json
  topic = data['topic']
  description = data['description']
  
  # do a petition to the API
  feedback = requests.post(f'{API_URL}/generate-vocabulary', json={'topic': topic, 'description': description})
  
  return feedback.json()


@app.route('/speaking')
def speaking():
  return render_template('conversation.html')

@app.route('/api/speaking', methods=['POST'])
def respond_conversation():
  """ 
  do a petition to the API
  """
  data = request.json
  conversation = data['conversation'][-MAX_LIMIT_OF_CHARACTERS:]
  context = data['context']
  
  # do a petition to the API
  next_message = requests.post(f'{API_URL}/speaking', json={'conversation': conversation, 'context': context})
  
  return next_message.json()

@app.route('/questions')
def questions():
  return render_template('questions.html')

@app.route('/api/questions', methods=['POST'])
def answer_questions():
  """ 
  do a petition to the API
  """
  data = request.json
  topic = data['topic']
  
  # do a petition to the API
  answers = requests.post(f'{API_URL}/questions', json={'topic': topic})
  
  return answers.json()

if __name__ == '__main__':
  app.run(debug=True)
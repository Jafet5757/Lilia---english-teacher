import openai
import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path="../.env")

class ChatController:
  def __init__(self, model: str = "gpt-4o-mini"):
    self.client = openai.OpenAI(
      api_key = os.getenv("OPENAI_API_KEY")
    )
    self.model = model
    
  def send_message(self, messages: list):
    """ 
    Send a message to the llm
    
    arguments:
    messages: list of dict (role, content)
    
    return: str content
    """
    completion = self.client.chat.completions.create(
      model=self.model,
      messages=messages
    )
    
    return completion
  
  def get_calification_from_text(self, text: str):
    """ 
    Get the calification from the text
    
    arguments:
    text: str
    
    return: str content
    """
    messages = [
      {"role": "system", "content": "Eres un experto en el idioma inglés, revisa este texto que acabo de escribir y basado en tu expertiz calificalo de A1 a C2"},
      {"role": "user", "content": "Responde solo con la calificación, no agregues comentarios, por ejemplo: 'B2'"},
      {"role": "user", "content": text}
    ]
    
    return self.send_message(messages).choices[0].message.content
  
  def respond_conversation(self, conversation: str, context: str = "Eres un experto en el idioma inglés, y un buen profesor"):
    """ 
    Respond a conversation
    
    arguments:
    conversation: str with the conversation (role, content)
    
    return: str next message
    """
    messages = [
      {"role": "system", "content": "Responde con un mensaje que continue la conversación, se amable y ayúda a la otra persona a seguir aprendiendo el idioma dando recomendaciones y retroalimentación cuando sea necesario"},
      {"role": "system", "content": f"Contexto en el que se da la conversación: {context}"},
      {"role": "system", "content": '''Responde con un mensaje en formato json, por ejemplo: {"message": "Hello, how are you?", "recommendation": "You can use the word 'good' to answer the question 'how are you?'"}'''},
      {"role": "user", "content": "Ayúdame a tener una conversación en inglés como si fuera un nativo, estoy aprendiendo el idioma"},
      {"role": "user", "content": conversation}
    ]

    return self.send_message(messages).choices[0].message.content

class WriteLetter(ChatController):
  """ 
  Revise a letter using the llm, help with the grammar and recommendations
  """
  def __init__(self, model: str = "gpt-4o-mini"):
    super().__init__(model)
    
  def get_feedback(self, letter: str):
    """ 
    Get feedback from the llm
    
    arguments:
    letter: str
    
    return: str content
    """
    messages = [
      {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
      {"role": "user", "content": "Dame una retroalimentación de mi carta, ayúdame con la gramatica y recomendaciones, señalame las areas en las que puedo mejorar y nuevo vocabulario en caso de ser necesario"},
      {"role": "user", "content": letter}
    ]
    
    return self.send_message(messages).choices[0].message.content
  
  def get_vocabulary(self, topic: str, description: str):
    """ 
    Generate vocabulary for a topic
    
    arguments:
    topic: str content
    description: str content
    
    return: list of str
    """
    messages = [
      {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
      {"role": "user", "content": '''Básado en un tema y descripción dame un listado de 10 palabras nuevas para aprender en inglés con su traducción y un ejemplo de uso, responde con el siguiente formato json de ejemplo, no agregués más texto para poder parsearlo: [{"word": "long","translation": "Grande","sentence": "The long table","score": 0},{"word": "little","translation": "Pequeño","sentence": "The little horse","score": 0}]'''},
      {"role": "user", "content": f"Tema: {topic}, Descripción: {description}"}
    ]
    
    return self.send_message(messages).choices[0].message.content
  
class Form(ChatController):
  """ 
  Create questions about a topic 
  """
  def __init__(self, topic:str, model:str = "gpt-4o-mini"):
    self.topic = topic
    super().__init__(model)
    
  def get_questions(self):
    """ 
    Get questions from the llm
    
    return: list of str
    """
    messages = [
      {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
      {"role": "user", "content": '''Básado en un tema dame un listado de 10 preguntas en inglés para hacer un examen de conocimiento sobre el tema, responde con el siguiente formato json de ejemplo, no agregués más texto para poder parsearlo: 
        {
          "topic": "History of Art",
          "questions": [
            {
              "id": "q1",
              "type": "open",
              "statement": "Explain the importance of the Renaissance in the evolution of European art.",
              "options": null,
              "correctAnswer": null,
              "metadata": {
                "suggestion": "Mention figures like Leonardo da Vinci and Michelangelo."
              }
            },
            {
              "id": "q2",
              "type": "multiple_choice",
              "statement": "Which of the following works is attributed to Leonardo da Vinci?",
              "options": [
                { "id": "a", "text": "Mona Lisa" },
                { "id": "b", "text": "Guernica" },
                { "id": "c", "text": "The Starry Night" }
              ],
              "correctAnswer": "a",
              "metadata": null
            },
            {
              "id": "q3",
              "type": "checkboxes",
              "statement": "Select the artistic movements that emerged in the 20th century:",
              "options": [
                { "id": "a", "text": "Cubism" },
                { "id": "b", "text": "Impressionism" },
                { "id": "c", "text": "Surrealism" },
                { "id": "d", "text": "Baroque" }
              ],
              "correctAnswer": ["a", "c"],
              "metadata": null
            }
          ],
          "metadata": {
            "totalQuestionsGenerated": 3,
            "estimatedTime": "3 minutes"
          }
        }
       '''},
      {"role": "user", "content": f"Tema: {self.topic}"}
    ]
    
    return self.send_message(messages).choices[0].message.content

# Testing
if __name__ == "__main__":
  letter = "Hi, my name is Jafet, I live in Mexico city near of a big supermarket opposite a park, I'm software developer and I very interesting in learn English because I want to work in a big company in the United States"
  write_letter = WriteLetter()
  print(write_letter.get_feedback(letter))
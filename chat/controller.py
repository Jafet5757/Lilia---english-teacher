import os
from dotenv import load_dotenv
import openai

# Si se usa ollama, se importa su función chat
try:
    from ollama import chat
except ImportError:
    chat = None

# Cargar el archivo .env
load_dotenv(dotenv_path="../.env")

class ChatController:
    def __init__(self, model: str = "gpt-4o-mini", source: str = "openai"):
        """
        Inicializa el controlador de chat.
        
        Parámetros:
          - model: nombre del modelo a utilizar.
          - source: fuente de LLM, "openai" o "ollama".
        """
        self.model = model
        self.source = source.lower()
        
        if self.source == "openai":
            self.client = openai.OpenAI(
                api_key=os.getenv("OPENAI_API_KEY")
            )
        elif self.source == "ollama":
            if chat is None:
                raise ImportError("El paquete 'ollama' no está instalado.")
        else:
            raise ValueError("Fuente no soportada. Use 'openai' o 'ollama'.")

    def send_message(self, messages: list) -> str:
        """
        Envía un mensaje al LLM y retorna el contenido de la respuesta.

        Parámetros:
          - messages: lista de diccionarios con la estructura {"role": ..., "content": ...}

        Retorna:
          - str con el contenido de la respuesta.
        """
        if self.source == "openai":
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return completion.choices[0].message.content
        elif self.source == "ollama":
            response = chat(model=self.model, messages=messages)
            return response['message']['content']

    def get_calification_from_text(self, text: str) -> str:
        """
        Califica un texto de acuerdo a un nivel de inglés (A1 a C2).

        Parámetros:
          - text: cadena con el texto a calificar.

        Retorna:
          - str con la calificación.
        """
        messages = [
            {"role": "system", "content": "Eres un experto en el idioma inglés, revisa este texto que acabo de escribir y basado en tu expertiz califícalo de A1 a C2"},
            {"role": "user", "content": "Responde solo con la calificación, no agregues comentarios, por ejemplo: 'B2'"},
            {"role": "user", "content": text}
        ]
        return self.send_message(messages)

    def respond_conversation(self, conversation: str, context: str = "Eres un experto en el idioma inglés, y un buen profesor") -> str:
        """
        Responde a una conversación continuándola y ofreciendo recomendaciones.

        Parámetros:
          - conversation: cadena con la conversación.
          - context: contexto adicional de la conversación.

        Retorna:
          - str con el mensaje de respuesta.
        """
        messages = [
            {"role": "system", "content": "Responde con un mensaje que continúe la conversación, sé amable y ayuda a la otra persona a seguir aprendiendo el idioma dando recomendaciones y retroalimentación cuando sea necesario"},
            {"role": "system", "content": f"Contexto en el que se da la conversación: {context}"},
            {"role": "system", "content": '''Responde con un mensaje en formato json, por ejemplo: {"message": "Hello, how are you?", "recommendation": "You can use the word 'good' to answer the question 'how are you?'" }'''}, 
            {"role": "user", "content": "Ayúdame a tener una conversación en inglés como si fuera un nativo, estoy aprendiendo el idioma"},
            {"role": "user", "content": conversation}
        ]
        return self.send_message(messages)

class WriteLetter(ChatController):
    """
    Revisa una carta utilizando el LLM, ofreciendo feedback sobre gramática y recomendaciones.
    """
    def __init__(self, model: str = "gpt-4o-mini", source: str = "openai"):
        super().__init__(model, source)
        
    def get_feedback(self, letter: str) -> str:
        """
        Obtiene retroalimentación de la carta.

        Parámetros:
          - letter: cadena con el contenido de la carta.

        Retorna:
          - str con el feedback.
        """
        messages = [
            {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
            {"role": "user", "content": "Dame una retroalimentación de mi carta, ayúdame con la gramática y recomendaciones, señálame las áreas en las que puedo mejorar y nuevo vocabulario en caso de ser necesario"},
            {"role": "user", "content": letter}
        ]
        return self.send_message(messages)
    
    def get_vocabulary(self, topic: str, description: str) -> str:
        """
        Genera vocabulario relacionado a un tema y descripción.

        Parámetros:
          - topic: tema a tratar.
          - description: descripción del contexto.

        Retorna:
          - str con un listado en formato json.
        """
        messages = [
            {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
            {"role": "user", "content": '''Básado en un tema y descripción dame un listado de 10 palabras nuevas para aprender en inglés con su traducción y un ejemplo de uso, responde con el siguiente formato json de ejemplo, no agregues más texto para poder parsearlo: [{"word": "long","translation": "Grande","sentence": "The long table","score": 0},{"word": "little","translation": "Pequeño","sentence": "The little horse","score": 0}]'''},
            {"role": "user", "content": f"Tema: {topic}, Descripción: {description}"}
        ]
        return self.send_message(messages)
    
class Form(ChatController):
    """
    Genera preguntas sobre un tema utilizando el LLM.
    """
    def __init__(self, topic: str, model: str = "gpt-4o-mini", source: str = "openai"):
        self.topic = topic
        super().__init__(model, source)
        
    def get_questions(self) -> str:
        """
        Obtiene un listado de preguntas en inglés para un examen sobre el tema.

        Retorna:
          - str con el listado en formato json.
        """
        messages = [
            {"role": "system", "content": "Eres un experto en el idioma inglés, y un buen profesor"},
            {"role": "user", "content": '''Básado en un tema dame un listado de 10 preguntas en inglés para hacer un examen de conocimiento sobre el tema, responde con el siguiente formato json de ejemplo, no agregues más texto para poder parsearlo: 
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
}'''}, 
            {"role": "user", "content": f"Tema: {self.topic}"}
        ]
        return self.send_message(messages)

# Ejemplo de uso
if __name__ == "__main__":
    letter = ("Hi, my name is Jafet, I live in Mexico City near a big supermarket opposite a park, "
              "I'm a software developer and I'm very interested in learning English because I want to work in a big company in the United States.")
    
    # Instancia utilizando OpenAI
    write_letter_openai = WriteLetter(source="openai")
    print("Feedback (OpenAI):", write_letter_openai.get_feedback(letter))
    
    # Instancia utilizando Ollama
    write_letter_ollama = WriteLetter(model="llama3.1", source="ollama")
    print("Feedback (Ollama):", write_letter_ollama.get_feedback(letter))

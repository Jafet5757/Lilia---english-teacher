from fastapi import FastAPI, Body
from chat.controller import WriteLetter, Form

# Variables globales para configurar el modelo y la fuente (openai o ollama)
GLOBAL_MODEL = "llama3.1"    # gpt-4o-mini | llama3.1
GLOBAL_SOURCE = "ollama"        # openai | ollama

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
  
@app.post("/writing")
def revise_letter(letter: str = Body(..., embed=True)):
    """
    Revisa una carta utilizando el LLM, ofreciendo retroalimentación sobre gramática y recomendaciones.

    Argumentos:
      - letter: str con el contenido de la carta

    Retorna:
      - dict con 'feedback' y 'level'
    """
    write_letter = WriteLetter(model=GLOBAL_MODEL, source=GLOBAL_SOURCE)
    feedback = write_letter.get_feedback(letter)
    level = write_letter.get_calification_from_text(letter)
    return {"feedback": feedback, "level": level}

@app.post("/generate-vocabulary")
def generate_vocabulary(topic: str = Body(..., embed=True), description: str = Body(..., embed=True)):
    """
    Genera vocabulario para un tema específico.

    Argumentos:
      - topic: str con el tema
      - description: str con la descripción del contexto

    Retorna:
      - dict con 'vocabulary'
    """
    write_letter = WriteLetter(model=GLOBAL_MODEL, source=GLOBAL_SOURCE)
    vocabulary = write_letter.get_vocabulary(topic, description)
    return {"vocabulary": vocabulary}

@app.post("/speaking")
def respond_conversation(conversation: str = Body(..., embed=True), context: str = Body(..., embed=True)):
    """
    Responde a una conversación y ofrece retroalimentación y recomendaciones.

    Argumentos:
      - conversation: str con la conversación
      - context: str con el contexto (se usa un valor por defecto si está vacío)

    Retorna:
      - dict con 'next_message'
    """
    write_letter = WriteLetter(model=GLOBAL_MODEL, source=GLOBAL_SOURCE)
    # Si no se proporciona contexto se asigna un valor por defecto
    context = context if context and context.strip() != "" else "Eres un experto en el idioma inglés, y un buen profesor"
    next_message = write_letter.respond_conversation(conversation, context)
    return {"next_message": next_message}

@app.post("/questions")
def answer_questions(topic: str = Body(..., embed=True)):
    """
    Genera preguntas sobre un tema específico utilizando el LLM.

    Argumentos:
      - topic: str con el tema

    Retorna:
      - dict con 'form' que contiene las preguntas generadas
    """
    form = Form(topic, model=GLOBAL_MODEL, source=GLOBAL_SOURCE)
    questions = form.get_questions()
    return {"form": questions}

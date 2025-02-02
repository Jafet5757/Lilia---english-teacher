from fastapi import FastAPI, Body
from pydantic import BaseModel
from chat.controller import WriteLetter

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
  
@app.post("/writing")
def revise_letter(letter: str = Body(..., embed=True)):
  """ 
  Revise a letter using the llm, help with the grammar and recommendations
  
  arguments:
  letter: str content
  
  return: dict feedback: str
  """
  write_letter = WriteLetter()
  feedback = write_letter.get_feedback(letter)
  level = write_letter.get_calification_from_text(letter)
  return {"feedback": feedback, "level": level}

@app.post("/generate-vocabulary")
def generate_vocabulary(topic: str = Body(..., embed=True), description: str = Body(..., embed=True)):
  """ 
  Generate vocabulary for a topic
  
  arguments:
  topic: str content
  description: str content
  
  return: dict vocabulary: list
  """
  write_letter = WriteLetter()
  vocabulary = write_letter.get_vocabulary(topic, description)
  return {"vocabulary": vocabulary}

@app.post("/speaking")
def respond_conversation(conversation: str = Body(..., embed=True), context: str = Body(..., embed=True)):
  """ 
  Respond a conversation
  
  arguments:
  conversation: str content
  
  return: dict next_message: str
  """
  write_letter = WriteLetter()
  next_message = write_letter.respond_conversation(conversation, context)
  return {"next_message": next_message}
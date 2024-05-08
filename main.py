import requests
import time
import re
import sys

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
@app.get("/")
def root():
    return {"message": "Hello World"}

#Enabling CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    message: str

async def returnmessage(message):
    def read_context_from_file(file_path): # function to read the context from a file
        with open(file_path, "r") as file:
            print("file loaded: ", file_path)
            return file.read()
    def interact_with_chatbot(context, question): # interact with chatbot
        endpoint = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2" # define the model endpoint
        headers = {"Authorization": "Bearer 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"}
        data = {
            "inputs": {
                "question": question,
                "context": context
            }
        }

        start_time = time.time()
        response = requests.post(endpoint, headers=headers, json=data)
        end_time = time.time()

        if response.status_code == 200:
            result = response.json()
            answer = result["answer"]
            score = result["score"]
            computation_time = end_time - start_time
            return answer, score, computation_time
        else:
            return "Error: Failed to get response from the chatbot.", None, None
    
    question = message
    questionwords = []
    answer = question
    for x in answer.split():
        questionwords.append(x.upper())
    with open("Scraper Text/bannedwords.txt") as bannedwords:
        for s in bannedwords:
            for i in questionwords:
                print(s.strip("\n"))
                while s.strip("\n") in questionwords:
                    questionwords.remove(s.strip("\n"))

    print(questionwords)      
    patterns = [r'\b%s\b' % re.escape(s.strip()) for s in questionwords]
    tobesearched = re.compile('|'.join(patterns))

    with open("Scraper Text/bigmergedfile.txt") as f:
        relevantinfofile = open("relevantinfo.txt","w")
        for i, s in enumerate(f):
            if tobesearched.search(s):
                print((s))
                relevantinfofile.write(s)

    file_path = "relevantinfo.txt"

    context = read_context_from_file(file_path)
    

    answer, score, computation_time = interact_with_chatbot(context,question)
    print("Chatbot Answer: ", answer)
    print("Score: ", score)
    print("Computation time(seconds): ", computation_time)
    return(answer)

@app.post("/message")
async def process_message(message_data: Message):
    print(message_data.message)
    response = await returnmessage(message_data.message)
    return {response}

import requests
import time
import os 

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

file_to_load = {
    "chemistry" : "chmchmub.txt",
    "chancellor" : "abouttheuniversity.txt",
    "postgraduate":"virtualpgopenday.txt",
    "zoology":"zoozoorp.txt",
    "business":"busprpub.txt",
    "computing":"cmpcmsub.txt"

}

folder_path = input("enter the folder path containing the context: ")

while True:
    question = input("enter the question (or enter 'q' to quit): ")
    if question.lower() == "q":
        break

    found = False
    for word in question.split():
        if word.lower() in file_to_load:
            file_path = os.path.join(folder_path,file_to_load[word.lower()])
            context = read_context_from_file(file_path)
            answer, score, computation_time = interact_with_chatbot(context,question) 
            print("answer: ", answer)
            print("score: ", score)
            print("computation time (Seconds)", computation_time)
            found = True
            break
        if not found:
            print("Question not found")

   
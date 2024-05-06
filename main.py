import requests
import time

def read_context_from_file(file_path): # function to read the context from a file
    with open(file_path, "r") as file:
        print("file loaded: ", file_path)
        return file.read()
def interact_with_chatbot(context, question): # interact with chatbot
    endpoint = "https://api-inference.huggingface.co/models/google-bert/bert-large-uncased-whole-word-masking-finetuned-squad" # define the model endpoint
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

file_path = input("enter the file path containing the context: ")

context = read_context_from_file(file_path)
question = input("enter the question:")

answer, score, computation_time = interact_with_chatbot(context,question)
print("Chatbot Answer: ", answer)
print("Score: ", score)
print("Computation time(seconds): ", computation_time)
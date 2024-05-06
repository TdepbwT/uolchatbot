import requests
import time


def interact_with_chatbot(context, question):
    endpoint = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
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

context = "The University of Lincoln is a public research university in Lincoln, England, with origins dating back to 1861. It gained university status in 1992 and its present name in 2001. The main campus is in the heart of the city of Lincoln alongside the Brayford Pool. There are satellite campuses across Lincolnshire in Riseholme and Holbeach and graduation ceremonies take place in Lincoln Cathedral."

question = input("enter the question:")

answer, score, computation_time = interact_with_chatbot(context,question)
print("Chatbot Answer: ", answer)
print("Score: ", score)
print("Computation time(seconds): ", computation_time)
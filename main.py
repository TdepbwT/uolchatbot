import requests
import time
import re
import sys
import os 

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

context = ""
contextName = ""

#All the files to load
file_to_load = {
    'creative advertising': 'aadaadub.txt',
    'accountancy and finance': 'accfinub.txt',
    'msc social work advanced professional practice ': 'adppswms.txt',
    'marketing and advertising': 'advmktub.txt',
    'university of lincoln arts foundation year': 'afyafyub.txt',
    'animal behaviour and welfare': 'eqsabwub.txt',
    'animation and visual effects': 'anianiub.txt',
    'architecture': 'arcarcub.txt',
    'bachelor of architecture with honours': 'arcboaub.txt',
    'fine art': 'artartub.txt',
    'banking and finance': 'banfinub.txt',
    'basis certificate in sustainable land management': 'bascesnc.txt',
    'basis quality of soils': 'basqusnc.txt',
    'basis soil and water management': 'basswmnc.txt',
    'brcgs lead auditor': 'beclaunc.txt',
    'biodiversity, conservation and nature recovery': 'biconrms.txt',
    'biology': 'bioresms.txt',
    'clinical animal behaviour': 'biocabms.txt',
    'biochemistry and molecular biology': 'biochmrp.txt',
    'biochemistry': 'biochmub.txt',
    'biomedical science': 'bmsbmsub.txt',
    'biotechnology': 'biotecms.txt',
    'biomedical engineering': 'bmdegrub.txt',
    'brcgs internal auditing': 'brcintnc.txt',
    'best interests assessor': 'btinaspi.txt',
    'international year 1 business and management': 'bumgicuc.txt',
    'doctorate of business administration': 'busadmtd.txt',
    'business with entrepreneurship': 'busdevub.txt',
    'business economics': 'busecoub.txt',
    'business and finance': 'busfinub.txt',
    "pre-master's business": 'busgicuz.txt',
    'international business management': 'busibmub.txt',
    'international business': 'busintms.txt',
    'business management': 'busmdlub.txt',
    'business': 'busprpub.txt',
    'bioveterinary science': 'bvsresms.txt',
    'games computing': 'cgpcmpub.txt',
    'games computing with virtual and augmented reality': 'cgpvarub.txt',
    'chemistry': 'chmchmub.txt',
    'chemistry for drug discovery and development': 'chmdrgub.txt',
    'chemistry with education': 'chmeduub.txt',
    'forensic chemistry': 'chmfrsub.txt',
    'chemistry with mathematics': 'chmmthub.txt',
    'chemistry for net zero': 'chmntzub.txt',
    'photography': 'clmclmub.txt',
    'classical studies': 'clscvlub.txt',
    'computer science with artificial intelligence': 'cmpcaiub.txt',
    'computer science': 'cmpcmsub.txt',
    'computing by research': 'cmsresms.txt',
    'conservation of cultural heritage': 'conconub.txt',
    'criminology': 'cricriub.txt',
    'criminology and sociology': 'crisolub.txt',
    'criminology and social policy': 'crisopub.txt',
    'creative writing': 'crwcrwub.txt',
    'dance': 'dandanub.txt',
    'maritime and defence studies': 'defssbub.txt',
    'drama, theatre and performance': 'dradraub.txt',
    'ecology and conservation': 'eclcsvub.txt',
    'economics': 'ecoecoub.txt',
    'economics and finance': 'ecofinub.txt',
    'equality, diversity and inclusion literacy: the abc of edi': 'edilitpx.txt',
    'education and psychology': 'edmpsyub.txt',
    'education': 'edueduub.txt',
    'mechatronics': 'egrbcnub.txt',
    'mechanical engineering': 'egregrub.txt',
    'electrical and electronic engineering': 'egrelcub.txt',
    'general engineering': 'egrgenub.txt',
    'engineering management': 'engmdlub.txt',
    'english and creative writing': 'enlcrwub.txt',
    'drama and english': 'enldraub.txt',
    'english': 'enlenlub.txt',
    'english and history': 'enlhstub.txt',
    'energy materials and battery science': 'eymtbsms.txt',
    'food engineering': 'fdsengub.txt',
    'food and drink operations management': 'fdsfdoub.txt',
    'food and drink science and technology': 'fdsfdtub.txt',
    'forensic science': 'frsfrsub.txt',
    'forensic toxicology': 'frstxcub.txt',
    'film and television studies': 'ftvftvub.txt',
    'geography': 'gepgepub.txt',
    'graphic design': 'gragraub.txt',
    'health and social care': 'heaheaub.txt',
    'human resource management (open)': 'hrmhptub.txt',
    'history': 'hsthstub.txt',
    'illustration': 'illillub.txt',
    'interior architecture and design': 'intintub.txt',
    'international tourism management': 'inttouub.txt',
    'international relations': 'ististub.txt',
    'international relations and politics': 'istpolub.txt',
    'journalism studies': 'jouinvub.txt',
    'journalism': 'joujouub.txt',
    'law and criminology': 'lawcriub.txt',
    'law': 'lawlawub.txt',
    'logistics management (open)': 'logldlub.txt',
    'media studies': 'mdsmdsub.txt',
    'sound and music production': 'medaupub.txt',
    'media production': 'medmedub.txt',
    'film production': 'medproub.txt',
    'business and management': 'mgtprpub.txt',
    'midwifery': 'midmidub.txt',
    'brand management': 'mktbrmpx.txt',
    'business and marketing': 'mktprpub.txt',
    'modern history': 'modhstub.txt',
    'mathematics and computer science': 'mthcmpub.txt',
    'mathematics': 'mthmthub.txt',
    'mathematics with philosophy': 'mthphlub.txt',
    'mathematics and theoretical physics': 'mthphyub.txt',
    'music': 'musmusub.txt',
    'professional music studies': 'musssbub.txt',
    'musical theatre': 'mustheub.txt',
    'nursing (registered nurse - child)': 'nurcldub.txt',
    'nursing (registered nurse - mental health)': 'nurmnhub.txt',
    'nursing (registered nurse - adult)': 'nurnurub.txt',
    'paramedic science': 'nurparub.txt',
    'professional practice': 'nurppcub.txt',
    'pharmaceutical science with business management': 'phabusum.txt',
    'pharmaceutical science': 'phaphaub.txt',
    'philosophy': 'phlphlub.txt',
    'physics with astrophysics': 'phyaphub.txt',
    'physics with philosophy': 'phyphlub.txt',
    'physics': 'phyphyub.txt',
    'politics': 'polpolub.txt',
    'product design': 'prdprdub.txt',
    'psychology with mental health': 'psycpyub.txt',
    'psychology with forensic psychology': 'psyfsyub.txt',
    'psychology': 'psypsyub.txt',
    'psychology (sport and exercise psychology)': 'psysesub.txt',
    'diagnostic radiography': 'raddgcub.txt',
    'robotics': 'robrobub.txt',
    'international sports business management': 'sbmintms.txt',
    'sports business management': 'sbmsbmub.txt',
    'sport development and coaching': 'sdcsdcub.txt',
    'physical education and sport': 'sespesub.txt',
    'strength and conditioning in sport': 'sesscsub.txt',
    'sport and exercise science': 'sessesub.txt',
    'sport and exercise therapy': 'sessthub.txt',
    'university of lincoln science foundation year': 'sfysfyub.txt',
    'sociology': 'solsolub.txt',
    'social policy': 'sopsopub.txt',
    'social work practice': 'sowpraub.txt',
    'sports journalism': 'sptjouub.txt',
    'technical theatre and stage management': 'tectheub.txt',
    'events management': 'touemnub.txt',
    'zoology': 'zoozooub.txt'
}


async def returnmessage(message):
    def interact_with_chatbot(context, question): # interact with chatbot
        endpoint = "https://api-inference.huggingface.co/models/mrm8488/longformer-base-4096-finetuned-squadv2" # define the model endpoint
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


    answer, score, computation_time = interact_with_chatbot(context,question)
    print("Chatbot Answer: ", answer)
    print("Score: ", score)
    print("Computation time(seconds): ", computation_time)
    return(answer)

async def returncoursemessage(message):

    question = message
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

def read_context_from_file(file_path): # function to read the context from a file
    with open(file_path, "r") as file:
        print("file loaded: ", file_path)
        return file.read()

def findContextFile(contextString):
    global context
    global contextName
    for phrase, file_path in file_to_load.items():
        if contextString.lower() in phrase.lower().split():
            print(phrase)
            file_path = os.path.join("0805Cleaned", file_path)

            context = read_context_from_file(file_path)
            contextName = context.split("|")[0].strip()
            # print(context)
            # print(contextName)

@app.post("/message")
async def process_message(message_data: Message):
    print(message_data.message)
    response = await returnmessage(message_data.message)
    return {response}

@app.post("/context")
async def process_message(message_data: Message):
    print("finding context" + message_data.message)
    findContextFile(message_data.message)
    print(contextName)
    return {contextName}

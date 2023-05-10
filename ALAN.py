import openai
import time
import re
import os
import glob
from spinner import Spinner
from logic import *
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
load_dotenv()




openai.api_key = os.environ.get('OPENAI_API_KEY')
model_id = 'gpt-3.5-turbo'




def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    # api_usage = response['usage']
    # print('Total token consumed: {0}'.format(api_usage['total_tokens']))
    # stop means complete
    # print(response['choices'][0].finish_reason)
    # print(response['choices'][0].index)
    conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    return conversation




def checker(prompt, condition):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"{condition}. The Prompt: {prompt}",
    temperature=0,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text'].strip()




conversation = []
conversation.append({'role': 'system', 'content': 'Act as a Bioinformatics research assistant named ALAN (Amino acid Linkage and Analysis Navigator). Only introduce yourself and say that you will help with protein structure prediction and other bioinformatics problems.'})
conversation.append({'role': 'system', 'content': 'You have the ability to run BLAST searches. If the user ask for blast search, converse with them normally but make sure to ask for the sequence they want to search'})
conversation.append({'role': 'system', 'content': 'You have the ability to do protein structure prediction. If the user asks for protein structure prediction, converse with them normally but make sure to ask for the amino acid sequence they want a prediction of. Also ignore the length of amino acid sequences provided'})
conversation.append({'role':'system', 'content': 'If you are asked to open up tools or webpages, you should always make a selenium script in python to do so. You will use chrome by default for all selenium scripts. You must make sure the experimental option \'detach\' is True so that the browser stays open'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))




def check(text):
    # newconvo.append({'role': 'system', 'content': 'Check if this prompt is asking for BLAST Search AND has a nucleotide sequence, you will answer only \'Yes\' or \'No\'. The Prompt: {}'.format(prompt)})
    response = checker(text, 'Check what the prompt is asking for, if it is asking for Protein structure prediction, write \'PROTEIN\', and if it asking for BLAST search, write \'BLAST\'. If the prompt doesn\'t ask for anything write anything except PROTEIN and BLAST')
    return response
    


def structurepredictioncheck(text):
    # newconvo.append({'role': 'system', 'content': 'Check if this prompt is asking for BLAST Search AND has a nucleotide sequence, you will answer only \'Yes\' or \'No\'. The Prompt: {}'.format(prompt)})
    response = checker(text, 'Check if this prompt is explicitly asking for protein structure prediction AND has a amino acid sequence. Reply \'Yes\' if both of these conditions are met')
    if response == 'Yes' or response == 'Yes.':
        return True
    else:
        return False




def extract_code(text):
    pattern = r"```(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)
    if len(matches) == 0:
        # print('CONSOLE: No matches found') 
        return False
    else: 
        # print('CONSOLE: Match found')
        cnt = 0
        for text in matches: 
            with open(f'code{cnt}.py', 'w') as output_file:
                bro = text.replace('python', '')
                output_file.write(bro)
            cnt += 1
        return True




def BLAST(query):
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    prefs = {"download.default_directory" : "/Users/acedrakon/Desktop/Python/ALAN/ALAN/BLAST"}
    chrome_options.add_experimental_option("prefs",prefs)


    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi')

    driver.find_element(By.ID, 'homeBlastn').click()
    driver.find_element(By.ID, 'seq').send_keys(query)
    driver.find_element(By.ID, 'blastButton1').click()

    wait = WebDriverWait(driver, 30)
    try: 
        download = wait.until(expected_conditions.visibility_of_element_located((By.ID, 'btnDwnld')))
        download.click()
        driver.find_element(By.ID, 'dwText').click()
    except: 
        print('You sequence gotta be wrong or sumn')

def protein(seq):
    chrome_options = Options()
    chrome_options.add_experimental_option('detach', True)
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://esmatlas.com/resources?action=fold')
    element = driver.find_element(By.ID, 'search-input')
    element.send_keys(seq)
    element.send_keys(Keys.ENTER)



def extractNT_SEQ(prompt):
    conversation = []
    conversation.append({'role': 'system', 'content': f'Look through this text and write back only the nucleotide sequence and nothing else, if there is no nucleotide sequence write \'ASKING\' only. The prompt: {prompt}'})
    conversation = ChatGPT_conversation(conversation)
    response = conversation[-1]['content'].strip()
    if re.search('ASKING', response):
        e = input(Fore.BLUE + 'Write Nucleotide Sequence: ')
        return e
    else:  
        return response


def extractAA__SEQ(prompt):
    conversation = []
    conversation.append({'role': 'system', 'content': f'Look through this text and write back only the amino acid sequence and nothing else, if there is no amino acid sequence write \'ASKING\' only. The prompt: {prompt}'})
    conversation = ChatGPT_conversation(conversation)
    response = conversation[-1]['content'].strip()
    print(response)
    if re.search('ASKING', response):
        e = input(Fore.BLUE + 'Write Amino Acid Sequence: ')
        return e
    else:  
        return response

def parse_BLAST():
    list_of_files = glob.glob('BLAST/*') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime)
    a = open(latest_file)
    text = ''
    for i in range(20):
        x = a.readline()
        text = text + x + '\n'
    return text

while True:
    prompt = input(Fore.RED + 'User:')
    with Spinner(Fore.GREEN + "Thinking... "):
        request = check(prompt)
    if request == 'BLAST':
        seq = extractNT_SEQ(prompt)
        BLAST(seq)
        with Spinner(Fore.GREEN + "Analyzing BLAST Results... "):
            time.sleep(5)
            result = parse_BLAST()
            conversation.append({'role': 'user', 'content': 'Analyze this BLAST search and tell me the organism name and any other important infromation. Here is the BLAST result: ' + result})
            conversation = ChatGPT_conversation(conversation)
            response = '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
            print(Fore.GREEN + response)
    elif request == 'PROTEIN': 
        seq = extractAA__SEQ(prompt)
        protein(seq)
    else:
        conversation.append({'role': 'user', 'content': prompt})
        with Spinner(Fore.GREEN + "Thinking... "):
            conversation = ChatGPT_conversation(conversation)

        response = '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
        response_state = extract_code(response)

        if response_state == False:
            print(response)
        else: 
            filename = 'code0.py'
            os.system(f'python3 {filename}')

# while True: 
#     prompt = input(Fore.YELLOW + 'User:')
#     print('-------------------------------------')
#     print(Fore.RED + goal_extraction(prompt))
#     print('-------------------------------------')
#     conversation.append({'role': 'user', 'content': prompt})
#     with Spinner("Thinking... "):
#         conversation = ChatGPT_conversation(conversation)
#     response = '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
#     print(Fore.GREEN + response)
#     print('-------------------------------------')
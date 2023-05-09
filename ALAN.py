import openai
import re
import os
from spinner import Spinner
from logic import *
from colorama import Fore
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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
    return response



conversation = []
conversation.append({'role': 'system', 'content': 'Act as a Bioinformatics research assistant named ALAN (Amino acid Linkage and Analysis Navigator). Only introduce yourself and say that you will help with protein structure prediction and other bioinformatics problems.'})
conversation.append({'role': 'system', 'content': 'You have the ability to run BLAST searches. If the user ask for blast search, converse with them normally but make sure to ask for the sequence they want to search'})
conversation.append({'role':'system', 'content': 'If you are asked to open up tools or webpages, you should always make a selenium script in python to do so. You will use chrome by default for all selenium scripts. You must make sure the experimental option \'detach\' is True so that the browser stays open'})
conversation = ChatGPT_conversation(conversation)
print('{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip()))




def BLAST_CHECK(text):
    newconvo = []
    prompt = text
    # newconvo.append({'role': 'system', 'content': 'Check if this prompt is asking for BLAST Search AND has a nucleotide sequence, you will answer only \'Yes\' or \'No\'. The Prompt: {}'.format(prompt)})
    newconvo.append({'role': 'system', 'content': 'Act as a text checker, you must check if the prompt is asking for BLAST search AND has a nucleotide sequence. If both of these conditions are true, you will reply \'Yes\'. For all other cases, reply normally. Don\'t write anything else. . The Prompt: {}'.format(prompt)})
    newconvo = ChatGPT_conversation(newconvo)
    response = newconvo[-1]['content'].strip()
    print(response)
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

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://blast.ncbi.nlm.nih.gov/Blast.cgi')

    driver.find_element_by_id('homeBlastn').click()
    driver.find_element_by_id('seq').send_keys(query)
    driver.find_element_by_id('blastButton1').click()



def extractSEQ(prompt):
    conversation = []
    conversation.append({'role': 'system', 'content': f'Look through this text and write back only the nucleotide sequence: {prompt}'})
    conversation = ChatGPT_conversation(conversation)
    response = '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
    return response




while True:
    prompt = input(Fore.RED + 'User:')
    with Spinner(Fore.GREEN + "Thinking... "):
        check = BLAST_CHECK(prompt)
        if check == True:
            seq = extractSEQ(prompt)
            BLAST(seq)
        else:
            conversation.append({'role': 'user', 'content': prompt})
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
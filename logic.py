import openai
import re
import os
from spinner import Spinner

openai.api_key = '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'
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


def goal_extraction(prompt):
    conversation = []
    conversation.append({'role': 'system', 'content': f'Generate a list of goal to achieve the task in this prompt, also be specific with the bioinformatics tools that can be used. The prompt: {prompt}'})
    with Spinner("Thinking... "):
        conversation = ChatGPT_conversation(conversation)
    return '{0}: {1}\n'.format(conversation[-1]['role'].strip(), conversation[-1]['content'].strip())
    




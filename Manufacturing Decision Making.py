# imports
# If these fail, please check you're running from an 'activated' environment with (llms) in the command prompt

import os
import requests
import json
from typing import List
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display, update_display
from openai import OpenAI
import openai



# Initialize and constants

load_dotenv(override=True)
API_KEY = api_key_for_OPENAI

if API_KEY and API_KEY.startswith('sk-proj-') and len(API_KEY)>10:
    print("API key looks good so far")
else:
    print("There might be a problem with your API key? Please visit the troubleshooting notebook!")

openai.api_key = API_KEY  # Set the API key directly
MODEL = 'gpt-4o-mini'
client = openai.OpenAI(api_key=API_KEY)
#openai_client = openai.OpenAI()


import openai
import json
import requests

def manufacturing_advice(factory_setup, goal):
    try:
        # Prepare OpenAI request
        chat_response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a smart manufacturing assistant. Suggest efficient production strategies based on the factory constraints."},
                {"role": "user", "content": f"Factory Setup: {factory_setup}\nGoal: {goal}\nWhat is the best strategy?"}
            ]
        )

        # Extract the content from the response
        response_content = chat_response.choices[0].message.content

        # Return the response content
        return response_content

    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
factory_setup = "3 CNC machines, 2 robotic arms"
goal = "Produce 100 parts by tomorrow"

print(manufacturing_advice(factory_setup, goal))
